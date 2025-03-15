from loguru import logger
from kraken_api.moke import KrakenMokeAPI
from quixstreams import Application
from config import settings
from kraken_api.websocket import KrakenWebsocket
from kraken_api.rest import KrakenRestAPI
from typing import Union
from kraken_api.base import TradesAPI
from typing import Literal


def main(
    kafka_bootstrap_servers: str,
    kafka_topic: str,
    trades_api: TradesAPI,
    data_source: Literal['live','historical','test']
):
    """
        Read the trade data from the Krakan API and push it to the Kafka topic
        1. Read the trade data from the Krakan API(https://docs.kraken.com/api/docs/websocket-v2/trade)
        2. Push the trade data to the Kafka topic

    Args:
        kafka_bootstrap_servers: str
        kafka_topic: str
        trades_api: TradesAPI with 2 methods: get_trades , is_done
        data_source: Literal['live','historical','test']

    Returns:
        None
    """
    logger.info(f"Starting trade service in {data_source} mode!")
    
    # initialize the quix stream and this client handle the all the low level details to connect to the Kafka
    app = Application(
        broker_address=kafka_bootstrap_servers,
        auto_offset_reset='earliest' if data_source == 'historical' else 'latest'
    )

    # Add Topic
    topic = app.topic(kafka_topic, value_serializer="json")

    try:
        with app.get_producer() as producer:
            # For historical/test data: process once and exit
            if data_source in ['historical']:
                while not trades_api.is_done():
                    trades = trades_api.get_trades()
                    logger.info(f"Fetched {len(trades)} historical trades")
                    
                    for trade in trades:
                        logger.info(f"Pushing historical trade to Kafka topic:{topic.name}: {trade}")
                        message = topic.serialize(key=trade.pair, value=trade.to_dict())
                        producer.produce(topic=topic.name, value=message.value, key=message.key)
                    producer.flush()
                logger.info("Historical data processing completed")
                
            # For live data: continuous processing
            else:
                logger.info("Starting live data processing")
                while True:  # Continuous loop for live data
                    if not trades_api.is_done():
                        trades = trades_api.get_trades()
                        if trades:  # Only process if we have trades
                            logger.info(f"Fetched {len(trades)} live trades")
                            
                            for trade in trades:
                                logger.info(f"Pushing live trade to Kafka topic:{topic.name}: {trade}")
                                message = topic.serialize(key=trade.pair, value=trade.to_dict())
                                producer.produce(topic=topic.name, value=message.value, key=message.key)
                            producer.flush()
                    
                    # Small delay for live mode to prevent overwhelming the API
                    if data_source == 'live':
                        import time
                        time.sleep(1)
                        
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise
    finally:
        logger.info("Cleaning up resources...")
        trades_api.cleanup()


if __name__ == "__main__":

    # Initialize the Kracken the API based on the datasource
    logger.info(f"Initializing the Kraken API based on the data source: {settings.data_source}")    
    if settings.data_source == 'live':
        kraken_api = KrakenWebsocket(pairs=settings.kraken_pairs)
    elif settings.data_source == 'historical':
        kraken_api = KrakenRestAPI(pairs=settings.kraken_pairs, last_ndays=settings.last_ndays)
    elif settings.data_source == 'test':
        kraken_api = KrakenMokeAPI(pairs=settings.kraken_pairs)
    else:
        raise ValueError(f"Invalid data source: {settings.data_source}")
    main(
        kafka_bootstrap_servers=settings.kafka_bootstrap_servers,
        kafka_topic=settings.kafka_topic,
        trades_api=kraken_api,
        data_source=settings.data_source
    )
