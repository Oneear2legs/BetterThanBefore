"""LibQuotes scraper for Prigogine quotes."""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import logging

from .base import BaseScraper

logger = logging.getLogger(__name__)


class LibQuotesScraper(BaseScraper):
    """Scraper for LibQuotes Ilya Prigogine page."""

    def __init__(self):
        super().__init__(name="LibQuotes", priority=3)
        self.url = "https://libquotes.com/ilya-prigogine"

    def fetch_quotes(self) -> List[Dict[str, Any]]:
        """Fetch quotes from LibQuotes."""
        self.apply_rate_limit()
        quotes = []

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; PrigogineQuotesBot/1.0)"
            }

            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Find quote containers
            quote_containers = soup.find_all("div", class_="quote-item")
            if not quote_containers:
                quote_containers = soup.find_all("blockquote")

            for container in quote_containers:
                quote_text = container.get_text(strip=True)

                if not quote_text or len(quote_text) < 20:
                    continue

                quotes.append(
                    {
                        "text": quote_text,
                        "source_url": self.url,
                        "language": "en",
                        "author": "Ilya Prigogine",
                        "source_name": "LibQuotes",
                        "book": None,
                        "confidence": 0.8,
                    }
                )

            if quotes:
                self.record_success()
            else:
                self.record_failure("No quotes found")

        except Exception as e:
            self.record_failure(str(e))
            logger.error(f"LibQuotes scraper error: {e}")

        return quotes
