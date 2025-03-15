from quixstreams import Application
from quixstreams.models import TimestampType
from typing import Any, Optional, List, Tuple
from datetime import timedelta
from config import settings


def custom_ts_extractor(
    value: Any,
    headers: Optional[List[Tuple[str, bytes]]],
    timestamp: float,
    timestamp_type: TimestampType,
    ) -> int:
    """
    Specifying a custom timestamp extractor to use the timestamp from the message payload 
    instead of Kafka timestamp.
    """
    return value["timestamp_ms"]


def init_candle(trade: dict) -> dict:
    """
    Initialize the state for aggregation when a new window starts.

    It will prime the aggregation when the first record arrives 
    in the window.
    """
    return {
        'open': trade['price'],
        'close': trade['price'],
        'high': trade['price'],
        'low': trade['price'],
        'volume': trade['volume'],
        'timestamp_ms': trade['timestamp_ms'],
        'pair': trade['pair']
    }



def update_candle(candle: dict, trade: dict) -> dict:
    """
    Update the state for aggregation when a new record arrives.
    """
    candle['close'] = trade['price']
    candle['high'] = max(candle['high'], trade['price'])
    candle['low'] = min(candle['low'], trade['price'])
    candle['volume'] += trade['volume']
    candle['timestamp_ms']=trade['timestamp_ms'],
    candle['pair']=trade['pair']
    
    return candle
    
def main(
    kafka_bootstrap_servers: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    candle_seconds: int
    ):

    """
        1. Ingest trade data from kafka topic
        2. generate candle using tubmling window
        3. write candle data to kafka topic

        Args:
            kafka_bootstrap_servers (str): kafka bootstrap servers
            kafka_input_topic (str): kafka input topic
            kafka_output_topic (str): kafka output topic
            kafka_consumer_group (str): kafka consumer group
            candle_seconds (int): candle seconds

        Returns:
            None 
    """
    print("Hello from candle!")
   
    #Initialize Quixstream application
    app= Application(
        broker_address=kafka_bootstrap_servers,
        consumer_group=kafka_consumer_group        
    )
    #initalize the input topic    
    input_topic=app.topic(
        name=kafka_input_topic,
        value_deserializer='json',
        timestamp_extractor=custom_ts_extractor  #custom_ts_extractor is a function that extracts the timestamp from the message payload
    )
    #initalize the output topic
    output_topic=app.topic(
        name=kafka_output_topic,
        value_serializer='json'
    )
    #Aggregation of trading into candle using tumbling windlow
   # sdf=  app.dataframe(topic=input_topic).tumbling_window(timedelta(seconds=candle_seconds)).reduce(reducer=update_candle, initializer=init_candle).current()  
    

    sdf=app.dataframe(topic=input_topic)
    sdf = (

    # Define a tumbling window of 10 minutes
    sdf.tumbling_window(timedelta(seconds=candle_seconds))

     #create reduce agregation 
    .reduce(reducer=update_candle, initializer=init_candle)

    # Emit results only for closed windows
    .current()
    )

    # define the tumbling window
    #sdf=app.tumbling_window(timedelta(seconds=candle_seconds))
    # Apply the reducer to update the candle data or initialize with first trade
   ## sdf=sdf.reduce(reducer=update_candle, initializer=init_candle)

    #Emit all intermediate candle data to make system more responsive
    ##sdf.current()  
    
    # if you want to email final candle data use sdf.final()
    # send final candle data to output topic
    

    #Extract the open,low,high,close from te data fram
        # Extract relevant columns
    sdf = sdf.apply(lambda value: {
        'pair': value['value']['pair'],
        'timestamp_ms': value['value']['timestamp_ms'],
        'open': value['value']['open'],
        'high': value['value']['high'],
        'low': value['value']['low'],
        'close': value['value']['close'],
        'volume': value['value']['volume'],
        'windows_start': value['start'],
        'windows_end': value['end']
    })
    #Keep only relevent column
    #sdf=[[

     #   'pair','timestamp_ms','open','high','low','close','volume','windows_start','windows_end'
    #]]

    
    sdf = sdf.update(lambda value: logger.info(f'Candle:{value}'))

   
    sdf.to_topic(topic=output_topic)
    app.run()

    

    #create a kafka consumer for the input topic
    

if __name__ == "__main__":

   
    main(
        kafka_bootstrap_servers=settings.kafka_bootstrap_servers,
        kafka_input_topic=settings.kafka_input_topic,
        kafka_output_topic=settings.kafka_output_topic,
        kafka_consumer_group=settings.kafka_consumer_group,
        candle_seconds=settings.candle_seconds
    )
