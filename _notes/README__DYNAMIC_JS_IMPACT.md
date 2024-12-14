
### Impact of dynamic JS-based content, potential solutions:
```
Selenium:
 - Estimated Time Cost: High
 - Best Use Case: Full browser interaction and rendering JS-heavy pages.
 - Notes: Slower due to full browser overhead, especially for heavy pages

Playwright:
 - Estimated Time Cost: Moderate
 - Best Use Case: Headless browser, rendering JS-heavy pages.
 - Notes: Faster than Selenium with modern web apps.

Puppeteer:
 - Estimated Time Cost: Moderate
 - Best Use Case: Headless browser, rendering JS-heavy pages.
 - Notes: Faster than Selenium, close to Playwright in speed.

Requests-HTML:
 - Estimated Time Cost: Low to Moderate
 - Best Use Case: Static pages and light JS rendering.
 - Notes: rendering.	Best for non-dynamic pages, but slower than Playwright/Puppeteer.



I have checked cost of using requests-html (with Puppeteer) and it doesn't enough have sense in this scrapping solutions.
Also, new issue during renderring pages started to happen. Simply 'request'ing seems ok here.
```
