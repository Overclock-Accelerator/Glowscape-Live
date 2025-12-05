# Debugging Enhancements Changelog

## Summary

Added comprehensive debugging and logging throughout the GlowScape application to diagnose why pricing extraction tools fail.

## Changes Made

### 1. Enhanced Logging in `tools/pricing_extraction.py`

**Added:**
- Import logging module
- Logger configuration with DEBUG level
- Detailed logging before and after every Firecrawl API call
- Parameter logging for all API calls
- Result type and keys logging
- Content length tracking for scraped pages
- Page classification logging (pricing vs service vs other)
- Full exception traces with `exc_info=True`

**Functions Updated:**
- `_get_firecrawl_client()` - Logs API key validation
- `map_medspa_website()` - Logs mapping process and results
- `scrape_medspa_pricing()` - Logs scraping parameters and content
- `crawl_medspa_for_pricing()` - Detailed crawl tracking
- `extract_structured_pricing()` - Structured extraction logging

**Enhanced Error Messages:**
All functions now return detailed error info:
```json
{
  "success": false,
  "error": "Human-readable message",
  "error_type": "ExceptionClassName",
  "debug_info": {
    "exception_details": "...",
    "result_keys": [...],
    "result_preview": "..."
  }
}
```

### 2. Enhanced Logging in `glowscape_agent.py`

**Added:**
- Import logging module
- Configured logging with both file and console handlers
- File logging to `glowscape_debug.log`
- DEBUG level logging throughout
- API key validation logging for all services
- Agent creation tracking
- User input logging
- Response generation logging

**Functions Updated:**
- `create_glowscape_agent()` - Validates all API keys with logging
- `main()` - Logs session lifecycle and user interactions

### 3. Enhanced Logging in `server.py`

**Added:**
- DEBUG level logging
- File logging to `glowscape_server_debug.log`
- Request logging with full message
- Response type tracking
- Response content preview logging
- Enhanced exception handling with full traces

**Functions Updated:**
- Global logging configuration
- `chat()` endpoint - Detailed request/response logging

### 4. New Test Script: `test_debug_pricing.py`

**Purpose:** Isolated testing environment for pricing extraction

**Features:**
- DEBUG logging enabled
- Tests the specific failing URL (upliftedrx.com)
- Writes to dedicated log file `test_debug.log`
- Displays response on screen
- Complete error handling with traces

**Usage:**
```bash
python test_debug_pricing.py
```

### 5. New Documentation: `docs/DEBUGGING_GUIDE.md`

**Contents:**
- Overview of debugging features
- Log file locations and formats
- Testing instructions
- Common issues and solutions
- Error message interpretation
- Environment variable checklist
- API monitoring guidance
- Best practices
- Example debug session

## Log Files Generated

1. **`glowscape_debug.log`** - CLI mode logs
2. **`glowscape_server_debug.log`** - Server mode logs
3. **`test_debug.log`** - Test script logs

All log files are:
- Already in `.gitignore` (pattern: `*.log`)
- Written with DEBUG level detail
- Include timestamps, module names, and levels
- Contain full exception traces

## Logging Format

```
TIMESTAMP - MODULE - LEVEL - MESSAGE
```

Example:
```
2025-12-05 12:34:56,789 - tools.pricing_extraction - INFO - Starting crawl for pricing on: https://example.com (max_pages=20)
2025-12-05 12:34:57,123 - tools.pricing_extraction - DEBUG - Firecrawl client initialized successfully
2025-12-05 12:34:58,456 - tools.pricing_extraction - DEBUG - Crawl API returned. Result type: <class 'dict'>
```

## What You Can Now Debug

### API Issues
- API key validation failures
- Firecrawl API responses
- Rate limiting problems
- Network connectivity issues

### Tool Failures
- Empty results from Firecrawl
- Missing data keys
- Classification logic
- Content extraction

### Agent Issues
- Tool selection problems
- Response generation
- Message processing
- Error handling

## How to Use

### Quick Test
```bash
python test_debug_pricing.py
```

### Check Logs
```bash
# View latest errors
grep "ERROR" test_debug.log

# Watch logs in real-time
tail -f glowscape_debug.log

# Search for Firecrawl calls
grep "Firecrawl.*API" test_debug.log
```

### Debug Flow

1. Run test script or agent
2. Check console output for immediate errors
3. Review log file for detailed trace
4. Look for:
   - API key validation: "found (length: X)"
   - API calls: "Calling Firecrawl X API"
   - Results: "Result type:", "Result keys:"
   - Errors: "ERROR -" or "Exception in"

## Key Debug Points

### Before API Call
```
INFO - Starting crawl for pricing on: https://...
DEBUG - Firecrawl client initialized
DEBUG - Crawl parameters: {...}
INFO - Calling Firecrawl crawl_url API
```

### After API Call
```
DEBUG - Crawl API returned. Result type: <class 'dict'>
DEBUG - Result keys: dict_keys([...])
INFO - Crawl returned X pages
```

### Error Scenario
```
ERROR - Crawl returned empty result
ERROR - Exception in crawl_medspa_for_pricing: ...
Traceback (most recent call last):
  ...
```

## Next Steps for Debugging upliftedrx.com Issue

1. **Run test script:**
   ```bash
   python test_debug_pricing.py
   ```

2. **Check test_debug.log for:**
   - Firecrawl API call success
   - Result structure
   - Error messages
   - Exception traces

3. **Look for specific patterns:**
   - "Crawl returned X pages" - Should be > 0
   - "Classified as PRICING page" - Should find pricing pages
   - "ERROR" or "Exception" - Indicates failure point

4. **Compare with expected flow:**
   - API key validated ✓
   - Firecrawl client created ✓
   - Crawl API called ✓
   - Result received ✓
   - Data extracted ✓
   - Pages classified ✓

## Files Modified

- `tools/pricing_extraction.py` - Added comprehensive logging
- `glowscape_agent.py` - Added agent and session logging
- `server.py` - Added server request/response logging

## Files Created

- `test_debug_pricing.py` - Test script for debugging
- `docs/DEBUGGING_GUIDE.md` - Comprehensive debugging documentation
- `DEBUGGING_CHANGELOG.md` - This file

## Benefits

1. **Visibility:** See exactly what's happening at each step
2. **Diagnostics:** Identify failure points immediately
3. **Debugging:** Full context for troubleshooting
4. **Monitoring:** Track API usage and performance
5. **Testing:** Isolated test environment for verification

