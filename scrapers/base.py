"""Base scraper class for Prigogine quotes."""

import time
import random
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Abstract base class for all quote scrapers."""

    def __init__(self, name: str, priority: int = 1, rate_limit: float = 1.0):
        """
        Initialize scraper.

        Args:
            name: Identifier for the scraper source
            priority: Priority order (1 = highest)
            rate_limit: Minimum seconds between requests
        """
        self.name = name
        self.priority = priority
        self.rate_limit = rate_limit
        self.last_request_time = 0
        self.consecutive_failures = 0
        self.max_failures = 3

    @abstractmethod
    def fetch_quotes(self) -> List[Dict[str, Any]]:
        """
        Fetch quotes from source.

        Returns:
            List of quote dicts with structure:
            {
                'text': str,
                'source_url': str,
                'language': str,  # detected language
                'author': str,
                'book': Optional[str],
                'translations': Dict[str, str],  # other language versions if found
                'confidence': float  # 0-1 authenticity score
            }
        """
        pass

    def apply_rate_limit(self):
        """Apply rate limiting between requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            sleep_time = self.rate_limit - elapsed + random.uniform(0.1, 0.5)
            time.sleep(sleep_time)
        self.last_request_time = time.time()

    def record_success(self):
        """Record successful fetch."""
        self.consecutive_failures = 0

    def record_failure(self, error: str = ""):
        """Record failed fetch."""
        self.consecutive_failures += 1
        logger.warning(f"{self.name} failed (attempt {self.consecutive_failures}): {error}")

    def is_available(self) -> bool:
        """Check if scraper should be tried (circuit breaker)."""
        return self.consecutive_failures < self.max_failures

    def get_status(self) -> Dict[str, Any]:
        """Get scraper health status."""
        return {
            "name": self.name,
            "available": self.is_available(),
            "failures": self.consecutive_failures,
            "last_request": datetime.fromtimestamp(self.last_request_time).isoformat()
            if self.last_request_time
            else None,
        }
