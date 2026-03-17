"""Wikiquote scraper for Prigogine quotes."""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import logging

from .base import BaseScraper

logger = logging.getLogger(__name__)


class WikiquoteScraper(BaseScraper):
    """Scraper for Wikiquote Ilya Prigogine page."""

    def __init__(self):
        super().__init__(name="Wikiquote", priority=1)
        self.base_url = "https://en.wikiquote.org/wiki/Ilya_Prigogine"
        self.language_urls = {
            "fr": "https://fr.wikiquote.org/wiki/Ilya_Prigogine",
            "de": "https://de.wikiquote.org/wiki/Ilya_Prigogine",
            "ru": "https://ru.wikiquote.org/wiki/Илья_Пригожин",
        }

    def fetch_quotes(self) -> List[Dict[str, Any]]:
        """Fetch quotes from Wikiquote in multiple languages."""
        self.apply_rate_limit()
        quotes = []

        try:
            # Fetch English quotes
            quotes.extend(self._fetch_language_quotes("en", self.base_url))

            # Fetch other languages
            for lang, url in self.language_urls.items():
                try:
                    quotes.extend(self._fetch_language_quotes(lang, url))
                except Exception as e:
                    logger.warning(f"Failed to fetch {lang} from Wikiquote: {e}")

            if quotes:
                self.record_success()
            else:
                self.record_failure("No quotes found")

        except Exception as e:
            self.record_failure(str(e))
            logger.error(f"Wikiquote scraper error: {e}")

        return quotes

    def _fetch_language_quotes(self, lang: str, url: str) -> List[Dict[str, Any]]:
        """Fetch quotes from a specific language Wikiquote page."""
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; PrigogineQuotesBot/1.0)"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        quotes = []

        # Find quote sections - typically in <dl> or <blockquote> tags
        quote_containers = soup.find_all("dl")

        for container in quote_containers:
            # Extract quote text (usually in <dd> or after <dt>)
            text_elem = container.find("dd")
            if not text_elem:
                # Alternative: look for direct text
                continue

            quote_text = text_elem.get_text(strip=True)
            if not quote_text or len(quote_text) < 20:
                continue

            # Try to find source information
            source_elem = container.find_next("dd", class_="noprint")
            source_text = (
                source_elem.get_text(strip=True)
                if source_elem
                else "Wikiquote"
            )

            quotes.append(
                {
                    "text": quote_text,
                    "source_url": url,
                    "language": lang,
                    "author": "Ilya Prigogine",
                    "source_name": "Wikiquote",
                    "book": source_text if source_text != "Wikiquote" else None,
                    "confidence": 0.9,
                }
            )

        return quotes
