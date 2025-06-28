import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig, LXMLWebScrapingStrategy, BFSDeepCrawlStrategy, \
    FilterChain, DomainFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

visited_urls = set()

async def scrape_page(start_url):
    global visited_urls
    filter_chain = FilterChain([
        # Only crawl specific domains
        DomainFilter(
            allowed_domains=["docs.healthsafepay.com"],
            blocked_domains=["dev-wallet.healthsafepay.com", "stg-wallet.healthsafepay.com", "wallet.healthsafepay.com",
                             "walletstage.healthsafepay.com", "walletprod.healthsafepay.com"]
        )
    ])
    config = CrawlerRunConfig(
        # wait_for="css:.theme-doc-markdown",
        markdown_generator=DefaultMarkdownGenerator(),
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=50,  # Increase depth for deeper crawling
            include_external=False,  # Include external links
            filter_chain=filter_chain
        ),
        target_elements=[".theme-doc-markdown"],  # Specify elements to scrape
        excluded_tags=["nav", "footer"],  # Exclude unnecessary tags
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True
    )

    async with AsyncWebCrawler(headless=True, verbose=True) as crawler:
        results = await crawler.arun(
            url=start_url,
            session_id="site_crawl_session",
            config=config,
            cache_mode=CacheMode.BYPASS
        )

        all_markdown = ""
        for result in results:  # Iterate over all pages
            if result.url not in visited_urls:
                visited_urls.add(result.url)
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


async def scrape_list_of_urls(urls):
    if isinstance(urls, list):
        for url in urls:
            if url not in visited_urls:
                await scrape_page(url)
            else:
                print(f"Skipping already visited URL: {url}")
    else:
        print("Input should be a list of URLs.")


if __name__ == '__main__':
    asyncio.run(scrape_list_of_urls(["https://docs.healthsafepay.com/docs/overview",
"https://docs.healthsafepay.com/docs/category/business",
"https://docs.healthsafepay.com/docs/category/developers",
"https://docs.healthsafepay.com/docs/developers/Getting-Started",
"https://docs.healthsafepay.com/docs/developers/onboarding/register-with-hcp",
"https://docs.healthsafepay.com/docs/developers/onboarding/stripe-configuration",
"https://docs.healthsafepay.com/docs/developers/onboarding/express-checkout-with-digital-wallet",
"https://docs.healthsafepay.com/docs/developers/Core-Capabilities",
"https://docs.healthsafepay.com/docs/developers/Core-Capabilities/Manage%20Wallet",
"https://docs.healthsafepay.com/docs/developers/Core-Capabilities/Manage%20Wallet/Adding%20Payment%20Method",
"https://docs.healthsafepay.com/docs/developers/Core-Capabilities/Manage%20Wallet/Update%20Payment%20Method",
"https://docs.healthsafepay.com/docs/developers/Core-Capabilities/Manage%20Wallet/Delete%20Payment%20Method",
"https://docs.healthsafepay.com/docs/developers/Core-Capabilities/Payments",
"https://docs.healthsafepay.com/docs/developers/Core-Capabilities/Payments/Payment-modes",
"https://docs.healthsafepay.com/docs/developers/Core-Capabilities/Payments/Pre-Auth%20Transactions",
"https://docs.healthsafepay.com/docs/developers/Core-Capabilities/Payments/Partial-Authorization",
"https://docs.healthsafepay.com/docs/developers/Core-Capabilities/Payments/sale-transactions",
"https://docs.healthsafepay.com/docs/developers/Core-Capabilities/Payment-Methods/Payment-Methods-types",
"https://docs.healthsafepay.com/docs/developers/Core-Capabilities/Payment-Methods/Payment-Methods-types/Card",
"https://docs.healthsafepay.com/docs/developers/Core-Capabilities/Payment-Methods/Payment-Methods-types/Card/default%20card",
"https://docs.healthsafepay.com/docs/developers/Core-Capabilities/Payment-Methods/Payment-Methods-types/Card/manufacturer-card",
"https://docs.healthsafepay.com/docs/developers/Core-Capabilities/Payment-Methods/Payment%20Method%20Channels",
"https://docs.healthsafepay.com/docs/developers/Core-Capabilities/Payment-Methods/Payment%20Method%20Channels/on-screen-entry",
"https://docs.healthsafepay.com/docs/developers/Core-Capabilities/Payment-Methods/Payment%20Method%20Channels/text-channel",
"https://docs.healthsafepay.com/docs/developers/Core-Capabilities/Payment-Methods/Payment%20Method%20Channels/email-channel",
"https://docs.healthsafepay.com/docs/developers/Core-Capabilities/Payment-Methods/Payment%20Method%20Channels/ws2",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-ui/Known-Issues",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-ui/Languages",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-ui/widget-translation",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-ui/widget-translation/child-session-translation",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-ui/Widget-Experience/Guest-vs-Wallet-Experience",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-ui/Widget-Experience/Embedded%20Experience",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-ui/Widget-Experience/Widget-Modes",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-ui/widget-capabilities",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-ui/widget-capabilities/payment-method-selector",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-ui/Integration/Integration-Options/Hosted-Experience",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-ui/Integration/Integration-Options/Embedded-Experience",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-ui/Integration/Integration-Options/TypeScript-Support",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-ui/Integration",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api/sessions",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api/sessions/create-session-request-response",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api/sessions/poll%20get%20sessions",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api/sessions/error_codes",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api/Payment-Methods",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api/Payment-Methods/set-up-payment-method",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api/Payment-Methods/find%20payment%20methods",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api/Payment-Methods/update%20payment%20method",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api/Payment-Methods/delete%20payment%20method",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api/Payment-Methods/error_codes",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api/Payments",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api/Payments/make%20a%20payment%20via%20UI",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api/Payments/payment-api",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api/Payments/Managing-MerchantTransactionId",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api/Payments/One%20time%20pay",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api/Payments/Pay%20and%20Save",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api/Payments/Agent%20assisted%20payments",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api/Payments/Refunds",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api/Payments/error_codes",
"https://docs.healthsafepay.com/docs/developers/convenient-checkout-api/API-Terminology",
"https://docs.healthsafepay.com/docs/developers/Add-on-services/Webhooks",
"https://docs.healthsafepay.com/docs/developers/Add-on-services/Webhooks/Configuration",
"https://docs.healthsafepay.com/docs/developers/Add-on-services/Webhooks/Payments",
"https://docs.healthsafepay.com/docs/developers/Add-on-services/Webhooks/Payment%20Methods",
"https://docs.healthsafepay.com/docs/developers/Add-on-services/Webhooks/Refunds",
"https://docs.healthsafepay.com/docs/developers/Add-on-services/Webhooks/Disputes",
"https://docs.healthsafepay.com/docs/developers/Add-on-services/Webhooks/Partial%20Authorization",
"https://docs.healthsafepay.com/docs/developers/Add-on-services/Reports/introduction",
"https://docs.healthsafepay.com/docs/developers/Add-on-services/Reports/ECG-SetUp",
"https://docs.healthsafepay.com/docs/developers/Add-on-services/Reports/Merchant-payout",
"https://docs.healthsafepay.com/docs/developers/Add-on-services/Reports/Combined%20Report",
"https://docs.healthsafepay.com/docs/developers/Add-on-services/Reports/Transaction-level-fee-report",
"https://docs.healthsafepay.com/docs/developers/Add-on-services/Reports/Report%20metadata",
"https://docs.healthsafepay.com/docs/developers/Customer-migration/Migration",
"https://docs.healthsafepay.com/docs/developers/Customer-migration/Extract",
"https://docs.healthsafepay.com/docs/developers/Special%20Use%20Cases/Payment%20Methods/Add-Duplicate-Payment-Method",
"https://docs.healthsafepay.com/docs/developers/Special%20Use%20Cases/Payment%20Methods/Replace-Payment-Method",
"https://docs.healthsafepay.com/docs/developers/Special%20Use%20Cases/Payments/Retry-Logic-for-Payment-And-Payment-Method-Entry",
"https://docs.healthsafepay.com/docs/developers/Special%20Use%20Cases/Payments/payments",
"https://docs.healthsafepay.com/docs/developers/Special%20Use%20Cases/Payments/Unusual%20payments%20failiure",
"https://docs.healthsafepay.com/docs/developers/Testing/Performance-Testing-Baseline",
"https://docs.healthsafepay.com/docs/developers/Testing/Testing",
"https://docs.healthsafepay.com/docs/developers/Trouble-Shooting/firewall-restrictions",
"https://docs.healthsafepay.com/docs/developers/Admin",
"https://docs.healthsafepay.com/docs/onboarding/Merchant-Onboarding",
"https://docs.healthsafepay.com/docs/ideas"]))
