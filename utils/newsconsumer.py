import os
import requests
import urllib.parse as urlparse
from urllib.parse import urlencode
class NewsConsumer:
    
    NEWS_API_KEY_NAME = "NEWS_API_KEY"
    BASE_URL = "https://newsapi.org/v2/everything?"
    REQUESTS_LIMIT = 100

    def __init__(self):
        self.num_requests=0
        
    def makeRequest(self, q: str, page: int, language: str = "en", page_size: int = 100) -> dict:
        if self.num_requests >= NewsConsumer.REQUESTS_LIMIT:
            return {}
        assert page_size > 0, "page_size can't be lesser than 0"
        assert page > 0, "pagination variable can't be a negative number"
        url_parts = list(urlparse.urlparse(NewsConsumer.BASE_URL))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update({'q':q, 'language':language, 'pageSize':page_size, 'page':page, 'apiKey':os.getenv(NewsConsumer.NEWS_API_KEY_NAME)})
        url_parts[4] = urlencode(query)
        self.num_requests+=page_size
        return requests.get(urlparse.urlunparse(url_parts)).json()