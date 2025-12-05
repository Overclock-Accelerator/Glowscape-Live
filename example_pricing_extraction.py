"""
Example: Pricing Extraction Workflow

This example demonstrates a complete workflow for extracting and analyzing
pricing information from a medspa website using GlowScape.
"""

from dotenv import load_dotenv
from glowscape_agent import create_glowscape_agent

# Load environment variables
load_dotenv(".env.local")


def example_simple_extraction():
    """
    Example 1: Simple one-step pricing extraction
    
    This is the recommended approach for most use cases.
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Simple Pricing Extraction")
    print("="*70)
    print("\nUse case: Extract all pricing from a medspa website in one step")
    print("Target: https://www.upliftedrx.com/\n")
    
    # Create agent
    agent = create_glowscape_agent()
    
    # Single request to extract all pricing
    print("Agent is processing...\n")
    response = agent.run(
        "Extract all pricing information from https://www.upliftedrx.com/ "
        "and organize it in a table by service category. "
        "Include service names, prices, and descriptions.",
        stream=False
    )
    
    print("\n" + "-"*70)
    print("RESULT:")
    print("-"*70)
    print(response.content if hasattr(response, 'content') else response)


def example_multi_step_workflow():
    """
    Example 2: Multi-step workflow with mapping first
    
    Use this when you want more control over the extraction process.
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Multi-Step Workflow")
    print("="*70)
    print("\nUse case: First map the site, then extract pricing")
    print("Target: https://www.upliftedrx.com/\n")
    
    agent = create_glowscape_agent()
    
    # Step 1: Map the website
    print("Step 1: Mapping website structure...\n")
    map_response = agent.run(
        "Map all pages on https://www.upliftedrx.com/ and identify which pages likely contain pricing information",
        stream=False
    )
    
    print("\n" + "-"*70)
    print("MAPPING RESULT:")
    print("-"*70)
    print(map_response.content if hasattr(map_response, 'content') else map_response)
    
    # Step 2: Extract pricing from discovered pages
    print("\n\nStep 2: Extracting pricing from identified pages...\n")
    pricing_response = agent.run(
        "Now crawl https://www.upliftedrx.com/ focusing on the pricing pages you just identified. "
        "Extract all service prices and organize them by category.",
        stream=False
    )
    
    print("\n" + "-"*70)
    print("PRICING EXTRACTION RESULT:")
    print("-"*70)
    print(pricing_response.content if hasattr(pricing_response, 'content') else pricing_response)


def example_targeted_extraction():
    """
    Example 3: Extract specific service pricing
    
    Use this when you only need pricing for specific services.
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Targeted Service Extraction")
    print("="*70)
    print("\nUse case: Extract pricing for specific services only")
    print("Target: https://www.upliftedrx.com/ (Botox and Filler services)\n")
    
    agent = create_glowscape_agent()
    
    print("Agent is processing...\n")
    response = agent.run(
        "Extract pricing from https://www.upliftedrx.com/ but only for "
        "Botox, dermal fillers, and injectable services. Show the results in a clear format.",
        stream=False
    )
    
    print("\n" + "-"*70)
    print("RESULT:")
    print("-"*70)
    print(response.content if hasattr(response, 'content') else response)


def example_compare_medspas():
    """
    Example 4: Compare pricing across multiple medspas
    
    Use this to analyze pricing across competitors.
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Compare Multiple Medspas")
    print("="*70)
    print("\nUse case: Extract and compare pricing from multiple medspas")
    print("Note: This example would use multiple websites (simplified here)\n")
    
    agent = create_glowscape_agent()
    
    # In a real scenario, you'd do this for multiple sites
    medspa_url = "https://www.upliftedrx.com/"
    
    print(f"Extracting pricing from: {medspa_url}\n")
    response = agent.run(
        f"Extract pricing from {medspa_url} and focus on: "
        "1. Botox pricing, "
        "2. Filler pricing, "
        "3. Facial treatment pricing. "
        "Format as a comparison-ready table.",
        stream=False
    )
    
    print("\n" + "-"*70)
    print("RESULT:")
    print("-"*70)
    print(response.content if hasattr(response, 'content') else response)
    
    print("\n" + "-"*70)
    print("NOTE: To compare multiple medspas, repeat this for each URL")
    print("then ask the agent to compare the results.")
    print("-"*70)


def example_location_plus_pricing():
    """
    Example 5: Find medspas and extract pricing
    
    Complete workflow: discover medspas in a city, then extract their pricing.
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Complete Workflow - Location Discovery + Pricing")
    print("="*70)
    print("\nUse case: Find medspas in a city, then extract pricing from their websites")
    print("Target: Fort Lee, NJ\n")
    
    agent = create_glowscape_agent()
    
    # Step 1: Find medspas in the area
    print("Step 1: Finding medspas in Fort Lee, NJ...\n")
    location_response = agent.run(
        "Find medspas in Fort Lee, NJ using Google Maps. Include their websites.",
        stream=False
    )
    
    print("\n" + "-"*70)
    print("MEDSPAS FOUND:")
    print("-"*70)
    print(location_response.content if hasattr(location_response, 'content') else location_response)
    
    # Step 2: Extract pricing from one of them
    print("\n\nStep 2: Extracting pricing from Uplifted RX (one of the results)...\n")
    pricing_response = agent.run(
        "Now extract all pricing information from https://www.upliftedrx.com/ "
        "which is one of the medspas we just found.",
        stream=False
    )
    
    print("\n" + "-"*70)
    print("PRICING FROM UPLIFTED RX:")
    print("-"*70)
    print(pricing_response.content if hasattr(pricing_response, 'content') else pricing_response)


def main():
    """Main menu to run different examples."""
    print("\n" + "="*70)
    print(" GlowScape Pricing Extraction Examples")
    print("="*70)
    print("\nThese examples demonstrate different ways to use GlowScape")
    print("for extracting medspa pricing information.")
    print("\nWARNING: These examples make real API calls and will consume")
    print("credits from your Firecrawl and OpenAI accounts.")
    
    examples = {
        "1": ("Simple one-step extraction", example_simple_extraction),
        "2": ("Multi-step workflow (map then extract)", example_multi_step_workflow),
        "3": ("Targeted extraction (specific services)", example_targeted_extraction),
        "4": ("Compare multiple medspas", example_compare_medspas),
        "5": ("Complete workflow (find + extract)", example_location_plus_pricing),
    }
    
    print("\n\nSelect an example to run:\n")
    for key, (description, _) in examples.items():
        print(f"{key}. {description}")
    print("0. Exit")
    
    choice = input("\nEnter choice (0-5): ").strip()
    
    if choice == "0":
        print("\nExiting...")
        return
    
    if choice in examples:
        _, example_func = examples[choice]
        try:
            example_func()
            print("\n\nExample completed successfully!")
        except Exception as e:
            print(f"\n\nExample failed with error: {e}")
    else:
        print("\nInvalid choice")


if __name__ == "__main__":
    main()

