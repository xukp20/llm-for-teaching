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

    for rule_id, table in enumerate(tables):
        max_score = rules[rule_id]["score"]
        rule_id = rule_id + 1
        process, scores = check_one_rule(ref_problem, student_problem, table, app_key)
        # check validity
        if len(scores) != 1:
            print("Error: scores should have length 1")
            print(scores)
            continue
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


def match_problems(parsed_problem_list, split_result):
    ref_problems = {problem["id"]: problem for problem in parsed_problem_list}
    check_pairs = [
        {
            "id": problem[0],
            "ref": ref_problems[problem[0]],    # dict
            "student": problem[1]   # text
        }
        for problem in split_result
    ]

    return check_pairs

def get_all_problem_ids(parsed_problem_list):
    return list(set([problem["id"] for problem in parsed_problem_list]))

def check(refs_path, student_ans_file, app_key):
    parsed_problem_list = ParsedProblemList.from_file(refs_path).to_dict()
    split_result = split_only_problem(student_ans_file)

    check_pairs = match_problems(parsed_problem_list, split_result)

    all_records = {}
    for pair in check_pairs:
        id = pair["id"]
        records = check_one_problem(pair["ref"]["problem"], pair["student"], pair["ref"]["rules"], app_key)

        all_records[id] = records

    return all_records


# tool
def print_one_problem_record(records):
    """
        Print the record in a human-readable way.
    """
    string = ""
    string += f"### Ref\n{records['ref']}\n"
    string += f"### Student\n{records['student']}\n"
    string += f"### Rules\n"
    string += format_rules_table_with_scores(records["rules"], records["scores"], records["reasons"])
    string += f"### Agg Scores\n"
    string += format_subproblem_table(records["agg_scores"])
    
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