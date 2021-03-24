import concurrent
import logging
import time
import random
from datetime import datetime
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from dask.bytes.tests.test_http import requests

logger = logging.getLogger(__name__)


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
    start_time = datetime.now()
    keys = ["datetime", "city", "state", "shape", "duration", "summary", "posted"]

    # Get the monthly page.
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    # Get tags of all events available from the monthly page. These contain basic event info and subpage link.
    event_tags = soup.find_all("tr")[1:]

    logger.info(f"scraping {len(event_tags)} events...")
    # Get events subpages. We need those for full event summaries.
    event_subpages_tags = soup.find_all("a", href=True)[1:]
    event_subpages = [
        urljoin("http://www.nuforc.org/webreports/", tag["href"])
        for tag in event_subpages_tags
    ]


    # XXX: Utilize 'ThreadPoolExecutor' utility to request event summaries in a multi-threaded approach.
    # This has proved to be much, much faster than requesting event summaries one by one.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for event in event_subpages:
            futures.append(
                executor.submit(
                    get_event_summary, event_page=event, return_event_page=True
                )
            )

    # Cast event summaries to a dictionary, with event subpage link as key and event summary as value.
    event_summaries = dict([future.result() for future in futures])

    """
    Create a nested, final dictionary, where:
    - keys are event subpages
    - values are dictionaries with basic info extracted from monthly page
    - 'summary' key value in the nested dictionary is replaced with full summary taken from event subpage
     (see event_summaries above)
    """
    events = dict.fromkeys(event_subpages)
    for i, event in enumerate(events):
        events[event] = dict(zip(keys, event_tags[i].text.split("\n")[1:-1]))
        events[event]["summary"] = event_summaries[event]

    logger.info(f"scraping finished in {datetime.now() - start_time}")

    return events


def get_event_summary(event_page, return_event_page=False):
    page = requests.get(event_page)
    soup = BeautifulSoup(page.text, "html.parser")
    try:
        tags = soup.find_all("tr")
        summary = str(tags[2].text.split("\n")[1])
    except:
        return "Unable to get summary"

    if return_event_page:
        return (event_page, summary)

    return summary
