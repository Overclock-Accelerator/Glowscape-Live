"""
GlowScape Server - FastAPI wrapper for the GlowScape agent

Provides a REST API endpoint to interact with the GlowScape agent.
Designed for deployment on Railway.
"""

import os
import logging
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from glowscape_agent import create_glowscape_agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(".env.local")

# Global agent instance
agent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize agent on startup and cleanup on shutdown."""
    global agent
    try:
        logger.info("Initializing GlowScape agent...")
        agent = create_glowscape_agent()
        logger.info("GlowScape agent initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")
        raise
    
    yield
    
    logger.info("Shutting down GlowScape server...")


# Create FastAPI app
app = FastAPI(
    title="GlowScape API",
    description="MedSpa Location Data Extraction Agent API",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., description="User message to send to the agent", min_length=1)
    stream: bool = Field(default=False, description="Whether to stream the response")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="Agent's response")
    success: bool = Field(default=True, description="Whether the request was successful")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "GlowScape API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "agent_initialized": agent is not None
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to the GlowScape agent and receive a response.
    
    Args:
        request: ChatRequest containing the user message
        
    Returns:
        ChatResponse containing the agent's response
    """
    if agent is None:
        logger.error("Agent not initialized")
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        logger.info(f"Processing message: {request.message[:100]}...")
        
        # Get response from agent
        response = agent.run(request.message, stream=False)
        
        # Extract content from response
        if hasattr(response, 'content'):
            response_text = response.content
        elif isinstance(response, str):
            response_text = response
        else:
            response_text = str(response)
        
        logger.info(f"Response generated (length: {len(response_text)})")
        
        return ChatResponse(
            response=response_text,
            success=True
        )
        
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable (Railway provides this)
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "server:app",
        host=host,
        port=port,
        reload=False,  # Disable reload in production
        log_level="info"
    )
