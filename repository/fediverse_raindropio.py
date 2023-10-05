from repository.raindropio import RaindropIOHandler


class FediverseRaindropIOHandler(RaindropIOHandler):
    def __init__(self, token: str, collection_id: str) -> None:
        super().__init__(token, collection_id)

    def get(self) -> list:
        urls = self._get_site_urls()
        feed_urls = []
        for url in urls:
            feed_url = f"{url}.rss"
            if feed_url in feed_urls:  # Skip duplicate
                continue
            feed_urls.append(feed_url)
        return feed_urls
