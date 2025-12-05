# Environment Setup Guide

## Required Environment Variables

Create a file named `.env.local` in the root directory with the following variables:

```bash
# OpenAI API Key (REQUIRED)
# Used for: Agent's LLM processing and analysis
# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-openai-api-key-here

# Apify API Token (REQUIRED for Google Maps searches)
# Used for: Google Maps/Places data extraction
# Get from: https://console.apify.com/account/integrations
APIFY_API_TOKEN=your-apify-api-token-here

# Firecrawl API Key (REQUIRED for pricing extraction)
# Used for: Website crawling and pricing extraction
# Get from: https://firecrawl.dev (sign up for free tier)
FIRECRAWL_API_KEY=your-firecrawl-api-key-here

# Server Configuration (OPTIONAL - only needed for API deployment)
PORT=8000
HOST=0.0.0.0
```

## Getting API Keys

### 1. OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Add to `.env.local`

**Cost:** Pay-as-you-go, GPT-4o-mini is cost-effective (~$0.15 per 1M input tokens)

### 2. Apify API Token

1. Go to https://console.apify.com/account/integrations
2. Sign up or log in
3. Find your API token in the Integrations section
4. Copy the token
5. Add to `.env.local`

**Cost:** Free tier includes $5 credit/month, then pay-as-you-go

### 3. Firecrawl API Key

1. Go to https://firecrawl.dev
2. Sign up for an account
3. Get your API key from the dashboard
4. Copy the key
5. Add to `.env.local`

**Cost:** Free tier available with limited requests, paid plans start at $20/month

## Verification

After setting up your `.env.local` file, verify it works:

```bash
# Test that environment variables load correctly
python -c "from dotenv import load_dotenv; import os; load_dotenv('.env.local'); print('OpenAI:', 'OK' if os.getenv('OPENAI_API_KEY') else 'MISSING'); print('Apify:', 'OK' if os.getenv('APIFY_API_TOKEN') else 'MISSING'); print('Firecrawl:', 'OK' if os.getenv('FIRECRAWL_API_KEY') else 'MISSING')"
```

## Optional: Production Deployment

For Railway or other cloud deployments, add environment variables through the platform's dashboard instead of using `.env.local`.

### Railway Setup

1. Go to your Railway project dashboard
2. Click on "Variables" tab
3. Add each variable:
   - `OPENAI_API_KEY`
   - `APIFY_API_TOKEN`
   - `FIRECRAWL_API_KEY`
4. Railway will automatically use these in deployment

## Security Notes

⚠️ **NEVER commit `.env.local` to git!**

- The `.gitignore` file already excludes it
- Keep your API keys secret
- Rotate keys if accidentally exposed
- Use different keys for development and production

## Troubleshooting

### "OPENAI_API_KEY not found"
- Check that `.env.local` exists in the project root
- Verify the key name is exactly `OPENAI_API_KEY` (case-sensitive)
- Restart your terminal/IDE after creating `.env.local`

### "APIFY_API_TOKEN not found"
- Make sure you're using `APIFY_API_TOKEN` not `APIFY_API_KEY`
- Check Apify dashboard for correct token

### "FIRECRAWL_API_KEY not found"
- Verify you've signed up at firecrawl.dev
- Check that the key is correctly copied (no extra spaces)

### Keys not loading
- Ensure python-dotenv is installed: `pip install python-dotenv`
- Check file is named exactly `.env.local` (note the dot prefix)
- Verify file is in the project root directory

