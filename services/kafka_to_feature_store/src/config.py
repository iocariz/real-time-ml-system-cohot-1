import os
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings

# Load environment variables
load_dotenv(find_dotenv())

from pydantic_settings import BaseSettings

class Config(BaseSettings):
    hopsworks_project_name: str = os.getenv('HOPSWORKS_PROJECT_NAME')
    hopsworks_api_key: str = os.getenv('HOPSWORKS_API_KEY')


config = Config()