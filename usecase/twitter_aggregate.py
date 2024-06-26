import base64
import os
import random
import re
import tempfile
import time
import uuid
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

import dropbox
import feedgenerator
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

from repository.interface.feed_urls import IFeedURLs
from usecase.interface.aggregate_feed import IAggregateFeed

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class Capture:
    def __init__(self) -> None:
        self.counter = 0

    def run(self, page):
        time.sleep(1)
        print(self.counter)
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
        self.N = 10  # number of user fetched

    @staticmethod
    def make_creds(creds_file, token_file):
        creds = None
        if os.path.exists(token_file.name):
            creds = Credentials.from_authorized_user_file(token_file.name, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    creds_file.name, SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_file.name, "w") as token:
                token.write(creds.to_json())

        return creds, creds_file, token_file

    @staticmethod
    def fill_form(page, field_type, value, timeout=5000) -> None:
        try:
            if field_type == "email":
                input_field = page.get_by_label("email")
            elif field_type == "username":
                input_field = page.get_by_label("phone or username")
            else:
                raise ValueError(f"Unknown field type: {field_type}")

            input_field.wait_for(timeout=timeout)
            input_field.fill(value)

            next_button = page.get_by_role("button", name="Next")
            next_button.wait_for(timeout=timeout)

            time.sleep(3)
            page.screenshot(path=f"./img/{field_type}_b.png")

            next_button.click()

            return True
        except PlaywrightTimeoutError:
            print(f"Timeout waiting for {field_type} field")
            return False

    def input_username_or_email(self, page, max_attempts=3):
        form_completed = False
        attempts = 0
        while not form_completed and attempts < max_attempts:
            time.sleep(3)
            try:
                if page.get_by_label("email").is_visible():
                    # page.screenshot(path=f"./img/email_a.png")
                    self.fill_form(page, "email", self.email)
                elif page.get_by_label("Phone or username").is_visible():
                    # page.screenshot(path=f"./img/username_a.png")
                    self.fill_form(page, "username", self._id)
                else:
                    form_completed = True
                    print("Form completion detected")
                    break
                attempts += 1
            except PlaywrightTimeoutError:
                print(f"Timeout on attempt {attempts}")
                break

    def input_password(self, page):
        time.sleep(3)
        # page.screenshot(path=f"./img/pass.png")
        password_input = page.get_by_label("Password", exact=True)
        password_input.wait_for(timeout=5000)
        password_input.fill(self.passwd)
        # page.screenshot(path=f"./img/pass_post.png")
        page.get_by_test_id("LoginForm_Login_Button").click()
        pass

    def input_otp(self, page):
        try:
            time.sleep(3)
            # page.screenshot(path=f"./img/otp.png")
            user_id_input = page.get_by_test_id("ocfEnterTextTextInput")
            user_id_input.wait_for(timeout=5000)  # 5秒間待つ
            if user_id_input.is_visible():
                time.sleep(30)
                otp = self.get_otp()
                user_id_input.fill(otp)
                page.get_by_test_id("ocfEnterTextNextButton").click()
        except:
            # 確認がない場合はpass
            pass

    @staticmethod
    def get_otp() -> str:
        dbx = dropbox.Dropbox(os.getenv("DBX_ACCESS_TOKEN"))

        # 一時ファイル生成
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as credential_file:
            # DL: creds
            md, res = dbx.files_download(f"/{os.getenv('GMAIL_CREDS_PATH')}")
            credential_file.write(res.content.decode("utf-8"))

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as token_file:
            # DL: token
            md, res = dbx.files_download(f"/{os.getenv('GMAIL_TOKEN_PATH')}")
            token_file.write(res.content.decode("utf-8"))

        creds, credential_file, token_file = make_creds(credential_file, token_file)

        # update: credential, token
        with open(credential_file.name, "rb") as f:
            data = f.read()
            mode = dropbox.files.WriteMode.overwrite
            dbx.files_upload(data, f"/{os.getenv('GMAIL_CREDS_PATH')}", mode)

        with open(token_file.name, "rb") as f:
            data = f.read()
            mode = dropbox.files.WriteMode.overwrite
            dbx.files_upload(data, f"/{os.getenv('GMAIL_TOKEN_PATH')}", mode)

        os.remove(credential_file.name)
        os.remove(token_file.name)

        try:
            # Call the Gmail API
            service = build("gmail", "v1", credentials=creds)
            sender = "info@x.com"
            query = f"from:{sender}"
            response = service.users().messages().list(userId="me", q=query).execute()
            messages = response.get("messages", [])

            for message in messages[:10]:
                msg = (
                    service.users()
                    .messages()
                    .get(userId="me", id=message["id"])
                    .execute()
                )

                payload = msg["payload"]
                if "parts" in payload:
                    parts = payload["parts"]
                    for part in parts:
                        if part["mimeType"] == "text/plain":
                            data = part["body"]["data"]
                            # base64 エンコードされた本文をデコード
                            raw_data = base64.urlsafe_b64decode(data).decode("utf-8")
                            # print(raw_data)
                            break
                else:
                    # メッセージに複数のパーツが含まれていない場合、直接本文を取得
                    data = payload["body"]["data"]
                    raw_data = base64.urlsafe_b64decode(data).decode("utf-8")
                    # print(raw_data)

                otp = raw_data.split("\n")[11].rstrip("\r")
                break

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")

        return otp

    def run(self) -> None:
        feeds = feedgenerator.Rss201rev2Feed(
            title=self.title,
            link=self.link,
            description=self.description,
        )

        with sync_playwright() as p:
            # ログイン処理
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto("https://x.com/i/flow/login")

            # input parameter username or/and email
            self.input_username_or_email(page)

            # input password
            self.input_password(page)

            # OTP
            self.input_otp(page)

            # get twitter links
            raw_urls = self.feed_url_handler.get()

            raw_urls = random.sample(raw_urls, min(self.N, len(raw_urls)))  # ランダムにN人選ぶ
            for link in raw_urls:
                # userを取り出し
                user = urlparse(link).path.split("/")[1]

                try:
                    page.goto(f"https://x.com/{user}/media/")
                except PlaywrightError as e:
                    print(f"Error: {e}")
                    continue
                time.sleep(3)
                page.screenshot(path=f"./img/{link}.png")

                # ページによってはこれをクリックする必要がある
                # try:
                #     confirm_sensitive = page.get_by_test_id("empty_state_button_text")
                #     confirm_sensitive.wait_for(timeout=5000)  # 5秒間待つ
                #     if confirm_sensitive.is_visible():
                #         page.get_by_test_id("empty_state_button_text").click()
                #     # capture.run(page)
                # except:
                #     # 確認がない場合はpass
                #     pass

                # htmlファイルを取得
                html_content = page.content()
                # capture.run(page)

                # パターンに従うurlを取得
                image_urls = []
                img_url_pattern = r"https://pbs\.twimg\.com/media/\w+\?format=\w+"
                img_urls = re.findall(img_url_pattern, html_content)
                image_urls.extend(img_urls)
                print(image_urls)

                # feed追加
                for image_url in image_urls:
                    # titleの生成
                    pattern = r"/media/(\w+)\?"
                    match = re.search(pattern, image_url)

                    title = None
                    if match:
                        extracted_string = match.group(1)
                        title = f"{user}-{extracted_string}"
                        print(extracted_string)
                    else:
                        title = f"{user}-{str(uuid.uuid4())[:8]}"
                        print("No match found")

                    # 原寸画像のurlへ変換
                    img_link = image_url + "&name=orig"
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
