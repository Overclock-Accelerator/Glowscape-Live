"""
MedSpa Pricing Extraction Tool using Firecrawl

Tool for discovering and extracting pricing information from medspa websites
using Firecrawl's mapping, crawling, and scraping capabilities.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from agno.tools import tool

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _get_firecrawl_client():
    """Get Firecrawl client instance."""
    try:
        from firecrawl import Firecrawl
    except ImportError as e:
        logger.error(f"Firecrawl import failed: {e}")
        raise ImportError(
            "firecrawl-py is required. Install with: pip install firecrawl-py"
        )
    
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        logger.error("FIRECRAWL_API_KEY not found in environment")
        raise ValueError(
            "FIRECRAWL_API_KEY not found in environment. "
            "Please add it to your .env.local file. "
            "Get your API key from https://firecrawl.dev"
        )
    
    return Firecrawl(api_key=api_key)


def _extract_pricing_from_content(content: str, url: str) -> Dict[str, Any]:
    """
    Parse pricing information from scraped content.
    
    Args:
        content: Markdown or HTML content from scraping
        url: The URL that was scraped
        
    Returns:
        Dictionary with extracted pricing information
    """
    # This is a helper function that could be enhanced with LLM parsing
    # For now, it returns the raw content for the agent to process
    return {
        "url": url,
        "content": content,
        "content_length": len(content)
    }


@tool
def map_medspa_website(url: str) -> str:
    """
    Map a medspa website to discover all available pages.
    
    This tool discovers the structure of a website and returns all URLs found.
    Use this first to understand what pages are available before scraping pricing info.
    
    Args:
        url: The medspa website URL to map (e.g., 'https://www.example.com')
        
    Returns:
        JSON string containing all discovered URLs and site structure
    """
    try:
        app = _get_firecrawl_client()
        result = app.map(url)
        
        if not result:
            logger.error(f"Firecrawl map returned empty result for {url}")
            return json.dumps({
                "success": False,
                "error": "No links found or invalid response from Firecrawl - empty result",
                "url": url,
                "debug_info": "Firecrawl API returned None or empty response"
            }, indent=2)
        
        # Handle both dict and object responses
        if isinstance(result, dict):
            links = result.get('links', [])
        else:
            # It's an object, access as attribute
            links = getattr(result, 'links', [])
        
        if not links:
            logger.error(f"Firecrawl map returned no links for {url}")
            return json.dumps({
                "success": False,
                "error": "No links found",
                "url": url,
                "debug_info": f"Result type: {type(result).__name__}"
            }, indent=2)
        
        # Organize URLs by likely content type
        
        categorized = {
            "pricing_pages": [],
            "service_pages": [],
            "contact_pages": [],
            "about_pages": [],
            "other_pages": []
        }
        
        for link in links:
            link_lower = link.lower()
            if any(keyword in link_lower for keyword in ['price', 'pricing', 'cost', 'packages']):
                categorized["pricing_pages"].append(link)
            elif any(keyword in link_lower for keyword in ['service', 'treatment', 'procedure', 'menu']):
                categorized["service_pages"].append(link)
            elif any(keyword in link_lower for keyword in ['contact', 'book', 'appointment']):
                categorized["contact_pages"].append(link)
            elif any(keyword in link_lower for keyword in ['about', 'team', 'provider']):
                categorized["about_pages"].append(link)
            else:
                categorized["other_pages"].append(link)
        
        return json.dumps({
            "success": True,
            "base_url": url,
            "total_pages": len(links),
            "categorized_pages": categorized,
            "all_links": links
        }, indent=2)
        
    except Exception as e:
        logger.error(f"Exception in map_medspa_website: {e}", exc_info=True)
        return json.dumps({
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "url": url,
            "debug_info": {
                "exception_details": str(e),
                "exception_type": type(e).__name__
            }
        }, indent=2)


@tool
def scrape_medspa_pricing(url: str) -> str:
    """
    Scrape pricing information from a specific medspa website page.
    
    Use this tool to extract the actual content from a pricing page or service page.
    The content will be returned in markdown format for easy parsing.
    
    Args:
        url: The specific page URL to scrape for pricing information
        
    Returns:
        JSON string containing scraped content and metadata
    """
    try:
        app = _get_firecrawl_client()
        
        # Scrape the page with markdown format
        result = app.scrape(
            url,
            formats=['markdown', 'html'],
            only_main_content=True
        )
        
        if not result:
            logger.error(f"Firecrawl scrape returned empty result for {url}")
            return json.dumps({
                "success": False,
                "error": "Failed to scrape URL - empty result",
                "url": url,
                "debug_info": "Firecrawl API returned None or empty response"
            }, indent=2)
        
        # Handle both dict and object responses
        if isinstance(result, dict):
            markdown_content = result.get('markdown', '')
            html_content = result.get('html', '')
            metadata = result.get('metadata', {})
        else:
            # It's an object, access as attributes
            markdown_content = getattr(result, 'markdown', '')
            html_content = getattr(result, 'html', '')
            metadata = getattr(result, 'metadata', {})
        
        # Extract title and description from metadata
        if isinstance(metadata, dict):
            title = metadata.get('title', '')
            description = metadata.get('description', '')
        else:
            title = getattr(metadata, 'title', '')
            description = getattr(metadata, 'description', '')
        
        return json.dumps({
            "success": True,
            "url": url,
            "title": title,
            "description": description,
            "markdown_content": markdown_content,
            "content_length": len(markdown_content),
            "has_html": bool(html_content)
        }, indent=2)
        
    except Exception as e:
        logger.error(f"Exception in scrape_medspa_pricing: {e}", exc_info=True)
        return json.dumps({
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "url": url,
            "debug_info": {
                "exception_details": str(e),
                "exception_type": type(e).__name__
            }
        }, indent=2)


@tool
def crawl_medspa_for_pricing(url: str, max_pages: int = 20) -> str:
    """
    Crawl an entire medspa website to discover and extract all pricing information.
    
    This is a comprehensive tool that crawls multiple pages on the website,
    focusing on finding pricing and service information. Use this when you want
    to extract all pricing data from a medspa website in one operation.
    
    Args:
        url: The base URL of the medspa website to crawl
        max_pages: Maximum number of pages to crawl (default: 20)
        
    Returns:
        JSON string containing all crawled pages with pricing-related content
    """
    try:
        app = _get_firecrawl_client()
        
        # Crawl the website with focus on content extraction
        result = app.crawl(
            url,
            limit=max_pages,
            scrape_options={
                'formats': ['markdown'],
                'only_main_content': True
            },
            poll_interval=5
        )
        
        if not result:
            logger.error(f"Firecrawl crawl returned empty result for {url}")
            return json.dumps({
                "success": False,
                "error": "Crawl returned empty result",
                "url": url,
                "debug_info": "Firecrawl API returned None or empty response"
            }, indent=2)
        
        # Handle both dict and object responses (CrawlJob object)
        if isinstance(result, dict):
            pages_data = result.get('data', [])
        else:
            # It's a CrawlJob object, access as attribute
            pages_data = getattr(result, 'data', [])
        
        if not pages_data:
            logger.error(f"Firecrawl crawl returned no data for {url}. Result type: {type(result).__name__}")
            return json.dumps({
                "success": False,
                "error": "Crawl failed or returned no data",
                "url": url,
                "debug_info": {
                    "result_type": type(result).__name__,
                    "result_str": str(result)[:500]
                }
            }, indent=2)
        
        # Filter and organize pages that likely contain pricing
        pricing_pages = []
        service_pages = []
        other_pages = []
        
        for page in pages_data:
            # Handle both dict and object page data
            if isinstance(page, dict):
                page_url = page.get('url', '')
                markdown = page.get('markdown', '')
                metadata = page.get('metadata', {})
            else:
                page_url = getattr(page, 'url', '')
                markdown = getattr(page, 'markdown', '')
                metadata = getattr(page, 'metadata', {})
            
            # Extract title from metadata
            if isinstance(metadata, dict):
                title = metadata.get('title', '')
            else:
                title = getattr(metadata, 'title', '')
            
            page_info = {
                "url": page_url,
                "title": title,
                "content": markdown,
                "content_length": len(markdown)
            }
            
            # Check if page likely contains pricing
            content_lower = markdown.lower()
            url_lower = page_url.lower()
            
            has_price_keywords = any(
                keyword in content_lower or keyword in url_lower
                for keyword in ['price', 'pricing', 'cost', '$', 'package', 'menu']
            )
            
            has_service_keywords = any(
                keyword in content_lower or keyword in url_lower
                for keyword in ['service', 'treatment', 'procedure', 'botox', 'filler', 'facial']
            )
            
            if has_price_keywords:
                pricing_pages.append(page_info)
            elif has_service_keywords:
                service_pages.append(page_info)
            else:
                other_pages.append(page_info)
        
        return json.dumps({
            "success": True,
            "base_url": url,
            "total_pages_crawled": len(pages_data),
            "pricing_pages_found": len(pricing_pages),
            "service_pages_found": len(service_pages),
            "pricing_pages": pricing_pages,
            "service_pages": service_pages,
            "summary": f"Crawled {len(pages_data)} pages, found {len(pricing_pages)} pricing pages and {len(service_pages)} service pages"
        }, indent=2)
        
    except Exception as e:
        logger.error(f"Exception in crawl_medspa_for_pricing: {e}", exc_info=True)
        return json.dumps({
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "url": url,
            "debug_info": {
                "exception_details": str(e),
                "exception_type": type(e).__name__
            }
        }, indent=2)


@tool
def extract_structured_pricing(website_url: str) -> str:
    """
    Extract structured pricing data from a medspa website using AI analysis.
    
    This is the most comprehensive tool that combines crawling and AI-powered
    extraction to return structured pricing information including service names,
    prices, categories, and descriptions.
    
    Args:
        website_url: The medspa website URL to analyze
        
    Returns:
        JSON string with structured pricing data organized by service category
    """
    try:
        # First, crawl the site to get all content
        app = _get_firecrawl_client()
        
        # Use a more focused crawl
        crawl_result = app.crawl(
            website_url,
            limit=15,
            scrape_options={
                'formats': ['markdown'],
                'only_main_content': True
            },
            poll_interval=5
        )
        
        if not crawl_result:
            logger.error(f"Firecrawl crawl returned empty result for {website_url}")
            return json.dumps({
                "success": False,
                "error": "Failed to crawl website - empty result",
                "website_url": website_url,
                "debug_info": "Firecrawl API returned None or empty response"
            }, indent=2)
        
        # Handle both dict and object responses (CrawlJob object)
        if isinstance(crawl_result, dict):
            pages_data = crawl_result.get('data', [])
        else:
            # It's a CrawlJob object, access as attribute
            pages_data = getattr(crawl_result, 'data', [])
        
        if not pages_data:
            logger.error(f"Firecrawl crawl returned no data for {website_url}. Result type: {type(crawl_result).__name__}")
            return json.dumps({
                "success": False,
                "error": "Failed to crawl website - no data in result",
                "website_url": website_url,
                "debug_info": {
                    "result_type": type(crawl_result).__name__,
                    "result_str": str(crawl_result)[:500]
                }
            }, indent=2)
        
        # Combine all content for analysis
        all_content = []
        
        for page in pages_data:
            # Handle both dict and object page data
            if isinstance(page, dict):
                page_url = page.get('url', '')
                page_title = page.get('metadata', {}).get('title', '')
                page_content = page.get('markdown', '')
            else:
                page_url = getattr(page, 'url', '')
                page_metadata = getattr(page, 'metadata', {})
                page_title = page_metadata.get('title', '') if isinstance(page_metadata, dict) else getattr(page_metadata, 'title', '')
                page_content = getattr(page, 'markdown', '')
            
            all_content.append({
                "url": page_url,
                "title": page_title,
                "content": page_content
            })
        
        # Return the raw data for the agent to analyze
        # The Agno agent will use its LLM to extract structured pricing
        return json.dumps({
            "success": True,
            "website_url": website_url,
            "pages_analyzed": len(all_content),
            "content_for_analysis": all_content,
            "instructions": (
                "Analyze the content above and extract all pricing information. "
                "For each service, identify: service name, price or price range, "
                "category (e.g., injectables, facials, laser treatments), "
                "and any relevant descriptions or details."
            )
        }, indent=2)
        
    except Exception as e:
        logger.error(f"Exception in extract_structured_pricing: {e}", exc_info=True)
        return json.dumps({
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "website_url": website_url,
            "debug_info": {
                "exception_details": str(e),
                "exception_type": type(e).__name__
            }
        }, indent=2)
