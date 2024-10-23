from src.preprocess.split import split_only_problem

import os, json
base_path = "data/1"
refs_path = os.path.join(base_path, "refs")
mids_path = os.path.join(base_path, "mids")
grading_file = os.path.join(refs_path, "grading_rules.md")
ref_answer_file = os.path.join(refs_path, "ref_answer.md")

student_ans_dir = os.path.join(base_path, "raw_answers")
student_file = "主观题 HW1.md"

# split the student answer file
student_ans_file = os.path.join(student_ans_dir, student_file)
# split_result = split_only_problem(student_ans_file)

# load the grading rules
parsed_path = os.path.join(mids_path, "problems.json")
# with open(parsed_path, "r") as f:
    # ref_problems = json.load(f)
# translate to id: problem
# ref_problems = {problem["id"]: problem for problem in ref_problems}

# match the student answer with the grading rules
# check_pairs = [
#     {
#         "ref": ref_problems[problem[0]],    # dict
#         "student": problem[1]   # text
#     }
#     for problem in split_result
# ]

# check one by one

# def format_rules_table(rules, start_id=1):
#     """
#         Map the list of rules to a md table:
#         inputs are a list of dict with keys: id, rule, score
#         | id | rule | score |
#     """
#     table = "| 规则序号 | 所属小题 | 评分规则 | 分值 |\n| --- | --- | --- | --- |\n"
#     for i, rule in enumerate(rules):
#         table += f"| {i+start_id} | {rule['id']} | {rule['rule']} | {rule['score']} |\n"
#     return table

# def format_rules_tables(rules):
#     """
#         One table for each rule, but different id.    
#     """
#     tables = []
#     for i, rule in enumerate(rules):
#         tables.append(format_rules_table([rule], start_id=i+1))
#     return tables

# input_pattern = """
# ### 参考答案
# {ref_problem}

# ### 学生答案
# {student_problem}

# ### 评分标准
# {rules_table}
# """

# for pair in check_pairs:

#     # format the input
#     # inputs = {
#     #     "ref_problem": pair["ref"]["problem"],
#     #     "student_problem": pair["student"],
#     #     "rules_table": format_rules_table(pair["ref"]["rules"])
#     # }

#     # print(input_pattern.format(**inputs))

#     for table in format_rules_tables(pair["ref"]["rules"]):
#         inputs = {
#             "ref_problem": pair["ref"]["problem"],
#             "student_problem": pair["student"],
#             "rules_table": table
#         }

#         print(input_pattern.format(**inputs))
#         # print(table)
#         print("\n\n\n")

#     break


from src.grading.check import check

key = "app-fKyyxey5TrMJg9Y7pWFindBX"

all_results = check(parsed_path, student_ans_file, key)

# print(all_results)

import json
json.dump(all_results, open("./results.json", "w"))

# for result in all_results:
#     print(result)
#     print("\n\n\n")

# loads
all_results = json.load(open("./results.json", "r"))

for id, result in all_results.items():
    print(id)
    print(result["ref"])
    print(result["student"])
    for i in range(len(result["scores"])):
        print(result["rules"][i])
        print(result["scores"][i])
        print(result["reasons"][i])

