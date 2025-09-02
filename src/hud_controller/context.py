"""Context that persists across hot-reloads for DeepResearch."""
from hud.server.context import run_context_server
import asyncio
from typing import List, Dict, Any
from datetime import datetime

class Context:
    def __init__(self):
        self.search_count = 0
        self.fetch_count = 0
        self.search_history = []
        self.fetch_history = []
        self.submitted_answer = None  # Store the agent's final answer
    
    def add_search(self, query: str, results: List[Dict[str, str]]):
        """Track a search operation."""
        self.search_count += 1
        self.search_history.append({
            'query': query,
            'results_count': len(results),
            'timestamp': datetime.now().isoformat()
        })
        # Keep only last 100 searches in memory
        if len(self.search_history) > 100:
            self.search_history = self.search_history[-100:]
    
    def add_fetch(self, url: str, content_length: int):
        """Track a fetch operation."""
        self.fetch_count += 1
        self.fetch_history.append({
            'url': url,
            'content_length': content_length,
            'timestamp': datetime.now().isoformat()
        })
        # Keep only last 100 fetches in memory
        if len(self.fetch_history) > 100:
            self.fetch_history = self.fetch_history[-100:]
    
    def get_search_count(self) -> int:
        """Get total number of searches performed."""
        return self.search_count
    
    def get_fetch_count(self) -> int:
        """Get total number of fetches performed."""
        return self.fetch_count
    
    def get_total_operations(self) -> int:
        """Get total number of operations performed."""
        return self.search_count + self.fetch_count
    
    def get_recent_searches(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent search history."""
        return self.search_history[-limit:]
    
    def get_recent_fetches(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent fetch history."""
        return self.fetch_history[-limit:]
    
    def submit_answer(self, answer: str):
        """Store the agent's final answer."""
        self.submitted_answer = answer
    
    def get_submitted_answer(self) -> str:
        """Get the submitted answer."""
        return self.submitted_answer
    
    def reset_stats(self):
        """Reset all statistics."""
        self.search_count = 0
        self.fetch_count = 0
        self.search_history = []
        self.fetch_history = []
        self.submitted_answer = None

if __name__ == "__main__":
    asyncio.run(run_context_server(Context()))