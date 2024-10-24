from src.utils.paths import FilePaths, KeyPaths, read_key

import os

mids_path = FilePaths.get_mids_path("1")
ref_answer_file = FilePaths.get_ref_answer_file("1")
grading_file = FilePaths.get_grading_rules_file("1")

student_file = "2022011095_周赫_2893.zip"

# set the student file
student_ans_file = os.path.join(FilePaths.get_raw_answers_path("1"), student_file)

# load the grading rules
parsed_path = FilePaths.get_parsed_problems_file("1")
key = read_key(KeyPaths.get_grading_key())

from src.grading.check import check, print_all_records

all_results = check(parsed_path, student_ans_file, key)

md_report = print_all_records(all_results)

with open("report1.md", "w") as f:
    f.write(md_report)