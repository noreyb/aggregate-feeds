import time
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

import feedgenerator
import requests
from bs4 import BeautifulSoup

from repository.interface.feed_urls import IFeedURLs
from usecase.interface.aggregate_feed import IAggregateFeed


class NitterAggregateFeed(IAggregateFeed):
    def __init__(
        self,
        feed_url_handler: IFeedURLs,
        output_path: str,
        title: str,
        link: str,
        description: str,
    ) -> None:
        self.feed_url_handler = feed_url_handler
        self.output_path = output_path
        self.title = title
        self.link = link
        self.description = description

    def run(self) -> None:
        feeds = feedgenerator.Rss201rev2Feed(
            title=self.title,
            link=self.link,
            description=self.description,
        )

        # get twitter links
        raw_urls = self.feed_url_handler.get()
        for link in raw_urls:
            # get nitter content
            user = urlparse(link).path.split("/")[1]
            content = self.__get_nitter_content(user)
            if content is None:
                continue

            # parse nitter content
            soup = BeautifulSoup(content, "html.parser")
            bodies = soup.find_all(class_="tweet-body")
            # rows = soup.find_all(class_="gallery-row")
            for body in bodies:
                rows = body.find_all(class_="gallery-row")
                tweet_content = body.find(class_="tweet-content")
                for row in rows:
                    # imgs = f"https://nitter.net{row.find_all('a')}"
                    imgs = row.find_all("a")
                    for img in imgs:
                        img_link = f"https://nitter.net{img['href']}"
                        title = tweet_content.text
                        description = user

                        # add feed
                        enclosure = feedgenerator.Enclosure(
                            url=img_link, length="0", mime_type="image/jpg"
                        )

                        feeds.add_item(
                            title=title,
                            link=img_link,
                            description=description,
                            enclosure=enclosure,
                        )
        self.output(feeds)

    def output(self, feeds):
        with open(self.output_path, "w") as f:
            f.write(feeds.writeString("utf-8"))
        tree = ET.parse(self.output_path)
        ET.indent(tree, space="    ")
        tree.write(
            self.output_path,
            encoding="utf-8",
            xml_declaration=True,
        )

    def __get_nitter_content(self, user):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
            # 'Accept-Encoding': 'gzip, deflate, br',
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
        }

        nitter_base = "https://nitter.net"
        url = f"{nitter_base}/{user}/media"
        response = requests.get(url, headers=headers)
        time.sleep(2)
        if response.status_code != requests.codes.ok:
            return None

        return response.content
