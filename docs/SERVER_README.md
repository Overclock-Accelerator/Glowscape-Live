# GlowScape Server

FastAPI server wrapper for the GlowScape MedSpa extraction agent.

## Local Development

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env.local` file with:

```
OPENAI_API_KEY=your_openai_api_key_here
APIFY_API_TOKEN=your_apify_token_here
```

### 3. Run the Server

```bash
python server.py
```

Or using uvicorn directly:

```bash
uvicorn server:app --reload --port 8000
```

The server will be available at `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /
GET /health
```

### Chat with Agent
```
POST /chat
```

**Request Body:**
```json
{
  "message": "Find medspas in Los Angeles using Google Maps",
  "stream": false
}
```

**Response:**
```json
{
  "response": "Agent's response here...",
  "success": true
}
```

## Example Usage

### Using curl
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Find medspas in Los Angeles using Google Maps"}'
```

### Using Python requests
```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "Find medspas in Los Angeles using Google Maps"}
)

print(response.json())
```

### Using JavaScript fetch
```javascript
fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Find medspas in Los Angeles using Google Maps'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Railway Deployment

### 1. Prerequisites
- Railway account
- GitHub repository with this code

### 2. Deploy Steps

1. **Connect Repository**
   - Go to Railway dashboard
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose this repository

2. **Set Environment Variables**
   - In Railway project settings, go to "Variables"
   - Add:
     - `OPENAI_API_KEY`
     - `APIFY_API_TOKEN`
   - Railway automatically sets `PORT`

3. **Deploy**
   - Railway will automatically detect the `Procfile` and `requirements.txt`
   - Build and deployment will start automatically
   - Once deployed, you'll get a URL like `https://your-app.railway.app`

### 3. Monitor Deployment

- Check logs in Railway dashboard
- Test health endpoint: `https://your-app.railway.app/health`
- Test chat endpoint with POST request

## Project Structure

```
GlowScape/
├── server.py              # FastAPI server (this file)
├── glowscape_agent.py     # Agent implementation
├── tools/                 # Agent tools
├── requirements.txt       # Python dependencies
├── Procfile              # Railway/Heroku deployment config
├── railway.json          # Railway-specific config
└── .env.local            # Local environment variables (not committed)
```

## Notes

- The agent is initialized once on server startup for efficiency
- Each POST request to `/chat` sends a message to the agent and returns the response
- CORS is enabled for all origins (configure appropriately for production)
- Railway automatically provides the `PORT` environment variable
- Logs are sent to stdout for Railway log aggregation
