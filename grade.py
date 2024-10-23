from src.preprocess.split import split_only_problem

import os, json
base_path = "data/1"
refs_path = os.path.join(base_path, "refs")
mids_path = os.path.join(base_path, "mids")
grading_file = os.path.join(refs_path, "grading_rules.md")
ref_answer_file = os.path.join(refs_path, "ref_answer.md")

student_ans_dir = os.path.join(base_path, "raw_answers")
student_file = "主观题 HW1.md"

# set the student file
student_ans_file = os.path.join(student_ans_dir, student_file)

# load the grading rules
parsed_path = os.path.join(mids_path, "problems.json")

from src.grading.check import check, print_all_records_with_ref_scores, print_all_records

key = "app-fKyyxey5TrMJg9Y7pWFindBX"

# all_results = check(parsed_path, student_ans_file, key)

# import json
# json.dump(all_results, open("./results.json", "w"), ensure_ascii=False, indent=4)

# loads
all_results = json.load(open("./results.json", "r"))

md_report = print_all_records(all_results)

with open("report.md", "w") as f:
    f.write(md_report)