import os

import click
from dotenv import load_dotenv
from injector import Injector

from container import (
    BooruFactory,
    ComicFactory,
    FediverseFactory,
    KemonoFactory,
    TwitterFactory,
)
from usecase.interface.aggregate_feed import IAggregateFeed

# TODO: remove later
load_dotenv()


@click.group()
def cli():
    pass


@cli.command()
def booru():
    factory = BooruFactory(
        base_url=os.getenv("BOORU_BASE_URL"),
        endpoint=os.getenv("BOORU_ENDPOINT"),
        output_path="./output/booru.xml",
        title="agg-booru",
        link="https://noreyb.github.io/agg-feed",
        description="booru",
    )
    injector = Injector(factory.configure)
    feed_aggregate = injector.get(IAggregateFeed)
    feed_aggregate.run()


@cli.command()
def comic():
    factory = ComicFactory(
        token=os.getenv("RAINDROP_TOKEN"),
        collection_id=os.getenv("RAINDROP_COMIC"),
        random_page=True,
        output_path="./output/comic.xml",
        title="agg-comic",
        link="https://noreyb.github.io/agg-feed",
        description="comic",
    )
    injector = Injector(factory.configure)
    feed_aggregate = injector.get(IAggregateFeed)
    feed_aggregate.run()


@cli.command()
def kemono():
    factory = KemonoFactory(
        base_url=os.getenv("KEMONO_BASE_URL"),
        endpoint=os.getenv("KEMONO_ENDPOINT"),
        output_path="./output/fediverse.xml",
        title="agg-fediverse",
        link="https://noreyb.github.io/agg-feed",
        description="fediverse",
    )
    injector = Injector(factory.configure)
    feed_aggregate = injector.get(IAggregateFeed)
    feed_aggregate.run()


@cli.command()
def fediverse():
    factory = FediverseFactory(
        token=os.getenv("RAINDROP_TOKEN"),
        collection_id=os.getenv("RAINDROP_FEDIVERSE"),
        random_page=True,
        output_path="./output/fediverse.xml",
        title="agg-fediverse",
        link="https://noreyb.github.io/agg-feed",
        description="fediverse",
    )
    injector = Injector(factory.configure)
    feed_aggregate = injector.get(IAggregateFeed)
    feed_aggregate.run()


@cli.command()
def twitter():
    factory = TwitterFactory(
        token=os.getenv("RAINDROP_TOKEN"),
        collection_id=os.getenv("RAINDROP_TWITTER"),
        email=os.getenv("TWITTER_EMAIL"),
        _id=os.getenv("TWITTER_ID"),
        passwd=os.getenv("TWITTER_PASSWORD"),
        random_page=True,
        output_path="./output/twitter.xml",
        title="agg-twitter",
        link="https://noreyb.github.io/agg-feed",
        description="twitter",
    )
    injector = Injector(factory.configure)
    feed_aggregate = injector.get(IAggregateFeed)
    feed_aggregate.run()


def main():
    cli()


if __name__ == "__main__":
    load_dotenv()
    main()
