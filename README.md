# llm-for-teaching
LLM TAs.

## Usage

1. Clone this repo.
2. Get `data/` dir and put it under the project root.
    - `1` under `data/` dir means the first assignment.
    - under the assignment dir:
      - `mids/`: contains `problems.json` which is the parsed problem, answer and grading rules by LLM. You can modify the grading rules by hand if needed.
      - `raw_answers/`: contains the raw answers from students, could be .zip, .md, or .rar for now. There could be an optional ground truth file `scores.json` containing the scores given by TA, if so, then the grading report will contain the ground truth scores.
      - `refs/`: has `grading_rules.md`, `problems.md` and `ref_answer.md` which are the raw text format of the grading rules, problems and reference answers before auto parsing.
      - `results/`: json and md results will be generated here.
3. Get `configs/` dir and put it under `src/` dir.
    - `keys/`: contains app keys for dify servers (But they are slow in practice, to be removed).
4. Run `batch_grading.py` with your desired assignment id.
