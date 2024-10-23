from src.preprocess.split import split

import os
base_path = "data/1"
refs_path = os.path.join(base_path, "refs")
mids_path = os.path.join(base_path, "mids")
grading_file = os.path.join(refs_path, "grading_rules.md")
ref_answer_file = os.path.join(refs_path, "ref_answer.md")

# load key for parse_grading_rules from src.configs.keys.parse_grading_rules.txt
key = open("src/configs/keys/parse_grading_rules.txt", "r").read().strip()

output_path = os.path.join(mids_path, "problems1.json")

from src.preprocess.parse_grading_rules import parse_grading_rules

parse_grading_rules(ref_answer_file, grading_file, output_path, key)