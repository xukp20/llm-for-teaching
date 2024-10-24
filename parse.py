from src.preprocess.split import split
from src.utils.paths import FilePaths, KeyPaths, read_key

import os

mids_path = FilePaths.get_mids_path("1")
ref_answer_file = FilePaths.get_ref_answer_file("1")
grading_file = FilePaths.get_grading_rules_file("1")

# load key for parse_grading_rules from src.configs.keys.parse_grading_rules.txt
key = read_key(KeyPaths.get_parse_grading_rules_key())

output_path = os.path.join(mids_path, "problems1.json")

from src.preprocess.parse_grading_rules import parse_grading_rules

parse_grading_rules(ref_answer_file, grading_file, output_path, key)