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
