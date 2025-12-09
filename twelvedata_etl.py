import os
from dotenv import load_dotenv
from database import get_db
from utils import fetch_api, normalize_twelvedata

load_dotenv()

# API key de Twelve Data (asegúrate de exportarla en tu entorno)
TWELVE_DATA_KEY = os.getenv("TWELVEDATA_KEY")
TWELVE_DATA_URL = "https://api.twelvedata.com/time_series"

SYMBOLS = [
    "AAPL",      # Apple Inc.
    "MSFT",      # Microsoft Corporation
    "GOOGL",     # Alphabet Inc. (Google)
    "AMZN",      # Amazon.com, Inc.
    "META",      # Meta Platforms, Inc.
    "INTC",      # Intel Corporation
    "NVDA",      # NVIDIA Corporation
    "ORCL"       # Oracle Corporation
]

async def run_etl(interval="1day", outputsize=30):
    """
    ETL para Twelve Data: obtiene serie temporal de precios de un símbolo.
    """
    db = await get_db()

    all_data = {}

    for symbol in SYMBOLS:

        params = {
            "symbol": symbol,
            "interval": interval,
            "outputsize": outputsize,
            "apikey": TWELVE_DATA_KEY
        }

        raw_data = fetch_api(TWELVE_DATA_URL, params=params)
        df = normalize_twelvedata(raw_data)

        data = df.to_dict(orient="records")
        await db[f"td_prices_{symbol}"].insert_many(data)
        all_data[symbol] = data

    return all_data
