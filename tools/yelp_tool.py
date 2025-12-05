"""
Yelp Scraper Tool

Tool for scraping business data from Yelp (currently returns placeholder data).
"""

import json
from agno.tools import tool


@tool
def yelp_scraper(location: str, search_query: str = "MedSpa") -> str:
    """
    Scrape business data from Yelp.
    
    Use this tool when the user explicitly asks to use Yelp for searching.
    
    Args:
        location: The city, region, or geographic area to search in.
        search_query: The type of business to search for (default: "MedSpa").
        
    Returns:
        String containing scraped data from Yelp.
    """
    # Placeholder gibberish data
    gibberish_data = {
        "source": "Yelp",
        "location": location,
        "search_query": search_query,
        "status": "scraped",
        "results": [
            {
                "name": "Xzqrtpw MedSpa & Wellness",
                "address": "1234 Flimbop Ave, " + location,
                "rating": 4.7,
                "review_count": 142,
                "phone": "(555) YELP-DATA",
                "categories": ["glorbnik", "medspa", "fnord"],
                "price_range": "$$",
                "data_quality": "quaziblorb"
            },
            {
                "name": "Zephylux Beauty Clinic",
                "address": "5678 Wompzilla Blvd, " + location,
                "rating": 4.9,
                "review_count": 287,
                "phone": "(555) YLP-SCRP",
                "categories": ["aesthetics", "splendiferous", "wellness"],
                "price_range": "$$$",
                "data_quality": "magnificorpio"
            },
            {
                "name": "Quixotica Rejuvenation Center",
                "address": "9012 Bramblesnorf St, " + location,
                "rating": 4.5,
                "review_count": 93,
                "phone": "(555) ELP-DATA",
                "categories": ["medspa", "fizzlebop", "treatments"],
                "price_range": "$$$$",
                "data_quality": "scrumptilescent"
            }
        ],
        "total_found": 3,
        "scraped_at": "2025-12-05T00:00:00Z",
        "encryption_key": "blipborp_42",
        "data_integrity": "wompwomp_verified"
    }
    
    return f"Successfully scraped Yelp data for '{search_query}' in {location}!\n\n{json.dumps(gibberish_data, indent=2)}"

