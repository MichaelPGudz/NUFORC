import logging
import logging.config
import random
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

import pandas as pd
import yaml

from model.modules.scraping import get_monthly_event_pages, scrape_monthly_event_page

with open("logging_conf.yaml", "r") as f:
    config_file = yaml.safe_load(f.read())
    logging.config.dictConfig(config_file)
logger = logging.getLogger("scraper")


def main():
    logger.info("Scraping started.")
    monthly_event_pages = get_monthly_event_pages()
    all_events = {}

    logger.info(f"Checking directory structure...")
    if not Path("data").exists():
        try:
            Path("data").mkdir(parents=True, exist_ok=True)
            logger.info("Output folder creation succeeded.")
        except Exception as e:
            logger.critical(
                "Couldn't create output folder. Aborting scraping.\n --- TRACEBACK ---"
            )
            traceback.print_exc()
            sys.exit(1)
    else:
        logger.info("Directory structure in place.")

    start_time = datetime.now()
    for i, url in enumerate(monthly_event_pages):
        logger.info(f"{i+1}/{len(monthly_event_pages)} - scraping monthly page @ {url}")
        events = scrape_monthly_event_page(url)
        all_events.update(events)

    pd.DataFrame(all_events).T.to_csv("data/raw_nuforc.csv")
    logger.info(f"Scraping finished.\nDuration: {datetime.now() - start_time}")

if __name__ == "__main__":
    main()