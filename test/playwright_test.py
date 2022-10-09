import os
import time
from urllib.parse import *

from playwright.sync_api import sync_playwright as playwright
from playwright.sync_api._generated import Response, Request, Page, Browser, BrowserContext


def run(pw):
    browser = pw.chromium.launch(headless=False)
    page = browser.new_page()
    # Subscribe to "request" and "response" events.
    add_page_listener(page)
    # page.goto("http://shuqi.demo.dtwave.com")
    page.goto("https://example.com")
    for i in range(240):
        time.sleep(5)
        add_browser_listener(browser)
    browser.close()


def add_page_listener(page: Page):
    print('add listener to page:', page.title())
    page.on("request", handle_request)
    page.on("response", handle_response)


def add_browser_listener(browser: Browser):
    contexts = browser.contexts
    for ctx in contexts:
        add_context_listener(ctx)


def add_context_listener(context: BrowserContext):
    pages = context.pages
    for page in pages:
        add_page_listener(page)


def handle_request(request: Request):
    print(">>", request.method, request.url)


def handle_response(response: Response):
    if 'content-type' not in response.headers:
        print(response.url, ' no content-type')
        return
    content_type = response.headers['content-type']
    print("<<", response.status, '(', content_type, ')', response.url)
    content = response.body()
    result = urlparse(response.url)
    print(result)
    path = "./" + result.netloc
    file_name = result.path if result.path != "/" else "/index.html"
    file_path = path + file_name  # + '?' + result.query
    mkdir(file_path)
    if ('text/' in content_type) or ('javascript' in content_type):
        download(file_path, str(content, encoding='utf8'))
    elif 'image/' in content_type:
        download_bytes(file_path, content)
    elif 'octet-stream' in content_type:
        download_bytes(file_path, content)
    else:
        print("Unknown content_type:" + content_type)


def download(file_path: str, content: str):
    with open(file_path, encoding='utf8', mode="w") as f:
        f.write(content)


def download_bytes(file_path: str, content: bytes):
    with open(file_path, mode="wb") as f:
        f.write(content)


def mkdir(file_path: str):
    try:
        os.makedirs(file_path[:file_path.rindex('/')])
    except Exception as e:
        pass


if __name__ == "__main__":
    with playwright() as pw:
        run(pw)
