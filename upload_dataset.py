from hud.datasets import save_tasks
import uuid

tasks = []

tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "When was The Specialty Food Association (SFA) founded?",
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
    "prompt": "What year was hud (Y-Combinator) founded?",
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
    "prompt": "What is Sundar Pichai's (Google CEO) wife's first name?",
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
            "expected_answer": "Anjali"
        }
    }
})

tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "What was the first name of the actor who played Dom Cobb in Inception?",
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
            "expected_answer": "Leonardo"
        }
    }
})

tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "What was the first name of the actor who played Harvey Dent in The Dark Knight?",
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
            "expected_answer": "Aaron"
        }
    }
})

tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "What was the last name of the actor who played Caledon Hockley in Titanic?",
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
            "expected_answer": "Zane"
        }
    }
})

tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "When was the paper 'Sparse Autoencoders Find Highly Interpretable Features in Language Models' first published to arXiv?",
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
    "prompt": "What year was OpenAI's o3 model first announced?",
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
    "prompt": "When was The Specialty Food Association (SFA) founded?",
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
    "prompt": "What year was hud (Y-Combinator) founded?",
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
    "prompt": "What is Sundar Pichai's (Google CEO) wife's first name?",
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
            "expected_answer": "Anjali"
        }
    }
})

tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "What was the first name of the actor who played Dom Cobb in Inception?",
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
            "expected_answer": "Leonardo"
        }
    }
})

tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "What was the first name of the actor who played Harvey Dent in The Dark Knight?",
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
            "expected_answer": "Aaron"
        }
    }
})

tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "What was the last name of the actor who played Caledon Hockley in Titanic?",
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
            "expected_answer": "Zane"
        }
    }
})

tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "When was the paper 'Sparse Autoencoders Find Highly Interpretable Features in Language Models' first published to arXiv?",
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
    "prompt": "What year was OpenAI's o3 model first announced?",
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
    "prompt": "When was The Specialty Food Association (SFA) founded?",
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
    "prompt": "What year was hud (Y-Combinator) founded?",
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
    "prompt": "What is Sundar Pichai's (Google CEO) wife's first name?",
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
            "expected_answer": "Anjali"
        }
    }
})

tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "What was the first name of the actor who played Dom Cobb in Inception?",
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
            "expected_answer": "Leonardo"
        }
    }
})

tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "What was the first name of the actor who played Harvey Dent in The Dark Knight?",
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
            "expected_answer": "Aaron"
        }
    }
})

tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "What was the last name of the actor who played Caledon Hockley in Titanic?",
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
            "expected_answer": "Zane"
        }
    }
})

tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "When was the paper 'Sparse Autoencoders Find Highly Interpretable Features in Language Models' first published to arXiv?",
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
    "prompt": "What year was OpenAI's o3 model first announced?",
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

save_tasks(tasks, "kizro/deep_research_taskset")