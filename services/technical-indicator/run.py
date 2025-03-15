from loguru import logger
from quixstreams import Application,State
from candle_fun import update_candle
from candle_fun import compute_technical_indicators
from typing import Literal
def main(
    kafka_bootstrap_servers: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    candle_seconds: int,
    data_source: Literal['live','historical','test']
    
):
    logger.info("Hello from technical-inidicator!")
    """
      3 Steps:
       1. Ingest the candle data from candle service(input topic)
       2. Calculate the technical indicators
       3. Write the technical indicators to the output topic

       ARGS:
        kafka_bootstrap_servers: str,
        kafka_input_topic: str,
        kafka_output_topic: str,
        kafka_consumer_group: str,
        candle_seconds: int,
        data_source: Literal['live','historical','test']

        Returns:
            None
    """

    #Initialize Quixstream application
    app = Application(
         broker_address=kafka_bootstrap_servers,
        consumer_group=kafka_consumer_group,
        auto_offset_reset='earliest' if data_source == 'historical' else 'latest'
    )

    #Initialize the input topic 
    input_topic = app.topic(
        name=kafka_input_topic,
        value_deserializer='json',
        
    )

    #Initialize the output topic
    output_topic = app.topic(
        name=kafka_output_topic,
        value_serializer='json'
    )       

    #Ingest the candle data from candle service(input topic)
    sdf = app.dataframe(input_topic)

    #filter the data by candle_seconds
    sdf = sdf.filter(lambda value: value['candle_seconds'] == candle_seconds)

    #Update the state with the latest candle
    sdf=sdf.apply(update_candle, stateful=True)

    #Compute the technical indicators
    sdf=sdf.apply(compute_technical_indicators, stateful=True)


    sdf = sdf.update(lambda value: logger.info(f"Final Message: {value}"))

    #set the output topic
    sdf = sdf.to_topic(output_topic)

    #start the application
    app.run()
        
    

if __name__ == "__main__":

    from config import settings
    main(
         kafka_bootstrap_servers=settings.kafka_bootstrap_servers,
        kafka_input_topic=settings.kafka_input_topic,
        kafka_output_topic=settings.kafka_output_topic,
        kafka_consumer_group=settings.kafka_consumer_group,
        candle_seconds=settings.candle_seconds,
        data_source=settings.data_source

        
    )
