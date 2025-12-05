"""
Google Maps Search Tool

Tool for searching businesses on Google Maps using Apify's Google Places scraper.
"""

import os
import json
from agno.tools import tool
from apify_client import ApifyClient


@tool
def google_maps_search(location: str, search_query: str = "MedSpa") -> str:
    """
    Search for businesses on Google Maps using Apify's Google Places scraper.
    
    Use this tool ONLY when the user explicitly asks to use Google Maps for searching.
    
    Args:
        location: The city, region, or geographic area to search in.
        search_query: The type of business to search for (default: "MedSpa").
        
    Returns:
        String containing information about the search results from Google Maps.
    """
    apify_token = os.getenv("APIFY_API_TOKEN")
    if not apify_token:
        return "Error: APIFY_API_TOKEN not configured."
    
    # Initialize Apify client
    client = ApifyClient(apify_token)
    
    # Prepare the input for the Google Places scraper
    run_input = {
        "searchStringsArray": [f"{search_query} in {location}"],
        "maxCrawledPlacesPerSearch": 25,
        "language": "en",
        "maxReviews": 0,
        "maxImages": 0,
    }
    
    try:
        # Run the actor and wait for it to finish
        run = client.actor("compass/crawler-google-places").call(run_input=run_input)
        
        # Fetch results from the actor's dataset
        results = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            results.append(item)
        
        # Format the results
        if not results:
            return f"No results found for '{search_query}' in {location}."
        
        formatted_results = f"Found {len(results)} results for '{search_query}' in {location}:\n\n"
        for idx, place in enumerate(results[:10], 1):  # Show first 10 results
            formatted_results += f"{idx}. {place.get('title', 'N/A')}\n"
            if place.get('address'):
                formatted_results += f"   Address: {place.get('address')}\n"
            if place.get('phone'):
                formatted_results += f"   Phone: {place.get('phone')}\n"
            if place.get('website'):
                formatted_results += f"   Website: {place.get('website')}\n"
            if place.get('rating'):
                formatted_results += f"   Rating: {place.get('rating')} ({place.get('reviewsCount', 0)} reviews)\n"
            formatted_results += "\n"
        
        if len(results) > 10:
            formatted_results += f"... and {len(results) - 10} more results.\n"
        
        return formatted_results
    
    except Exception as e:
        return f"Error running Google Maps search: {str(e)}"
