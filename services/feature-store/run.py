from config import settings, hopsworks_config
from quixstreams.sinks.core.csv import CSVSink
from quixstreams import Application
from loguru import logger
#from quixstreams import HopsworksFeatureStoreSink
from sink import HopsworksFeatureStoreSink
from typing import Literal
def main(
    kafka_bootstrap_servers: str,
    kafka_input_topic: str,
    kafka_consumer_group: str,
    output_sink: HopsworksFeatureStoreSink,
    data_source: Literal['live','historical','test']
    #feature_group_name: str,
    #feature_group_version: int,
):

    """
    2 things to do:
    1. It will read the data from the kafka topic and 
    2. save it to the feature-store.

    Args:
        kafka_bootstrap_servers: str
        kafka_input_topic: str
        kafka_consumer_group: str
        output_sink: HopsworksFeatureStoreSink
        data_source: Literal['live','historical','test']
    """
    logger.info("Hello from feature-store!")
    app = Application(
        broker_address=kafka_bootstrap_servers,
        consumer_group=kafka_consumer_group,
        auto_offset_reset='earliest' if data_source == 'historical' else 'latest'   
    )
    #initalize the input topic 
    input_topic = app.topic(
        name=kafka_input_topic,
        value_deserializer='json',
    )
    
    
    #Push the data to the feature-store using quixstreams sink
    # Initialize a CSV sink with a file path 
    #csv_sink = CSVSink(path="technical_indicator.csv")

    sdf = app.dataframe(input_topic)
    # Do some processing here ...
    # Sink data to a CSV file
    sdf.sink(output_sink)
    app.run()

    


if __name__ == "__main__":


     #sink the data to the feature-store
    output_sink=HopsworksFeatureStoreSink(

        #hopsworks credentials
        api_key=hopsworks_config.hopsworks_api_key,
        project_name=hopsworks_config.hopsworks_project_name,

        #feature-group config
        feature_group_name=settings.feature_group_name,
        feature_group_version=settings.feature_group_version,
        feature_group_primary_key=settings.feature_group_primary_key,
        feature_group_event_time=settings.feature_group_event_time,
        feature_group_mateization_interval=settings.feature_group_mateization_interval
    )

    main(
        kafka_bootstrap_servers=settings.kafka_bootstrap_servers,
        kafka_input_topic=settings.kafka_input_topic,
        kafka_consumer_group=settings.kafka_consumer_group,
        output_sink=output_sink,
        data_source=settings.data_source
    )
