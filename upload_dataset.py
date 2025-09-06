from hud.datasets import save_tasks
import uuid

tasks = []

tasks.append({
    "id": "SFA",
    "prompt": "When was The Specialty Food Association (SFA) founded? When you have your final answer, return just the year, no other text.",
    "mcp_config": {
        "deepresearch": {
            "command": "docker",
            "args": ["run", "--rm", "-i", "deepresearch:dev"]
        }
    },
    "setup_tool": {
        "name": "setup",
        "arguments": {}
    },
    "evaluate_tool": {
        "name": "evaluate",
        "arguments": {
            "expected_answer": "1952" 
        }
    }
})

tasks.append({
    "id": "IOI",
    "prompt": "When was the paper 'Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small' first published to arXiv? When you have your final answer, return just the year, no other text.",
    "mcp_config": {
        "deepresearch": {
            "command": "docker",
            "args": ["run", "--rm", "-i", "deepresearch:dev"]
        }
    },
    "setup_tool": {
        "name": "setup",
        "arguments": {}
    },
    "evaluate_tool": {
        "name": "evaluate",
        "arguments": {
            "expected_answer": "2022"
        }
    }
})

tasks.append({
    "id": "arXiv",
    "prompt": "When was arXiv founded? When you have your final answer, return just the year, no other text.",
    "mcp_config": {
        "deepresearch": {
            "command": "docker",
            "args": ["run", "--rm", "-i", "deepresearch:dev"]
        }
    },
    "setup_tool": {
        "name": "setup",
        "arguments": {}
    },
    "evaluate_tool": {
        "name": "evaluate",
        "arguments": {
            "expected_answer": "1991"
        }
    }
})

tasks.append({
    "id": "GA4GH",
    "prompt": "When was the Global Alliance for Genomics and Health (GA4GH) founded? When you have your final answer, return just the year, no other text.",
    "mcp_config": {"deepresearch": {"command": "docker","args": ["run","--rm","-i","deepresearch:dev"]}},
    "setup_tool": {"name": "setup","arguments": {}},
    "evaluate_tool": {"name": "evaluate","arguments": {"expected_answer": "2013"}}
})

tasks.append({
    "id": "DASI",
    "prompt": "When was the Data & Society Research Institute founded? When you have your final answer, return just the year, no other text.",
    "mcp_config": {"deepresearch": {"command": "docker","args": ["run","--rm","-i","deepresearch:dev"]}},
    "setup_tool": {"name": "setup","arguments": {}},
    "evaluate_tool": {"name": "evaluate","arguments": {"expected_answer": "2014"}}
})

tasks.append({
    "id": "RDI",
    "prompt": "When was Rare Diseases International (RDI) established? When you have your final answer, return just the year, no other text.",
    "mcp_config": {"deepresearch": {"command": "docker","args": ["run","--rm","-i","deepresearch:dev"]}},
    "setup_tool": {"name": "setup","arguments": {}},
    "evaluate_tool": {"name": "evaluate","arguments": {"expected_answer": "2015"}}
})

tasks.append({
    "id": "LNF",
    "prompt": "When was The Long Now Foundation founded? When you have your final answer, return just the year, no other text.",
    "mcp_config": {"deepresearch": {"command": "docker","args": ["run","--rm","-i","deepresearch:dev"]}},
    "setup_tool": {"name": "setup","arguments": {}},
    "evaluate_tool": {"name": "evaluate","arguments": {"expected_answer": "1996"}}
})

tasks.append({
    "id": "ONNX",
    "prompt": "When was the Open Neural Network Exchange (ONNX) first released? When you have your final answer, return just the year, no other text.",
    "mcp_config": {"deepresearch": {"command": "docker","args": ["run","--rm","-i","deepresearch:dev"]}},
    "setup_tool": {"name": "setup","arguments": {}},
    "evaluate_tool": {"name": "evaluate","arguments": {"expected_answer": "2017"}}
})

tasks.append({
    "id": "SAM",
    "prompt": "When was the paper 'Segment Anything' first posted to arXiv? When you have your final answer, return just the year, no other text.",
    "mcp_config": {"deepresearch": {"command": "docker","args": ["run","--rm","-i","deepresearch:dev"]}},
    "setup_tool": {"name": "setup","arguments": {}},
    "evaluate_tool": {"name": "evaluate","arguments": {"expected_answer": "2023"}}
})

tasks.append({
    "id": "FA3",
    "prompt": "When was the paper 'FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision' first posted to arXiv? When you have your final answer, return just the year, no other text.",
    "mcp_config": {"deepresearch": {"command": "docker","args": ["run","--rm","-i","deepresearch:dev"]}},
    "setup_tool": {"name": "setup","arguments": {}},
    "evaluate_tool": {"name": "evaluate","arguments": {"expected_answer": "2024"}}
})

tasks.append({
    "id": "CoRL",
    "prompt": "In what year was the first Conference on Robot Learning (CoRL) held? When you have your final answer, return just the year, no other text.",
    "mcp_config": {"deepresearch": {"command": "docker","args": ["run","--rm","-i","deepresearch:dev"]}},
    "setup_tool": {"name": "setup","arguments": {}},
    "evaluate_tool": {"name": "evaluate","arguments": {"expected_answer": "2017"}}
})

tasks.append({
    "id": "LDM",
    "prompt": "When was the paper 'High-Resolution Image Synthesis with Latent Diffusion Models' first posted to arXiv? When you have your final answer, return just the year, no other text.",
    "mcp_config": {"deepresearch": {"command": "docker","args": ["run","--rm","-i","deepresearch:dev"]}},
    "setup_tool": {"name": "setup","arguments": {}},
    "evaluate_tool": {"name": "evaluate","arguments": {"expected_answer": "2021"}}
})
print(len(tasks))

save_tasks(tasks, "kizro/deep_research_taskset")