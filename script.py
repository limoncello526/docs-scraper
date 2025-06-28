import asyncio

from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig, LXMLWebScrapingStrategy, \
    FilterChain, DomainFilter, BestFirstCrawlingStrategy
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.async_configs import BrowserConfig

async def scrape_page(start_url):
    visited_urls = set()  # Initialize visited URLs for this session
    filter_chain = FilterChain([
        # Only crawl specific domains
        DomainFilter(
            allowed_domains=["docs.healthsafepay.com"],
            blocked_domains=["dev-wallet.healthsafepay.com", "stg-wallet.healthsafepay.com", "wallet.healthsafepay.com",
                             "walletstage.healthsafepay.com", "walletprod.healthsafepay.com"]
        )
    ])

    browser_cfg = BrowserConfig(headless=True)
    config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator(),
        deep_crawl_strategy=BestFirstCrawlingStrategy(
            max_depth=100,
            filter_chain=filter_chain,
            include_external=False,
        ),
        target_elements=[".theme-doc-markdown"],  # Specify elements to scrape
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True,
        scan_full_page=True
    )

    async with AsyncWebCrawler(config=browser_cfg, verbose=True) as crawler:
        results = await crawler.arun(
            url=start_url,
            session_id="site_crawl_session",
            config=config,
            cache_mode=CacheMode.BYPASS
        )

        all_markdown = ""
        for result in results:  # Iterate over all pages
            url = result.url.rstrip('/') if result.url.endswith('/') else result.url
            if url not in visited_urls:
                visited_urls.add(url)
                if result.success:
                    all_markdown += result.markdown + "\n\n"
                else:
                    print(f"Failed to load page: {result.url}")
            else:
                print(f"Page already crawled: {result.url}")

        if all_markdown:
            print(all_markdown)
        else:
            print("Failed to scrape any pages.")

if __name__ == '__main__':
    asyncio.run(scrape_page("https://docs.healthsafepay.com"))