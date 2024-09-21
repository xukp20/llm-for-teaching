from src.preprocess.split import split

import os
base_path = "data/1"
refs_path = os.path.join(base_path, "refs")
grading_file = os.path.join(refs_path, "grading_rules.md")
ref_answer_file = os.path.join(refs_path, "ref_answer.md")

split_result = split(ref_answer_file, grading_file)

to_parse = []
pattern = """
### Id
{id}

### Problem & Answer
{problem}

### Grading Rules
{rules}
"""

for i, text in enumerate(split_result):
    to_parse.append(pattern.format(id=text[0], problem=text[1], rules=text[2]))
    print(to_parse[i])


# load key for parse_grading_rules from src.configs.keys.parse_grading_rules.txt
key = open("src/configs/keys/parse_grading_rules.txt", "r").read().strip()

# parse grading rules
from src.api.dify_api import completion_messages
for i, text in enumerate(to_parse):
    inputs = {
        "query": text,
    }
    response = completion_messages(inputs, key)
    import json
    print(json.loads(response.strip("```json").strip("```").replace("\\", "\\\\").replace("\\\\\\\\", "\\\\")))