from loguru import logger
from quixstreams import Application
from news_datasource import NewsDatasource
from config import settings,cryptopanic_config
from typing import Optional
from news_download import NewsDownload


def main(
    kafka_bootstrap_servers:str,
    kafka_topic:str,
    news_datasource:NewsDatasource, 
):

    """
      this service will get the news from the cryptopanic REST API and push it to the kafka topic
      Args:
        kafka_bootstrap_servers: str
        kafka_topic: str
        news_datasource: NewsDatasource

       Returns:
       None

    """
    logger.info("Hello from news!")

    #initialize the kafka application
    app = Application(
        broker_address=kafka_bootstrap_servers
    )
    logger.info(f"news-run: initialized kafka application")

    #Topics where the news will be pushed
    output_topic = app.topic(name=kafka_topic,value_serializer="json")
    logger.info(f"news-run: initialized output topic")
    #create the Streaming Dataframe
    sdf = app.dataframe(source=news_datasource)  
    logger.info(f"news-run: initialized streaming dataframe")
    #print the sdf
    sdf.print(metadata=True)
    logger.info(f"news-run: printed streaming dataframe")
    #push the news to the kafka topic
    sdf.to_topic(output_topic)
    logger.info(f"news-run: pushed news to the kafka topic")
    app.run()
    logger.info(f"news-run: running application")
        

if __name__ == "__main__":


    #news download instance
    news_download = NewsDownload(
        cryptopanic_api_key=cryptopanic_config.cryptopanic_api_key,
    )



    #initialize the news datasource which wrap the news download and the polling interval
    news_datasource = NewsDatasource(
        news_download=news_download,        
        polling_interval = settings.polling_interval

    )


    main(
        kafka_bootstrap_servers=settings.kafka_bootstrap_servers,
        kafka_topic=settings.kafka_topic,
        news_datasource=news_datasource
    )
