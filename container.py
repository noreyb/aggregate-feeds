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


class BooruContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    feed_url_handler: IFeedURLs = providers.Factory(
        GithubIOHandler,
        base_url=config.base_url,
        endpoint=config.endpoint,
    )
    aggregate_feed: IAggregateFeed = providers.Factory(
        BooruAggregateFeed,
        feed_url_handler=feed_url_handler,
        output_path=config.output_path,
        title=config.title,
        link=config.link,
        description=config.description,
    )


class ComicContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    feed_url_handler: IFeedURLs = providers.Factory(
        ComicRaindropIOHandler,
        token=config.token,
        collection_id=config.collection_id,
    )
    aggregate_feed: IAggregateFeed = providers.Factory(
        ComicAggregateFeed,
        feed_url_handler=feed_url_handler,
        output_path=config.output_path,
        title=config.title,
        link=config.link,
        description=config.description,
    )


class KemonoContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    feed_url_handler: IFeedURLs = providers.Factory(
        GithubIOHandler,
        base_url=config.base_url,
        endpoint=config.endpoint,
    )
    aggregate_feed: IAggregateFeed = providers.Factory(
        KemonoAggregateFeed,
        feed_url_handler=feed_url_handler,
        output_path=config.output_path,
        title=config.title,
        link=config.link,
        description=config.description,
    )


class FediverseContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    feed_url_handler: IFeedURLs = providers.Factory(
        FediverseRaindropIOHandler,
        token=config.token,
        collection_id=config.collection_id,
    )
    aggregate_feed: IAggregateFeed = providers.Factory(
        FediverseAggregateFeed,
        feed_url_handler=feed_url_handler,
        output_path=config.output_path,
        title=config.title,
        link=config.link,
        description=config.description,
    )
