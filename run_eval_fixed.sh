#!/bin/bash
# Fixed evaluation command for DeepResearch with vLLM

# Correct command with proper syntax
vf-eval hud-vf-gym \
    --model "Qwen/Qwen2.5-7B-Instruct" \
    --env-args '{"taskset": "kizro/deep_research_taskset", "config_path": "./configs/deepresearch.yaml"}' \
    --api-base-url "http://localhost:8000/v1" \
    --num-examples 16 \
    --rollouts-per-example 16 \
    --max-concurrent-requests 16
