from urllib.parse import urljoin

from bs4 import BeautifulSoup
from dask.bytes.tests.test_http import requests


def get_monthly_event_pages(
    events_url="http://www.nuforc.org/webreports/ndxevent.html",
):
    page = requests.get(events_url)
    soup = BeautifulSoup(page.text, "html.parser")
    monthly_event_pages = [
        urljoin("http://www.nuforc.org/webreports/", x["href"])
        for x in list(soup.find_all("a", href=True))[1:-1]
    ]
    return monthly_event_pages


def scrape_monthly_event_page(url):
    keys = ["datetime", "city", "state", "shape", "duration", "summary", "posted"]

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    monthly_event_tags = soup.find_all("tr")[1:]
    monthly_event_list = [
        dict(zip(keys, tag.text.split("\n")[1:-1])) for tag in monthly_event_tags
    ]

    return monthly_event_list
