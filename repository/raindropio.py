import random
import time

import requests

from repository.interface.feed_urls import IFeedURLs


class RaindropIOHandler(IFeedURLs):
    def __init__(self, token: str, collection_id: str, random_page: bool = False):
        self.token = token
        self.collection_id = collection_id
        self.random_page = random_page

    def __pick_all_items(self, url: str, endpoint: str, headers: dict) -> list:
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

    def __pick_random_items(self, url: str, endpoint: str, headers: dict) -> list:
        n_page = 0
        while True:
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
            if count == 0:
                break
            n_page += 1
        total_page = n_page
        n_page = random.randint(0, total_page - 1)
        print(f"total_page: {total_page}, n_page: {n_page}")
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
        items = resp.json()["items"]
        return items

    def __get_items(self) -> list:
        url = "https://api.raindrop.io/rest/v1"
        endpoint = "/raindrops"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        if self.random_page:
            items = self.__pick_random_items(url, endpoint, headers)
        else:
            items = self.__pick_all_items(url, endpoint, headers)
        return items

    def _get_site_urls(self) -> list:
        items = self.__get_items()
        urls = []
        for item in items:
            urls.append(item["link"])
        return urls
