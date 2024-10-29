import random
import time
from xml.etree import ElementTree as ET
from urllib.parse import urlparse, quote

import feedgenerator
import feedparser
import requests
from dateutil.parser import parse

from repository.interface.feed_urls import IFeedURLs
from usecase.interface.aggregate_feed import IAggregateFeed


class BooruAggregateFeed(IAggregateFeed):
    def __init__(
        self,
        feed_url_handler: IFeedURLs,
        output_path: str,
        title: str,
        link: str,
        description: str,
        N: int = 2,
    ) -> None:
        self.feed_url_handler = feed_url_handler
        self.output_path = output_path
        self.title = title
        self.link = link
        self.description = description
        self.N = N

    def run(self) -> None:
        feeds = feedgenerator.Rss201rev2Feed(
            title=self.title,
            link=self.link,
            description=self.description,
        )

        feed_urls = self.feed_url_handler.get()
        feed_urls = random.sample(feed_urls, min(self.N, len(feed_urls)))
        for feed_url in feed_urls:
            rss_feed = self.__get_rss_contents(feed_url)
            entries = rss_feed["entries"]
            feeds = self.__add_feed_item(feeds, entries)
        self.output(feeds)

    def __get_rss_contents(self, feed_url: str) -> dict:
        r = requests.get(
            feed_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) ",
            },
        )
        time.sleep(2)
        if r.status_code != requests.codes.ok:
            raise Exception(r.text)
        return feedparser.parse(r.text)

    def __add_feed_item(self, feeds, entries):
        for entry in entries:
            enclosure = None
            if 1 < len(entry["links"]):  # Only catch media note
                enclosure = feedgenerator.Enclosure(
                    url=entry["links"][1]["href"],
                    length=entry["links"][1]["length"],
                    mime_type=entry["links"][1]["type"],
                )

            
            # o = urlparse(entry["link"])
            # link = o._replace(query=quote(o.query))
            # link = link.geturl()
            # print(link)

            feeds.add_item(
                title=entry["title"],
                link=entry["link"],
                description=entry["description"],
                enclosure=enclosure,
                # pubdate=parse(entry["published"]),
            )
        return feeds

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
