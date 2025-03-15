from quixstreams import Application
from quixstreams.models import TimestampType
from typing import Any, Optional, List, Tuple
from datetime import timedelta
import logging
from config import settings
from typing import Literal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def custom_ts_extractor(
    value: Any,
    headers: Optional[List[Tuple[str, bytes]]],
    timestamp: float,
    timestamp_type: TimestampType,
) -> int:
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
    candle['close'] = trade['price']
    candle['high'] = max(candle['high'], trade['price'])
    candle['low'] = min(candle['low'], trade['price'])
    candle['volume'] += trade['volume']
    candle['timestamp_ms'] = trade['timestamp_ms']
    candle['pair'] = trade['pair']
    return candle

def main(
    kafka_bootstrap_servers: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    candle_seconds: int,
    data_source: Literal['live','historical','test']
):

    
    #Initialize Quixstream application
    app = Application(
        broker_address=kafka_bootstrap_servers,
        consumer_group=kafka_consumer_group,
        #this is for how the data should consume from kafka
        auto_offset_reset='earliest' if data_source == 'historical' else 'latest'
    )

    #initalize the input topic 
    input_topic = app.topic(
        name=kafka_input_topic,
        value_deserializer='json',
        timestamp_extractor=custom_ts_extractor
    )

    #initalize the output topic 
    output_topic = app.topic(
        name=kafka_output_topic,
        value_serializer='json'
    )
    #Aggregation of trading into candle using tumbling windlow
    sdf = app.dataframe(input_topic)
    sdf = (
        sdf.tumbling_window(timedelta(seconds=candle_seconds))
        .reduce(reducer=update_candle, initializer=init_candle)
        .current()
    )

    # Extract relevant columns from output
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

    sdf['candle_seconds']=candle_seconds
    #this line is very importent and it will update the data to candle topic. if its not there candleservice will say message that "Waiting for message"
    sdf = sdf.update(lambda value: logger.info(f'Candle: {value}'))

    #Set the output to output topic candle
    sdf.to_topic(output_topic)
    app.run()

if __name__ == "__main__":
    main(
        kafka_bootstrap_servers=settings.kafka_bootstrap_servers,
        kafka_input_topic=settings.kafka_input_topic,
        kafka_output_topic=settings.kafka_output_topic,
        kafka_consumer_group=settings.kafka_consumer_group,
        candle_seconds=settings.candle_seconds,
        data_source=settings.data_source
    )
