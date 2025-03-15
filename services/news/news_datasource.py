import os
import time
from typing import List
from quixstreams.sources.base import StatefulSource
from news_download import NewsDownload
from loguru import logger
from typing import Optional

class NewsDatasource(StatefulSource):
    def __init__(self,
        news_download: NewsDownload,
        polling_interval:Optional[int] = 10
    ):
        logger.info("news-datasource: starting initialization")
        super().__init__(name="news_datasource")
        self.news_download = news_download
        self.polling_interval = polling_interval
        logger.info("news-datasource: initialization complete")

    
    def setup(self):    
        logger.info("news-datasource: setup complete")
        self.state.set("last_published_at", None)
        self.flush()
        logger.info("news-datasource: state set to None")

        
    
    def run(self):
        logger.info("news-datasource: starting run loop")
        last_published_at = self.state.get("last_published_at", None)
        while self.running:
                      
                # Download news
                news = self.news_download.get_news()
                logger.info(f"news-datasource: downloaded {len(news)} news items")

                # Filter news if we have a last published timestamp if last_published_at is not None
                if last_published_at is not None:
                    news = [news_item for news_item in news if news_item.published_at > last_published_at]
                    logger.info(f"news-datasource: filtered to {len(news)} new items")

                # Process each news item
                for news_item in news:
                  
                    msg = self.serialize(
                        key="news",
                        value=news_item.to_dict()
                    )
                    self.produce(
                            key=msg.key,
                            value=msg.value
                    
                    )
                #get the last published news item
                if news:
                    last_published_at = news[-1].published_at

                # Update state after successful produce
                self.state.set("last_published_at", last_published_at)
                   
                self.flush()
                # Sleep before next poll
                time.sleep(self.polling_interval)

            

   





