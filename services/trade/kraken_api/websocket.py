from typing import List
import json
from websocket import create_connection
from .trade import Trade
from datetime import datetime
from loguru import logger


class KrakenWebsocket:
    URL = "wss://ws.kraken.com/v2"

    def __init__(self, pairs: List[str]):
        self.pairs = pairs

        # Create the websocket connection
        self._ws_client = create_connection(url=self.URL)

        # Send the subscribe message
        self._subscribe()

    def get_trades(self) -> List[Trade]:
        """
        get the trades from the websocket and return a list of trades

        Args:
            None

        Returns:
            List[Trade]: A list of Trade objects
        """
        print("get_trades inside")
        # get the trades from the websocket

        data = self._ws_client.recv()

        if "heartbeat" in data:
            logger.info("Heartbeat received")
            return []

        # parse the trades from the websocket
        try:
            data = json.loads(data)
        except Exception as e:
            print("Error parsing data from websocket", e)
            return []
        # get the trades from the data
        try:
            trades = data["data"]
        except Exception as e:
            print("No field data in the response", e)
            return []
        # create the list of trades
        trades_list = []
        for trade in trades:
            trades_list.append(
                Trade(
                    pair=trade["symbol"],
                    price=trade["price"],
                    volume=trade["qty"],
                    timestamp=trade["timestamp"],
                    timestamp_ms=self._convert_timestamp(trade["timestamp"]),
                )
            )

        return trades_list

    def _convert_timestamp(self, timestamp: str) -> int:
        """
        Convert the timestamp to a timestamp in milliseconds
        """
        return int(
            datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp() * 1000
        )

    def _subscribe(self):
        """
        Subscribe to the trades channel and wait for the trades
        """
        self._ws_client.send(
            json.dumps(
                {
                    "method": "subscribe",
                    "params": {
                        "channel": "trade",
                        "symbol": self.pairs,
                        "snapshot": True,
                    },
                }
            )
        )

        for pair in self.pairs:
            _ = self._ws_client.recv()
            _ = self._ws_client.recv()
