"""
Test script to debug pricing extraction with enhanced logging
"""

import os
import logging
from dotenv import load_dotenv
from glowscape_agent import create_glowscape_agent

# Configure logging  
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('test_debug.log')
    ]
)
logger = logging.getLogger(__name__)

# Load environment
load_dotenv(".env.local")

def test_pricing_extraction():
    """Test pricing extraction with the URL that failed."""
    
    print("=" * 80)
    print("Testing pricing extraction for: https://www.upliftedrx.com/")
    print("=" * 80)
    
    # Create agent
    agent = create_glowscape_agent()
    
    # Test URL
    test_url = "https://www.upliftedrx.com/"
    message = f"Analyze the price of services: {test_url}"
    
    try:
        # Run agent
        response = agent.run(message, stream=False)
        
        # Print response
        print("\n" + "=" * 80)
        print("RESPONSE:")
        print("=" * 80)
        if hasattr(response, 'content'):
            print(response.content)
        else:
            print(str(response))
        print("=" * 80)
            
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        print(f"\nERROR: {e}")
        print("Check test_debug.log for details")

if __name__ == "__main__":
    test_pricing_extraction()

