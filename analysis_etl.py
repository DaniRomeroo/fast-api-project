import numpy as np
from datetime import datetime
from database import get_db

def compute_price_trend(prices: list[float]):
    if len(prices) < 2:
        return None, None

    first = prices[-1]
    last = prices[0]

    change_pct = ((last - first) / first) * 100 if first != 0 else 0.0

    if change_pct > 1:
        trend = "up"
    elif change_pct < -1:
        trend = "down"
    else:
        trend = "flat"

    return trend, round(change_pct, 2)


def classify_social_interest(mentions: list[float]):
    if not mentions:
        return None

    avg_mentions = np.mean(mentions)

    if avg_mentions >= 50:
        return "high"
    elif avg_mentions >= 20:
        return "medium"
    else:
        return "low"


def build_summary(price_trend, social_level, correlation):
    if price_trend is None or social_level is None:
        return "Not enough data to generate a meaningful interpretation."

    if price_trend == "up" and social_level == "high":
        return (
            "The stock price is rising alongside strong social interest, "
            "suggesting aligned market momentum and public attention."
        )

    if price_trend == "down" and social_level == "high":
        return (
            "High social interest combined with falling prices may indicate "
            "speculative attention without market confirmation."
        )

    if price_trend == "up" and social_level == "low":
        return (
            "The stock price is increasing despite limited social interest, "
            "suggesting institutional or low-profile momentum."
        )

    if price_trend == "down" and social_level == "low":
        return (
            "The stock price is trending downward with limited social interest, "
            "indicating weak momentum and attention."
        )

    if price_trend == "flat":
        return (
            "The stock shows little price movement, indicating consolidation "
            "or market indecision regardless of social attention."
        )

    return "No clear pattern could be identified from the available data."


async def analyze_symbol(symbol: str, td_limit: int = 30, aw_limit: int = 30):

    db = await get_db()
    td_collection = db[f"td_prices_{symbol}"]

    td_records = (
        await td_collection
        .find()
        .sort("_id", -1)
        .limit(td_limit)
        .to_list(length=td_limit)
    )

    td_prices = []
    for record in td_records:
        try:
            td_prices.append(float(record.get("close")))
        except (TypeError, ValueError):
            continue

    aw_collection = db[f"apewisdom_{symbol}"]

    aw_records = (
        await aw_collection
        .find()
        .sort("_id", -1)
        .limit(aw_limit)
        .to_list(length=aw_limit)
    )

    aw_mentions = []
    for record in aw_records:
        try:
            aw_mentions.append(float(record.get("mentions")))
        except (TypeError, ValueError):
            continue

    correlation = None
    if td_prices and aw_mentions:
        min_len = min(len(td_prices), len(aw_mentions))
        if min_len > 1:
            corr = np.corrcoef(
                td_prices[:min_len],
                aw_mentions[:min_len]
            )[0, 1]
            if not np.isnan(corr):
                correlation = round(float(corr), 3)

    price_trend, price_change_pct = compute_price_trend(td_prices)
    social_level = classify_social_interest(aw_mentions)

    summary = build_summary(price_trend, social_level, correlation)

    return {
        "symbol": symbol,

        "td_last_price": td_prices[0] if td_prices else None,
        "aw_last_mentions": aw_mentions[0] if aw_mentions else None,

        "price_trend": price_trend,
        "price_change_pct": price_change_pct,
        "social_interest": social_level,

        "correlation": correlation,

        "td_count": len(td_prices),
        "aw_count": len(aw_mentions),

        "td_prices_series": td_prices[::-1],
        "aw_mentions_series": aw_mentions[::-1],

        "analysis_timestamp": datetime.utcnow().isoformat(),
        "summary": summary
    }
