"""Simple script to filter HuggingFace dataset by task rates."""
import csv
from datasets import load_dataset
from huggingface_hub import login
import os

# Configuration
CSV_FILE = "runs.csv"  # Your CSV file with rates
DATASET_NAME = "kizro/deep_research_taskset-50rows"  # Dataset to filter
OUTPUT_NAME = "kizro/deep_research_taskset-50rows_filtered"  # Output dataset name
MIN_RATE = 0.2  # Keep tasks with rate >= 0.3
MAX_RATE = 0.8  # Keep tasks with rate <= 0.7

# Read CSV and get task rates
task_rates = {}
with open(CSV_FILE, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['task'].startswith('task_'):
            idx = int(row['task'].split('_')[1])
            task_rates[idx] = float(row['rate'])

print(f"Found {len(task_rates)} tasks")

# Find which tasks to keep
tasks_to_keep = []
for idx, rate in task_rates.items():
    if MIN_RATE <= rate <= MAX_RATE:
        tasks_to_keep.append(idx)
        print(f"✓ Keeping task_{idx} (rate: {rate:.2f})")
    else:
        print(f"✗ Removing task_{idx} (rate: {rate:.2f})")

print(f"\nKeeping {len(tasks_to_keep)} out of {len(task_rates)} tasks")

# Load and filter dataset
dataset = load_dataset(DATASET_NAME)
if 'train' in dataset:
    data = dataset['train']
else:
    data = dataset[list(dataset.keys())[0]]

print(f"\nOriginal dataset: {len(data)} rows")

# Filter dataset
filtered_data = data.select(tasks_to_keep)
print(f"Filtered dataset: {len(filtered_data)} rows")

# Show example
if len(filtered_data) > 0:
    print("\nExample row:")
    print(filtered_data[0])

# Upload filtered dataset
response = input("\nUpload filtered dataset? (y/n): ")
if response.lower() == 'y':
    # Login
    if os.getenv("HF_TOKEN"):
        login(token=os.getenv("HF_TOKEN"))
    else:
        login()
    
    # Upload
    filtered_data.push_to_hub(
        OUTPUT_NAME,
        private=False,  # Set to True for private
        commit_message=f"Filtered to keep tasks with rate between {MIN_RATE} and {MAX_RATE}"
    )
    
    print(f"\n✅ Uploaded to: https://huggingface.co/datasets/{OUTPUT_NAME}")
