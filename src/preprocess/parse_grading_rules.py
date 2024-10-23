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