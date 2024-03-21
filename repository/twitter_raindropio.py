from repository.raindropio import RaindropIOHandler


class TwitterRaindropIOHandler(RaindropIOHandler):
    def __init__(self, token: str, collection_id: str, random_page: bool) -> None:
        self.token = token
        self.collection_id = collection_id
        self.random_page = random_page

    def get(self) -> list:
        raw_urls = self._get_site_urls()
        raw_urls = [e for e in raw_urls if "twitter.com" in e]
        return raw_urls  # return raw urls, not feed urls
