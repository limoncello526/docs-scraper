import asyncio
import datetime
import os

from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig, LXMLWebScrapingStrategy, \
    FilterChain, DomainFilter, BestFirstCrawlingStrategy
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.async_configs import BrowserConfig

async def scrape_page(start_url):
    visited_urls = set()  # Initialize visited URLs for this session
    filter_chain = FilterChain([
        # Only crawl specific domains
        DomainFilter(
            allowed_domains=["docs.healthsafepay.com", "developers.healthsafepay.com"],
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
            session_id=f"site_crawl_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
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
            os.makedirs("markdown_files", exist_ok=True)
            filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            relative_path = f"markdown_files/docs-{filename}.md"
            with open(relative_path, "w", encoding="utf-8") as file:
                file.write(all_markdown)
        else:
            print("Failed to scrape any pages.")

def load_and_split_markdown_files():
    from langchain.document_loaders import UnstructuredMarkdownLoader
    from langchain.text_splitter import MarkdownHeaderTextSplitter
    import glob
    import os

    md_folder = os.path.join(os.path.dirname(__file__), "markdown_files")
    md_files = glob.glob(os.path.join(md_folder, "*.md"))

    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "Header 1"), ("##", "Header 2")]
    )

    for md_file in md_files:
        print(f"Processing: {md_file}")
        loader = UnstructuredMarkdownLoader(md_file)
        docs = loader.load()
        for doc in docs:
            chunks = header_splitter.split_text(doc.page_content)
            for i, chunk in enumerate(chunks):
                print(f"Chunk {i+1} from {md_file}:")
                print(chunk)
                print("-"*40)

if __name__ == '__main__':
    asyncio.run(scrape_page("https://developers.healthsafepay.com"))
    load_and_split_markdown_files()
