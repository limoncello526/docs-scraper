import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

async def scrape_docs(name):
    js_code = [
        f"""
        const nextButton = Array.from(document.querySelectorAll(
            '.theme-doc-sidebar-item-category .theme-doc-sidebar-item-category-level-2 .menu__list-item'))
            .find(el => el.textContent === '{name}');
        nextButton && nextButton.click();
        """
    ]
    config = CrawlerRunConfig(
        wait_for="css:.theme-doc-markdown",
        markdown_generator=DefaultMarkdownGenerator()
    )

    async with AsyncWebCrawler(headless=True, verbose=True) as crawler:
        result = await crawler.arun(
            url="https://docs.healthsafepay.com/docs/developers/onboarding/express-checkout-with-digital-wallet/",
            session_id="my_session",
            js_code=js_code,
            js_only=True,
            config=config,
            cache_mode=CacheMode.BYPASS
        )

        if result.success:
            print(result.markdown)
        else:
            print("Failed to load the page or execute JavaScript.")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(scrape_docs('Express Checkout with Digital Wallets'))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
