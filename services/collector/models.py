from pydantic import BaseModel, Field
from datetime import datetime

class CoinPrice(BaseModel):
    coin_id: str = Field(..., description="The ID of the coin")
    timestamp_utc: datetime = Field(..., description="The timestamp of when the price was feteched")
    price_usd: float = Field(..., description="Current price of the coin in USD", gt=0)
    volume_24h: float = Field(..., description="The volume of the coin in the last 24 hours", ge=0)
    source: str = "coingecko"