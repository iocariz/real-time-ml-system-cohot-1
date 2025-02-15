from quixstreams import Application
import json
from loguru import logger
from src.hopsworks_api import push_date_to_feature_store

def kafka_to_feature_store(
        kafka_topic: str,
        kafka_broker_address: str,
        feature_group_name: str,
        feature_group_version: int,
) -> None:
    """
    Reads 'ohcl' data from Kafka topic and writes it to the feature store.
    More specifically, it reads the data to the feature group specified by
    'feature_group_name' and 'feature_group_version'.
    
    Args:
        kafka_topic: The Kafka topic to read data from.
        kafka_broker_address: The Kafka broker address.
        feature_group_name: The name of the feature group to write data to.
        feature_group_version: The version of the feature group to write data to.
    
    Returns:
        None    
    """
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group='kafka_to_feature_store',
    )

    #input_topic = app.topic(name=kafka_topic, value_deserializer='json')

    with app.get_consumer() as consumer:
        consumer.subscribe(topics=[kafka_topic])

        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            elif msg.error():
                logger.error('Kafka error: {}'.format(msg.error()))
                continue  
            else:
                # Write the data to the feature store
                #Parse the message
                ohcl = json.loads(msg.value().decode('utf-8')) 
                #Write the data to the feature store
                
                push_date_to_feature_store(
                    feature_group_name=eature_group_name, 
                    feature_group_version=feature_group_version,
                    data=ohcl,
                    )
                logger.info('Data written to feature store')
                consumer.store_offsets(message=msg)

if __name__ == '__main__':
    kafka_to_feature_store(
        kafka_topic='ohcl',
        kafka_broker_address='broker:19092',
        feature_group_name='ohcl',
        feature_group_version=1,
    )

  


    