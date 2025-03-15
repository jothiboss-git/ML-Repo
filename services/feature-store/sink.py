from quixstreams.sinks.base import BatchingSink, SinkBatch 
import hopsworks
from loguru import logger
import pandas as pd
from datetime import datetime, timezone


class HopsworksFeatureStoreSink(BatchingSink):

    """
       Sink the data to the hopsworks feature-store
    """
  # you can find the code in the quixstreams documentation
    def __init__(self, 
            api_key: str, 
            project_name: str,
            feature_group_name: str, 
            feature_group_version: int,
            feature_group_primary_key: list[str],
            feature_group_event_time: str,
            feature_group_mateization_interval: int
    ):

        """
         Establish a connection to the hopsworks feature-store
        """
        self.api_key = api_key
        self.project_name = project_name
        self.feature_group_name = feature_group_name
        self.feature_group_version = feature_group_version
        self.feature_group_primary_key = feature_group_primary_key
        self.feature_group_event_time = feature_group_event_time
        self.feature_group_mateization_interval = feature_group_mateization_interval
        
        #Establish the connection to the hopsworks feature-store . Refer the code at hopsworks documentation
        project=hopsworks.login(project=self.project_name, api_key_value=self.api_key)
        self.feature_store=project.get_feature_store()
        #Get the feature group or create it if it doesn't exist . Refer the code at hopsworks documentation
        self.feature_group=self.feature_store.get_or_create_feature_group(
            name=self.feature_group_name,
            version=self.feature_group_version,
            primary_key=self.feature_group_primary_key,
            event_time=self.feature_group_event_time,
            online_enabled=True,
           
        )

        self.setup()

        #set the feature group mateization interval. this is the interval at which the feature group will be materialized.run every 15 minutes
        self.feature_group.materialization_job.schedule (
            cron_expression=f"0 0/{self.feature_group_mateization_interval} * ? * * *",
            start_time=datetime.now(tz=timezone.utc),
           
        )

        

        #Call baseclass constructor to initialize the batches
        super().__init__()

    def setup(self):
       
        logger.info(f"Feature group created: {self.feature_group}")


    def write(self, batch: SinkBatch):
        # Simulate some DB connection here
        data = [item.value for item in batch]
        data= pd.DataFrame(data)

        #breakpoint()
        try:
            # Try to write data to the db
            self.feature_group.insert(data)
        except TimeoutError:
            # In case of timeout, tell the app to wait for 30s 
            # and retry the writing later
            raise SinkBackpressureError(
               retry_after=30.0, 
               topic=batch.topic, 
               partition=batch.partition,
            )
