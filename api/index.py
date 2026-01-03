"""
Entry point for Vercel serverless function.
This file imports and exports the FastAPI app from app.py.
"""
from app import app

# Export the app so Vercel can use it as the ASGI application
__all__ = ['app']
