import sys

import click
from dotenv import load_dotenv

from container import (
    BooruContainer,
    ComicContainer,
    FediverseContainer,
    KemonoContainer,
)


def _get_wired_app(
    container, output_path: str, title: str, link: str, description: str
):
    container.config.from_dict(
        {
            "output_path": output_path,
            "title": title,
            "link": link,
            "description": description,
        }
    )
    container.wire(modules=[sys.modules[__name__]])
    return container.aggregate_feed()


@click.group()
def cli():
    pass


@cli.command()
def booru():
    container = BooruContainer()
    container.config.base_url.from_env("GITHUB_IO_BASE_URL")
    container.config.endpoint.from_env("GITHUB_IO_ENDPOINT")
    feed_aggregate = _get_wired_app(
        container,
        "./output/booru.xml",
        "agg-booru",
        "https://noreyb.github.io/agg-feed",
        "booru",
    )
    feed_aggregate.run()


@cli.command()
def comic():
    container = ComicContainer()
    container.config.token.from_env("RAINDROP_TOKEN")
    container.config.collection_id.from_env("RAINDROP_COLLECTION_ID")
    feed_aggregate = _get_wired_app(
        container,
        "./output/comic.xml",
        "agg-comic",
        "https://noreyb.github.io/agg-feed",
        "comic",
    )
    feed_aggregate.run()


@cli.command()
def kemono():
    container = KemonoContainer()
    container.config.base_url.from_env("GITHUB_IO_BASE_URL")
    container.config.endpoint.from_env("GITHUB_IO_ENDPOINT")
    feed_aggregate = _get_wired_app(
        container,
        "./output/kemono.xml",
        "agg-kemono",
        "https://noreyb.github.io/agg-feed",
        "kemono",
    )
    feed_aggregate.run()


@cli.command()
def fediverse():
    container = FediverseContainer()
    container.config.token.from_env("RAINDROP_TOKEN")
    container.config.collection_id.from_env("RAINDROP_COLLECTION_ID")
    feed_aggregate = _get_wired_app(
        container,
        "./output/fediverse.xml",
        "agg-fediverse",
        "https://noreyb.github.io/agg-feed",
        "fediverse",
    )
    container.config.random_page.from_value(True)
    feed_aggregate.run()


def main():
    cli()


if __name__ == "__main__":
    load_dotenv()
    main()
