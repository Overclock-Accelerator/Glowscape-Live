# GlowScape Agent

A conversational AI agent specialized in extracting and analyzing MedSpa business information from multiple data sources including Google Maps, Yelp, and comprehensive website pricing extraction.

## Features

- **Interactive terminal-based chat interface**
- **MedSpa location discovery** - Find medspas by city using Google Maps or Yelp
- **Pricing extraction** - Automatically crawl and extract pricing from medspa websites
- **Structured data** - Extract names, addresses, phones, ratings, reviews, services, hours, and prices
- **AI-powered analysis** - Organize and categorize pricing by service type
- **Multi-source integration** - Google Maps (via Apify), Yelp, and Firecrawl for web scraping
- **REST API** - Deploy as a web service on Railway or other platforms

## Project Structure

```
GlowScape/
├── glowscape_agent.py           # Main agent application (CLI)
├── server.py                    # FastAPI server wrapper
├── tools/                       # Custom tools directory
│   ├── __init__.py             # Tools module initialization
│   ├── google_maps_tool.py     # Google Maps scraping via Apify
│   ├── yelp_tool.py            # Yelp scraping
│   ├── medspa_extraction.py    # Mock data tool
│   └── pricing_extraction.py   # Firecrawl-based pricing extraction
├── requirements.txt             # Python dependencies
├── .env.local                  # Environment variables (create this)
├── README.md                   # This file
├── PRICING_TOOL_GUIDE.md       # Detailed pricing tool documentation
├── test_pricing_extraction.py  # Test suite for pricing tools
├── Procfile                    # Railway deployment config
└── railway.json                # Railway configuration
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env.local` file:**
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   APIFY_API_TOKEN=your_apify_api_token_here
   FIRECRAWL_API_KEY=your_firecrawl_api_key_here
   ```
   
   Get API keys from:
   - OpenAI: https://platform.openai.com/api-keys
   - Apify: https://console.apify.com/account/integrations
   - Firecrawl: https://firecrawl.dev

3. **Run the agent:**
   ```bash
   python glowscape_agent.py
   ```

## Usage

### CLI Mode

Once running, you can interact with GlowScape:

- **Get capabilities:** "What can you help me with?"
- **Find MedSpas by location:** "Find medspas in Miami using Google Maps"
- **Extract pricing:** "Extract all pricing from https://www.upliftedrx.com/"
- **Scrape Yelp:** "Find medspas on Yelp in Fort Lee, NJ"
- **Exit:** Type `quit`, `exit`, or `q`

### API Mode

Start the server:
```bash
python server.py
```

Then make requests:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Extract pricing from https://www.upliftedrx.com/"}'
```

### Test Pricing Tools

Run the test suite:
```bash
python test_pricing_extraction.py
```

## Current Status

- ✅ Interactive CLI agent
- ✅ FastAPI REST API server
- ✅ Google Maps integration via Apify
- ✅ Yelp scraping integration
- ✅ **Firecrawl website scraping and pricing extraction**
- ✅ Multi-tool orchestration
- ✅ Railway deployment ready

## Tools

### Location Discovery Tools

#### `google_maps_search`
Search for medspas using Google Maps/Places via Apify.
- **Parameter:** `query` (str) - Search query like "medspas in Miami"
- **Returns:** Business listings with addresses, ratings, reviews, etc.

#### `yelp_scraper`
Search for medspas on Yelp.
- **Parameter:** `query` (str) - Search query with location
- **Returns:** Yelp business data

### Pricing Extraction Tools (Firecrawl)

#### `map_medspa_website`
Discover all pages on a medspa website.
- **Parameter:** `url` (str) - Website URL
- **Returns:** Categorized list of all page URLs
- **Use case:** First step to understand site structure

#### `scrape_medspa_pricing`
Scrape a specific pricing page.
- **Parameter:** `url` (str) - Specific page URL
- **Returns:** Page content in markdown format
- **Use case:** When you know the exact pricing page URL

#### `crawl_medspa_for_pricing`
Crawl entire website for pricing information.
- **Parameters:** 
  - `url` (str) - Base website URL
  - `max_pages` (int) - Maximum pages to crawl (default: 20)
- **Returns:** All pages with automatic pricing/service categorization
- **Use case:** Comprehensive pricing extraction (recommended)

#### `extract_structured_pricing`
AI-powered structured pricing extraction.
- **Parameter:** `url` (str) - Website URL
- **Returns:** Content ready for LLM analysis and structuring
- **Use case:** Get organized pricing data by service category

## Detailed Documentation

For comprehensive pricing extraction documentation, see [PRICING_TOOL_GUIDE.md](PRICING_TOOL_GUIDE.md)

## Deployment

### Railway Deployment

1. Connect your GitHub repository to Railway
2. Add environment variables in Railway dashboard
3. Railway will automatically deploy using `Procfile`

### Local Development

Run the server locally:
```bash
uvicorn server:app --reload --port 8000
```

## Development Notes

- The agent explicitly communicates which tools it uses for transparency
- All tools return JSON for easy parsing and integration
- Pricing extraction uses Firecrawl's advanced crawling capabilities
- LLM analysis helps structure and categorize extracted pricing data

