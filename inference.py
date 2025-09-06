import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Edit this string with your prompt
PROMPT = "When was the arxiv founded? When you have your final answer, return just the year, no other text."

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-14B-Instruct", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-3B-Instruct",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto" if torch.cuda.is_available() else None,
    trust_remote_code=True
)

# Format the prompt
messages = [{"role": "user", "content": PROMPT}]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

# Generate response
inputs = tokenizer(text, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=512, temperature=0.7)
response = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)

# Print result
print(f"\nPrompt: {PROMPT}")
print(f"\nResponse: {response}")
