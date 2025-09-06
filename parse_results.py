#!/usr/bin/env python3
"""
Parse raw results text and show, for each task, the 0/1 reward over all runs.

Usage:
  python runs_by_task.py < raw.txt > runs.csv
  # or force 10 runs and print Markdown:
  python runs_by_task.py --runs 10 --format md < raw.txt > runs.md
"""
import re
import ast
import sys
import csv
import argparse
from collections import defaultdict, Counter

def extract_list(name: str, text: str):
    m = re.search(rf"{name}\s*=\s*(\[[\s\S]*?\])", text)
    return ast.literal_eval(m.group(1)) if m else None

def extract_metrics_field(field: str, text: str):
    m = re.search(r"metrics\s*=\s*(\{[\s\S]*\})", text)
    if not m:
        return None
    metrics = ast.literal_eval(m.group(1))
    return metrics.get(field)

def deduce_runs_per_task(tasks):
    c = Counter(tasks)
    counts = set(c.values())
    if len(counts) == 1:
        return counts.pop()
    # fallback: use distance between first two occurrences of the first task
    first = tasks[0]
    idxs = [i for i, t in enumerate(tasks) if t == first]
    if len(idxs) > 1:
        return idxs[1]
    return 10  # last-resort default

def natural_task_key(s: str):
    m = re.search(r"(\d+)$", s)
    return (0, int(m.group(1))) if m else (1, s)

def group_binary(tasks, binary, runs_per_task=None):
    if len(tasks) != len(binary):
        raise ValueError(f"Length mismatch: tasks={len(tasks)} vs binary={len(binary)}")
    if runs_per_task is None:
        runs_per_task = deduce_runs_per_task(tasks)

    by_task = defaultdict(list)
    for t, b in zip(tasks, binary):
        # b could be 0/1 or float close to them
        b01 = int(round(float(b)))
        by_task[t].append(b01)

    # normalize to runs_per_task (truncate or right-pad with None)
    for t, seq in by_task.items():
        if len(seq) > runs_per_task:
            by_task[t] = seq[:runs_per_task]
        elif len(seq) < runs_per_task:
            by_task[t] = seq + [None] * (runs_per_task - len(seq))

    ordered_tasks = sorted(by_task.keys(), key=natural_task_key)
    return ordered_tasks, by_task, runs_per_task

def write_csv(ordered_tasks, by_task, runs_per_task, out_fp):
    writer = csv.writer(out_fp)
    header = ["task"] + [f"run_{i+1}" for i in range(runs_per_task)] + ["sum", "rate"]
    writer.writerow(header)
    for t in ordered_tasks:
        seq = by_task[t]
        s = sum(0 if v in (None, 0) else 1 for v in seq)
        rate = s / runs_per_task if runs_per_task else 0.0
        writer.writerow([t] + seq + [s, f"{rate:.2f}"])

def write_markdown(ordered_tasks, by_task, runs_per_task, out_fp):
    header = ["task"] + [f"run_{i+1}" for i in range(runs_per_task)] + ["sum", "rate"]
    out_fp.write("| " + " | ".join(header) + " |\n")
    out_fp.write("|" + "|".join(["---"] * len(header)) + "|\n")
    for t in ordered_tasks:
        seq = by_task[t]
        s = sum(0 if v in (None, 0) else 1 for v in seq)
        rate = s / runs_per_task if runs_per_task else 0.0
        row = [t] + [("" if v is None else str(v)) for v in seq] + [str(s), f"{rate:.2f}"]
        out_fp.write("| " + " | ".join(row) + " |\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=None,
                    help="Force runs-per-task (default: auto-detect). Use 10 for your case.")
    ap.add_argument("--format", choices=["csv", "md"], default="csv",
                    help="Output format (csv or md). Default: csv.")
    args = ap.parse_args()

    raw = sys.stdin.read()

    tasks = extract_list("task", raw)
    if tasks is None:
        sys.stderr.write("Error: couldn't find task=[...]\n")
        sys.exit(1)

    # Prefer binary from metrics['hud_task_reward_func']
    binary = extract_metrics_field("hud_task_reward_func", raw)
    if binary is None:
        # Fallback: threshold the continuous 'reward' list
        reward = extract_list("reward", raw)
        if reward is None:
            sys.stderr.write("Error: neither metrics['hud_task_reward_func'] nor reward=[...] found\n")
            sys.exit(2)
        binary = [1 if float(x) >= 0.5 else 0 for x in reward]

    ordered_tasks, by_task, runs_per_task = group_binary(tasks, binary, args.runs)

    if args.runs is not None and args.runs != runs_per_task:
        # If user forced runs, re-normalize sequences to that count
        runs_per_task = args.runs
        for t, seq in by_task.items():
            if len(seq) > runs_per_task:
                by_task[t] = seq[:runs_per_task]
            elif len(seq) < runs_per_task:
                by_task[t] = seq + [None] * (runs_per_task - len(seq))

    if args.format == "csv":
        write_csv(ordered_tasks, by_task, runs_per_task, sys.stdout)
    else:
        write_markdown(ordered_tasks, by_task, runs_per_task, sys.stdout)

if __name__ == "__main__":
    main()
