import os
import random
import re
import time
import uuid
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

import feedgenerator
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

from repository.interface.feed_urls import IFeedURLs
from usecase.interface.aggregate_feed import IAggregateFeed


class Capture:
    def __init__(self) -> None:
        self.counter = 0

    def run(self, page):
        time.sleep(5)
        page.screenshot(path=f"./img/{self.counter}.png")
        self.counter += 1


class TwitterAggregateFeed(IAggregateFeed):
    def __init__(
        self,
        feed_url_handler: IFeedURLs,
        email: str,
        _id: str,
        passwd: str,
        output_path: str,
        title: str,
        link: str,
        description: str,
    ) -> None:
        self.feed_url_handler = feed_url_handler
        self.email = email
        self._id = _id
        self.passwd = passwd
        self.output_path = output_path
        self.title = title
        self.link = link
        self.description = description

    def run(self) -> None:
        feeds = feedgenerator.Rss201rev2Feed(
            title=self.title,
            link=self.link,
            description=self.description,
        )
        # capture = Capture()

        with sync_playwright() as p:
            # ログイン処理
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto("https://twitter.com/i/flow/login")
            # capture.run(page)

            email_input = page.get_by_label("Phone")
            email_input.wait_for(timeout=5000)
            email_input.fill(self.email)
            page.get_by_role("button", name="Next").click()
            # capture.run(page)

            # user_idの入力画面があるかどうかを待ってから確認
            try:
                user_id_input = page.get_by_test_id("ocfEnterTextTextInput")
                user_id_input.wait_for(timeout=5000)  # 5秒間待つ
                if user_id_input.is_visible():
                    user_id_input.fill(self._id)
                    page.get_by_test_id("ocfEnterTextNextButton").click()
            except:
                # 確認がない場合はpass
                pass
            # capture.run(page)

            password_input = page.get_by_label("Password", exact=True)
            password_input.wait_for(timeout=5000)
            password_input.fill(self.passwd)
            page.get_by_test_id("LoginForm_Login_Button").click()
            # capture.run(page)

            # get twitter links
            raw_urls = self.feed_url_handler.get()
            # Twitter linkを取得

            raw_urls = random.sample(raw_urls, min(4, len(raw_urls)))  # ランダムに4人選ぶ
            for link in raw_urls:
                # userを取り出し
                user = urlparse(link).path.split("/")[1]

                try:
                    page.goto(f"https://twitter.com/{user}/media/")
                except PlaywrightError as e:
                    print(f"Error: {e}")
                    continue
                # capture.run(page)

                # ページによってはこれをクリックする必要がある
                try:
                    confirm_sensitive = page.get_by_test_id("empty_state_button_text")
                    confirm_sensitive.wait_for(timeout=5000)  # 5秒間待つ
                    if confirm_sensitive.is_visible():
                        page.get_by_test_id("empty_state_button_text").click()
                    # capture.run(page)
                except:
                    # 確認がない場合はpass
                    pass

                # htmlファイルを取得
                html_content = page.content()
                # capture.run(page)

                # パターンに従うurlを取得
                image_urls = []
                img_url_pattern = r"https://pbs\.twimg\.com/media/\w+\?format=\w+"
                img_urls = re.findall(img_url_pattern, html_content)
                image_urls.extend(img_urls)
                print(image_urls)

                # 原寸画像のurlへ変換
                image_urls = [f"{s}&name=orig" for s in image_urls]

                # feed追加
                for image_url in image_urls:
                    # titleの生成
                    pattern = r"/media/(\w+)\?"
                    match = re.search(pattern, image_url)

                    if match:
                        extracted_string = match.group(1)
                        print(extracted_string)
                    else:
                        print("No match found")

                    img_link = image_url
                    title = f"{user}-{str(uuid.uuid4())[:8]}"
                    description = user

                    # add feed
                    enclosure = feedgenerator.Enclosure(
                        url=img_link, length="0", mime_type="image/jpg"
                    )

                    feeds.add_item(
                        title=title,
                        link=img_link,
                        description=description,
                        enclosure=enclosure,
                    )
        self.output(feeds)

    def output(self, feeds):
        with open(self.output_path, "w") as f:
            f.write(feeds.writeString("utf-8"))
        tree = ET.parse(self.output_path)
        ET.indent(tree, space="    ")
        tree.write(
            self.output_path,
            encoding="utf-8",
            xml_declaration=True,
        )
