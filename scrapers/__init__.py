"""Prigogine quotes scraper modules."""

from .base import BaseScraper
from .cache import QuoteCache
from .wikiquote import WikiquoteScraper
from .goodreads import GoodreadsScraper
from .libquotes import LibQuotesScraper
from .azquotes import AZQuotesScraper
from .quotefancy import QuoteFancyScraper

__all__ = [
    'BaseScraper',
    'QuoteCache',
    'WikiquoteScraper',
    'GoodreadsScraper',
    'LibQuotesScraper',
    'AZQuotesScraper',
    'QuoteFancyScraper',
]
