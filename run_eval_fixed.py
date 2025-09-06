import verifiers as vf
from openai import AsyncOpenAI


"""
vf-eval hud-vf-gym \
    --model "Qwen/Qwen2.5-14B-Instruct" \
    --env-args '{"taskset": "kizro/deep_research_taskset", "config_path": "./configs/deepresearch.yaml"}' \
    --api-base-url "http://localhost:8000/v1" \
    --num-examples 25 \
    --rollouts-per-example 10 \
    --max-concurrent-requests 1
"""

env = vf.load_environment(
    env_id="hud-vf-gym",
    taskset="kizro/deep_research_taskset",  
    config_path="./configs/deepresearch.yaml",
)

client = AsyncOpenAI(
    base_url="http://localhost:8000/v1",  # vLLM's OpenAI-compatible endpoint
    api_key=""
)

results = env.evaluate(
    client, "Qwen/Qwen2.5-14B-Instruct",
    num_examples=5,
    rollouts_per_example=10,
    max_concurrent=128,
)
import json
# dump to a json file
with open("results.json", "w") as f:
    json.dump(results, f)