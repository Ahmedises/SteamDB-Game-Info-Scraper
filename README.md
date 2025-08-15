# SteamDB-Game-Info-Scraper
This project was built to scrape JavaScript-rendered pages from SteamDB and extract comprehensive game information, including titles, release dates, ratings, tags, and popularity trends. The collected data was intended for use in game market research and trend analysis.

SteamDB employs Cloudflare protection along with dynamic content loading, which made direct scraping challenging. To overcome this, I implemented Cloudflare bypass techniques combined with rotating proxies and custom HTTP headers to replicate real browser requests. This ensured stable, uninterrupted data collection over extended scraping sessions.

The scraper was implemented with Playwright for handling JavaScript rendering, then integrated into Scrapy-Playwright to benefit from Scrapy’s pipelining, item processing, and scalability. This hybrid approach allowed for high accuracy in data extraction while efficiently managing large-scale scraping tasks.

By combining rendering control, proxy rotation, and anti-bot evasion, the scraper consistently delivered structured, high-quality datasets despite SteamDB’s security measures.
