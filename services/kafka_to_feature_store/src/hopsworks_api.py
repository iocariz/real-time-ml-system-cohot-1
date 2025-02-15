import hopsworks
from src.config import config
import pandas as pd
def push_date_to_feature_store(
        feature_group_name: str,
        feature_group_version: int,
        date: str,
) -> None:
    """
    Writes the date to the feature store.
    
    Args:
        feature_group_name: The name of the feature group to write data to.
        feature_group_version: The version of the feature group to write data to.
        date: The date to write to the feature store.
    
    Returns:
        None    
    """

    project = hopsworks.login(
        project=config.hopsworks_project_name,
        api_key_value=config.hopsworks_api_key,
    )

    # Get the feature store
    feature_store = project.get_feature_store()

    # Get the feature group
    ohcl_fg = feature_store.get_feature_group(
        name=feature_group_name,
        version=feature_group_version,
        description='OHCL data coming from Kraken',
        primary_key=['product_id', 'timestamp'],
        event_time='timestamp',
        online_enabled=True,
    )
    # transfor the data(dict) to a dataframe
    
    ohcl_df = pd.DataFrame([data])

    # Write the data to the feature store
    ohcl_fg.insert(
        data=date,
    )