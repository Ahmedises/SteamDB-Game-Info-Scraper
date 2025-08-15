import scrapy
from scrapy_playwright.page import PageMethod
from urllib.parse import urlencode, urljoin
from games.items import GamesItem

class DetailsSpider(scrapy.Spider):
    name = "details"
    handle_httpstatus_list = [403]
    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": False,
        },
        "PLAYWRIGHT_CONTEXTS": {
            "default": {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                "java_script_enabled": True,
                "locale": "en-US",
                "timezone_id": "America/New_York",
                "extra_http_headers": {
                    "Accept-Language": "en-US,en;q=0.9",
                },
            }
        }
    }

    def start_requests(self):
        url = "https://steamdb.info/instantsearch/"
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod('wait_for_selector', 'div.ais-Hits')
                ],
                errback=self.errback
            )
        )

    async def parse(self, response):
        page = response.meta['playwright_page']
        await page.wait_for_load_state(state='networkidle')

        details = await page.query_selector_all('li.ais-Hits-item')
        for detail in details:
            link_handle = await detail.query_selector('a')
            href = await link_handle.get_attribute('href') if link_handle else None
            if href:
                full_url = urljoin("https://steamdb.info", href)
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_details,
                    meta=dict(
                        playwright=True,
                        playwright_include_page=True,
                        playwright_page_methods=[
                            PageMethod('wait_for_load_state', 'networkidle')
                        ],
                        errback=self.errback
                    )
                )

        await page.close()

    async def parse_details(self, response):
        page = response.meta['playwright_page']
        await page.wait_for_load_state(state='networkidle')

        # استخراج البيانات المطلوبة من صفحة اللعبة
        game_name = await page.inner_text("h1")
        game_id = response.url.split('/')[-2] if '/app/' in response.url else None

        # أمثلة للـ selectors (ممكن نعدلها حسب HTML الفعلي للموقع)
        price = await self.safe_inner_text(page, ".price-tag")
        developer = await self.safe_inner_text(page, "table tr:has(td:contains('Developer')) td:nth-child(2)")
        publisher = await self.safe_inner_text(page, "table tr:has(td:contains('Publisher')) td:nth-child(2)")
        overall_reviews = await self.safe_inner_text(page, "table tr:has(td:contains('Reviews')) td:nth-child(2)")
        total_players = await self.safe_inner_text(page, "table tr:has(td:contains('Players')) td:nth-child(2)")
        rating = await self.safe_inner_text(page, "table tr:has(td:contains('Rating')) td:nth-child(2)")
        supported_systems = await self.safe_inner_text(page, "table tr:has(td:contains('Supported Systems')) td:nth-child(2)")
        technologies = await self.safe_inner_text(page, "table tr:has(td:contains('Technologies')) td:nth-child(2)")

        game_details = GamesItem()
        game_details['name'] = game_name
        game_details["id"] = game_id
        game_details["price"]= price
        game_details["developer"] = developer
        game_details["publisher"] = publisher
        game_details["overall_reviews"] = overall_reviews
        game_details["total_players"] = total_players
        game_details["rating"] = rating
        game_details["supported_systems"] = supported_systems
        game_details["technologies"] = technologies
        yield game_details

        
        await page.close()

    async def safe_inner_text(self, page, selector):
        """Helper function to safely get inner text from selector"""
        try:
            element = await page.query_selector(selector)
            if element:
                return (await element.inner_text()).strip()
        except:
            return None

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
