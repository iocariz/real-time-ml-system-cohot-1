from datetime import timedelta
from loguru import logger
from src.config import config

def init_ohlc_candle(value:dict) -> dict:
    return {
        'open': value['price'],
        'high': value['price'],
        'low': value['price'],
        'close': value['price'],
        'product_id': value['product_id'],

    }

def update_ohlc_candle(ohlc_candle: dict, trade: dict) -> dict:
    """
    Updates the OHLC candle with the latest trade event

    Args:
        ohlc_candle (dict): The current OHLC candle
        trade (dict): The latest trade event
    
    """
    return {
        'open': trade['price'],
        'high': max(ohlc_candle['high'], trade['price']),
        'low': min(ohlc_candle['low'], trade['price']),
        'close': trade['price'],
        'product_id': trade['product_id'],

    }

def trade_to_ohlc(
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_broker_address: str,
    ohlc_window_seconds: int,
)  -> None:

    """
    Reads trade events from a Kafka topic, and produces OHLC events to another Kafka topic

    Args:
        kafka_input_topic (str): The Kafka topic to read trade events from
        kafka_output_topic (str): The Kafka topic to produce OHLC events to
        kafka_broker_address (str): The Kafka broker address
        ohlc_window_seconds (int): The window size in seconds to calculate OHLC events

    Returns:
        None
    """

    from quixstreams import Application

    # this handelsde all low level kafka operations
    app = Application(
        broker_address=kafka_broker_address, 
        consumer_group='trade-to-ohlc',
        auto_offset_reset='earliest',
    )

    # specify the input and output for this application
    input_topic = app.topic(name=kafka_input_topic, value_deserializer='json')
    output_topic = app.topic(name=kafka_output_topic, value_serializer='json')

    # create a streaming dataframe from the input topic
    # to apply transformations on the data

    sdf = app.dataframe(input_topic)

    # apply a window of ohlc_window_seconds

    sdf = sdf.tumbling_window(duration_ms=timedelta(seconds=ohlc_window_seconds))
    sdf = sdf.reduce(reducer=update_ohlc_candle, initializer=init_ohlc_candle).final()

    #extract the open, high, low, close prices from the OHLC candle
    sdf['open'] = sdf['value']['open']   
    sdf['high'] = sdf['value']['high']
    sdf['low'] = sdf['value']['low']
    sdf['close'] = sdf['value']['close']

    sdf['product_id'] = sdf['value']['product_id']
    sdf['timestamp'] = sdf['end']

    #select the columns to keep
    sdf = sdf[['product_id', 'timestamp', 'open', 'high', 'low', 'close']]

    #apply transformation to the data

    sdf = sdf.update(logger.info)

    sdf = sdf.to_topic(output_topic)

    #kick off the application
    app.run(sdf)

if __name__ == '__main__':

    # read the configuration from the environment
   
    trade_to_ohlc(
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_broker_address=config.kafka_broker_address,
        ohlc_window_seconds=config.ohcl_window_seconds,
    )






