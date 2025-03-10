import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

from pydantic_settings import BaseSettings

class Config(BaseSettings):
    product_id: str = 'BTC/EUR'
    kafka_broker_address: str = os.getenv('KAFKA_BROKER_ADDRESS') 
    kafka_topic_name: str = 'trade'

config = Config()
    
