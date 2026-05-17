"""Client to wikimedia pageview api.

API doc: https://wikitech.wikimedia.org/wiki/Analytics/AQS/Pageview_API
Supported endpoints:
- per-article
- top
- aggregate
- unique-devices
- legacy/pagecounts
"""

from importlib.metadata import PackageNotFoundError, version
from typing import Any
from urllib.parse import quote, unquote

import requests

try:
    __version__ = version("pageviewapi")
except PackageNotFoundError:
    __version__ = "0.4.0"

PROJECT_URL = "https://github.com/Commonists/pageview-api"
USER_AGENT = {"User-Agent": f"Python pageview-api client v{__version__} <{PROJECT_URL}>"}

API_BASE_URL = "https://wikimedia.org/api/rest_v1/metrics"

PA_ENDPOINT = "pageviews/per-article"
PA_ARGS = "{project}/{access}/{agent}/{page}/{granularity}/{start}/{end}"

TOP_ENDPOINT = "pageviews/top"
TOP_ARGS = "{project}/{access}/{year}/{month}/{day}"

AG_ENDPOINT = "pageviews/aggregate"
AG_ARGS = "{project}/{access}/{agent}/{granularity}/{start}/{end}"

UD_ENDPOINT = "unique-devices"
UD_ARGS = "{project}/{access}/{granularity}/{start}/{end}"

PC_ENDPOINT = "legacy/pagecounts/aggregate"
PC_ARGS = "{project}/{access_site}/{granularity}/{start}/{end}"


class PageviewResponse(dict):  # type: ignore[type-arg]
    """A Wikimedia Pageview API response with attribute-style read access.

    Recursively wraps nested dicts and lists so the full response tree is
    navigable via attributes. Dict data keys always take priority over built-in
    dict methods, so ``response.items`` returns the ``items`` data value rather
    than the ``dict.items`` method when that key is present.

    Use ``from_json`` rather than the constructor directly when the input may
    contain nested dicts or lists — the constructor only wraps the top level.
    """

    def __getattribute__(self, key: str) -> Any:
        if not key.startswith("_"):
            try:
                return dict.__getitem__(self, key)
            except KeyError:
                pass
        return super().__getattribute__(key)

    @classmethod
    def from_json(cls, obj: Any) -> Any:
        """Recursively convert a JSON value into a ``PageviewResponse`` tree."""
        if isinstance(obj, dict):
            return cls({k: cls.from_json(v) for k, v in obj.items()})
        if isinstance(obj, list):
            return [cls.from_json(item) for item in obj]
        return obj


class ZeroOrDataNotLoadedException(Exception):
    """Raised on 404 — no data or data not yet filled.

    https://wikitech.wikimedia.org/wiki/Analytics/PageviewAPI#Gotchas
    """


class ThrottlingException(Exception):
    """Raised on 429 — client is sending too many requests.

    https://wikitech.wikimedia.org/wiki/Analytics/PageviewAPI#Gotchas
    """


def per_article(
    project: str,
    page: str,
    start: str,
    end: str,
    access: str = "all-access",
    agent: str = "all-agents",
    granularity: str = "daily",
) -> dict[str, Any]:
    """Per-article pageview counts.

    >>> import pageviewapi
    >>> pageviewapi.per_article('en.wikipedia', 'Paris', '20151106', '20151120')
    """
    args = PA_ARGS.format(
        project=project,
        page=_quote_article_name(page),
        start=start,
        end=end,
        access=access,
        agent=agent,
        granularity=granularity,
    )
    return _api(PA_ENDPOINT, args)


def top(
    project: str,
    year: int | str,
    month: int | str,
    day: int | str,
    access: str = "all-access",
) -> dict[str, Any]:
    """Top 1000 most visited articles for a project on a given date.

    >>> import pageviewapi
    >>> views = pageviewapi.top('fr.wikipedia', 2015, 11, 14)
    >>> views['items'][0]['articles'][0]
    {'article': 'Wikipédia:Accueil_principal', 'rank': 1, 'views': 1600547}
    """
    args = TOP_ARGS.format(project=project, access=access, year=year, month=month, day=day)
    return _api(TOP_ENDPOINT, args)


def aggregate(
    project: str,
    start: str,
    end: str,
    access: str = "all-access",
    agent: str = "all-agents",
    granularity: str = "daily",
) -> dict[str, Any]:
    """Aggregate pageview counts for a project.

    >>> import pageviewapi
    >>> pageviewapi.aggregate('fr.wikipedia', '2015100100', '2015103100')
    """
    args = AG_ARGS.format(
        project=project,
        start=start,
        end=end,
        access=access,
        agent=agent,
        granularity=granularity,
    )
    return _api(AG_ENDPOINT, args)


def unique_devices(
    project: str,
    start: str,
    end: str,
    access: str = "all-access",
    granularity: str = "daily",
) -> dict[str, Any]:
    """Unique devices accessing a project."""
    args = UD_ARGS.format(project=project, start=start, end=end, access=access, granularity=granularity)
    return _api(UD_ENDPOINT, args)


def legacy_pagecounts(
    project: str,
    start: str,
    end: str,
    access_site: str = "all-sites",
    granularity: str = "daily",
) -> dict[str, Any]:
    """Legacy pagecounts aggregate.

    >>> import pageviewapi
    >>> pageviewapi.legacy_pagecounts('fr.wikipedia', '2010010100', '2011010100')
    """
    project_arg = "all-projects" if project == "all-projects" else f"{project}.org"
    args = PC_ARGS.format(
        project=project_arg,
        start=start,
        end=end,
        access_site=access_site,
        granularity=granularity,
    )
    return _api(PC_ENDPOINT, args)


def _api(end_point: str, args: str, api_url: str = API_BASE_URL) -> dict[str, Any]:
    url = "/".join([api_url, end_point, args])
    response = requests.get(url, headers=USER_AGENT)
    if response.status_code == 200:
        return PageviewResponse.from_json(response.json())
    elif response.status_code == 404:
        raise ZeroOrDataNotLoadedException()
    elif response.status_code == 429:
        raise ThrottlingException()
    else:
        response.raise_for_status()
        return {}  # unreachable, satisfies type checker


def _quote_article_name(page: str) -> str:
    return quote(unquote(page), safe="")
