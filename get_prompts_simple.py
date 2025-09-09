"""Simple script to get cleaned prompts from a HuggingFace dataset."""
from datasets import load_dataset

def get_cleaned_prompts(dataset_name, prompt_column="prompt"):
    """
    Get prompts from a dataset and remove "Return just the answer, no other text."
    
    Args:
        dataset_name: HuggingFace dataset name
        prompt_column: Column containing prompts (default: "prompt")
    
    Returns:
        List of cleaned prompt strings
    """
    # Load dataset
    dataset = load_dataset(dataset_name)
    
    # Handle DatasetDict (multiple splits)
    if hasattr(dataset, 'keys'):
        # Use train split if available, otherwise first split
        if 'train' in dataset:
            dataset = dataset['train']
        else:
            dataset = dataset[list(dataset.keys())[0]]
    
    # Extract prompts
    prompts = dataset[prompt_column]
    
    # Clean prompts - remove the specific text
    cleaned_prompts = []
    for prompt in prompts:
        if prompt:
            cleaned = prompt.replace("Return just the answer, no other text.", "").strip()
            cleaned_prompts.append(cleaned)
    
    return cleaned_prompts

# Example usage
if __name__ == "__main__":
    # Example with the dataset from your config
    dataset_name = "kizro/deep_research_taskset-50rows"
    
    print(f"Getting prompts from {dataset_name}...")
    prompts = get_cleaned_prompts(dataset_name)
    
    print(f"\nFound {len(prompts)} prompts")
    print(prompts)