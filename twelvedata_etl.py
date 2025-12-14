import os
from dotenv import load_dotenv
from database import get_db
import twelvedata_client
from datetime import datetime
import logging


load_dotenv()
logger = logging.getLogger("twelvedata_etl")

# API key de Twelve Data (asegúrate de exportarla en tu entorno)
TWELVE_DATA_KEY = os.getenv("TWELVEDATA_KEY")
TWELVE_DATA_URL = "https://api.twelvedata.com/time_series"

SYMBOLS = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "INTC", "NVDA", "ORCL"]

async def run_etl(interval="1day", outputsize=30):
    db = await get_db()
    all_data = {}

    for symbol in SYMBOLS:
        logger.info(f"Fetching data for {symbol} from TwelveData...")
        params = {
            "symbol": symbol,
            "interval": interval,
            "outputsize": outputsize,
            "apikey": TWELVE_DATA_KEY
        }

        try:
            raw_data = twelvedata_client.fetch_api(TWELVE_DATA_URL, params=params)
            df = twelvedata_client.normalize_twelvedata(raw_data)
            data = df.to_dict(orient="records")

            await db[f"td_prices_{symbol}"].insert_many(data)

            logger.info(f"Inserted data for {symbol} into collection td_prices_{symbol}")

            all_data[symbol] = data

            await db["td_logs"].insert_one({
                "timestamp": datetime.now(),
                "message": f"{symbol} processed ({len(data)} records inserted)"
            })

        except Exception as exc:
            logger.error(f"Error {symbol}: {exc}")

    return all_data

async def get_last_results():
    db = await get_db()
    results = {}

    for symbol in SYMBOLS:
        collection = db[f"td_prices_{symbol}"]

        last_records = (
            await collection
            .find()
            .sort("_id", -1)
            .limit(30)
            .to_list(length=30)
        )

        # Convertir ObjectId -> string
        for record in last_records:
            record["_id"] = str(record["_id"])

        results[symbol] = last_records

    return results

async def get_history():
    db = await get_db()

    history = (
        await db["td_logs"]
        .find()
        .sort("timestamp", -1)
        .to_list(length=200)
    )

    for entry in history:
        entry["_id"] = str(entry["_id"])
        entry["timestamp"] = entry["timestamp"].isoformat()

    return history