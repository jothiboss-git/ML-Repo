from typing import List
from .trade import Trade
from .base import TradesAPI
import requests
import time
from loguru import logger
import json

class KrakenRestAPI(TradesAPI):
    def __init__(self, pairs:List[str],last_ndays:int):
        logger.info(f"Historical Data Fetching from KrakenRestAPI with pairs: {pairs} and last_ndays: {last_ndays}")
        self.pairs = pairs
        self.last_ndays = last_ndays
        self.apis = [
            KrakenRestAPISinglePair(pair=pair, last_ndays=self.last_ndays)
            for pair in pairs
        ]
        logger.info(f"Initialized KrakenRestAPI with pairs: {pairs}")

    def get_trades(self) -> List[Trade]:
        """
        Get the trades for each pair and sort them by timestamp and return the list of trades
        """
        logger.info('Inside KrakenRestAPI get_trades to merge the trades from all pairs')
        trades = []
        for api in self.apis:
            if not api.is_done():
                try:
                    logger.info(f"Fetching trades for pair {api.pair}")
                    pair_trades = api.get_trades()
                    logger.info(f"Fetched {len(pair_trades)} trades for pair {api.pair}")
                    trades.extend(pair_trades)
                    #logger.info(f"Fetched {len(pair_trades)} trades for pair {api.pair}")
                except Exception as e:
                    logger.error(f"Error fetching trades for pair {api.pair}: {str(e)}")
                    continue

        #sort the trades by timestamp
        trades.sort(key=lambda x: x.timestamp)
        logger.info(f"Total trades fetched: {len(trades)}")
        return trades

    def is_done(self) -> bool:
        """
        Returns True if all pairs have finished fetching trades
        """
        return all(api.is_done() for api in self.apis)

class KrakenRestAPISinglePair(TradesAPI):
    url = 'https://api.kraken.com/0/public/Trades'
    
    def __init__(self, pair:str, last_ndays:int):
        self.pair = pair
        self.last_ndays = last_ndays
        self._is_done = False
        #get current timestamp in nanoseconds
        self.since_timestamp_ns = int(time.time_ns() - last_ndays * 24 * 60 * 60 * 1000000000)
        logger.info(f"Initializing the Kraken REST API for {self.pair} for the last {self.last_ndays} days")

    def get_trades(self) -> List[Trade]:
        """
        Send the request to the kraken REST API and get the trades for a pair
        """
        headers = {
            'Accept': 'application/json'
        }

        params = {
            'pair': self.pair,
            'since': self.since_timestamp_ns
        }

        response = requests.request('GET', self.url, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(f"Failed to get trades for {self.pair} from Kraken: {response.status_code} {response.text}")
            
        try:
            data = json.loads(response.text)
            if 'error' in data and data['error']:
                raise Exception(f"Kraken API error: {data['error']}")
            
            # Get the first (and only) pair's trades from the response
            pair_key = list(data['result'].keys())[0]
            logger.info(f"Pair key: {pair_key}")    
            trades_data = data['result'][pair_key]
            
            # Convert the response to a list of Trade objects
            trades = [Trade.from_kraken_restapi_response(
                pair=self.pair, 
                price=trade[0],
                volume=trade[1],
                timestamp_seconds=trade[2]
                ) for trade in trades_data]
            logger.info(f"Fetched inside KrakenRestAPISinglePair {len(trades)} trades for pair {self.pair}")
            
            # Update the since timestamp for pagination
            self.since_timestamp_ns = int(float(data['result']['last']))
            
            # Check if we are done
            if self.since_timestamp_ns > int(time.time_ns()-1000000000):
                self._is_done = True
            if self.since_timestamp_ns == 0: 
                self._is_done = True
                
            return trades
            
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse trades for {self.pair} from Kraken: {e}")
        except KeyError as e:
            raise Exception(f"Unexpected response structure from Kraken: {e}")
    
    def is_done(self) -> bool:
        return self._is_done
    
