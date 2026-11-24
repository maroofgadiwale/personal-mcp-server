from fastmcp import FastMCP
from dotenv import load_dotenv
from pathlib import Path
import requests
import os

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

mcp = FastMCP("Remote-MCP")

@mcp.tool
def add(x: float, y: float) -> float:
    """Add two numbers."""
    return x + y

@mcp.tool
def guess_country(name: str) -> dict:
    """Guess the country based on the user's name"""

    api_key = os.getenv("NATIONALIZE_API_KEY")

    if not api_key:
        return {"error": "API key not loaded"}

    params = {
        "name": name,
        "apikey": api_key
    }

    response = requests.get(
        "https://api.nationalize.io",
        params=params,
        timeout=15
    )
    response.raise_for_status()

    data = response.json()

    if not data.get("country"):
        return {"message": "Country prediction unavailable"}

    return data["country"][0]

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.0", port=8000)