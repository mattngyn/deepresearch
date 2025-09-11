import verifiers as vf
from openai import AsyncOpenAI


"""
vf-eval hud-vf-gym \
    --model "Qwen/Qwen2.5-14B-Instruct" \
    --env-args '{"taskset": "kizro/deep_research_taskset-50rows_filtered", "config_path": "./configs/deepresearch.yaml"}' \
    --api-base-url "http://localhost:8000/v1" \
    --num-examples 13 \
    --rollouts-per-example 16 \
    --max-concurrent 128
"""

env = vf.load_environment(
    env_id="hud-vf-gym",
    taskset="kizro/deep_research_taskset-50rows_filtered",  
    config_path="./configs/deepresearch.yaml",
)

client = AsyncOpenAI(
    base_url="http://localhost:8000/v1",  # vLLM's OpenAI-compatible endpoint
    api_key=""
)

results = env.evaluate(
    client, "Qwen/Qwen2.5-14B-Instruct",
    num_examples=13,
    rollouts_per_example=16,
    max_concurrent=128,
)
import json

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_dict"):  # common in model outputs
            return obj.to_dict()
        if hasattr(obj, "__dict__"):  # fallback
            return obj.__dict__
        return str(obj)  # last resort

with open("results.json", "w") as f:
    json.dump(results, f, cls=CustomEncoder, indent=2)
