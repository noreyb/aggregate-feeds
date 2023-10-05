import time

import requests
from bs4 import BeautifulSoup

from repository.interface.feed_urls import IFeedURLs


class GithubIOHandler(IFeedURLs):
    def __init__(self):
        pass

    def get(self) -> list:
        resp = requests.get(
            f"{self.base_url}/{self.endpoint}",
        )
        time.sleep(1)
        if resp.status_code != requests.codes.ok:
            raise Exception(resp.text)

        soup = BeautifulSoup(resp.text, "html.parser")
        feed_urls = []
        for elem in soup.find_all("a"):
            feed_url = elem.get("href")
            if "opml" in feed_url:
                continue
            feed_url = f"{self.base_url}/{feed_url}"
            feed_urls.append(feed_url)
        return feed_urls
