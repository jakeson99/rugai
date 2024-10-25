from loguru import logger

from config.config import settings
from scraper.selenium_scraper import scrape_img_src_selenium
from scraper.simple_scraper import download_images, scrape_img_src


@logger.catch
def main():
    if settings.use_selenium:
        download_images(image_urls=scrape_img_src_selenium())

    else:
        download_images(image_urls=scrape_img_src())


if __name__ == "__main__":
    main()
