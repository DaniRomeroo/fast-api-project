import requests
from tenacity import retry, stop_after_attempt, wait_exponential
import pandas as pd

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))

def fetch_api(url, params=None, headers=None):

    response = requests.get(url, params=params, headers=headers, timeout=10)
    if response.status_code == 429:
        raise Exception("Rate limit exceeded")
    response.raise_for_status()
    return response.json()

def normalize_twelvedata(data):
    
    if "values" not in data:
        return pd.DataFrame()
    
    df = pd.DataFrame(data["values"])
    # Nos quedamos solo con fecha y precio de cierre
    df = df[["datetime", "close"]]
    # Convertimos la fecha a datetime
    df["datetime"] = pd.to_datetime(df["datetime"])
    # Ordenamos por fecha ascendente
    df = df.sort_values("datetime").reset_index(drop=True)
    return df