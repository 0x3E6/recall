import asyncio
import os
from urllib.parse import *

from pyppeteer import launch
from pyppeteer.network_manager import Request, Response

"""
[INFO] Chromium extracted to: /root/.local/share/pyppeteer/local-chromium/588429
┌──(root㉿kali)-[~/…/pyppeteer/local-chromium/588429/chrome-linux]
└─# ./chrome 
[39994:39994:1008/111108.588806:ERROR:zygote_host_impl_linux.cc(89)] Running as root without --no-sandbox is not supported. See https://crbug.com/638180.
"""


async def main():
    params = {'headless': False, 'appMode': True, 'args': ["--no-sandbox"]}
    # export CHROME_PATH=/opt/google/chrome/chrome
    chrome_path = os.getenv("CHROME_PATH")
    if chrome_path != "":
        print(chrome_path)
        params['executablePath'] = chrome_path
    browser = await launch(params)
    page = await browser.newPage()
    # await page.setRequestInterception(True)

    @page.on("request")
    def request_handler(request: Request):
        print(">>>>>> " + request.method + " " + request.url)
        # await request.continue_()

    @page.on("response")
    async def response_handler(response: Response):
        content_type = response.headers['content-type']
        result = urlparse(response.url)
        ### error
        content = await response.text()
        if content is None:
            print("Content None")
            return
        print("content " + content)
        print("mkdir " + result.netloc)
        os.mkdir(result.netloc)
        path = "./" + result.netloc + "/"
        file_name = result.path if result.path != "/" else "index.html"
        file_path = path + file_name
        if 'text/html' in content_type:
            print(content_type)
            download(file_path, content)
        else:
            print("Unknown content_type:" + content_type)

    await page.goto('https://example.com')
    await page.screenshot({'path': 'example.png'})
    await browser.close()


def download(file_path: str, content: str):
    with open(file_path, encoding='utf8', mode="w") as f:
        f.write(content)
        print("Saved " + file_path)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
