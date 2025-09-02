"""Simple DeepResearch MCP server for HUD."""
import httpx
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urlparse
from hud.server import MCPServer
from hud.server.context import attach_context
from typing import List, Dict

mcp = MCPServer(name="deepresearch")
ctx = None

@mcp.initialize
async def init(init_ctx):
    global ctx
    ctx = attach_context("/tmp/hud_ctx.sock")

@mcp.shutdown
async def cleanup():
    global ctx
    ctx = None

@mcp.tool()
async def search(query: str, max_results: int = 10) -> List[Dict[str, str]]:
    """
    Search the web for information and return titles and URLs.
    
    Args:
        query: The search query string
        max_results: Maximum number of results to return (default: 10)
    
    Returns:
        List of dictionaries containing 'title' and 'url' for each result
    """
    results = []
    
    try:
        # Use DuckDuckGo HTML search (no API key required)
        search_url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
        
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(
                search_url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Find search results
            result_links = soup.find_all('a', class_='result__a')
            
            for link in result_links[:max_results]:
                title = link.get_text(strip=True)
                url = link.get('href', '')
                
                if title and url:
                    results.append({
                        'title': title,
                        'url': url
                    })
            
            # If no results found with the primary method, try alternative parsing
            if not results:
                # Try alternative selectors
                for result in soup.find_all('div', class_='result')[:max_results]:
                    title_elem = result.find('a', class_='result__a')
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        url = title_elem.get('href', '')
                        if title and url:
                            results.append({
                                'title': title,
                                'url': url
                            })
                            
    except Exception as primary_error:
        # Fallback to a simple Google search if DuckDuckGo fails
        try:
            search_url = f"https://www.google.com/search?q={quote_plus(query)}"
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(
                    search_url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    }
                )
                soup = BeautifulSoup(response.text, 'lxml')
                
                # Parse Google search results
                for g in soup.find_all('div', class_='g')[:max_results]:
                    title_elem = g.find('h3')
                    link_elem = g.find('a')
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        url = link_elem.get('href', '')
                        if title and url and url.startswith('http'):
                            results.append({
                                'title': title,
                                'url': url
                            })
        except Exception as fallback_error:
            return [{"error": f"Search failed. Primary: {str(primary_error)}, Fallback: {str(fallback_error)}"}]
    
    # Store search history in context
    ctx.add_search(query, results)
    
    return results if results else [{"message": "No results found"}]

@mcp.tool()
async def fetch(url: str, max_length: int = 10000) -> str:
    """
    Fetch and extract text content from a URL.
    
    Args:
        url: The URL to fetch content from
        max_length: Maximum length of text to return (default: 10000 characters)
    
    Returns:
        Extracted text content from the webpage
    """
    try:
        # Validate URL
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return f"Invalid URL: {url}"
        
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            response = await client.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
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
        return f"HTTP error {e.response.status_code}: {e.response.reason_phrase}"
    except httpx.RequestError as e:
        return f"Request error: {str(e)}"
    except Exception as e:
        return f"Error fetching URL: {str(e)}"

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
    return "DeepResearch environment ready with search and fetch tools"

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