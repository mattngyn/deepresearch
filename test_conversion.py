import ast
import json

txt_file = "res1.txt"
json_file = "output.json"

with open(txt_file, "r", encoding="utf-8") as f:
    txt_content = f.read().strip()

# Convert string to Python object safely
data = ast.literal_eval(txt_content)

# Write as JSON
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Converted {txt_file} into {json_file}")
