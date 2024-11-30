from __future__ import annotations

import asyncio

from pyppeteer import launch


async def download_chromium():
    browser = await launch()
    await browser.close()


asyncio.get_event_loop().run_until_complete(download_chromium())
