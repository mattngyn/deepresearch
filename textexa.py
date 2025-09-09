"""Standalone Exa API client for search and fetch operations."""
import httpx
import os
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import asyncio


class ExaClient:
    """Client for interacting with Exa search and content APIs."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with API key from parameter or environment."""
        self.api_key = "2345f9e9-ceda-4a07-982f-63d459a6f1be"
        self.search_url = "https://api.exa.ai/search"
        self.contents_url = "https://api.exa.ai/contents"
    
    async def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Search the web for information and return titles and URLs using Exa API.
        
        Args:
            query: The search query string
            max_results: Maximum number of results to return (default: 5)
        
        Returns:
            List of dictionaries containing 'title' and 'url' for each result
        """
        results = []
        
        if not self.api_key:
            return [{
                "error": "Exa API key not found",
                "message": "Please set EXA_API_KEY environment variable",
                "instructions": "Get your API key from https://dashboard.exa.ai/home"
            }]
        
        try:
            # Increase timeout for complex queries
            timeout = httpx.Timeout(30.0, read=60.0)  # 30s default, 60s for reading
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    self.search_url,
                    headers={
                        "x-api-key": self.api_key,
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
                            'url': url
                        })
                
                # If no results, provide helpful feedback
                if not results:
                    return [{
                        "message": "No results found",
                        "query": query,
                        "autopromptString": data.get('autopromptString', query)
                    }]
                    
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                return [{
                    "error": "Invalid Exa API key",
                    "message": "Please check your EXA_API_KEY environment variable",
                    "status_code": str(e.response.status_code)
                }]
            elif e.response.status_code == 429:
                return [{
                    "error": "Exa API rate limit exceeded",
                    "message": "Please wait before making more requests",
                    "status_code": str(e.response.status_code)
                }]
            else:
                return [{
                    "error": f"Exa API error: {e.response.status_code}",
                    "message": str(e),
                    "response": e.response.text[:500]
                }]
        except Exception as e:
            return [{
                "error": f"Search failed: {type(e).__name__}",
                "message": str(e)
            }]
        
        return results
    
    async def fetch(self, url: str, max_length: int = 2500) -> str:
        """
        Fetch and extract text content from a URL using Exa API.
        
        Args:
            url: The URL to fetch content from
            max_length: Maximum length of text to return (default: 2500 characters)
        
        Returns:
            Extracted text content from the webpage
        """
        # Validate URL
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return f"Invalid URL: {url}"
        
        if not self.api_key:
            # Fallback to direct fetch if no API key
            return await self._direct_fetch(url, max_length)
        
        try:
            # Increase timeout for content fetching
            timeout = httpx.Timeout(30.0, read=60.0)  # 30s default, 60s for reading
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    self.contents_url,
                    headers={
                        "x-api-key": self.api_key,
                        "Content-Type": "application/json"
                    },
                    json={
                        "urls": [url],
                        "text": True,
                        "livecrawl": "fallback"  # Use cache first, livecrawl if needed
                    }
                )
                
                response.raise_for_status()
                data = response.json()
                
                # Extract text content
                results = data.get('results', [])
                if results and len(results) > 0:
                    text = results[0].get('text', '')
                    
                    # Limit text length
                    if text and len(text) > max_length:
                        text = text[:max_length] + "...[truncated]"
                    
                    return text if text else "No text content found"
                else:
                    return "No content available for this URL"
                    
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                # Invalid API key, fallback to direct fetch
                return await self._direct_fetch(url, max_length)
            elif e.response.status_code == 429:
                return "Exa API rate limit exceeded. Please wait before fetching more content."
            else:
                return f"Exa API error: {e.response.status_code} - {e.response.text[:200]}"
        except Exception as e:
            # Fallback to direct fetch on any error
            return await self._direct_fetch(url, max_length)
    
    async def _direct_fetch(self, url: str, max_length: int) -> str:
        """
        Direct fetch fallback when Exa API is not available.
        Note: This method may be rate limited by websites.
        """
        try:
            # Longer timeout for direct fetching as some sites are slow
            timeout = httpx.Timeout(30.0, read=45.0)
            async with httpx.AsyncClient(follow_redirects=True, timeout=timeout) as client:
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
                
                return text if text else "No text content found"
                
        except httpx.HTTPStatusError as e:
            return f"HTTP error {e.response.status_code}: {e.response.reason_phrase} (Note: This URL may be blocking automated access)"
        except httpx.RequestError as e:
            return f"Request error: {str(e)}"
        except Exception as e:
            return f"Error fetching URL: {str(e)}"


# Convenience functions that match the server.py interface
async def search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Convenience function for search - matches server.py interface."""
    client = ExaClient()
    return await client.search(query, max_results)


async def fetch(url: str, max_length: int = 2500) -> str:
    """Convenience function for fetch - matches server.py interface."""
    client = ExaClient()
    return await client.fetch(url, max_length)


# Example usage and testing
async def main():

    print("\n=== Using Convenience Functions ===")
    results = await search("In which year did the Japanese scientist Koichi Mizushima receive the Kato Memorial Prize?")
    print(results)

    url = ""
    #content = await fetch(url)
    #print(content)

if __name__ == "__main__":
    # Run the example
    asyncio.run(main())
