# DeepResearch HUD Environment

A simple HUD environment for web research with search, fetch, and answer submission capabilities. Perfect for creating research-based benchmarks and evaluating agents.

## Features

- **Search Tool**: Search the web and get titles and URLs of results
- **Fetch Tool**: Extract text content from any URL
- **Answer Tool**: Submit final answers for evaluation
- **Automatic Evaluation**: Task-specific evaluation with exact match checking
- Persistent state tracking across operations

## Quick Start

```bash
# Build and run locally
hud dev

# Or build first
docker build -t deepresearch:dev .
hud dev --image deepresearch:dev
```

## Available Tools

### 1. Search
Search the web for information and return titles and URLs.

**Parameters:**
- `query` (string): The search query
- `max_results` (int, optional): Maximum number of results to return (default: 10)

**Returns:** List of dictionaries containing:
- `title`: The title of the search result
- `url`: The URL of the search result

### 2. Fetch
Fetch and extract text content from a URL.

**Parameters:**
- `url` (string): The URL to fetch content from
- `max_length` (int, optional): Maximum length of text to return (default: 10000 characters)

**Returns:** Extracted text content from the webpage

### 3. Answer
Submit the final answer to the research question.

**Parameters:**
- `final_answer` (string): The agent's final answer to the task

**Returns:** Confirmation message

### 4. Setup (Required for HUD)
Initializes the environment for a new task. Automatically resets statistics.

### 5. Evaluate (Required for HUD)
Evaluates if the submitted answer matches the expected answer.

**Parameters:**
- `expected_answer` (string): The correct answer to check against

**Returns:** Evaluation result with:
- `reward`: 1.0 for correct, 0.0 for incorrect
- `done`: Always true (task complete)
- `info`: Additional details about the evaluation

## Creating Tasks

Following [HUD's benchmark best practices](https://docs.hud.so/evaluate-agents/create-benchmarks), here's how to create research tasks:

```python
import uuid
from hud.datasets import Task

# Example task: Research question about Obama's birth year
research_task = {
    "id": str(uuid.uuid4()),
    "prompt": "What year was Barack Obama born?",
    "mcp_config": {
        "hud": {
            "url": "https://mcp.hud.so/v3/mcp",
            "headers": {
                "Authorization": "Bearer ${HUD_API_KEY}",
                "Mcp-Image": "your-org/deepresearch:latest"
            }
        }
    },
    "setup_tool": {
        "name": "setup",
        "arguments": {}
    },
    "evaluate_tool": {
        "name": "evaluate",
        "arguments": {
            "expected_answer": "1961"
        }
    },
    "metadata": {
        "difficulty": "easy",
        "category": "history",
        "topic": "US Presidents"
    }
}

# More complex example: Multi-step research
complex_task = {
    "id": str(uuid.uuid4()),
    "prompt": "Find the year when the first iPhone was released.",
    "mcp_config": {
        "hud": {
            "url": "https://mcp.hud.so/v3/mcp",
            "headers": {
                "Authorization": "Bearer ${HUD_API_KEY}",
                "Mcp-Image": "your-org/deepresearch:latest"
            }
        }
    },
    "setup_tool": {
        "name": "setup",
        "arguments": {}
    },
    "evaluate_tool": {
        "name": "evaluate",
        "arguments": {
            "expected_answer": "2007"
        }
    },
    "metadata": {
        "difficulty": "easy",
        "category": "technology",
        "topic": "Apple products"
    }
}
```

## Workflow

1. **Setup Phase**: Environment is initialized, stats are reset
2. **Research Phase**: Agent uses search and fetch tools to gather information
3. **Answer Phase**: Agent submits final answer using the answer tool
4. **Evaluation Phase**: The evaluate tool checks the submitted answer against the expected answer

## Creating a Benchmark Dataset

```python
from hud.datasets import save_tasks

# Create multiple research tasks
research_tasks = [
    {
        "id": str(uuid.uuid4()),
        "prompt": "What year was Barack Obama born?",
        "evaluate_tool": {
            "name": "evaluate",
            "arguments": {"expected_answer": "1961"}
        },
        # ... other task fields
    },
    {
        "id": str(uuid.uuid4()),
        "prompt": "Who wrote the novel '1984'?",
        "evaluate_tool": {
            "name": "evaluate",
            "arguments": {"expected_answer": "George Orwell"}
        },
        # ... other task fields
    },
    # Add more tasks...
]

# Save to HuggingFace
save_tasks(
    research_tasks,
    repo_id="my-org/deepresearch-benchmark",
    private=False,
    tags=["research", "web", "factual-qa"]
)
```

## Project Structure

```
deepresearch/
├── src/
│   └── hud_controller/
│       ├── server.py      # MCP server with all tools
│       └── context.py     # Persistent state and answer storage
├── Dockerfile            # Container configuration
├── pyproject.toml       # Python dependencies
└── README.md           # This file
```

## State Management

The environment tracks:
- Submitted answers for evaluation
- Total number of searches performed
- Total number of fetches performed
- History of recent operations

## Best Practices for Tasks

1. **Clear Prompts**: Be specific about what answer format you expect
2. **Consistent Answers**: Use standardized formats (e.g., just years for dates)
3. **Single Answers**: For MVP, keep answers simple and unambiguous
4. **Test Tasks**: Verify that the answer can be found through web search

## Dependencies

- `hud-python`: HUD framework
- `httpx`: Async HTTP client
- `beautifulsoup4`: HTML parsing
- `lxml`: XML/HTML processor

## Development

To modify the evaluation logic:

1. Edit `src/hud_controller/server.py` to change the evaluate function
2. Update `src/hud_controller/context.py` for additional state management
3. Rebuild: `docker build -t deepresearch:dev .`
4. Test: `hud dev`

## Learn More

- [HUD Documentation](https://docs.hud.so)
- [Creating Benchmarks](https://docs.hud.so/evaluate-agents/create-benchmarks)
- [MCP Specification](https://modelcontextprotocol.io)