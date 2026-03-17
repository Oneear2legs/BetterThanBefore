"""A-Z Quotes scraper for Prigogine quotes."""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import logging

from .base import BaseScraper

logger = logging.getLogger(__name__)


class AZQuotesScraper(BaseScraper):
    """Scraper for A-Z Quotes Ilya Prigogine page."""

    def __init__(self):
        super().__init__(name="A-Z Quotes", priority=4)
        self.url = "https://www.azquotes.com/author/11886-Ilya_Prigogine"

    def fetch_quotes(self) -> List[Dict[str, Any]]:
        """Fetch quotes from A-Z Quotes."""
        self.apply_rate_limit()
        quotes = []

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; PrigogineQuotesBot/1.0)"
            }

            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Find quote containers - typically div with class "quote"
            quote_containers = soup.find_all("a", class_="quote-link")

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
                        "source_name": "A-Z Quotes",
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
            logger.error(f"A-Z Quotes scraper error: {e}")

        return quotes
