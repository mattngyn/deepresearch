from hud.datasets import save_tasks
import uuid

tasks = []

# Task 1: Specific historical detail
tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "What was the exact altitude in feet that Chuck Yeager first broke the sound barrier on October 14, 1947? Return just the number, no other text.",
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
            "expected_answer": "43000"  # Some sources say 45000, but 43000 is most commonly cited
        }
    },
    "metadata": {
        "difficulty": "hard",
        "category": "aviation history",
        "topic": "sound barrier",
        "notes": "Chuck Yeager broke the sound barrier at 43,000 feet (some sources say 45,000)"
    }
})

# Task 2: Scientific discovery year
tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "In what year did Kary Mullis invent the polymerase chain reaction (PCR) technique? Return just the year, no other text.",
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
            "expected_answer": "1983"  # PCR was invented in 1983
        }
    },
    "metadata": {
        "difficulty": "hard",
        "category": "science",
        "topic": "molecular biology",
        "notes": "Kary Mullis invented PCR in 1983, won Nobel Prize in 1993"
    }
})

# Task 3: Specific programming language history
tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "What was the original name of the Python programming language's predecessor that Guido van Rossum worked on at CWI in the Netherlands? Return just the name, no other text.",
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
            "expected_answer": "ABC"  # ABC was the language Guido worked on before Python
        }
    },
    "metadata": {
        "difficulty": "hard",
        "category": "computer science",
        "topic": "programming languages",
        "notes": "Guido van Rossum worked on ABC language before creating Python"
    }
})

# Task 4: Economic history specific number
tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "What was the closing value of the Dow Jones Industrial Average on Black Monday, October 19, 1987? Return just the number, no other text.",
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
            "expected_answer": "1738.74"  # Could also accept "1739" for rounding
        }
    },
    "metadata": {
        "difficulty": "hard",
        "category": "economics",
        "topic": "stock market history",
        "notes": "DJIA closed at 1738.74 on Black Monday (22.6% drop)"
    }
})

# Task 5: Space exploration detail
tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "What was the designation number of the Soviet Luna probe that first successfully transmitted images from the far side of the Moon in 1959? Return just the name, no other text.",
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
            "expected_answer": "Luna 3"  # Also accept just "3"
        }
    },
    "metadata": {
        "difficulty": "hard",
        "category": "space exploration",
        "topic": "soviet space program",
        "notes": "Luna 3 photographed the far side of the Moon on October 7, 1959"
    }
})

# Task 6: Literature - specific award year
tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "In what year did Gabriel García Márquez win the Nobel Prize in Literature? Return just the year, no other text.",
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
            "expected_answer": "1982"
        }
    },
    "metadata": {
        "difficulty": "medium",
        "category": "literature",
        "topic": "nobel prizes",
        "notes": "Gabriel García Márquez won the Nobel Prize in Literature in 1982"
    }
})

# Task 7: Mathematics history
tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "What is the smallest known Wieferich prime number? Return just the number, no other text.",
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
            "expected_answer": "1093"
        }
    },
    "metadata": {
        "difficulty": "very hard",
        "category": "mathematics",
        "topic": "number theory",
        "notes": "Only two Wieferich primes are known: 1093 and 3511"
    }
})

# Task 8: Medical history
tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "In what year was the first successful human heart transplant performed by Dr. Christiaan Barnard? Return just the year, no other text.",
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
            "expected_answer": "1967"
        }
    },
    "metadata": {
        "difficulty": "medium",
        "category": "medical history",
        "topic": "organ transplantation",
        "notes": "First human heart transplant was on December 3, 1967 in Cape Town"
    }
})

# Task 9: Computer history - specific version
tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "What was the version number of the first public release of Linux kernel announced by Linus Torvalds in 1991? Return just the number, no other text.",
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
            "expected_answer": "0.01"  # First release was 0.01 in September 1991
        }
    },
    "metadata": {
        "difficulty": "hard",
        "category": "computer science",
        "topic": "operating systems",
        "notes": "Linux 0.01 was released in September 1991"
    }
})

# Task 10: Art history - specific painting dimension
tasks.append({
    "id": str(uuid.uuid4()),
    "prompt": "What is the width in centimeters of Leonardo da Vinci's Mona Lisa painting? Return just the number, no other text.",
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
            "expected_answer": "53"  # The Mona Lisa is 77cm × 53cm
        }
    },
    "metadata": {
        "difficulty": "medium",
        "category": "art history",
        "topic": "renaissance art",
        "notes": "Mona Lisa dimensions: 77cm (height) × 53cm (width)"
    }
})

save_tasks(tasks, "kizro/deep_research_taskset")