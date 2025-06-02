import json
import logging
import os 
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.message import Message
from google.cloud import bigquery
from datetime import datetime, timezone 
from services.collector.models import CoinPrice

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

with open("config.json", "r") as f:
    config = json.load(f)

PROJECT_ID = config["gcp"]["project_id"]
SUBSCRIPTION_ID = config["pubsub"]["subscription_id"]
BQ_DATASET = config["bigquery"]["dataset"]
BQ_TABLE = config["bigquery"]["table"]

bq_client = bigquery.Client(project=PROJECT_ID)

def insert_to_bq(valid_data: CoinPrice):
    table_id = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"
    row = {
        "coin_id": valid_data.coin_id,
        "timestamp_utc": valid_data.timestamp_utc.isoformat(),
        "price_usd": valid_data.price_usd,
        "volume_24h": valid_data.volume_24h,
        "source": valid_data.source,
    }

    logger.info(f"📥 Inserting into BigQuery: {row}")
    errors = bq_client.insert_rows_json(table_id, [row])
    if errors:
        logger.error(f"❌ BigQuery insertion errors: {errors}")
    else:
        logger.info("✅ Successfully inserted row into BigQuery")

def callback(message: Message):
    try:
        logger.info(f"📩 Received message: {message.data.decode('utf-8')}")
        payload = json.loads(message.data.decode("utf-8"))

        validated_data = CoinPrice.model_validate(payload)
        insert_to_bq(validated_data)

        message.ack()
        logger.info("✅ Message acknowledged")

    except Exception as e:
        logger.error(f"❌ Failed to process message: {e}")
        message.nack()

def main():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
  
    logger.info(f"🔄 Listening on {subscription_path}")
    future = subscriber.subscribe(subscription_path, callback=callback)
  
    try:
        future.result()
    except KeyboardInterrupt:
        logger.info("👋 Shutting down subscriber.")
        future.cancel()

if __name__ == "__main__":
    main()

import asyncio

def start_subscriber():
    def run():
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
      
        logger.info(f"🔄 Listening on {subscription_path}")
        future = subscriber.subscribe(subscription_path, callback=callback)
      
        try:
            future.result()
        except Exception as e:
            logger.error(f"🚨 Error in subscriber: {e}")
            future.cancel()

    return asyncio.to_thread(run)
