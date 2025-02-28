import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from loguru import logger

from config.config import settings


def get_data(url: str):
    r = requests.get(url, timeout=120)
    return r.text


def scrape_img_src(
    url_string=settings.url_base_name,
    last_page=settings.url_pages,
    use_list=settings.use_list,
    url_list_file=settings.url_list_file,
) -> list:
    """Scrapes give url and subsequent pages to return img src https addresses.

    Args:
        url_string(str): Url that will be scraped for image src urls.
        last_page(int): Integer of last page that will be scraped.
        use_list(bool): If True the function will use a txt file of url strings
                        as input. If False the function will generate the url
                        strings using url_string and last_page.
        url_list_file(FilePath): Txt file containing the urls to scrape from.
                        each url is on a new line.

    Returns:
        image_list(list): list of image urls that were scraped from the pages.

    """
    logger.info("Starting image url scraping.")
    image_list = []

    if use_list:
        with open(url_list_file) as file:
            urls = file.readlines()
        urls = [url.strip() for url in urls]

        for url in urls:
            image_list.extend(get_img_urls(page_url_string=url))

    else:
        # get pages 1 to last_page
        for i in range(1, last_page + 1):
            page_url_string = f"{url_string}?page={i}"
            image_list.extend(get_img_urls(page_url_string=page_url_string))

    logger.info(f"{len(image_list)} image urls were found.")

    with open(f"{settings.save_dir}/images.txt", "w") as file:
        for item in image_list:
            file.write(f"{item}\n")

    return image_list


def get_img_urls(page_url_string: str) -> list:
    """For the given page_url_string find all instances of img[src]
    in the html code and add the https address to a list.

    Args:
        page_url_string: url string that wil be scraped.

    Returns:
        image_list(list): list of image https addresses.

    """  # noqa: D205
    image_list = []
    logger.info(f"Scraping image urls for: {page_url_string}")
    htmldata = get_data(page_url_string)
    soup = BeautifulSoup(htmldata, "html.parser")
    for item in soup.find_all("img"):
        if item["src"] != "":
            https_string = "".join(["https:", item["src"]])
            image_list.append(https_string)
    return image_list


def download_images(image_urls: list, save_dir=settings.save_dir) -> None:
    """Download given list of image urls to the specified save_dir."""
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    logger.info(f"Downloading images to {save_dir}")

    for url in image_urls:
        try:
            response = requests.get(url, timeout=90)
            response.raise_for_status()  # Check if request was successful
            # get filename from url
            file_name = url.split("/")[-1]
            file_path = os.path.join(save_dir, f"{file_name}.jpg")
            # save image to path and overwrite if it exists
            with open(file_path, "wb") as file:
                file.write(response.content)

            logger.debug(f"Successfully downloaded {url}")
        except Exception as e:  # noqa: BLE001, PERF203
            logger.warning(f"Failed to download {url}: {e}")

    logger.info("Finished downloading images.")
