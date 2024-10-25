import time

from bs4 import BeautifulSoup
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config.config import settings


def scrape_img_src_selenium(
    url_list_file=settings.url_list_file, save_dir=settings.save_dir
):
    """Read page urls from the given list and return all image urls present
    on the page.
    """
    logger.info("Starting image url scraping using selenium.")
    image_list = []

    with open(url_list_file) as file:
        urls = file.readlines()
    urls = [url.strip() for url in urls]

    for url in urls:
        image_list.extend(get_img_urls_selenium(page_url_string=url))

    logger.info(f"{len(image_list)} image urls were found.")

    with open(f"{save_dir}/images.txt", "w") as file:
        for item in image_list:
            file.write(f"{item}\n")

    return image_list


def get_img_urls_selenium(page_url_string: str) -> list:
    """Use selenium to load and scroll to generate a list of image urls."""
    logger.info(f"Getting image urls for {page_url_string}")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    driver.get(page_url_string)
    time.sleep(3)

    scroll_pause_time = 2
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1

    while True:
        driver.execute_script(f"window.scrollTo(0, {screen_height}*{i});")
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if (screen_height * i) > scroll_height:
            break

    page = driver.page_source
    driver.quit()
    soup = BeautifulSoup(page, "html.parser")
    container = soup.find_all("div", class_="woocommerce-image__wrapper")
    image_list = []
    for div in container:
        img_tag = div.find("img")
        if img_tag:
            img_src = img_tag["src"]
            if img_src.endswith(".jpg"):
                image_list.append(img_src)
    logger.info(f"{len(image_list)} image urls found for {page_url_string}")
    return image_list
