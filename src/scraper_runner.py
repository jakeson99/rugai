from loguru import logger

from scraper.simple_scraper import download_images, scrape_img_src


@logger.catch
def main():
    download_images(image_urls=scrape_img_src())


if __name__ == "__main__":
    main()
