# Moke the trade data
from pydantic import BaseModel

# Pydantic is a data validation and settings management library for Pytho
from datetime import datetime
from typing import List
from time import sleep
# from .trade import Trade


class Trade(BaseModel):
    """
    Trade data from Krakan API
      "symbol": "MATIC/USD",
      "side": "buy",
      "price": 0.5147,
      "qty": 6423.46326,
      "ord_type": "limit",
      "trade_id": 4665846,
      "timestamp": "2023-09-25T07:48:36.925533Z"
    """

    # symbol: str
    price: float
    pair: str
    volume: float
    timestamp: datetime
    timestamp_ms: int

    def to_dict(self) -> dict:
        # return self.model_dump()
        return {
            "symbol": self.pair,
            "price": self.price,
            "qty": self.volume,
            "timestamp_ms": self.timestamp_ms,
        }


class KrakenMokeAPI:
    def __init__(self, pair: str):
        self.pair = pair

    def get_trades(self) -> List[Trade]:
        moke_trades = [
            Trade(
                pair=self.pair,
                price=0.5147,
                volume=6423.46326,
                timestamp=datetime.now(),
                timestamp_ms=int(datetime.now().timestamp() * 1000),
            ),
            Trade(
                pair=self.pair,
                price=0.5247,
                volume=6423.46326,
                timestamp=datetime.now(),
                timestamp_ms=int(datetime.now().timestamp() * 1000),
            ),
        ]

        sleep(1)
        return moke_trades
