# Holden Wallpaper Scraper
- Scrape The Wallpapers from [Holden Decor](https://holdendecor.co.uk/)
- Use AI to tags each wallpaper (dogs, plants, cars, what main colour?, etc.)

## Quick Start
- Install dependencies: `uv sync`
- Run the spider: 
```bash
cd holden_scrape
uv run scrapy crawl holden_wallpaper -O scrape_info.json
```
- To apply tags to the downloaded wallpapers, run the notebook: `project-code/image_tagging/test_tagging.ipynb`
- To generate a report (that will become the image filter on Google Sheets), run the notebook: `project-code/combine_data/show.ipynb`