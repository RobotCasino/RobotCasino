#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright


async def navigate_to_youtube():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=['--no-sandbox', '--disable-setuid-sandbox'],
        )
        
        context = await browser.new_context()
        
        page = await context.new_page()
        
        print("Navigating to YouTube...")
        
        await page.goto("https://www.youtube.com")
        
        await page.wait_for_load_state("networkidle")
        
        title = await page.title()
        print(f"Page title: {title}")
        
        url = page.url
        print(f"Current URL: {url}")
        
        await page.screenshot(path="youtube_screenshot.png")
        print("Screenshot saved as 'youtube_screenshot.png'")
        
        print("Waiting 3 seconds before closing...")
        await asyncio.sleep(3)
        
        await browser.close()
        print("Browser closed successfully!")


def main():
    """Main function."""
    print("=" * 50)
    print("YouTube Browser Automation with Playwright")
    print("=" * 50)
    
    asyncio.run(navigate_to_youtube())
    
    print("=" * 50)
    print("Automation completed!")
    print("=" * 50)

class Robot:

    async def run(self, lol: str):
        print(lol)
        


if __name__ == "__main__":
    myrobot = Robot()

    myrobot.run("Hello from Robot class!")



