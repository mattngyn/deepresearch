"""Simple DeepResearch MCP server for HUD."""
import os
import json
from urllib.parse import urlparse
from hud.server import MCPServer
from hud.server.context import attach_context
from typing import List, Dict

mcp = MCPServer(name="deepresearch")
ctx = None

# Load hardcoded responses - works both locally and in Docker container
HARDCODED_RESPONSES = {}
try:
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "hardcoded_exa_responses.json")
    
    with open(json_path, "r") as f:
        HARDCODED_RESPONSES = json.load(f)
        print(f"Loaded {len(HARDCODED_RESPONSES.get('search_responses', {}))} search responses and {len(HARDCODED_RESPONSES.get('fetch_responses', {}))} fetch responses", file=os.stderr)
except Exception as e:
    print(f"Warning: Could not load hardcoded responses: {e}", file=os.stderr)
    HARDCODED_RESPONSES = {"search_responses": {}, "fetch_responses": {}}

@mcp.initialize
async def init(init_ctx):
    global ctx
    ctx = attach_context("/tmp/hud_ctx.sock")

@mcp.shutdown
async def cleanup():
    global ctx
    ctx = None

@mcp.tool()
async def search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Search the web for information and return titles and URLs using Exa API.
    
    Args:
        query: The search query string
        max_results: Maximum number of results to return (default: 10)
    
    Returns:
        List of dictionaries containing 'title' and 'url' for each result
    """
    # Check hardcoded responses - ONLY use hardcoded, no fallback
    if query in HARDCODED_RESPONSES.get("search_responses", {}):
        hardcoded_results = HARDCODED_RESPONSES["search_responses"][query]
        
        # Ensure the response format matches Exa API exactly
        if isinstance(hardcoded_results, list):
            # Limit results to max_results if needed
            limited_results = hardcoded_results[:max_results] if len(hardcoded_results) > max_results else hardcoded_results
            
            # Store search history in context (same as real API)
            ctx.add_search(query, limited_results)
            
            return limited_results
    
    # Query not found in hardcoded responses
    return [{
        "error": "Query not supported",
        "message": "Please perform another query. This query is not available in the hardcoded responses."
    }]

@mcp.tool()
async def fetch(url: str, max_length: int = 5000) -> str:
    """
    Fetch and extract text content from a URL using Exa API.
    
    Args:
        url: The URL to fetch content from
        max_length: Maximum length of text to return (default: 10000 characters)
    
    Returns:
        Extracted text content from the webpage
    """
    # Validate URL
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return f"Invalid URL: {url}"
    
    # Check hardcoded responses - ONLY use hardcoded, no fallback
    if url in HARDCODED_RESPONSES.get("fetch_responses", {}):
        hardcoded_content = HARDCODED_RESPONSES["fetch_responses"][url]
        
        # Ensure it's a string (matching Exa fetch response format)
        if isinstance(hardcoded_content, str):
            # Apply the same length limit as real fetch
            if len(hardcoded_content) > max_length:
                hardcoded_content = hardcoded_content[:max_length] + "...[truncated]"
            
            # Store fetch history in context (same as real API)
            ctx.add_fetch(url, len(hardcoded_content))
            
            return hardcoded_content
    
    # URL not found in hardcoded responses
    return "URL not supported. Please use another URL. This URL is not available in the hardcoded responses."


@mcp.tool()
async def answer(final_answer: str) -> str:
    """
    Submit the final answer to the research question.
    
    Args:
        final_answer: The agent's final answer to the task
    
    Returns:
        Confirmation message
    """
    ctx.submit_answer(final_answer)
    return f"Answer submitted: {final_answer}"

@mcp.tool()
async def setup() -> str:
    """Required for HUD environments. Initialize for a new task."""
    # Reset for a fresh task
    ctx.reset_stats()
    return ""

@mcp.tool()
async def evaluate(expected_answer: str) -> dict:
    """
    Required for HUD environments. Evaluates if the submitted answer matches the expected answer.
    
    Args:
        expected_answer: The correct answer to check against
    
    Returns:
        Evaluation result with reward and content string
    """
    submitted = ctx.get_submitted_answer()
    
    # Check if an answer was submitted
    if submitted is None:
        return {
            "reward": 0.0,
            "content": f"No answer submitted. Searches: {ctx.get_search_count()}, Fetches: {ctx.get_fetch_count()}"
        }
    
    # Exact match check (case-insensitive, stripped)
    submitted_clean = submitted.strip().lower()
    expected_clean = expected_answer.strip().lower()
    
    is_correct = submitted_clean == expected_clean
    
    # Build result message
    result_msg = f"{'✅ Correct!' if is_correct else '❌ Incorrect.'} "
    result_msg += f"Submitted: '{submitted}', Expected: '{expected_answer}'. "
    result_msg += f"Stats: {ctx.get_search_count()} searches, {ctx.get_fetch_count()} fetches, {ctx.get_total_operations()} total operations."
    
    return {
        "reward": 1.0 if is_correct else 0.0,
        "content": result_msg
    }

if __name__ == "__main__":
    mcp.run()