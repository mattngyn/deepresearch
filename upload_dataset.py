from hud.datasets import save_tasks
import uuid

tasks = []

tasks.append({
    "id": str(uuid.uuid4()),
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
    "id": str(uuid.uuid4()),
    "prompt": "When was the paper 'Sparse Autoencoders Find Highly Interpretable Features in Language Models' first published to arXiv? When you have your final answer, return just the year, no other text.",
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
            "expected_answer": "2023"
        }
    }
})


tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "When was the paper 'Convergent Linear Representations of Emergent Misalignment' first published to arXiv? When you have your final answer, return just the year, no other text.",
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
            "expected_answer": "2025"
        }
    }
})

tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "What year was OpenAI's o3 model first announced? When you have your final answer, return just the year, no other text.",
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
            "expected_answer": "2024"
        }
    }
})

tasks.append({
    "id": str(uuid.uuid4()),
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
    "id": str(uuid.uuid4()),
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

save_tasks(tasks, "kizro/deep_research_taskset")