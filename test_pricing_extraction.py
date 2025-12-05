"""
Test script for pricing extraction tools

This script demonstrates how to use the new Firecrawl-based pricing
extraction tools with the GlowScape agent.
"""

import os
from dotenv import load_dotenv
from glowscape_agent import create_glowscape_agent

# Load environment variables
load_dotenv(".env.local")


def test_map_website():
    """Test mapping a medspa website."""
    print("\n" + "="*60)
    print("TEST 1: Mapping Website Structure")
    print("="*60)
    
    agent = create_glowscape_agent()
    response = agent.run(
        "Map all pages on https://www.upliftedrx.com/",
        stream=False
    )
    
    print("\nAgent Response:")
    print(response.content if hasattr(response, 'content') else response)


def test_crawl_for_pricing():
    """Test crawling a website for pricing information."""
    print("\n" + "="*60)
    print("TEST 2: Crawling Website for Pricing")
    print("="*60)
    
    agent = create_glowscape_agent()
    response = agent.run(
        "Crawl https://www.upliftedrx.com/ for all pricing information, limit to 15 pages",
        stream=False
    )
    
    print("\nAgent Response:")
    print(response.content if hasattr(response, 'content') else response)


def test_extract_structured_pricing():
    """Test extracting structured pricing data."""
    print("\n" + "="*60)
    print("TEST 3: Extracting Structured Pricing Data")
    print("="*60)
    
    agent = create_glowscape_agent()
    response = agent.run(
        "Extract all pricing information from https://www.upliftedrx.com/ and organize it by service category",
        stream=False
    )
    
    print("\nAgent Response:")
    print(response.content if hasattr(response, 'content') else response)


def test_specific_page_scrape():
    """Test scraping a specific pricing page."""
    print("\n" + "="*60)
    print("TEST 4: Scraping Specific Page")
    print("="*60)
    
    agent = create_glowscape_agent()
    
    # First map to find the pricing page URL
    print("\nStep 1: Finding pricing page...")
    map_response = agent.run(
        "Map https://www.upliftedrx.com/ and tell me which page has pricing",
        stream=False
    )
    print(map_response.content if hasattr(map_response, 'content') else map_response)


def test_compare_approach():
    """Test comparing the different approaches."""
    print("\n" + "="*60)
    print("TEST 5: Comparing Approaches")
    print("="*60)
    
    agent = create_glowscape_agent()
    
    print("\n--- Approach 1: Quick extraction (recommended) ---")
    response1 = agent.run(
        "Extract all pricing from https://www.upliftedrx.com/",
        stream=False
    )
    print(response1.content if hasattr(response1, 'content') else response1)


def main():
    """Run all tests."""
    # Check for API key
    if not os.getenv("FIRECRAWL_API_KEY"):
        print("ERROR: FIRECRAWL_API_KEY not found in environment.")
        print("Please add it to your .env.local file:")
        print("FIRECRAWL_API_KEY=your_api_key_here")
        return
    
    print("\n" + "="*60)
    print("GlowScape Pricing Extraction Tool Tests")
    print("="*60)
    print("\nThese tests demonstrate the different pricing extraction tools.")
    print("Tests will use https://www.upliftedrx.com/ as an example.")
    print("\nNOTE: These tests make real API calls to Firecrawl and will")
    print("consume credits from your account.")
    
    # Menu
    print("\n\nSelect a test to run:")
    print("1. Map website structure (lightweight)")
    print("2. Crawl for pricing (comprehensive)")
    print("3. Extract structured pricing (most useful)")
    print("4. Scrape specific page")
    print("5. Compare approaches")
    print("6. Run all tests")
    print("0. Exit")
    
    choice = input("\nEnter choice (0-6): ").strip()
    
    tests = {
        "1": test_map_website,
        "2": test_crawl_for_pricing,
        "3": test_extract_structured_pricing,
        "4": test_specific_page_scrape,
        "5": test_compare_approach,
    }
    
    if choice == "0":
        print("Exiting...")
        return
    elif choice == "6":
        for test_func in tests.values():
            try:
                test_func()
            except Exception as e:
                print(f"\nTest failed: {e}")
    elif choice in tests:
        try:
            tests[choice]()
        except Exception as e:
            print(f"\nTest failed: {e}")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
