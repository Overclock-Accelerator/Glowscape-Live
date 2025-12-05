# GlowScape Pricing Extraction Tools Guide

## Overview

GlowScape now includes powerful Firecrawl-based tools for extracting pricing information from medspa websites. These tools can discover, crawl, and extract structured pricing data from any medspa website.

## Prerequisites

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up Firecrawl API key:**
   - Get your API key from [firecrawl.dev](https://firecrawl.dev)
   - Add to your `.env.local` file:
```
FIRECRAWL_API_KEY=your_api_key_here
```

## Available Tools

### 1. `map_medspa_website(url)`
**Purpose:** Discover all pages on a medspa website

**When to use:** 
- First step to understand website structure
- Find pricing and service pages before scraping
- Quick discovery without downloading full content

**Example:**
```python
result = agent.run("Map all pages on https://www.upliftedrx.com/")
```

**Returns:**
- Categorized list of URLs (pricing pages, service pages, contact pages, etc.)
- Total page count
- All discovered links

---

### 2. `scrape_medspa_pricing(url)`
**Purpose:** Scrape content from a specific page

**When to use:**
- You know the exact URL of a pricing page
- Need detailed content from a single page
- Want markdown/HTML content for analysis

**Example:**
```python
result = agent.run("Scrape pricing from https://www.upliftedrx.com/price-list")
```

**Returns:**
- Page title and description
- Full markdown content
- Metadata

---

### 3. `crawl_medspa_for_pricing(url, max_pages=20)`
**Purpose:** Crawl entire website and automatically find pricing pages

**When to use:**
- You want comprehensive pricing data from the whole site
- Don't know which specific pages have pricing
- Need organized results with pricing vs service pages separated

**Example:**
```python
result = agent.run("Crawl https://www.upliftedrx.com/ for all pricing information")
```

**Returns:**
- All crawled pages with content
- Automatic categorization (pricing pages vs service pages)
- Summary of findings

**Recommended for:** Most use cases - it's comprehensive and automatic

---

### 4. `extract_structured_pricing(url)`
**Purpose:** AI-powered extraction of structured pricing data

**When to use:**
- You need organized, structured pricing information
- Want services categorized and prices extracted
- Need clean data for analysis or database storage

**Example:**
```python
result = agent.run("Extract all pricing data from https://www.upliftedrx.com/")
```

**Returns:**
- Service names
- Prices or price ranges
- Categories
- Descriptions
- Ready for LLM analysis

**Recommended for:** Final data extraction after understanding site structure

---

## Recommended Workflow

### Workflow 1: Quick Extraction (Recommended)
For most medspa websites, use this single-step approach:

```python
agent.run("Extract all pricing information from https://www.upliftedrx.com/")
```

The agent will automatically:
1. Crawl the website
2. Find pricing pages
3. Extract and organize pricing data
4. Present in structured format

---

### Workflow 2: Detailed Analysis
For more control or difficult websites:

**Step 1:** Discover structure
```python
agent.run("Map all pages on https://www.upliftedrx.com/")
```

**Step 2:** Crawl for content
```python
agent.run("Crawl https://www.upliftedrx.com/ for pricing, limit 15 pages")
```

**Step 3:** Extract structured data
```python
agent.run("Analyze the crawled content and extract all service prices in a table")
```

---

## Example Use Cases

### Example 1: Simple Price Extraction
```
You: Extract pricing from https://www.upliftedrx.com/

GlowScape will:
- Crawl the website
- Find pricing pages
- Extract services and prices
- Present in organized format
```

### Example 2: Compare Multiple Medspas
```
You: Extract pricing from these medspas:
- https://www.upliftedrx.com/
- https://www.examplemedspa.com/
- https://www.anothermedspa.com/

GlowScape will:
- Process each website
- Extract pricing from all
- Can compare pricing across medspas
```

### Example 3: Specific Service Pricing
```
You: Find botox pricing from https://www.upliftedrx.com/

GlowScape will:
- Crawl the site
- Filter for botox-related pricing
- Present relevant pricing information
```

---

## Tips and Best Practices

### 1. Start with Crawl or Extract
- Use `crawl_medspa_for_pricing` or `extract_structured_pricing` first
- These are comprehensive and automatic

### 2. Pricing Page Variations
Medspas often have pricing in multiple places:
- Dedicated `/pricing` or `/price-list` pages
- Individual service pages
- Treatment category pages
- Package/membership pages

The crawl tools automatically find all of these.

### 3. Handle Missing Pricing
Some medspas don't publish prices online. The agent will:
- Report what information IS available
- Identify service offerings
- Note if pricing requires consultation

### 4. Rate Limits
- Free Firecrawl tier has limits
- Use `max_pages` parameter to control crawl scope
- Start with 10-20 pages for most medspas

### 5. Content Analysis
The agent's LLM will:
- Parse pricing from various formats ($100, $50-$100, "Starting at $75")
- Identify service categories
- Extract package deals
- Note special offers

---

## Integration Examples

### CLI Usage
```bash
python glowscape_agent.py
```
Then type:
```
Extract all pricing from https://www.upliftedrx.com/
```

### API Usage
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Extract pricing from https://www.upliftedrx.com/"
  }'
```

### Python SDK Usage
```python
from glowscape_agent import create_glowscape_agent

agent = create_glowscape_agent()
response = agent.run("Extract pricing from https://www.upliftedrx.com/")
print(response.content)
```

---

## Troubleshooting

### "FIRECRAWL_API_KEY not found"
- Add your API key to `.env.local`
- Restart the agent/server

### "No pricing found"
- Try mapping the site first to see available pages
- Some medspas hide pricing behind contact forms
- Check if pricing requires login

### Crawl taking too long
- Reduce `max_pages` parameter
- Use `scrape_medspa_pricing` on known pricing pages
- Some sites have many pages; be patient

### Rate limit errors
- Firecrawl free tier has limits
- Wait and retry
- Upgrade Firecrawl plan for higher limits

---

## Cost Considerations

Firecrawl pricing (as of documentation):
- Free tier: Limited requests per month
- Paid tiers: Per-page pricing

Recommendations:
- Use `map_website` first (lightweight)
- Target specific pages with `scrape_medspa_pricing`
- Use `max_pages` to control costs
- Cache results to avoid re-crawling

---

## Next Steps

1. **Test on sample medspas:** Try the Uplifted RX example
2. **Build a database:** Store extracted pricing data
3. **Automate monitoring:** Track pricing changes over time
4. **Expand coverage:** Process multiple medspas in a city
5. **Add analytics:** Compare pricing across regions

---

## Support

For issues or questions:
- Check Firecrawl documentation: https://docs.firecrawl.dev
- Review Agno documentation: https://docs.agno.com
- Check tool responses for error messages
