import re

import us
from iso3166 import countries
from model.lookups.geography_lookups import (
    can_province_names,
    non_iso_3166_country_names,
)


def extract_city(location):
    """

    Args:
        location:

    Returns:

    """
    if not isinstance(location, str):
        return None

    #   If location contains brackets, take the sequence before the first bracket.
    regex = re.compile(r".+?(?=\()")
    match = regex.search(location)
    if match is not None:
        match = match.group()
        if "/" in match:
            return match.split("/")[0]
        elif "," in match:
            return match.split(",")[0]
        else:
            return match

    #   If name doesn't contain brackets, take it as is and check if it's a country.
    if "/" in location:
        return location.split("/")[0]
    elif "," in location:
        return location.split(",")[0]
    elif search_country_name(location) is not None:
        return None
    else:
        return location


def get_state(state_abbrev, return_country=False):
    """

    Args:
        state_abbrev:
        return_country:

    Returns:

    """
    if not isinstance(state_abbrev, str):
        return None

    state = us.states.lookup(state_abbrev)
    if state is not None:
        if return_country == True:
            return (state, "USA")
        else:
            return state

    else:
        state = can_province_names.get(state_abbrev)
        if state is not None:
            if return_country == True:
                return (state, "Canada")
            else:
                return state


def extract_country(location, state=None):
    """

    Args:
        location:
        state:

    Returns:

    """
    if not isinstance(location, str):
        return None

    #   If a state of some country has been provided, try to return it.
    state = get_state(state, return_country=True)
    if state is not None:
        return state[1]

    #   If location contains brackets, take the sequence before the first bracket.
    regex = re.compile(r"\((.*?)\)")
    match = regex.findall(location)
    if match != []:
        match = match[-1]
        if "/" in match:
            return match.split("/")[0]
        elif "," in match:
            return match.split(",")[0]
        elif search_country_name(match) is not None:
            return search_country_name(match)

    return None


def search_country_name(name, lookup=non_iso_3166_country_names):
    """

    Args:
        name:
        lookup:

    Returns:

    """
    if not isinstance(name, str):
        return None
    try:
        return lookup[name.lower()]
    except KeyError:
        try:
            return countries.get(name)[0]
        except KeyError:
            return None
