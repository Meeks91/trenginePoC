"""
Content Filter Configuration
==============================
PruningContentFilter setup and excluded_tags list for Crawl4AI.
"""

from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

from config import PRUNING_THRESHOLD


def create_markdown_generator() -> DefaultMarkdownGenerator:
    """Create a markdown generator with PruningContentFilter."""
    pruning_filter = PruningContentFilter(
        threshold=PRUNING_THRESHOLD,
        threshold_type="fixed",
    )
    return DefaultMarkdownGenerator(content_filter=pruning_filter)
