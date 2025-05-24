import asyncio
import json
import logging
import httpx
import os
from datetime import datetime, timezone
from pathlib import Path
from google.cloud import pubsub_v1
from services.collector.models import CoinPrice

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

PROJECT_ID = os.getenv("PROJECT_ID", "virtual-voyage-457204-c3")
PUBSUB_TOPIC = os.getenv("PUBSUB_TOPIC", "coin_ticks")

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, PUBSUB_TOPIC)

API_URL = "https://api.coingecko.com/api/v3"
COINS = ["bitcoin"]
VS_CURRENCY = "usd"

async def fetch_prices():
    """
    Fetch prices from the CoinGecko API, validate using CoinPrice model,
    and prepare them for downstream publishing.
    """
    params = {
        "ids": ",".join(COINS),
        "vs_currency": VS_CURRENCY,
        "include_market_cap": "true",
        "include_24hr_vol": "true",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/coins/markets", params=params)
        response.raise_for_status()
        data = response.json()

        now = datetime.utcnow().replace(tzinfo=timezone.utc)

        for coin_data in data:
            try:
                coin_id = coin_data["id"]
                price = coin_data["current_price"]
                volume = coin_data.get("total_volume", 0)

                tick = CoinPrice(
                    coin_id=coin_id,
                    timestamp_utc=now,
                    price_usd=price,
                    volume_24h=volume,
                    source="coingecko"
                )

                logging.info(f"✅ VALID: {tick}")

                def json_serializer(obj):
                    if isinstance(obj, datetime):
                        return obj.isoformat()
                    raise TypeError("Type not serializable")

                payload = json.dumps(tick.dict(), default=json_serializer).encode("utf-8")
                future = publisher.publish(topic_path, payload)
                await asyncio.wrap_future(future)
                logging.info(f"📤 Published tick for {coin_id}")

            except Exception as e:
                logging.error(f"[ERROR] while parsing coin data: {e}")

async def start_scheduler():
    """
    Starts a periodic loop that fetches prices every 30 seconds.
    This should be triggered once when the FastAPI app starts.
    """
    logging.info("📡 Starting scheduler loop…")
    while True:
        try:
            await fetch_prices()
        except Exception as e:
            logging.exception(f"[Scheduler error]: {e}")
        await asyncio.sleep(30)
