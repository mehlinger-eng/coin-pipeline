CREATE TABLE IF NOT EXISTS `virtual-voyage-457204-c3.crypto_data.coin_prices` (
    coin_id STRING NOT NULL,
    timestamp_utc TIMESTAMP NOT NULL,
    price_usd FLOAT64 NOT NULL,
    volume_24h FLOAT64 NOT NULL,
    source STRING NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY DATE(timestamp_utc)
CLUSTER BY coin_id; 