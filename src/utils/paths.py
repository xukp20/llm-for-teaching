"""
    General paths for the project
"""

import os

# base path of the project
PROJECT_BASE=os.environ.get("PROJECT_BASE", "./")

# base path of all the data
DATA_BASE="data"

# under each hw subdir, there should be:
# references files: ref_answer.md (for problem and answer), grading_rules.md (for grading rules for each problem)
REF_DIR="refs"
# mids files: generated after preprocess the problem and grading rules
MIDS_DIR="mids"
# raw answers files: raw answers from students
RAW_ANSWERS_DIR="raw_answers"
# results
RESULTS_DIR="results"

# file name settings
REF_ANSWER_FILE="ref_answer.md"
GRADING_RULES_FILE="grading_rules.md"

PARSED_PROBLEMS_FILE="problems.json"

REF_SCORES_FILE="scores.json"

# tools
class FilePaths:
    @staticmethod
    def get_refs_path(hw_id):
        return os.path.join(PROJECT_BASE, DATA_BASE, hw_id, REF_DIR)

    @staticmethod
    def get_mids_path(hw_id):
        return os.path.join(PROJECT_BASE, DATA_BASE, hw_id, MIDS_DIR)

    @staticmethod
    def get_raw_answers_path(hw_id):
        return os.path.join(PROJECT_BASE, DATA_BASE, hw_id, RAW_ANSWERS_DIR)

    @staticmethod
    def get_ref_answer_file(hw_id):
        return os.path.join(FilePaths.get_refs_path(hw_id), REF_ANSWER_FILE)

    @staticmethod
    def get_grading_rules_file(hw_id):
        return os.path.join(FilePaths.get_refs_path(hw_id), GRADING_RULES_FILE)

    @staticmethod
    def get_parsed_problems_file(hw_id):
        return os.path.join(FilePaths.get_mids_path(hw_id), PARSED_PROBLEMS_FILE)

    @staticmethod
    def get_student_ans_file(hw_id, student_file):
        return os.path.join(FilePaths.get_raw_answers_path(hw_id), student_file)

    @staticmethod
    def get_ref_scores_file(hw_id):
        return os.path.join(FilePaths.get_raw_answers_path(hw_id), REF_SCORES_FILE)
    
    @staticmethod
    def get_results_path(hw_id):
        return os.path.join(PROJECT_BASE, DATA_BASE, hw_id, RESULTS_DIR)
    
    @staticmethod
    def get_project_base():
        return PROJECT_BASE

    @staticmethod
    def get_data_base():
        return DATA_BASE
    

# ---- For api keys ----
KEY_BASE="src/configs/keys"

# names
GRADING_KEY="grading.txt"
PARSE_GRADING_RULES_KEY="parse_grading_rules.txt"

class KeyPaths:
    @staticmethod
    def get_grading_key():
        return os.path.join(PROJECT_BASE, KEY_BASE, GRADING_KEY)

    @staticmethod
    def get_parse_grading_rules_key():
        return os.path.join(PROJECT_BASE, KEY_BASE, PARSE_GRADING_RULES_KEY)

    @staticmethod
    def get_key_base():
        return KEY_BASE
    

def read_key(key_path):
    with open(key_path, "r") as f:
        return f.read().strip()
    
def read_json(file_path):
    import json
    with open(file_path, "r") as f:
        return json.load(f)
    
def save_json(file_path, data):
    import json, os
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    with open(file_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_text(file_path, text):
    import os
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    with open(file_path, "w") as f:
        f.write(text)