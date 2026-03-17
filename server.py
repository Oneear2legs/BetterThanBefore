#!/usr/bin/env python3
"""
HTTP server for the Prigogine quotes app with web scraping and caching.
Fetches real citations from multiple sources on startup.
"""
import http.server
import socketserver
import os
import json
import random
import logging
from pathlib import Path
from urllib.parse import urlparse
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import scrapers
from scrapers import (
    QuoteCache,
    WikiquoteScraper,
    GoodreadsScraper,
    LibQuotesScraper,
    AZQuotesScraper,
    QuoteFancyScraper,
)

PORT = 8000

# Fallback quotes (used if scraping fails completely)
FALLBACK_QUOTES = [
    {
        "text": "Time and experience are the factors that transform life. We do not merely observe the passage of time; we participate in it, and through this participation our lives acquire new meanings and directions.",
        "language": "en",
        "author": "Ilya Prigogine",
        "source_name": "Fallback Database",
        "source_url": "https://en.wikipedia.org/wiki/Ilya_Prigogine",
        "confidence": 0.9,
        "translations": {
            "ru": "Время и опыт - те факторы, которые преобразуют жизнь. Мы не просто наблюдаем течение времени; мы участвуем в нём, и через это участие наша жизнь приобретает новые смыслы и направления.",
            "fr": "Le temps et l'expérience sont les facteurs qui transforment la vie. Nous ne faisons pas que observer le passage du temps; nous y participons, et par cette participation nos vies acquièrent de nouveaux sens et directions.",
            "de": "Zeit und Erfahrung sind die Faktoren, die das Leben verändern. Wir beobachten nicht nur den Ablauf der Zeit; wir nehmen an ihr teil, und durch diese Teilnahme erhalten unsere Leben neue Bedeutungen und Richtungen.",
            "es": "El tiempo y la experiencia son los factores que transforman la vida. No simplemente observamos el paso del tiempo; participamos en él, y a través de esta participación nuestras vidas adquieren nuevos significados y direcciones.",
        },
    },
    {
        "text": "We are at the vanguard of time, but rooted in the past. This is the paradox of our existence: we strive forward, yet cannot deny what has shaped us.",
        "language": "en",
        "author": "Ilya Prigogine",
        "source_name": "Fallback Database",
        "source_url": "https://en.wikipedia.org/wiki/Ilya_Prigogine",
        "confidence": 0.9,
        "translations": {
            "ru": "Мы находимся в авангарде времени, но с корнями в прошлом. Это парадокс нашего существования: мы стремимся вперёд, но не можем отрицать того, что нас сформировало.",
            "fr": "Nous sommes à l'avant-garde du temps, mais enracinés dans le passé. C'est le paradoxe de notre existence: nous avançons, mais ne pouvons nier ce qui nous a formés.",
            "de": "Wir sind an der Spitze der Zeit, aber in der Vergangenheit verwurzelt. Das ist das Paradoxon unserer Existenz: Wir streben vorwärts, können aber nicht leugnen, was uns geprägt hat.",
            "es": "Estamos en la vanguardia del tiempo, pero enraizados en el pasado. Esta es la paradoja de nuestra existencia: avanzamos, pero no podemos negar lo que nos ha formado.",
        },
    },
    {
        "text": "Chaos is not the opposite of order, but its source. In the most chaotic systems new order is born, new structures, new complexity.",
        "language": "en",
        "author": "Ilya Prigogine",
        "source_name": "Fallback Database",
        "source_url": "https://en.wikipedia.org/wiki/Ilya_Prigogine",
        "confidence": 0.9,
        "translations": {
            "ru": "Хаос - это не противоположность порядку, а его источник. В самых хаотичных системах рождается новый порядок, новые структуры, новая сложность.",
            "fr": "Le chaos n'est pas l'opposé de l'ordre, mais sa source. Dans les systèmes les plus chaotiques naît un nouvel ordre, de nouvelles structures, une nouvelle complexité.",
            "de": "Chaos ist nicht das Gegenteil von Ordnung, sondern ihre Quelle. In den chaotischsten Systemen entsteht neue Ordnung, neue Strukturen, neue Komplexität.",
            "es": "El caos no es lo opuesto del orden, sino su fuente. En los sistemas más caóticos nace un nuevo orden, nuevas estructuras, nueva complejidad.",
        },
    },
]

# Global cache and quote pool
cache = QuoteCache()
quote_pool: List[Dict[str, Any]] = []


def initialize_scrapers():
    """Initialize and run all scrapers on startup."""
    global quote_pool

    logger.info("🔍 Initializing quote scrapers...")

    scrapers = [
        WikiquoteScraper(),
        GoodreadsScraper(),
        LibQuotesScraper(),
        AZQuotesScraper(),
        QuoteFancyScraper(),
    ]

    # Clear old cache to fetch fresh quotes
    cache.clear()

    scraped_count = 0
    for scraper in scrapers:
        if not scraper.is_available():
            logger.warning(f"Skipping {scraper.name} (too many failures)")
            continue

        try:
            logger.info(f"  Scraping {scraper.name}...")
            quotes = scraper.fetch_quotes()
            if quotes:
                cache.add_quotes(quotes)
                scraped_count += len(quotes)
                logger.info(f"    ✓ Found {len(quotes)} quotes")
        except Exception as e:
            logger.error(f"  ✗ {scraper.name} failed: {e}")

    # Use cached quotes or fall back to hardcoded quotes
    quote_pool = cache.get_quotes()

    if not quote_pool:
        logger.warning(
            "⚠️  No quotes scraped, using fallback database"
        )
        quote_pool = FALLBACK_QUOTES
        cache.add_quotes(FALLBACK_QUOTES)
    else:
        # Add fallback quotes as additional options
        quote_pool.extend(FALLBACK_QUOTES)

    logger.info(f"✨ Loaded {len(quote_pool)} total quotes")
    return len(quote_pool)


def normalize_quote_for_frontend(quote: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert scraped quote format to frontend format.

    Handles single-language quotes by translating to the display format.
    """
    # If the quote has translations, use them; otherwise provide the quote in available languages
    translations = quote.get("translations", {})
    text = quote.get("text", "")
    lang = quote.get("language", "en")

    # Build language-specific versions
    result = {
        "russian": translations.get("ru", text if lang == "ru" else ""),
        "english": translations.get("en", text if lang == "en" else ""),
        "fr": translations.get("fr", text if lang == "fr" else ""),
        "de": translations.get("de", text if lang == "de" else ""),
        "es": translations.get("es", text if lang == "es" else ""),
        "ja": translations.get("ja", text if lang == "ja" else ""),
        "zh": translations.get("zh", text if lang == "zh" else ""),
        "it": translations.get("it", text if lang == "it" else ""),
        "pt": translations.get("pt", text if lang == "pt" else ""),
        "ar": translations.get("ar", text if lang == "ar" else ""),
        # Add source info
        "source": {
            "name": quote.get("source_name", "Unknown"),
            "url": quote.get("source_url", ""),
        },
        # Keep original text for reference
        "original_text": text,
        "original_language": lang,
    }

    return result


class QuoteHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler for the Prigogine quotes app."""

    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)

        if parsed_path.path == "/api/quote":
            self.handle_quote_request()
        else:
            super().do_GET()

    def handle_quote_request(self):
        """Handle quote API request."""
        try:
            if not quote_pool:
                self.send_error(503, "No quotes available")
                return

            # Get random quote from pool
            quote = random.choice(quote_pool)
            normalized = normalize_quote_for_frontend(quote)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            self.wfile.write(
                json.dumps(normalized, ensure_ascii=False).encode()
            )

        except Exception as e:
            logger.error(f"Error handling quote request: {e}")
            self.send_error(500, str(e))

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def start_server():
    """Start the HTTP server."""
    os.chdir(Path(__file__).parent)

    # Initialize scrapers on startup
    logger.info("")
    logger.info("=" * 60)
    logger.info("🌍 PRIGOGINE QUOTES APP - INITIALIZATION")
    logger.info("=" * 60)
    quote_count = initialize_scrapers()
    logger.info("=" * 60)
    logger.info("")

    with socketserver.TCPServer(("", PORT), QuoteHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"\n✨ Prigogine Insights App is running!")
        print(f"📍 Open your browser: {url}")
        print(f"🛑 Press Ctrl+C to stop the server")
        print(f"📊 Serving {quote_count} quotes from live sources\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✋ Server stopped.")


if __name__ == "__main__":
    start_server()
