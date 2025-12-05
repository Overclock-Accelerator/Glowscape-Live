# Debug Quick Start Guide

## What Was Added

Enhanced error reporting has been added to identify why pricing extraction fails. When Firecrawl API calls fail, you'll see detailed error information including what went wrong.

## Quick Test

Run this command to test with full debugging:

```bash
python test_debug_pricing.py
```

This will:
1. Test the exact URL that failed
2. Show the response on screen
3. Log any errors to `test_debug.log`

## What to Look For

### In Console Output
- Check if pricing data is extracted
- Look for "ERROR" messages

### In Log File (`test_debug.log`)

**Failure indicators:**
```
ERROR - Firecrawl crawl returned empty result
ERROR - Firecrawl crawl missing 'data' key
ERROR - FIRECRAWL_API_KEY not found
```

The error messages include `debug_info` with details about what the API returned.

## Common Issues

### 1. Empty Results
**Log shows:**
```
ERROR - Crawl returned empty result for https://...
```

**Cause:** Firecrawl API returned no data

**Check:**
- Firecrawl API credits
- Website accessibility
- API rate limits

### 2. API Key Missing
**Log shows:**
```
ERROR - FIRECRAWL_API_KEY not found in environment variables
```

**Fix:**
Add to `.env.local`:
```
FIRECRAWL_API_KEY=your_key_here
```

### 3. Import Error
**Log shows:**
```
ERROR - Failed to import FirecrawlApp
```

**Fix:**
```bash
pip install firecrawl-py
```

## View Logs

```bash
# View errors
cat test_debug.log

# Or on Windows
type test_debug.log
```

## Debug Flow

1. **Run test script**
   ```bash
   python test_debug_pricing.py
   ```

2. **Check console for immediate issues**

3. **Review log file for details**
   ```bash
   cat test_debug.log | grep -A 5 "ERROR"
   ```

4. **Look for the failure point:**
   - API key validation
   - Firecrawl client creation
   - API call execution
   - Result processing
   - Content extraction

## Error Messages

When Firecrawl fails, the tool returns detailed JSON with:

```json
{
  "success": false,
  "error": "Human-readable error",
  "url": "https://...",
  "debug_info": {
    "result_keys": ["available", "keys"],
    "result_preview": "First 500 chars of API response..."
  }
}
```

This helps identify exactly what went wrong with the API call.

## Files Created

- **`test_debug_pricing.py`** - Test script
- **`docs/DEBUGGING_GUIDE.md`** - Full debugging guide
- **`DEBUGGING_CHANGELOG.md`** - Complete list of changes
- **`DEBUG_QUICKSTART.md`** - This file

## Modified Files

- **`tools/pricing_extraction.py`** - Added logging to all tools
- **`glowscape_agent.py`** - Added session logging
- **`server.py`** - Added request/response logging

## Next Steps

1. Run `python test_debug_pricing.py`
2. Check `test_debug.log` for the error details
3. Refer to `docs/DEBUGGING_GUIDE.md` for issue-specific solutions

## All Available Logs

When running different modes:

| Mode | Command | Log File |
|------|---------|----------|
| Test Script | `python test_debug_pricing.py` | `test_debug.log` |
| CLI Mode | `python glowscape_agent.py` | `glowscape_debug.log` |
| Server Mode | `python server.py` | `glowscape_server_debug.log` |

All logs are in `.gitignore` and won't be committed.

