"""
GlowScape Agent - MedSpa Location Data Extraction Agent

A conversational AI agent specialized in extracting and analyzing 
MedSpa business information from Google Maps/Places.
"""

import os
import logging
from textwrap import dedent

from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat

from tools import (
    google_maps_search, 
    yelp_scraper,
    map_medspa_website,
    scrape_medspa_pricing,
    crawl_medspa_for_pricing,
    extract_structured_pricing
)

# Configure logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('glowscape_debug.log')
    ]
)
logger = logging.getLogger(__name__)

load_dotenv(".env.local")

GLOWSCAPE_DESCRIPTION = dedent("""
    You are GlowScape, a specialized AI agent designed to help users discover and extract 
    comprehensive data about MedSpa (Medical Spa) businesses. You have expertise in:
    
    - Locating MedSpa businesses across cities and regions
    - Extracting business details including names, addresses, phone numbers, and websites
    - Gathering ratings, reviews, and operational hours
    - Identifying service offerings and specializations
    - Compiling structured datasets for analysis
    - Extracting pricing information from medspa websites using advanced web scraping
    - Mapping website structures to discover all available pages
    
    You have access to multiple data sources including Google Maps, Yelp, and Firecrawl for
    comprehensive website analysis and pricing extraction.
""")

GLOWSCAPE_INSTRUCTIONS = [
    "Introduce yourself as GlowScape when users first interact with you.",
    "Explain your capabilities clearly when asked what you can do.",
    "You have access to Google Maps, Yelp, and Firecrawl tools for comprehensive data extraction.",
    "Use the google_maps_search tool when users want to find medspas by location.",
    "Use the yelp_scraper tool when users want Yelp-specific data.",
    "For pricing extraction from websites, use these Firecrawl tools:",
    "  - map_medspa_website: Discover all pages on a website first",
    "  - scrape_medspa_pricing: Scrape a specific pricing page",
    "  - crawl_medspa_for_pricing: Crawl entire site for pricing info (recommended)",
    "  - extract_structured_pricing: Get AI-analyzed structured pricing data (most comprehensive)",
    "When a user provides a medspa website URL, use crawl_medspa_for_pricing or extract_structured_pricing.",
    "After crawling, analyze the content to identify services, prices, and categorize them logically.",
    "Present pricing information in clear tables or structured formats.",
    "If pricing is not found, explain what information was available on the site.",
    "After using a tool, clearly state which data source was used.",
    "Provide structured, organized responses when presenting business data.",
]


def create_glowscape_agent() -> Agent:
    """Create and configure the GlowScape agent."""
    # Validate Apify API token for Google Maps tool
    apify_token = os.getenv("APIFY_API_TOKEN")
    if not apify_token:
        raise ValueError(
            "APIFY_API_TOKEN not found in environment. "
            "Please add it to your .env.local file."
        )
    
    # Validate Firecrawl API token
    firecrawl_token = os.getenv("FIRECRAWL_API_KEY")
    if not firecrawl_token:
        logger.error("FIRECRAWL_API_KEY not found - pricing tools will not work")
    
    agent = Agent(
        name="GlowScape",
        model=OpenAIChat(id="gpt-4o-mini"),
        description=GLOWSCAPE_DESCRIPTION,
        instructions=GLOWSCAPE_INSTRUCTIONS,
        tools=[
            google_maps_search, 
            yelp_scraper,
            map_medspa_website,
            scrape_medspa_pricing,
            crawl_medspa_for_pricing,
            extract_structured_pricing
        ],
        markdown=True,
        add_datetime_to_context=True,
    )
    return agent


def main():
    """Run the GlowScape agent in interactive terminal mode."""
    agent = create_glowscape_agent()
    
    print("\n" + "=" * 60)
    print("  GlowScape - MedSpa Location Data Agent")
    print("=" * 60)
    print("Type 'quit' or 'exit' to end the session.\n")
    
    # Initial greeting
    agent.print_response("Introduce yourself and explain what you can help with.", stream=True)
    
    # Interactive loop
    while True:
        try:
            user_input = input("\n\nYou: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ("quit", "exit", "q"):
                print("\nGoodbye! Thank you for using GlowScape.")
                break
            
            print("\nGlowScape: ", end="")
            agent.print_response(user_input, stream=True)
            
        except KeyboardInterrupt:
            print("\n\nSession interrupted. Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()

