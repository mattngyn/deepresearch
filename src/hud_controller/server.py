"""Simple DeepResearch MCP server for HUD."""
import httpx
import os
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urlparse
from hud.server import MCPServer
from hud.server.context import attach_context
from typing import List, Dict

mcp = MCPServer("DeepResearch", version="0.1.0")
ctx = None

@mcp.initialize
async def init(init_ctx):
    global ctx
    ctx = await attach_context(init_ctx)

@mcp.shutdown
async def cleanup():
    global ctx
    ctx = None

@mcp.tool()
async def search(query: str) -> dict:
    """
    Search the web for information and return titles and URLs using Exa API.
    
    Args:
        query: The search query string
    
    Returns:
        Dictionary containing search results with key 'results'. Each result contains:
        - title: The page title
        - url: The exact URL to fetch (MUST use this exact URL with fetch())
        - instruction: How to fetch this content
        
    Example return: {"results": [{"title": "Example Page", "url": "https://example.com/page", "instruction": "To read this content, call: fetch(url=\"https://example.com/page\")"}]}
    """
    results = []
    max_results = 1  # Hardcoded to 1 result
    
    # Get Exa API key from environment
    exa_api_key = "c3ad9f16-4d2e-47ad-bba5-a7ba060474bf"
    if not exa_api_key:
        return {
            "results": [],
            "error": "Exa API key not found",
            "message": "Please set EXA_API_KEY environment variable",
            "instructions": "Get your API key from https://dashboard.exa.ai/home"
        }
    
    try:
        # Use Exa search API
        search_url = "https://api.exa.ai/search"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                search_url,
                headers={
                    "x-api-key": exa_api_key,
                    "Content-Type": "application/json"
                },
                json={
                    "query": query,
                    "numResults": max_results,
                    "type": "keyword",
                    "userLocation": "us",  # Bias results for US region
                    "contents": {
                        "text": {"maxCharacters": 1000}  # Get text snippets
                    }
                }
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Extract results
            for result in data.get('results', []):
                title = result.get('title', '')
                url = result.get('url', '')
                
                if title and url:
                    results.append({
                        'title': title,
                        'url': url,
                        'instruction': f'To read this content, call: fetch(url="{url}")'
                    })
            
            # If no results, provide helpful feedback
            if not results:
                return {
                    "results": [],
                    "message": "No results found",
                    "query": query,
                    "autopromptString": data.get('autopromptString', query)
                }
                
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return {
                "results": [],
                "error": "Invalid Exa API key",
                "message": "Please check your EXA_API_KEY environment variable",
                "status_code": str(e.response.status_code)
            }
        elif e.response.status_code == 429:
            return {
                "results": [],
                "error": "Exa API rate limit exceeded",
                "message": "Please wait before making more requests",
                "status_code": str(e.response.status_code)
            }
        else:
            return {
                "results": [],
                "error": f"Exa API error: {e.response.status_code}",
                "message": str(e),
                "response": e.response.text[:500]
            }
    except Exception as e:
        return {
            "results": [],
            "error": f"Search failed: {type(e).__name__}",
            "message": str(e)
        }
    
    # Store search history in context
    ctx.add_search(query, results)
    
    return {"results": results}

@mcp.tool()
async def fetch(url: str) -> str:
    """
    Fetch and extract content from a URL using Exa API, including summary, highlights, and full text.
    
    CRITICAL: You MUST use the exact URL returned by search(). Do not modify or guess URLs.
    
    Args:
        url: The EXACT URL from search results (copy it exactly as shown)
    
    Returns:
        Formatted content including:
        - Summary with main takeaways
        - 3 key highlights (5 sentences each)
        - Full text content (truncated to 2500 characters)
        
    Example: If search returned {"url": "https://example.com/page"}, call: fetch(url="https://example.com/page")
    """
    max_length = 2500  # Hardcoded to 2500 characters
    # Validate URL
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return f"Invalid URL: {url}"
    
    
    # Get Exa API key
    exa_api_key = "c3ad9f16-4d2e-47ad-bba5-a7ba060474bf"
    if not exa_api_key:
        # Fallback to direct fetch if no API key
        return await _direct_fetch(url)
    
    try:
        # Use Exa contents API for reliable fetching
        contents_url = "https://api.exa.ai/contents"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                contents_url,
                headers={
                    "x-api-key": exa_api_key,
                    "Content-Type": "application/json"
                },
                json={
                    "urls": [url],
                    "text": {
                        "maxCharacters": max_length,
                        "includeHtmlTags": False
                    },
                    "highlights": {
                        "numSentences": 5,
                        "highlightsPerUrl": 3
                    },
                    "summary": {
                        "query": "main takeaways"
                    },
                    "livecrawl": "fallback"  # Use cache first, livecrawl if needed
                }
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Extract text content, summary, and highlights
            results = data.get('results', [])
            if results and len(results) > 0:
                result = results[0]
                text = result.get('text', '')
                summary = result.get('summary', '')
                highlights = result.get('highlights', [])
                
                # Build formatted response
                formatted_content = []
                
                # Add summary
                if summary:
                    formatted_content.append("=== SUMMARY (Main Takeaways) ===")
                    formatted_content.append(summary)
                    formatted_content.append("")
                
                # Add highlights
                if highlights:
                    formatted_content.append("=== KEY HIGHLIGHTS ===")
                    for i, highlight in enumerate(highlights[:3], 1):
                        formatted_content.append(f"\nHighlight {i}:")
                        formatted_content.append(highlight)
                    formatted_content.append("")
                
                # Add main text (truncated if needed)
                if text:
                    formatted_content.append("=== FULL CONTENT ===")
                    if len(text) > max_length:
                        text = text[:max_length] + "...[truncated]"
                    formatted_content.append(text)
                
                final_content = "\n".join(formatted_content)
                
                # Store fetch history in context
                ctx.add_fetch(url, len(final_content))
                
                return final_content if final_content else "No content available"
            else:
                return "No content available for this URL"
                
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            # Invalid API key, fallback to direct fetch
            return await _direct_fetch(url)
        elif e.response.status_code == 429:
            return "Exa API rate limit exceeded. Please wait before fetching more content."
        else:
            return f"Exa API error: {e.response.status_code} - {e.response.text[:200]}"
    except Exception as e:
        # Fallback to direct fetch on any error
        return await _direct_fetch(url)


async def _direct_fetch(url: str) -> str:
    """
    Direct fetch fallback when Exa API is not available.
    Note: This method may be rate limited by websites.
    """
    max_length = 2500  # Hardcoded to 2500 characters
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            response = await client.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                }
            )
            response.raise_for_status()
            
            # Parse HTML and extract text
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Limit text length
            if len(text) > max_length:
                text = text[:max_length] + "...[truncated]"
            
            # Store fetch history in context
            ctx.add_fetch(url, len(text))
            
            return text if text else "No text content found"
            
    except httpx.HTTPStatusError as e:
        return f"HTTP error {e.response.status_code}: {e.response.reason_phrase} (Note: This URL may be blocking automated access)"
    except httpx.RequestError as e:
        return f"Request error: {str(e)}"
    except Exception as e:
        return f"Error fetching URL: {str(e)}"

@mcp.tool()
async def answer(final_answer: str) -> str:
    """
    Submit the final answer to the research question.
    
    Args:
        final_answer: The complete answer to the research question
    
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
        expected_answer: The expected answer to compare against
    
    Returns:
        Dictionary containing:
        - success: Whether the answer matches
        - actual_answer: The submitted answer
        - expected_answer: The expected answer
        - stats: Performance statistics
    """
    actual = ctx.get_answer()
    success = actual and expected_answer and actual.strip().lower() == expected_answer.strip().lower()
    
    return {
        "success": success,
        "actual_answer": actual or "",
        "expected_answer": expected_answer,
        "stats": ctx.get_stats()
    }

@mcp.tool()
async def done() -> str:
    """Signal that you have completed the task."""
    return "Task completed"

# Run the server
if __name__ == "__main__":
    mcp.run()