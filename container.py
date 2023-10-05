from dependency_injector import containers, providers

from repository.comic_raindropio import ComicRaindropIOHandler
from repository.fediverse_raindropio import FediverseRaindropIOHandler
from repository.githubio import GithubIOHandler
from repository.interface.feed_urls import IFeedURLs
from usecase.booru_aggregate import BooruAggregateFeed
from usecase.comic_aggregate import ComicAggregateFeed
from usecase.fediverse_aggregate import FediverseAggregateFeed
from usecase.interface.aggregate_feed import IAggregateFeed
from usecase.kemono_aggregate import KemonoAggregateFeed


class FediverseContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    feed_url_handler: IFeedURLs = providers.Factory(
        FediverseRaindropIOHandler,
        base_url=config.fediverse_raindropio.base_url,
        endpoint=config.fediverse_raindropio.endpoint,
    )

    aggregate_feed: IAggregateFeed = providers.Factory(
        FediverseAggregateFeed,
        feed_url_handler=feed_url_handler,
        output_path=config.fediverse_raindropio.output_path,
        title=config.fediverse_raindropio.title,
        link=config.fediverse_raindropio.link,
        description=config.fediverse_raindropio.description,
    )


class ComicContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    feed_url_handler: IFeedURLs = providers.Factory(
        ComicRaindropIOHandler,
        base_url=config.comic_raindropio.base_url,
        endpoint=config.comic_raindropio.endpoint,
    )

    aggregate_feed: IAggregateFeed = providers.Factory(
        ComicAggregateFeed,
        feed_url_handler=feed_url_handler,
        output_path=config.comic_raindropio.output_path,
        title=config.comic_raindropio.title,
        link=config.comic_raindropio.link,
        description=config.comic_raindropio.description,
    )


class BooruContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    feed_url_handler: IFeedURLs = providers.Factory(
        GithubIOHandler,
        base_url=config.booru_raindropio.base_url,
        endpoint=config.booru_raindropio.endpoint,
    )

    aggregate_feed: IAggregateFeed = providers.Factory(
        BooruAggregateFeed,
        feed_url_handler=feed_url_handler,
        output_path=config.booru_raindropio.output_path,
        title=config.booru_raindropio.title,
        link=config.booru_raindropio.link,
        description=config.booru_raindropio.description,
    )


class KemonoContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    feed_url_handler: IFeedURLs = providers.Factory(
        GithubIOHandler,
        base_url=config.kemono_raindropio.base_url,
        endpoint=config.kemono_raindropio.endpoint,
    )

    aggregate_feed: IAggregateFeed = providers.Factory(
        KemonoAggregateFeed,
        feed_url_handler=feed_url_handler,
        output_path=config.kemono_raindropio.output_path,
        title=config.kemono_raindropio.title,
        link=config.kemono_raindropio.link,
        description=config.kemono_raindropio.description,
    )
