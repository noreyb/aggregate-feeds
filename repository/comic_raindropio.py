import time

import requests
from bs4 import BeautifulSoup

from repository.raindropio import RaindropIOHandler


class ComicRaindropIOHandler(RaindropIOHandler):
    def __init__(self, token: str, collection_id: str, random_page: bool) -> None:
        super().__init__(token, collection_id, random_page)

    def get(self) -> list:
        urls = self._get_site_urls()
        print(urls)
        feed_urls = []
        for url in urls:
            if self.__is_supported_giga(url):
                feed_url = self.__get_feed_url_giga(url)

                if feed_url in feed_urls:  # Skip duplicate
                    continue
                feed_urls.append(feed_url)
            elif self.__is_supported_comici(url):
                feed_url = self.__get_feed_url_comici(url)
                if feed_url is None:
                    continue
                if feed_url in feed_urls:  # Skip duplicate
                    continue
                feed_urls.append(feed_url)
            else:
                continue
        return feed_urls

    def __is_supported_giga(self, url: str) -> bool:
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
        # urlの中にusing_gigaviewerのリストの中の文字列があるかどうかを判定する

        return True in [domain in url for domain in using_gigaviewer]

    def __is_supported_comici(self, url: str) -> bool:
        using_comici = [
            "carula.jp",
            "comicride.jp",
            "comic-medu.com",
            "comics.manga-bang.com",
            "younganimal.com",
            "youngchampion.jp",
            "studio.booklista.co.jp",
            "ebookstore.corkagency.com",
            "comici.jp",
        ]
        # urlの中にusing_gigaviewerのリストの中の文字列があるかどうかを判定する

        return True in [domain in url for domain in using_comici]

    def __get_feed_url_giga(self, url: str) -> str:
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

    def __get_feed_url_comici(self, url: str) -> str:
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
            'div',
            class_="prof-link-item mode-right",
        )

        feed_url = None
        for e in feed_urls:
            feed_url = e.find_all('a')[2]['href']
        return feed_url
