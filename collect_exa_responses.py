"""Script to collect real Exa API responses and save them for hardcoding."""
import asyncio
import json
from textexa import search, fetch
from datetime import datetime
import time

# Define the queries and URLs you want to test
SEARCH_QUERIES = [
    "Who received the IEEE Frank Rosenblatt Award in 2010?",
    "Who was awarded the Oceanography Society's Jerlov Award in 2018?", 
    "What year did the Lego part with ID gal56 first release?",
    "In which year did the Japanese scientist Koichi Mizushima receive the Kato Memorial Prize?",
    "What player scored all the conversions for Spain in the rugby match between Spain and Romania that was part of the 2022 Rugby Europe Championship on February 27, 2022?",
    "What is the surname of the psychiatrist who prescribes medication for Marie Hanson for her periodic blackouts in Season 1, Episode 20 of Ally McBeal?",
    "What is the British-American kickboxer Andrew Tate's kickboxing name? Return just the answer, no other text.",
    "What instrument did Alec Aitken play well enough for a professional musician to remark, 'Aitken is the most accomplished amateur musician I have ever known'?",
    "On what day, month, and year did Tara Chand (a politician and a Dalit leader from Jammu and Kashmir) resign from the Indian National Congress in support of Ghulam Nabi Azad?",
    "What is the first and last name of the woman whom the British linguist Bernard Comrie married in 1985?"
]

FETCH_URLS = [
]

async def collect_responses():
    """Collect all search and fetch responses."""
    responses = {
        "metadata": {
            "collected_at": datetime.now().isoformat(),
            "description": "Hardcoded Exa API responses for testing",
            "format_notes": {
                "search": "Each search response is a list of dicts with 'title' and 'url' keys",
                "fetch": "Each fetch response is a string of the page content",
                "errors": "Error responses should be [{'error': 'type', 'message': 'details'}]"
            }
        },
        "search_responses": {},
        "fetch_responses": {}
    }
    
    # Collect all URLs from search results
    urls_to_fetch = list(FETCH_URLS)  # Start with predefined URLs
    
    # Collect search responses
    print("=== Collecting Search Responses ===")
    for i, query in enumerate(SEARCH_QUERIES, 1):
        print(f"\n[{i}/{len(SEARCH_QUERIES)}] Searching: {query}")
        
        # Retry logic for timeouts
        max_retries = 3
        for retry in range(max_retries):
            try:
                results = await search(query, max_results=5)
                responses["search_responses"][query] = results
                print(f"✓ Got {len(results)} results")
                
                # Collect ALL URLs from search results for fetching
                if results and isinstance(results, list):
                    for result in results:
                        if isinstance(result, dict) and "url" in result:
                            if result["url"] not in urls_to_fetch:
                                urls_to_fetch.append(result["url"])
                                print(f"  → Added URL to fetch: {result['url'][:60]}...")
                break  # Success, exit retry loop
                
            except Exception as e:
                if "ReadTimeout" in str(e) and retry < max_retries - 1:
                    print(f"⏱ Timeout, retrying in 5 seconds... (attempt {retry + 2}/{max_retries})")
                    await asyncio.sleep(5)
                else:
                    print(f"✗ Error: {e}")
                    # Maintain Exa API error format
                    responses["search_responses"][query] = [{
                        "error": f"Search failed: {type(e).__name__}",
                        "message": str(e)
                    }]
                    break
    
    # Collect fetch responses for ALL discovered URLs
    print(f"\n\n=== Collecting Fetch Responses ({len(urls_to_fetch)} URLs) ===")
    for i, url in enumerate(urls_to_fetch, 1):
        print(f"\n[{i}/{len(urls_to_fetch)}] Fetching: {url[:80]}...")
        
        # Retry logic for timeouts
        max_retries = 3
        for retry in range(max_retries):
            try:
                content = await fetch(url, max_length=2500)
                responses["fetch_responses"][url] = content
                print(f"✓ Got {len(content)} characters")
                break  # Success, exit retry loop
                
            except Exception as e:
                if "ReadTimeout" in str(e) and retry < max_retries - 1:
                    print(f"⏱ Timeout, retrying in 5 seconds... (attempt {retry + 2}/{max_retries})")
                    await asyncio.sleep(5)
                else:
                    print(f"✗ Error: {e}")
                    # Store error as string (matching Exa fetch error format)
                    responses["fetch_responses"][url] = f"Error fetching URL: {str(e)}"
                    break
    
    # Save to JSON file
    with open("hardcoded_exa_responses.json", "w") as f:
        json.dump(responses, f, indent=2)
    
    print(f"\n\n✅ Saved {len(responses['search_responses'])} search responses")
    print(f"✅ Saved {len(responses['fetch_responses'])} fetch responses")
    print("✅ Data saved to hardcoded_exa_responses.json")
    
    # Print format reminder
    print("\n📋 Response Format Guide:")
    print("- Search: List of dicts with 'title' and 'url' keys")
    print("- Fetch: String content (or error string)")
    print("- Search errors: [{'error': 'type', 'message': 'details'}]")
    
    return responses

if __name__ == "__main__":
    asyncio.run(collect_responses())
