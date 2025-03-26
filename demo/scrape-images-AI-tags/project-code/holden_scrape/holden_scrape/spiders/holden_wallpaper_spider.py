from scrapy.http import Response, Request
from scrapy.selector import SelectorList, Selector
from scrapy.linkextractors import LinkExtractor
from typing import List

import scrapy


class HoldenWallpaperSpider(scrapy.Spider):
    name = "holden_wallpaper"
    start_urls = [
        "https://holdendecor.co.uk/"
    ]
    # Define allowed URL prefixes to follow
    allowed_prefixes = [
        'https://holdendecor.co.uk/collections/',
        'https://holdendecor.co.uk/products/',
        'https://holdendecor.co.uk/style/'
        'https://holdendecor.co.uk/colour/'
        'https://holdendecor.co.uk/material/'
    ]
    
    # Set a maximum depth for crawling (optional)
    max_depth = 4
    
    def parse(self, response: Response):
        # Find all elements with src attributes ending with .jpg
        jpg_elements: SelectorList[Selector] = response.css('[src$=".jpg"]')
        for element in jpg_elements:
            yield {
                "image_urls": [element.attrib["src"]],  # Must be a list named 'image_urls'
                "alt": element.attrib.get("alt", element.css("::text").get()),
                "url": response.url,
            }
        for link in self.queue_next_urls(response):
            yield link

    def queue_next_urls(self, response: Response) -> List[Request]:
        # Extract links from the page
        links = LinkExtractor().extract_links(response)
        
        # Get current depth from meta or default to 1
        current_depth = response.meta.get('depth', 1)
        links_to_scrape = []
        # Only follow links if we haven't reached max depth
        if current_depth <= self.max_depth:
            for link in links:
                # Check if the link URL starts with any of our allowed prefixes
                if any(link.url.startswith(prefix) for prefix in self.allowed_prefixes):
                    # Follow the link and parse it
                    links_to_scrape.append(scrapy.Request(
                        url=link.url,
                        callback=self.parse,
                        meta={'depth': current_depth + 1}
                    ))
        return links_to_scrape