# apewisdom_etl.py
import logging
from database import get_db
import apewisdom_client
from datetime import datetime

logger = logging.getLogger(__name__)

SYMBOLS = ["AAPL", "MSFT", "GOOGL", "AMZON", "META", "INTC", "NVDA", "ORCL"]

async def run_etl(max_pages: int = 5):

    db = await get_db()
    all_data = {}

    for ticker in SYMBOLS:
        logger.info(f"Fetching data for {ticker} from ApeWisdom...")
        data = await apewisdom_client.get_stock_async(ticker, max_pages=max_pages)
        if not data:
            logger.warning(f"No data found for {ticker}")
            continue

        collection_name = f"apewisdom_{ticker}"
        await db[collection_name].insert_one(data)
        logger.info(f"Inserted data for {ticker} into collection {collection_name}")

        await db["apewisdom_logs"].insert_one({
            "timestamp": datetime.now(),
            "message": f"Inserted data for {ticker} ({len(data)} records)",
        })

        all_data[ticker] = data

    return all_data

async def get_last_results(limit = 100):

    db = await get_db()
    results = {}
    for ticker in SYMBOLS:
        collection_name = f"apewisdom_{ticker}"
        cursor = db[collection_name].find().sort("_id", -1)
        data = await cursor.to_list(length=limit)
        for item in data:
            if "_id" in item:
                item["_id"] = str(item["_id"])
        results[ticker] = data
    return results

async def get_history(limit = 100):

    db = await get_db()
    cursor = db["apewisdom_logs"].find().sort("timestamp", -1)
    history = await cursor.to_list(length=limit)
    for entry in history:
        if "_id" in entry:
            entry["_id"] = str(entry["_id"])
        if "timestamp" in entry:
            entry["timestamp"] = entry["timestamp"].isoformat()
    return history
