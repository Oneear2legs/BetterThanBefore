"""Quote caching layer."""

import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class QuoteCache:
    """In-memory and file-based caching for quotes."""

    def __init__(self, cache_file: Optional[str] = None):
        """
        Initialize cache.

        Args:
            cache_file: Path to persistent cache file
        """
        self.cache_file = cache_file or "/tmp/prigogine_quotes_cache.json"
        self.memory_cache: List[Dict[str, Any]] = []
        self.cache_timestamp = None
        self.load_from_file()

    def load_from_file(self):
        """Load quotes from persistent cache file."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.memory_cache = data.get("quotes", [])
                    self.cache_timestamp = data.get("timestamp")
                    logger.info(f"Loaded {len(self.memory_cache)} quotes from cache")
            except Exception as e:
                logger.warning(f"Failed to load cache: {e}")
                self.memory_cache = []

    def save_to_file(self):
        """Save quotes to persistent cache file."""
        try:
            os.makedirs(os.path.dirname(self.cache_file) or ".", exist_ok=True)
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "quotes": self.memory_cache,
                        "timestamp": datetime.now().isoformat(),
                        "count": len(self.memory_cache),
                    },
                    f,
                    ensure_ascii=False,
                    indent=2,
                )
            logger.info(f"Cached {len(self.memory_cache)} quotes to file")
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")

    def add_quotes(self, quotes: List[Dict[str, Any]]):
        """Add quotes to cache."""
        self.memory_cache.extend(quotes)
        self.cache_timestamp = datetime.now()
        self.save_to_file()

    def clear(self):
        """Clear all cached quotes."""
        self.memory_cache = []
        self.cache_timestamp = None
        if os.path.exists(self.cache_file):
            try:
                os.remove(self.cache_file)
            except Exception as e:
                logger.warning(f"Failed to delete cache file: {e}")

    def get_quotes(self) -> List[Dict[str, Any]]:
        """Get all cached quotes."""
        return self.memory_cache

    def get_random_quote(self) -> Optional[Dict[str, Any]]:
        """Get a random quote from cache."""
        if not self.memory_cache:
            return None
        import random

        return random.choice(self.memory_cache)

    def is_empty(self) -> bool:
        """Check if cache is empty."""
        return len(self.memory_cache) == 0

    def get_count(self) -> int:
        """Get number of cached quotes."""
        return len(self.memory_cache)
