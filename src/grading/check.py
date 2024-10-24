"""
    24/10/07 version 1: Check one grading rule at a time.
"""
from src.api.dify_api import completion_messages
from src.preprocess.parse_grading_rules import ParsedProblemList
from src.preprocess.split import split_only_problem

import json

def format_rules_table(rules, start_id=1):
    """
        Map the list of rules to a md table:
        inputs are a list of dict with keys: id, rule, score
        | id | rule | score |
    """
    table = "| 规则序号 | 所属小题 | 评分规则 | 分值 |\n| --- | --- | --- | --- |\n"
    for i, rule in enumerate(rules):
        table += f"| {i+start_id} | {rule['id']} | {rule['rule']} | {rule['score']} |\n"
    return table

def format_rules_table_with_scores(rules, scores, reasons=None, start_id=1):
    """
        Map the list of rules to a md table:
        inputs are a list of dict with keys: id, rule, score
        | id | rule | score | score |
    """
    if not reasons:
        table = "| 规则序号 | 所属小题 | 评分规则 | 分值 | 得分 |\n| --- | --- | --- | --- | --- |\n"
    else:
        table = "| 规则序号 | 所属小题 | 评分规则 | 分值 | 得分 | 评分原因 |\n| --- | --- | --- | --- | --- | --- |\n"

    for i, rule in enumerate(rules):
        if not reasons:
            table += f"| {i+start_id} | {rule['id']} | {rule['rule']} | {rule['score']} | {scores[i]} |\n"
        else:
            table += f"| {i+start_id} | {rule['id']} | {rule['rule']} | {rule['score']} | {scores[i]} | {reasons[i]} |\n"

    return table

def format_subproblem_table(agg_scores):
    """
        Map the dict of scores to a md table:
        inputs are a dict with key id.
        | id | score |
    """
    table = "| 小题序号 | 得分 |\n| --- | --- |\n"
    for id, score in agg_scores.items():
        table += f"| {id} | {score} |\n"
    return table

def format_rules_tables(rules):
    """
        One table for each rule, but different id.    
    """
    tables = []
    for i, rule in enumerate(rules):
        tables.append(format_rules_table([rule], start_id=i+1))
    return tables


input_pattern = """
### 参考答案
{ref_problem}

### 学生答案
{student_problem}

### 评分标准
{rules_table}
"""

def check_one_rule(ref_problem, student_problem, rules_table, app_key):
    inputs = {
        "ref_problem": ref_problem,
        "student_problem": student_problem,
        "rules_table": rules_table
    }

    query = input_pattern.format(**inputs)

    inputs = {
        "query": query,
    }
    response = completion_messages(inputs, app_key)

    response = response.strip("```json").strip("```").replace("\\", "\\\\").replace("\\\\\\\\", "\\\\")
    response = json.loads(response)
    process = response["process"]
    scores = response["scores"]

    return process, scores


# tool for agg rules for the same subproblem
def group_scores(agg_scores, new_score, rule):
    """
        Agg the scores by the id of the corresponding rule.

        Args:
            agg_scores: dict with key id.
            new_score: int
            rule: dict with keys: id, rule, score
        
        Returns:
            agg_scores: dict with key id.
    """
    rule_id = rule["id"]
    if rule_id in agg_scores:
        agg_scores[rule_id].append(new_score)
    else:
        agg_scores[rule_id] = [new_score]
    return agg_scores


from tqdm import tqdm
def check_one_problem(ref_problem, student_problem, rules, app_key):
    """
        Check one problem with multiple rules.

        Args:
            ref_problem: text of the reference problem with answers
            student_problem: text of the student's answer
            rules: list of dict with keys: id, rule, score
            app_key: key for the api
        
        Returns:
            records: dict with keys: ref, student, rules, scores, reasons, agg_scores
    """
    tables = format_rules_tables(rules)
    records = {
        "ref": ref_problem,
        "student": student_problem,
        "rules": rules
    }
    all_scores = []
    all_reasons = []
    agg_scores = {}

    for rule_id, table in tqdm(enumerate(tables), desc="Rules", total=len(tables)):
        max_score = rules[rule_id]["score"]
        rule_id = rule_id + 1
        process, scores = check_one_rule(ref_problem, student_problem, table, app_key)
        # check validity
        if len(scores) != 1:
            print("Warning: scores should have length 1")
            print(scores)
        if not str(rule_id) in scores:
            print("Error: rule_id not in scores")
            print(rule_id)
            print(scores)
            continue
        if scores[str(rule_id)] > max_score:
            print("Error: score exceeds max_score")
            print(scores)
            continue
        if not len(all_scores) == rule_id - 1:
            print("Error: all_scores length not match")
            print(all_scores)
            continue
        all_scores.append(scores[str(rule_id)])
        all_reasons.append(process)
        agg_scores = group_scores(agg_scores, scores[str(rule_id)], rules[rule_id-1])
    
    records["scores"] = all_scores
    records["reasons"] = all_reasons
    # sum the scores for each rule
    records["agg_scores"] = {rule_id: sum(scores) for rule_id, scores in agg_scores.items()}

    return records


def match_problems(ref_problems, split_result):
    check_pairs = [
        {
            "id": problem[0],
            "ref": ref_problems[problem[0]],    # dict
            "student": problem[1]   # text
        }
        for problem in split_result
    ]
    # look for missing problems
    missing_ids = set(ref_problems.keys()) - set([pair["id"] for pair in check_pairs])

    return check_pairs, missing_ids

def get_all_problem_ids(parsed_problem_list):
    return list(set([problem["id"] for problem in parsed_problem_list]))

def get_missing_problem_results(ref_problem):
    """
        Generate an empty record for the missing problem.
    """
    all_scores = []
    all_reasons = []
    agg_scores = {}

    records = {
        "ref": ref_problem["problem"],
        "student": "Missing!",
        "rules": ref_problem["rules"],
    }

    for rule in ref_problem["rules"]:
        process = "Missing answer"
        score = 0
        all_scores.append(score)
        all_reasons.append(process)
        agg_scores = group_scores(agg_scores, score, rule)

    records["scores"] = all_scores
    records["reasons"] = all_reasons
    records["agg_scores"] = {rule_id: sum(scores) for rule_id, scores in agg_scores.items()}

    return records


def check(refs_path, student_ans_file, app_key):
    parsed_problem_list = ParsedProblemList.from_file(refs_path).to_dict()
    ref_problems = {problem["id"]: problem for problem in parsed_problem_list}
    
    split_result = split_only_problem(student_ans_file)

    check_pairs, missing_ids = match_problems(ref_problems, split_result)

    all_records = {}
    for pair in check_pairs:
        id = pair["id"]
        records = check_one_problem(pair["ref"]["problem"], pair["student"], pair["ref"]["rules"], app_key)

        all_records[id] = records

    for id in missing_ids:
        ref_problem = ref_problems[id]
        records = get_missing_problem_results(ref_problem)
        all_records[id] = records

    # sort by id
    all_records = dict(sorted(all_records.items(), key=lambda x: x[0]))

    return all_records


# tool
def print_one_problem_record(records):
    """
        Print the record in a human-readable way.
    """
    try:
        string = ""
        string += f"### Ref\n{records['ref']}\n"
        string += f"### Student\n{records['student']}\n\n"
        string += f"### Rules\n"
        string += format_rules_table_with_scores(records["rules"], records["scores"], records["reasons"])
        string += f"### Agg Scores\n"
        string += format_subproblem_table(records["agg_scores"])
    except Exception as e:
        print(e)
        print(records)
    
    # remove 
    return string


def print_all_records(all_records):
    """
        Print the records in a human-readable way as a md table.
    """
    string = ""
    for id, records in all_records.items():
        string += f"## Problem {id}\n"
        string += print_one_problem_record(records)
        string += "\n"
    return string

def print_all_records_with_ref_scores(all_records, ref_scores):
    """
        Print the records in a human-readable way as a md table.
    """
    string = ""
    for id, records in all_records.items():
        string += f"## Problem {id}\n"
        string += print_one_problem_record(records)
        string += f"### Ref Scores\n"
        string += format_subproblem_table(ref_scores[id])
        string += "\n"
    return string


# high level entry
from src.utils.files import find_student_files
from src.utils.paths import FilePaths, save_json, read_json, save_text
import os
from tqdm import tqdm

def batch_check(
        hw_id,
        check_key):
    """
        Check all the student answers in the raw_answer_dir.
    
        1. Find all student files
        2. Use `check` to check each
        3. Look for scores file in the data dir, if so, add to the report
        4. Save the reports to the reports_dir
    """
    raw_answer_dir = FilePaths.get_raw_answers_path(hw_id)
    parsed_problems_file = FilePaths.get_parsed_problems_file(hw_id)
    ref_scores_file = FilePaths.get_ref_scores_file(hw_id)
    results_dir = FilePaths.get_results_path(hw_id)

    student_files = find_student_files(raw_answer_dir)
    ref_scores = {}
    if os.path.exists(ref_scores_file):
        ref_scores = read_json(ref_scores_file)

    for student_name in tqdm(student_files, desc="Checking", total=len(student_files)):
        # check report exists
        if os.path.exists(os.path.join(results_dir, f"{student_name}.json")):
            tqdm.write(f"Report for {student_name} exists, skip.")
            continue

        student_ans_file = student_files[student_name]
        student_records = check(parsed_problems_file, student_ans_file, check_key)
        if student_name in ref_scores:
            report = print_all_records_with_ref_scores(student_records, ref_scores[student_name])
        else:
            report = print_all_records(student_records)
        
        # save json
        json_report_file = os.path.join(results_dir, f"{student_name}.json")
        save_json(json_report_file, student_records)

        # save
        md_report_file = os.path.join(results_dir, f"{student_name}.md")
        save_text(md_report_file, report)
