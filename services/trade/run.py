from loguru import logger
from kraken_api.moke import KrakenMokeAPI
from quixstreams import Application
from config import settings
from kraken_api.websocket import KrakenWebsocket
from typing import Union


def main(
    kafka_bootstrap_servers: str,
    kafka_topic: str,
    kraken_api: Union[KrakenMokeAPI, KrakenWebsocket],
):
    """
        Read the trade data from the  Krakan API and push it to the Kafka topic
        1. Read the trade data from the Krakan API(https://docs.kraken.com/api/docs/websocket-v2/trade)
        2. Push the trade data to the Kafka topic

    Args:
        kafka_bootstrap_servers: str
        kafka_topic: str
        kraken_api: Union[KrakenMokeAPI,KrakenWebsocket]
    Returns:
        None
    """
    logger.info("Hello from trade!")
    #  kraken_api = KrakenMokeAPI(pair="BTC/USD")
    # initialize the quix stream and this client handle the all the low level details to connect to the Kafka
    app = Application(broker_address=kafka_bootstrap_servers)

    # Add Topic
    topic = app.topic(kafka_topic, value_serializer="json")

    #with app.get_producer() as producer:
    while True:
        trades = kraken_api.get_trades()

        with app.get_producer() as producer:
            for trade in trades:
                logger.info(f"Pushing trade to Kafka topic: {trade}")
                # Serialize the trade to byte
                message = topic.serialize(key=trade.pair, value=trade.to_dict())
                # push the trade to the Kafka topic

                producer.produce(topic=topic.name, value=message.value, key=message.key)


if __name__ == "__main__":
    kraken_api = KrakenWebsocket(pairs=settings.kraken_pairs)
    main(
        kafka_bootstrap_servers=settings.kafka_bootstrap_servers,
        kafka_topic=settings.kafka_topic,
        kraken_api=kraken_api,
    )
