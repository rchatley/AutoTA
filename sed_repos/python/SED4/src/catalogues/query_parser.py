import re


def published_after_from(query):
    match = re.search(r"PUBLISHEDAFTER\((\d+)\)", query)
    return int(match.group(1)) if match else None


def published_before_from(query):
    match = re.search(r"PUBLISHEDBEFORE\((\d+)\)", query)
    return int(match.group(1)) if match else None


def title_from(query):
    match = re.search(r"TITLECONTAINS\((.+?)\)", query)
    return match.group(1) if match else None


def first_name_from(query):
    match = re.search(r"FIRSTNAME='(\w+)'", query)
    return match.group(1) if match else None


def last_name_from(query):
    match = re.search(r"LASTNAME='(\w+)'", query)
    return match.group(1) if match else None
