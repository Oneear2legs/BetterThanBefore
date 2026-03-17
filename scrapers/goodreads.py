"""Goodreads scraper for Prigogine quotes."""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import logging
import re

from .base import BaseScraper

logger = logging.getLogger(__name__)


class GoodreadsScraper(BaseScraper):
    """Scraper for Goodreads Ilya Prigogine quotes page."""

    def __init__(self):
        super().__init__(name="Goodreads", priority=2)
        self.url = "https://www.goodreads.com/author/quotes/178375.Ilya_Prigogine"

    def fetch_quotes(self) -> List[Dict[str, Any]]:
        """Fetch quotes from Goodreads."""
        self.apply_rate_limit()
        quotes = []

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; PrigogineQuotesBot/1.0)"
            }

            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Find quote containers - typically div with class containing "quote"
            quote_divs = soup.find_all("div", class_=re.compile("quote"))

            for div in quote_divs:
                # Extract quote text
                text_elem = div.find("span", class_="text")
                if not text_elem:
                    continue

                quote_text = text_elem.get_text(strip=True)
                # Remove quote marks if present
                quote_text = quote_text.strip('"')

                if not quote_text or len(quote_text) < 20:
                    continue

                # Try to find book source
                book_elem = div.find("a", class_="book-title")
                book_title = (
                    book_elem.get_text(strip=True) if book_elem else None
                )

                quotes.append(
                    {
                        "text": quote_text,
                        "source_url": self.url,
                        "language": "en",
                        "author": "Ilya Prigogine",
                        "source_name": "Goodreads",
                        "book": book_title,
                        "confidence": 0.85,
                    }
                )

            if quotes:
                self.record_success()
            else:
                self.record_failure("No quotes found")

        except Exception as e:
            self.record_failure(str(e))
            logger.error(f"Goodreads scraper error: {e}")

        return quotes
