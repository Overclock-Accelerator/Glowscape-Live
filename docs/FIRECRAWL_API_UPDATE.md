# Firecrawl API Update

## Issues Fixed
1. **Error**: `'Firecrawl' object has no attribute 'crawl_url'`
2. **Error**: `'CrawlJob' object has no attribute 'keys'`

## Root Cause
The code was using the old Firecrawl SDK API which is no longer compatible with the current version of `firecrawl-py`. The new SDK:
1. Uses different class and method names
2. Returns **objects** (like `CrawlJob`) instead of dictionaries

## Changes Made

### 1. Updated Import Statement
**Before:**
```python
from firecrawl import FirecrawlApp
return FirecrawlApp(api_key=api_key)
```

**After:**
```python
from firecrawl import Firecrawl
return Firecrawl(api_key=api_key)
```

### 2. Updated Method Names & Parameters

#### Map Function
**Before:**
```python
result = app.map_url(url)
```

**After:**
```python
result = app.map(url)
```

#### Scrape Function
**Before:**
```python
result = app.scrape_url(
    url,
    params={
        'formats': ['markdown', 'html'],
        'onlyMainContent': True
    }
)
```

**After:**
```python
result = app.scrape(
    url,
    formats=['markdown', 'html'],
    only_main_content=True
)
```

#### Crawl Function
**Before:**
```python
result = app.crawl_url(
    url,
    params={
        'limit': max_pages,
        'scrapeOptions': {
            'formats': ['markdown'],
            'onlyMainContent': True
        }
    },
    poll_interval=5
)
```

**After:**
```python
result = app.crawl(
    url,
    limit=max_pages,
    scrape_options={
        'formats': ['markdown'],
        'only_main_content': True
    },
    poll_interval=5
)
```

## API Naming Convention Changes

| Old API | New API |
|---------|---------|
| `FirecrawlApp` class | `Firecrawl` class |
| `scrape_url()` | `scrape()` |
| `crawl_url()` | `crawl()` |
| `map_url()` | `map()` |
| `params={}` wrapper | Direct parameters |
| `onlyMainContent` | `only_main_content` |
| `scrapeOptions` | `scrape_options` |
| Dictionary responses | **Object responses** |

## Critical Change: Object vs Dictionary Responses

The new SDK returns **objects** instead of dictionaries:

**Old Way (dictionaries):**
```python
result = app.crawl_url(url)
pages = result['data']  # Dictionary access
```

**New Way (objects):**
```python
result = app.crawl(url)  # Returns CrawlJob object
pages = result.data  # Attribute access
```

### Updated Code Pattern
To handle both potential response types, the code now uses:

```python
# Handle both dict and object responses
if isinstance(result, dict):
    data = result.get('data', [])
else:
    # It's an object, access as attribute
    data = getattr(result, 'data', [])
```

## Files Updated
- `tools/pricing_extraction.py` - All Firecrawl API calls updated to new SDK

## Testing
Run the test script to verify the changes:
```bash
python test_pricing_extraction.py
```

## Reference
- [Firecrawl Python SDK Documentation](https://docs.firecrawl.dev/sdks/python)
- [Agno Firecrawl Tools Documentation](https://docs.agno.com/tools/firecrawl)

