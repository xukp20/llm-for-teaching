"""
    1. Split the problem set into separated problems.
    1.1 Problem and reference answer from the ref answer file.
    1.2 Grading rules from the grading file.
"""

def split_raw_text(raw_text):
    """
        Split the raw text into problems.

        Each file starts with "## <title>"
        Then each problem's content is after "### <problem name>"

        Split by "### <problem name>" to find the problem name and content after each "###"
    """

    problems = raw_text.split("### ")[1:]
    
    # for each, take the first line as the name
    # the rest as the content
    problem_list = []
    for problem in problems:
        name, content = problem.split("\n", 1)
        problem_list.append((name.strip(), content.strip()))
    
    return problem_list

def match_problems(problem_list, grading_rules_list):
    """
        Match the problems with grading rules.

        For each problem, find the grading rules that match the problem name.
    """

    # for each problem, find the grading rules that match the problem name
    matched_problems = []
    for i in range(len(problem_list)):
        problem_name, problem_content = problem_list[i]
        grading_rules_name, grading_rules_content = grading_rules_list[i]
        if problem_name != grading_rules_name:
            print(f"Problem name {problem_name} does not match grading rules name {grading_rules_name}")
        else:
            matched_problems.append((problem_name, problem_content, grading_rules_content))

    return matched_problems

# split to subproblems
# match all the patterns like “解：” <answer> "</end>"
# a list of "prefix", "suffix", "answer"
def split_subproblems(problem_content):
    """
        Split the problem content into subproblems.

        Split by "解：" to find the answer.
    """
    start = 0
    subproblems = []
    while True:
        start = problem_content.find("解：", start)
        if start == -1:
            break
        end = problem_content.find("</end>", start)
        if end == -1:
            break
        subproblem = {
            "prefix": problem_content[:start],
            "suffix": problem_content[end+len("</end>"):],
            "answer": problem_content[start+len("解："):end]
        }
        subproblems.append(subproblem)
        start = end
    
    return subproblems


def split(ref_answer_file, grading_file):
    """
        Split the ref answer file and grading file into separated problems.
    """
    with open(ref_answer_file, "r") as f:
        ref_answer = f.read()
    with open(grading_file, "r") as f:
        grading = f.read()

    problem_list = split_raw_text(ref_answer)
    grading_rules_list = split_raw_text(grading)

    split_result = match_problems(problem_list, grading_rules_list)

    return split_result


def split_only_problem(student_ans_file):
    """
        Split the student answer file into separated problems.
    """
    with open(student_ans_file, "r") as f:
        student_ans = f.read()

    problem_list = split_raw_text(student_ans)

    return problem_list