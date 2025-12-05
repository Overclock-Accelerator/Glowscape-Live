# GlowScape Debugging Guide

## Overview

This guide explains how to use the enhanced debugging features in GlowScape to troubleshoot issues with pricing extraction and other tools.

## Debug Logging

### Logging Levels

The application now has comprehensive DEBUG-level logging enabled throughout:

- **Agent initialization**: Tracks API key validation and agent setup
- **Tool execution**: Logs every Firecrawl API call with parameters and responses
- **Error handling**: Full exception traces with context

### Log Files

When running the application, debug information is written to:

1. **`glowscape_debug.log`** - Interactive CLI mode logs
2. **`glowscape_server_debug.log`** - FastAPI server logs
3. **`test_debug.log`** - Test script logs

### Log Format

```
2025-12-05 12:34:56,789 - module_name - LEVEL - Message
```

Example:
```
2025-12-05 12:34:56,789 - tools.pricing_extraction - INFO - Starting crawl for pricing on: https://example.com (max_pages=20)
2025-12-05 12:34:57,123 - tools.pricing_extraction - DEBUG - Firecrawl client initialized successfully
2025-12-05 12:34:57,456 - tools.pricing_extraction - DEBUG - Crawl parameters: {...}
```

## Testing Pricing Extraction

### Using the Test Script

A dedicated test script is available to debug pricing extraction:

```bash
python test_debug_pricing.py
```

This script:
- Enables DEBUG logging
- Tests the URL that failed: https://www.upliftedrx.com/
- Writes detailed logs to `test_debug.log`
- Shows the agent's response on screen

### Manual Testing

Test individual tools directly in Python:

```python
import logging
from dotenv import load_dotenv
from tools.pricing_extraction import crawl_medspa_for_pricing

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Load environment
load_dotenv(".env.local")

# Test the tool
result = crawl_medspa_for_pricing("https://www.upliftedrx.com/")
print(result)
```

## Common Issues and Diagnostics

### Issue: "Crawl failed or returned no data"

**Check the logs for:**
```
ERROR - Crawl returned empty result for https://...
```

**Debug info includes:**
- Whether the result was None or empty
- Available keys in the result
- Result type information

**Possible causes:**
1. Firecrawl API rate limiting
2. Website blocking crawlers
3. Invalid API key
4. Network connectivity issues

### Issue: API Key Not Found

**Check the logs for:**
```
ERROR - FIRECRAWL_API_KEY not found in environment variables
```

**Solution:**
1. Verify `.env.local` exists
2. Check the key is correctly set:
   ```
   FIRECRAWL_API_KEY=your_key_here
   ```
3. Restart the application

### Issue: Import Errors

**Check the logs for:**
```
ERROR - Failed to import FirecrawlApp: ...
```

**Solution:**
```bash
pip install firecrawl-py
```

## Debugging Tool Responses

### Enhanced Error Messages

All tools now return detailed error information in JSON format:

```json
{
  "success": false,
  "error": "Human-readable error message",
  "error_type": "ExceptionClassName",
  "url": "https://...",
  "debug_info": {
    "exception_details": "Full exception message",
    "result_keys": ["key1", "key2"],
    "result_preview": "First 500 chars..."
  }
}
```

### Interpreting Tool Logs

**Successful crawl:**
```
INFO - Starting crawl for pricing on: https://example.com
DEBUG - Firecrawl client initialized successfully
DEBUG - Crawl parameters: {...}
INFO - Calling Firecrawl crawl_url API for: https://example.com
DEBUG - Crawl API returned. Result type: <class 'dict'>
DEBUG - Result keys: dict_keys(['data', 'success'])
INFO - Crawl returned 15 pages
DEBUG - Processing page 1/15: https://example.com/services (content_length=2543)
DEBUG -   -> Classified as SERVICE page
INFO - Crawl complete: 3 pricing, 8 service, 4 other pages
```

**Failed crawl:**
```
INFO - Starting crawl for pricing on: https://example.com
DEBUG - Firecrawl client initialized successfully
INFO - Calling Firecrawl crawl_url API for: https://example.com
DEBUG - Crawl API returned. Result type: <class 'dict'>
ERROR - Crawl result missing 'data' key. Keys: dict_keys(['error', 'message'])
ERROR - Exception in crawl_medspa_for_pricing: API rate limit exceeded
```

## Environment Variables

Ensure these are set in `.env.local`:

```bash
# Required
OPENAI_API_KEY=sk-...
FIRECRAWL_API_KEY=fc-...
APIFY_API_TOKEN=apify_api_...

# Optional (for server)
PORT=8000
HOST=0.0.0.0
```

## Monitoring Firecrawl API

### Check API Key Validity

The logs will show:
```
DEBUG - FIRECRAWL_API_KEY found (length: 32)
```

If the key is valid but API calls fail, check:
1. Firecrawl dashboard: https://firecrawl.dev/dashboard
2. API rate limits
3. Account credits

### API Call Tracking

Every Firecrawl API call is logged:

**Map URL:**
```
INFO - Calling Firecrawl map_url API for: https://...
DEBUG - Map API returned. Result type: <class 'dict'>
```

**Scrape URL:**
```
INFO - Calling Firecrawl scrape_url API for: https://...
DEBUG - Scrape parameters: {...}
```

**Crawl URL:**
```
INFO - Calling Firecrawl crawl_url API for: https://...
DEBUG - Crawl parameters: {...}
```

## Analyzing Agent Behavior

### Agent Creation

```
INFO - Creating GlowScape agent...
DEBUG - APIFY_API_TOKEN found (length: 45)
DEBUG - FIRECRAWL_API_KEY found (length: 32)
DEBUG - OPENAI_API_KEY found (length: 51)
INFO - Initializing agent with tools...
INFO - GlowScape agent created successfully
```

### Message Processing

```
INFO - Processing user input: Analyze the price of services: https://...
DEBUG - Calling agent.run()...
DEBUG - agent.run() returned. Type: <class 'agno.agent.RunResponse'>
DEBUG - Extracted response from .content attribute
INFO - Response generated successfully (length: 1234)
```

## Getting Help

If you encounter issues:

1. **Check the log files** - Most issues will show clear error messages
2. **Verify API keys** - Ensure all required keys are set
3. **Test connectivity** - Make sure you can reach Firecrawl API
4. **Review tool responses** - Check the JSON responses for error details

## Best Practices

1. **Always check logs first** - Don't guess, read the logs
2. **Test with simple URLs** - Start with a known-good website
3. **Monitor API usage** - Keep track of Firecrawl credits
4. **Keep logs** - Don't delete log files until issue is resolved
5. **Use test script** - Run `test_debug_pricing.py` for isolated testing

## Example Debug Session

```bash
# 1. Run the test script
python test_debug_pricing.py

# 2. Check the output on screen
# 3. Review test_debug.log for detailed trace
tail -f test_debug.log

# 4. Look for ERROR or WARNING lines
grep "ERROR\|WARNING" test_debug.log

# 5. Check Firecrawl API responses
grep "Firecrawl.*API" test_debug.log
```

