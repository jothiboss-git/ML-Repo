from pydantic import BaseModel
from loguru import logger

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


    # to define the output of the class structure
    @classmethod
    def from_kraken_restapi_response(
      cls, 
      pair:str,
      price:float,
      volume:float,
      timestamp_seconds:float,
      
    )   -> 'Trade':
        """
        Return a Trade object from the Kraken REST API response

        example Response:
           [765637.0000, 0.5147, 1726272516.000000]

           price : float
           volume : float
           timestamp_ns : float
        """
        #convert timestamp_seconds from float to str
        timestamp_ms= int(float(timestamp_seconds)*1000)
        #final output structure
        #logger.info('Final output structure -------------')
        return cls(
          pair=pair,           
          price=price, 
          volume=volume,
          timestamp=cls._millisecondstodateStr(timestamp_ms),
          timestamp_ms=timestamp_ms)
    

    @staticmethod
    def _millisecondstodateStr(timestamp_ms:int)->str:
      return datetime.fromtimestamp(timestamp_ms/1000).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def datestr2timestamp_ms(datestr:str)->int:
      return int(datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S').timestamp()*1000)


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
