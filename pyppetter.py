# Importing Required Packages

import asyncio
from pyppeteer import launch
import pandas as pd

# Import CSV comprising list of URLs

csv = pd.read_csv('./pptr.csv')

async def main():
    browser = await launch()
    page = await browser.newPage()
    # Google Desktop Bot
    # await page.setUserAgent("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
    # Google Smartphone Bot
    await page.setUserAgent("Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.140 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
    
    # Setting up the Viewport
    await page.setViewport({'width': 414, 'height': 986})
    
    # Loop around to scrape all the URLs in CSV
    for i in range(len(csv['URL'])):
        url = csv['URL'][i]
        await page.goto(url)
        await page.screenshot({'path': 'Page#'+str(i+1)+".png", 'fullPage': True,})
    await browser.close()
asyncio.get_event_loop().run_until_complete(main())
