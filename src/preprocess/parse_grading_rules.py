"""
    Generate grading rules from the grading rules file for each problem
"""

class ParsedProblem:
    def __init__(self, id, problem, raw_rules, rules):
        self.id = id
        self.problem = problem
        self.raw_rules = raw_rules
        self.rules = rules

    def to_dict(self):
        return {
            "id": self.id,
            "problem": self.problem,
            "raw_rules": self.raw_rules,
            "rules": self.rules
        }
    
    @staticmethod
    def from_dict(d):
        return ParsedProblem(d["id"], d["problem"], d["raw_rules"], d["rules"])
    
    def __str__(self):
        return f"""
### Id
{self.id}

### Problem & Answer
{self.problem}

### Grading Rules
{self.raw_rules}
"""
    
    def __repr__(self):
        return self.__str__()
    

class ParsedProblemList:
    def __init__(self, problems):
        self.problems = problems
    
    def to_dict(self):
        return [problem.to_dict() for problem in self.problems]
    
    @staticmethod
    def from_dict(d):
        return ParsedProblemList([ParsedProblem.from_dict(problem) for problem in d])
    
    @staticmethod
    def from_file(file_path):
        import json
        with open(file_path, "r") as f:
            return ParsedProblemList.from_dict(json.load(f))
        
    def __str__(self):
        return "\n".join([str(problem) for problem in self.problems])
    
    def __repr__(self):
        return self.__str__()
    

from src.preprocess.split import split
from src.api.dify_api import completion_messages
import json


def parse_grading_rules(ref_answer_file, grading_file, output_path, app_key):
    split_result = split(ref_answer_file, grading_file)
    
    to_parse = []
    problems = []
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
        problems.append({
            "id": text[0],
            "problem": text[1],
            "raw_rules": text[2],
        })

    # parse grading rules
    for i, text in enumerate(to_parse):
        inputs = {
            "query": text,
        }
        response = completion_messages(inputs, app_key)
        problems[i]["rules"] = json.loads(response.strip("```json").strip("```").replace("\\", "\\\\").replace("\\\\\\\\", "\\\\"))

    # save problems
    # output to mids directory
    with open(output_path, "w") as f:
        json.dump(problems, f, ensure_ascii=False, indent=4)

    print(f"Problems saved to {output_path}")

    return ParsedProblemList([ParsedProblem.from_dict(problem) for problem in problems])