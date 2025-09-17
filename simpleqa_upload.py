#!/usr/bin/env python3
"""
Convert Hugging Face dataset basicv8vc/SimpleQA (split: test)
into DeepResearch 'tasks' format and save with hud.datasets.save_tasks.
"""

import json
import uuid
from typing import List, Dict

from datasets import load_dataset
from hud.datasets import save_tasks


def load_system_prompt():
    """Load system prompt from deepresearch_rl_config.json"""
    try:
        with open("deepresearch_rl_config.json", "r") as f:
            config = json.load(f)
            return config.get("actor", {}).get("system_prompt", "")
    except Exception as e:
        print(f"Warning: Could not load system prompt: {e}")
        return ""


def make_tasks(
    split: str,
    limit: int,
    docker_image: str,
    append_answer_instruction: bool,
    system_prompt: str,
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
            "system_prompt": system_prompt,
        }

        tasks.append(task)

    return tasks


def main():
    repo_id = "kizro/deep_research_taskset_full"  # destination for save_tasks
    split = "test"                           # dataset split
    limit = 50                              # 0 = all rows, or e.g. 100
    docker_image = "deepresearch:dev"        # docker image
    append_answer_instruction = True         # add instruction to prompt

    # Load system prompt from config
    system_prompt = load_system_prompt()
    if system_prompt:
        print(f"Loaded system prompt: {system_prompt[:50]}...")
    
    tasks = make_tasks(split, limit, docker_image, append_answer_instruction, system_prompt)
    print(f"Built {len(tasks)} tasks.")
    save_tasks(tasks, repo_id)


if __name__ == "__main__":
    main()
