import time
import json
import pprint

from functools import wraps
from typing import List, Tuple, Dict
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time() - start_time
        print(f"Function <{func.__name__}> work: {round(end_time, 2)}")
        return result
    return wrapper


def remove_url_params(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"
    return base_url


def save_to_json(data, filename):
    with open(filename, mode="w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def parse_company_links(driver) -> List[str]:
    all_links_company_in_page = []
    links = driver.find_elements(
        By.CSS_SELECTOR, ".company_logotype.directory_profile"
        )
    for link in links:
        all_links_company_in_page.append(link.get_attribute("href"))
    return all_links_company_in_page


def webdriver_scrapy_links(service: Service, url: str) -> Tuple[
        int, int, List[str]]:
    count_pages = 0
    count_company = 0

    with webdriver.Chrome(service=service) as driver:

        driver.get(url)

        wait = WebDriverWait(driver, 40)

        try:
            cookie_dialog = wait.until(
                EC.presence_of_element_located((
                    By.ID, "CybotCookiebotDialogBodyButtons"))
                )
            accept_button = cookie_dialog.find_element(
                By.ID, "CybotCookiebotDialogBodyButtonAccept"
                )
            accept_button.click()
        except TimeoutException:
            pass

        wait.until(
            EC.presence_of_element_located((
                By.CLASS_NAME, "directory-list"
            )))

        all_links = parse_company_links(driver)
        count_pages += 1
        count_company += len(all_links)

        driver.quit()

    return count_pages, count_company, all_links


@timer_decorator
def scrapy_links(url: str, service: Service, pages: int, filename: str) \
        -> Tuple[int, int]:
    count_pages, count_company_link = 0, 0

    all_links = []
    for i in range(pages):
        if i == 0:
            count_p, count_c_l, all_page_links = webdriver_scrapy_links(
                service, url)
        else:
            new_url = url + f"?page={i}"
            count_p, count_c_l, all_page_links = webdriver_scrapy_links(
                service, new_url)

        count_pages += count_p
        count_company_link += count_c_l
        all_links.append(all_page_links)

    save_to_json(all_links, filename)

    return count_pages, count_company_link


def read_links_with_json(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        data = json.load(file)
        for links_list in data:
            yield links_list


def scrape_metrics(driver):
    metrics_block = driver.find_element(
        By.CLASS_NAME, "profile-metrics")

    average_rating_element = metrics_block.find_element(
        By.CSS_SELECTOR, "[name='metrics-average-review-rating']")

    average_rating = average_rating_element.find_element(
        By.CLASS_NAME, "sg-rating__number").text

    total_reviews_element = metrics_block.find_element(
        By.CSS_SELECTOR, "[name='metrics-total-reviews']")

    total_reviews = total_reviews_element.find_element(
        By.CLASS_NAME, "sg-colored-card--accent").text

    common_project_size_element = metrics_block.find_element(
        By.XPATH,
        "//dt[contains(text(), 'Most Common Project Size')]\
            /following-sibling::dd")

    common_project_size = common_project_size_element.find_element(
        By.CLASS_NAME, "default").text

    average_referral_rating_element = metrics_block.find_element(
        By.XPATH,
        "//dt[contains(text(), 'Average Referral Rating')]\
            /following-sibling::dd")

    average_referral_rating = average_referral_rating_element.find_element(
        By.CLASS_NAME, "sg-colored-card--accent").text

    return {
        "Average Review Rating": average_rating,
        "Total Reviews": total_reviews,
        "Most Common Project Size": common_project_size,
        "Average Referral Rating": average_referral_rating
    }


def scrape_locations(driver):
    locations_list = []

    locations = driver.find_elements(By.CLASS_NAME, "profile-locations--item")

    for location in locations:
        location_name_element = location.find_element(
            By.CLASS_NAME, "location-button")
        location_name = location_name_element.text.strip()

        try:
            address_element = WebDriverWait(location, 10).until(
                EC.visibility_of_element_located((
                    By.CSS_SELECTOR, "address.detailed-address"))
            )
        except TimeoutException:
            # Handle the TimeoutException and continue to the next location
            continue

        street_address = address_element.find_element(
            By.CSS_SELECTOR, "span[itemprop='streetAddress']").text.strip()

        # Use try-except to handle NoSuchElementException
        try:
            locality = address_element.find_element(
                By.CSS_SELECTOR,
                "span[itemprop='addressLocality']").text.strip()
        except NoSuchElementException:
            locality = ""
        try:
            region = address_element.find_element(
                By.CSS_SELECTOR,
                "span[itemprop='addressRegion']").text.strip()
        except NoSuchElementException:
            region = ""
        try:
            country = address_element.find_element(
                By.CSS_SELECTOR,
                "span[itemprop='addressCountry']").text.strip()
        except NoSuchElementException:
            country = ""
        try:
            postal_code = address_element.find_element(
                By.CSS_SELECTOR, "span[itemprop='postalCode']").text.strip()
        except NoSuchElementException:
            postal_code = ""
        try:
            telephone_element = location.find_element(
                By.CSS_SELECTOR, "a.tel.location_element")
            telephone = telephone_element.text.strip()
        except NoSuchElementException:
            telephone = ""

        location_data = {
            "Location Name": location_name,
            "Street Address": street_address,
            "Locality": locality,
            "Region": region,
            "Country": country,
            "Postal Code": postal_code,
            "Telephone": telephone
        }

        locations_list.append(location_data)

    return locations_list


def scrape_chart_legend(driver):
    chart_legend = driver.find_element(By.CLASS_NAME, "chart-legend")

    chart_legend_title = chart_legend.find_element(
        By.CLASS_NAME, "chart-legend--title").text

    chart_legend_items = chart_legend.find_elements(
        By.CLASS_NAME, "chart-legend--item")

    data = {
        chart_legend_title: []
    }

    for chart_legend_item in chart_legend_items:
        item_data = {}
        item_data["Service Line"] = chart_legend_item.text.split("\n")[0]
        item_data["Percentage"] = chart_legend_item.find_element(
            By.TAG_NAME, "span").text
        data[f"{chart_legend_title}"].append(item_data)

    return data


def webdriver_scrapy_company(service: Service, url: str) -> Tuple[Dict, int]:

    with webdriver.Chrome(service=service) as driver:

        driver.get(url)

        wait = WebDriverWait(driver, 40)

        try:
            cookie_dialog = wait.until(
                EC.presence_of_element_located((
                    By.ID, "CybotCookiebotDialogBodyButtons"))
                )
            accept_button = cookie_dialog.find_element(
                By.ID, "CybotCookiebotDialogBodyButtonAccept"
                )
            accept_button.click()
        except TimeoutException:
            pass

        element_name_and_link = driver.find_element(
            By.XPATH, "//a[@class='website-link__item']")
        company_name = element_name_and_link.text.strip()
        company_link = element_name_and_link.get_attribute("href")
        company_website = remove_url_params(company_link)

        details_list = []

        details = driver.find_elements(
            By.XPATH, "//ul[@class='profile-summary__details']\
                /li[contains(@class, 'sg-text')]"
        )
        for detail in details:
            try:
                title_element = detail.find_element(
                    By.CLASS_NAME, "sg-text__title")
                title = title_element.text.strip()
            except NoSuchElementException:
                pass
            else:
                details_list.append(title)

        social_media_block = driver.find_element(
            By.CLASS_NAME, "profile-summary__social")
        social_media_links = social_media_block.find_elements(
            By.CLASS_NAME, "sg-social-media--link")

        social_media = []

        for link in social_media_links:
            url = link.get_attribute("href")
            social_media.append(url)

        data_metrics = scrape_metrics(driver)
        lovations = scrape_locations(driver)
        legend = scrape_chart_legend(driver)

        data = {
            "company_name": company_name,
            "information": {
                "website": company_website,
                "details": details_list,
                "social_media": social_media,
                "metrics": data_metrics,
                "locations": lovations,
                "legend": legend,
            }
        }

        driver.quit()

    return data


@timer_decorator
def scrapy_company(service: Service, filename: str):
    all_data = {
        "count_company": 0,
        "company": []}

    for data in read_links_with_json(filename):
        for link in data:
            data = webdriver_scrapy_company(service, link)
            all_data["company"].append(data)
            all_data["count_company"] += 1

    return all_data


@timer_decorator
def main():
    url = "https://clutch.co/it-services"
    service = Service("chromedriver_mac/chromedriver")
    pages = 50
    filename_links = "company_links.json"
    filename_company = "company_data.json"

    # сount_pages, count_company_link = scrapy_links(
    #     url, service, pages, filename_links
    #     )
    # print(f"Scraped all links. Total pages: {сount_pages}.\
    #         Total company links: {count_company_link}")

    company_data = scrapy_company(service, filename_links)
    save_to_json(company_data, filename_company)


if __name__ == "__main__":
    main()
