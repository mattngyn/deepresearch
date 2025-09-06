#!/usr/bin/env python3
"""
Convert Hugging Face dataset basicv8vc/SimpleQA (split: test)
into DeepResearch 'tasks' format and save with hud.datasets.save_tasks.
"""

import uuid
from typing import List, Dict

from datasets import load_dataset
from hud.datasets import save_tasks


def make_tasks(
    split: str,
    limit: int,
    docker_image: str,
    append_answer_instruction: bool,
) -> List[Dict]:
    # Load dataset
    ds = load_dataset("basicv8vc/SimpleQA", split=split)

    # Determine how many rows to use
    n = len(ds) if limit in (None, 0) else min(limit, len(ds))

    tasks: List[Dict] = []
    for i in range(n):
        row = ds[i]

        # Dataset columns: "problem" and "answer"
        problem = str(row.get("problem", "")).strip()
        answer = str(row.get("answer", "")).strip()

        # Append instruction if needed
        if append_answer_instruction:
            prompt = f"{problem}\n\nReturn just the answer, no other text."
        else:
            prompt = problem

        task_id = f"SQA_{i:05d}"

        task = {
            "id": task_id,
            "prompt": prompt,
            "mcp_config": {
                "deepresearch": {
                    "command": "docker",
                    "args": ["run", "--rm", "-i", docker_image],
                }
            },
            "setup_tool": {"name": "setup", "arguments": {}},
            "evaluate_tool": {
                "name": "evaluate",
                "arguments": {"expected_answer": answer},
            },
        }

        tasks.append(task)

    return tasks


def main():
    # -----------------------------
    # EDIT THESE VARIABLES AS NEEDED
    # -----------------------------
    repo_id = "kizro/deep_research_taskset"  # destination for save_tasks
    split = "test"                           # dataset split
    limit = 1000                              # 0 = all rows, or e.g. 100
    docker_image = "deepresearch:dev"        # docker image
    append_answer_instruction = True         # add instruction to prompt
    # -----------------------------

    tasks = make_tasks(split, limit, docker_image, append_answer_instruction)
    print(f"Built {len(tasks)} tasks.")
    save_tasks(tasks, repo_id)


if __name__ == "__main__":
    main()
