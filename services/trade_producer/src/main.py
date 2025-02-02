# Create an Application instance with Kafka configs
from typing import Dict, List

from loguru import logger
from quixstreams import Application

from src.kraken_apy import KrakenWebsocketTradeAPI
from src import config


def produce_trade(
    kafka_broker_address: str,
    kafka_topic_name: str,
    product_id: str,
) -> None:
    """
    Produce a trade event into a Kafka topic
    """
    app = Application(broker_address=kafka_broker_address)

    # Define a topic with JSON serialization
    topic = app.topic(name=kafka_topic_name, value_serializer='json')
    kraken_api = KrakenWebsocketTradeAPI(product_id=product_id)

    logger.info('Producing trade events')

    # Create a Producer instance
    with app.get_producer() as producer:
        while True:
            # Get trades from Kraken API
            trades: List[Dict] = kraken_api.get_trades()

            for trade in trades:
                # Serialize an event using the defined Topic
                message = topic.serialize(key=trade['product_id'], value=trade)

                # Produce a message into the Kafka topic
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(f'Produced trade event: {trade}')

            from time import sleep

            sleep(1)


if __name__ == '__main__':
    produce_trade(
        kafka_broker_address=config.kafka_broker_address, 
        kafka_topic_name=config.kafka_topic_name,
        product_id=config.product_id,
    )
