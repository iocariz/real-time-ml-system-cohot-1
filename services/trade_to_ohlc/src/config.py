import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

from pydantic_settings import BaseSettings

class Config(BaseSettings):
    kafka_broker_address: str = os.getenv('KAFKA_BROKER_ADDRESS') 
    kafka_input_topic: str = 'trade'
    kafka_output_topic: str = 'ohlc'
    ohcl_window_seconds: int =os.getenv('OHCL_WINDOW_SECONDS')

config = Config()