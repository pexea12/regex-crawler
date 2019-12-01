import validators
import re


def is_url(url):
    return validators.url(url)

def is_regex(regex):
    try:
        re.compile(regex)
        return True
    except re.error:
        return False
