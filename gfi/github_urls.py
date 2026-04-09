#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


GH_URL_PATTERNS = (
    re.compile(
        r"^(?:https?://)?(?:www\.)?github\.com/(?P<owner>[\w.-]+)/(?P<name>[\w.-]+?)(?:\.git)?/?$",
        re.IGNORECASE,
    ),
    re.compile(
        r"^git@github\.com:(?P<owner>[\w.-]+)/(?P<name>[\w.-]+?)(?:\.git)?$",
        re.IGNORECASE,
    ),
)


def parse_github_url(url: str) -> dict:
    """Take a GitHub repository URL and return its owner and repo name."""
    normalized_url = url.strip()

    for pattern in GH_URL_PATTERNS:
        match = pattern.match(normalized_url)
        if match:
            return match.groupdict()

    return {}
