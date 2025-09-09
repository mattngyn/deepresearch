"""Simple script to create a 10-row subset of your HuggingFace dataset."""
from datasets import load_dataset
from huggingface_hub import login
import os

# Configuration - EDIT THESE VALUES
SOURCE_DATASET = "kizro/deep_research_taskset"  # Replace with your dataset
NEW_DATASET_NAME = "kizro/deep_research_taskset-50rows"  # Replace with new name
NUM_ROWS = 50  # Number of rows to keep

# Optional: Set your HF token here or use environment variable HF_TOKEN
HF_TOKEN = None  # or "hf_your_token_here"

def create_subset():
    # Login
    token = HF_TOKEN or os.getenv("HF_TOKEN")
    if token:
        login(token=token)
    else:
        print("Please login to HuggingFace:")
        login()
    
    # Load dataset
    print(f"Loading dataset: {SOURCE_DATASET}")
    try:
        # Try with train split first
        dataset = load_dataset(SOURCE_DATASET, split="train")
    except:
        # If that fails, load all splits and pick the first one
        dataset_dict = load_dataset(SOURCE_DATASET)
        first_split = list(dataset_dict.keys())[0]
        dataset = dataset_dict[first_split]
        print(f"Using split: {first_split}")
    
    # Create subset
    original_size = len(dataset)
    subset_size = min(NUM_ROWS, original_size)
    subset = dataset.select(range(subset_size))
    
    print(f"Original: {original_size} rows → Subset: {subset_size} rows")
    print(f"\nFirst row preview:")
    print(subset[0])
    
    # Upload
    print(f"\nUploading to: {NEW_DATASET_NAME}")
    subset.push_to_hub(
        NEW_DATASET_NAME,
        private=False,  # Set to False if you want it public
        commit_message=f"First {subset_size} rows of {SOURCE_DATASET}"
    )
    
    print(f"\n✅ Success! View your dataset at:")
    print(f"https://huggingface.co/datasets/{NEW_DATASET_NAME}")

if __name__ == "__main__":
    create_subset()
