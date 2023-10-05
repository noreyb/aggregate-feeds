import time

import requests
from bs4 import BeautifulSoup

from repository.raindropio import RaindropIOHandler


class ComicRaindropIOHandler(RaindropIOHandler):
    def __init__(self, token: str, collection_id: str) -> None:
        super().__init__(token, collection_id)

    def get(self) -> list:
        urls = self._get_site_urls()
        feed_urls = []
        for url in urls:
            if self.__is_supported(url):
                feed_url = self.__get_feed_url(url)

                if feed_url in feed_urls:  # Skip duplicate
                    continue
                feed_urls.append(feed_url)
        return feed_urls

    def __is_supported(self, url: str) -> bool:
        using_gigaviewer = [
            "shonenjumpplus.com",
            "comic-ogyaaa.com",
            "sunday-webry",
            "tonarinoyj.jp",
            "kuragebunch.com",
            "comic-days.com",
            "andsofa.com",
            "morningtwo.com",
            "getsumagakichi.com",
            "viewer.heros-web.com",
            "comicborder.com",
            "comic-gardo.com",
            "comic-zenon.com",
            "magcomi.com",
            "comic-action.com",
            "comic-trail.com",
            "comicbushi-web.com",
            "feelweb.jp",
            "corocoro.jp",
        ]
        return url in using_gigaviewer

    def __get_feed_url(self, url: str) -> str:
        resp = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ",
            },
        )
        time.sleep(1)
        if resp.status_code != requests.codes.ok:
            raise Exception("Failed to get feed url")

        soup = BeautifulSoup(resp.text, "html.parser")
        feed_urls = soup.find_all(
            "link",
            attrs={
                "type": "application/rss+xml",
                "rel": "alternate",
            },
        )
        feed_url = feed_urls[0]["href"]
        if 1 != len(feed_urls):
            feed_url += "?free_only=1"
        return feed_url
