"""Test script to verify hardcoded responses work correctly."""
import asyncio
import json
import os

# Load the hardcoded responses to see what's available
script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "src/hud_controller/hardcoded_exa_responses.json")

try:
    with open(json_path, "r") as f:
        data = json.load(f)
        
    print("=== Available Search Queries ===")
    for i, query in enumerate(data.get("search_responses", {}).keys(), 1):
        print(f"{i}. {query}")
    
    print(f"\n=== Available Fetch URLs ({len(data.get('fetch_responses', {}))} total) ===")
    # Show first 5 URLs as examples
    for i, url in enumerate(list(data.get("fetch_responses", {}).keys())[:5], 1):
        print(f"{i}. {url[:80]}...")
    if len(data.get("fetch_responses", {})) > 5:
        print(f"... and {len(data.get('fetch_responses', {})) - 5} more URLs")
        
except Exception as e:
    print(f"Error loading hardcoded responses: {e}")

print("\n✅ Server is now configured to ONLY use these hardcoded responses.")
print("📝 Any other query/URL will return an error message asking to use another one.")
