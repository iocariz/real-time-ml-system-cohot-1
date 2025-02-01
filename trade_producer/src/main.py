# Create an Application instance with Kafka configs
from quixstreams import Application
from src.kraken_apy import KrakenWebsocketTradeAPI
from typing import List, Dict

def produce_trade(
    kafka_broker_address: str,
    kafka_topic_name: str,
) -> None:    
    """
    Produce a trade event into a Kafka topic
    """
    app = Application(
        broker_address=kafka_broker_address)

    # Define a topic with JSON serialization
    topic = app.topic(name=kafka_topic_name, value_serializer='json')
    kraken_api = KrakenWebsocketTradeAPI(product_id='BTC/USD')

      # Create a Producer instance
    with app.get_producer() as producer:

        while True:
            # Get trades from Kraken API
            trades: List[Dict] = kraken_api.get_trades()

            for trade in trades:

                # Serialize an event using the defined Topic 
                message = topic.serialize(key=trade["product_id"], 
                                          value=trade)

                # Produce a message into the Kafka topic
                producer.produce(
                    topic=topic.name, 
                    value=message.value, 
                    key=message.key
                )

                print('Message produced:', message)    
                from time import sleep
                sleep(1)

if __name__ == "__main__":
    produce_trade(
        kafka_broker_address='localhost:19092',
        kafka_topic_name='trade'
    )