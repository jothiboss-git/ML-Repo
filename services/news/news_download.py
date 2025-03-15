import requests
from typing import List,Tuple   
from loguru import logger
from pydantic import BaseModel

class News(BaseModel):
    """
    News model
    """
    title: str
    url: str
    source: str
    published_at: str

    def to_dict(self) -> dict:
        """
        Convert the News object to a dictionary
        """
        return self.model_dump()



class NewsDownload:

    URL="https://cryptopanic.com/api/free/v1/posts/"

    def __init__(self,
        cryptopanic_api_key: str
    ):
        self.cryptopanic_api_key = cryptopanic_api_key

    def get_news(self) -> List[News]:
        """
        Keep calling _get_batchnews() until the last page is reached
        """
        logger.info(f"news-download: getting news")
        news = []
        url = self.URL
        while True:
            batch_news, next_url = self._get_batchnews(url)
            logger.info(f"batch_news: length {len(batch_news)}")
            if not batch_news or next_url is None:
                break
            news.extend(batch_news)
            url = next_url

        #sort the news by published_at to get the latest news first , reverse=False
        news.sort(key=lambda x: x.published_at, reverse=False)
        return news

    def _get_batchnews(self, url:str) -> Tuple[List[News],str]:
        """
           connect to the cryptopanic REST API and get the news
           Args:
               url: the url to get the news
           Returns:
               news: the news
               next_url: the next url to get the news
            
        """
        logger.info(f"news-download: getting news from {url}")
        try:
            response = requests.get(
                url,
                params={"auth_token": self.cryptopanic_api_key}
            )
            #response.raise_for_status()  # Raise an exception for bad status codes
            response_json = response.json()
            
            news = [News(
                title=item["title"],
                url=item["url"],
                source=item["source"]["title"],  # source is a dict with title
                published_at=item["published_at"]
            ) for item in response_json["results"]]

            #Extract the next url from the response if it exists    
            next_url = response_json.get("next")
            return news, next_url

        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting news: {e}")
            return [], None
        except (KeyError, ValueError) as e:
            logger.error(f"Error parsing news response: {e}")
            return [], None

        



