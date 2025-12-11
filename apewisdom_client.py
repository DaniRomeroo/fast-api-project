# apewisdom_client.py
import asyncio
import httpx
import logging
from urllib.parse import urljoin
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

BASE = "https://apewisdom.io/api/v1.0"
TIMEOUT = 10

async def get_top_stocks_async(page: int = 1) -> Dict[str, Any]:

    url = urljoin(BASE + "/", f"filter/all-stocks/page/{page}")
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        return resp.json()

async def get_stock_async(ticker: str, max_pages: int = 5) -> Optional[Dict[str, Any]]:

    ticker = ticker.upper()
    for page in range(1, max_pages + 1):
        top_page = await get_top_stocks_async(page)
        for item in top_page.get("results", []):
            if item.get("ticker") == ticker:
                return {
                    "rank": item.get("rank"),
                    "ticker": item.get("ticker"),
                    "mentions": item.get("mentions"),
                    "upvotes": item.get("upvotes"),
                    "rank_24h_ago": item.get("rank_24h_ago"),
                    "mentions_24h_ago": item.get("mentions_24h_ago")
                }
    return {}
