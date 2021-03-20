import json
import os
import re
import string
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import us
from iso3166 import countries
from lib.lookups import geography_lookups

paths = {"raw": r"data/raw_nuforc.csv"}


def get_state_name(x):
    try:
        x = str(us.states.lookup(x))
    except TypeError:
        x = np.nan
    return x


def search_country_name(name, lookup=geography_lookups.non_iso_3166_country_names):
    if type(name) == float:
        return None
    try:
        return lookup[name.lower()]
    except KeyError:
        try:
            return countries.get(name)[0]
        except KeyError:
            return None


def get_country(name):
    if type(name) == float:
        return None
    #   Case when full string corresponds with country name.
    if search_country_name_lookup(name) != None:
        return search_country_name_lookup(name)

    #   Case when string contains brackets and/or commas; then the partial string before first bracket and first comma
    #   is the country name.
    partial_name = name
    if "(" in name:
        partial_name = partial_name[: partial_name.index("(")].strip()
        if "(" in name and not name.endswith(")"):
            partial_name = partial_name + ")"
    if "," in name:
        partial_name = partial_name.split(",")[0]
    if partial_name != name:
        if search_country_name_lookup(partial_name) != None:
            return search_country_name_lookup(partial_name)

    #    Case when string contains country name in last bracket.
    try:
        # Regex returns all data in brackets.
        regex = re.compile(r"\((.*?)\)")
        mo = regex.findall(name)
        name_regex = mo[-1]
        #   If final bracket contains commas, take value after last comma.
        if "," in name_regex:
            name_regex = name_regex.split(",")[-1].strip()
        #       Remove punctuation except forward slash.
        name_regex = name_regex.translate(
            str.maketrans("", "", string.punctuation.replace("/", ""))
        )
        if search_country_name_lookup(name_regex) != None:
            return search_country_name_lookup(name_regex)
    except IndexError:
        return None


df = (
    pd.read_csv(paths["raw"])
    .reset_index()
    .rename(
        columns={
            "state": "state_abbrev",
            "city": "original_location",
            "shape": "original_shape",
            "duration": "original_duration",
        }
    )
)


def save_debugs(df):
    locations = df.copy()
    locations.sort_values(by="city", ascending=False)[
        ["original_location", "state_abbrev", "city", "state"]
    ].to_excel(Path("temp") / "locations.xlsx")


def extract_city(location):
    if type(location) == float:
        return None
    try:
        #       If name contains brackets, look at everything preceding brackets.
        regex = re.compile(r".+?(?=\()")
        mo = regex.findall(location)
        s = mo[0]
        if "/" in s:
            return s.split("/")[0]
        elif "," in s:
            return s.split(",")[0]
        else:
            return s
    except IndexError:
        #       If name doesn't contain brackets, take it as is and check if it's a country.
        if "/" in location:
            return location.split("/")[0]
        elif "," in location:
            return location.split(",")[0]
        elif search_country_name(location) is not None:
            return None
        else:
            return location


def get_state(state):
    if state == None:
        return None
    else:
        return state


#     try:
#         x = str(us.states.lookup(x))
#     except TypeError:
#         x = np.nan
#     return x


df["city"] = df["original_location"].apply(get_city)
df["state"] = df["state_abbrev"].apply(get_state)
