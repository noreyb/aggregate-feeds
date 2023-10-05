import time

import requests

from repository.interface.feed_urls import IFeedURLs


class RaindropIOHandler(IFeedURLs):
    def __init__(self, token: str, collection_id: str):
        self.token = token
        self.collection_id = collection_id

    def __get_items(self) -> list:
        url = "https://api.raindrop.io/rest/v1"
        endpoint = "/raindrops"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        count = -1
        n_page = 0
        items = []
        while count != 0:
            query = {
                "perpage": 50,
                "page": n_page,
            }

            resp = requests.get(
                f"{url}{endpoint}/{self.collection_id}",
                headers=headers,
                params=query,
            )

            if resp.status_code != requests.codes.ok:
                print(resp.text)
                exit()

            time.sleep(1)
            count = len(resp.json()["items"])
            n_page += 1
            items += resp.json()["items"]
        return items

    def _get_site_urls(self) -> list:
        items = self.__get_items()

        urls = []
        for item in items:
            urls.append(item["link"])
        return urls
