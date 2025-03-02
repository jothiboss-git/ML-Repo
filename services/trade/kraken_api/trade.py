from pydantic import BaseModel

# Pydantic is a data validation and settings management library for Pytho
from datetime import datetime


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
    #timestamp: datetime
    timestamp : str
    timestamp_ms: int

    # @property
    # def timestamp_ms(self)->int:
    #    return int(self.timestamp.timestamp()*1000)

    def to_dict(self) -> dict:
        #return self.model_dump_json()
        return self.model_dump()

    # return {
    #    "symbol": self.pair,
    #    "price": self.price,
    #    "qty": self.volume,
    #    "timestamp_ms": self.timestamp_ms
    # }

    # return {**self.model_dump_json(), "timestamp_ms": self.timestamp_ms}
