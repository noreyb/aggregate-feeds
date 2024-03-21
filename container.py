from injector import Module

from repository.comic_raindropio import ComicRaindropIOHandler
from repository.fediverse_raindropio import FediverseRaindropIOHandler
from repository.githubio import GithubIOHandler

# from repository.interface.feed_urls import IFeedURLs
from repository.twitter_raindropio import TwitterRaindropIOHandler
from usecase.booru_aggregate import BooruAggregateFeed
from usecase.comic_aggregate import ComicAggregateFeed
from usecase.fediverse_aggregate import FediverseAggregateFeed
from usecase.interface.aggregate_feed import IAggregateFeed
from usecase.kemono_aggregate import KemonoAggregateFeed
from usecase.twitter_aggregate import TwitterAggregateFeed


class BooruFactory(Module):
    def __init__(
        self,
        base_url: str,
        endpoint: str,
        output_path: str,
        title: str,
        link: str,
        description: str,
    ):
        self.base_url = base_url
        self.endpoint = endpoint
        self.output_path = output_path
        self.title = title
        self.link = link
        self.description = description

    def configure(self, binder):
        binder.bind(
            IAggregateFeed,
            to=BooruAggregateFeed(
                GithubIOHandler(self.base_url, self.endpoint),
                self.output_path,
                self.title,
                self.link,
                self.description,
            ),
        )


class ComicFactory(Module):
    def __init__(
        self,
        token: str,
        collection_id: str,
        random_page: bool,
        output_path: str,
        title: str,
        link: str,
        description: str,
    ):
        self.token = token
        self.collection_id = collection_id
        self.random_page = random_page
        self.output_path = output_path
        self.title = title
        self.link = link
        self.description = description

    def configure(self, binder):
        binder.bind(
            IAggregateFeed,
            to=ComicAggregateFeed(
                ComicRaindropIOHandler(
                    token=self.token,
                    collection_id=self.collection_id,
                    random_page=self.random_page,
                ),
                self.output_path,
                self.title,
                self.link,
                self.description,
            ),
        )


class KemonoFactory(Module):
    def __init__(
        self,
        base_url: str,
        endpoint: str,
        output_path: str,
        title: str,
        link: str,
        description: str,
    ):
        self.base_url = base_url
        self.endpoint = endpoint
        self.output_path = output_path
        self.title = title
        self.link = link
        self.description = description

    def configure(self, binder):
        binder.bind(
            IAggregateFeed,
            to=KemonoAggregateFeed(
                GithubIOHandler(self.base_url, self.endpoint),
                self.output_path,
                self.title,
                self.link,
                self.description,
            ),
        )


class FediverseFactory(Module):
    def __init__(
        self,
        token: str,
        collection_id: str,
        random_page: bool,
        output_path: str,
        title: str,
        link: str,
        description: str,
    ):
        self.token = token
        self.collection_id = collection_id
        self.random_page = random_page
        self.output_path = output_path
        self.title = title
        self.link = link
        self.description = description

    def configure(self, binder):
        binder.bind(
            IAggregateFeed,
            to=FediverseAggregateFeed(
                FediverseRaindropIOHandler(
                    token=self.token,
                    collection_id=self.collection_id,
                    random_page=self.random_page,
                ),
                self.output_path,
                self.title,
                self.link,
                self.description,
            ),
        )


class TwitterFactory(Module):
    def __init__(
        self,
        token: str,
        collection_id: str,
        email: str,
        _id: str,
        passwd: str,
        random_page: bool,
        output_path: str,
        title: str,
        link: str,
        description: str,
    ):
        self.token = token
        self.collection_id = collection_id
        self.random_page = random_page
        self.output_path = output_path
        self.title = title
        self.link = link
        self.description = description
        self.email = email
        self._id = _id
        self.passwd = passwd

    def configure(self, binder):
        binder.bind(
            IAggregateFeed,
            to=TwitterAggregateFeed(
                TwitterRaindropIOHandler(
                    token=self.token,
                    collection_id=self.collection_id,
                    random_page=self.random_page,
                ),
                self.email,
                self._id,
                self.passwd,
                self.output_path,
                self.title,
                self.link,
                self.description,
            ),
        )
