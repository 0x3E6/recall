const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({headless:false, args:['--no-sandbox'], appMode: true});
  const page = await browser.newPage();
  await page.setRequestInterception(true);
  page.on('request', interceptedRequest => {
    if (interceptedRequest.isInterceptResolutionHandled()) return;
    if (
      interceptedRequest.url().endsWith('.png') ||
      interceptedRequest.url().endsWith('.jpg')
    )
      interceptedRequest.abort();
    else interceptedRequest.continue();
  });
  await page.goto('https://example.com');
  await page.screenshot()
  await browser.close();
})();