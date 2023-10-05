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
    feed_aggregate = _get_wired_app(
        container, "booru.xml", "booru", "https://booru.moe", "booru"
    )
    feed_aggregate.run()


@cli.command()
def comic():
    container = ComicContainer()
    container.config.token.from_env("RAINDROP_TOKEN")
    container.config.collection_id.from_env("RAINDROP_COLLECTION_ID")
    feed_aggregate = _get_wired_app(
        container, "comic.xml", "comic", "https://comic.moe", "comic"
    )
    feed_aggregate.run()


@cli.command()
def kemono():
    container = KemonoContainer()
    feed_aggregate = _get_wired_app(
        container, "kemono.xml", "kemono", "https://kemono.moe", "kemono"
    )
    feed_aggregate.run()


@cli.command()
def fediverse():
    container = FediverseContainer()
    container.config.token.from_env("RAINDROP_TOKEN")
    container.config.collection_id.from_env("RAINDROP_COLLECTION_ID")
    feed_aggregate = _get_wired_app(
        container, "fediverse.xml", "fediverse", "https://fediverse.moe", "fediverse"
    )
    feed_aggregate.run()


def main():
    cli()


if __name__ == "__main__":
    load_dotenv()
    main()