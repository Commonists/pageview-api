"""Client to wikimedia pageview api.

API doc: https://wikitech.wikimedia.org/wiki/Analytics/AQS/Pageview_API
Supported endpoints:
- per-article
- top
- aggregate
"""

from attrdict import AttrDict
import requests

__version__ = "0.4.0"

# User-agent
PROJECT_URL = "https://github.com/Commonists/pageview-api"
UA = "Python pageview-api client v{version} <{url}>"
USER_AGENT = {
    'User-Agent': UA.format(url=PROJECT_URL, version=__version__)
}

API_BASE_URL = "https://wikimedia.org/api/rest_v1/metrics"
# Per article
PA_ENDPOINT = "pageviews/per-article"
PA_ARGS = "{project}/{access}/{agent}/{page}/{granularity}/{start}/{end}"

# Top
TOP_ENDPOINT = "pageviews/top"
TOP_ARGS = "{project}/{access}/{year}/{month}/{day}"

# aggregate
AG_ENDPOINT = "pageviews/aggregate"
AG_ARGS = "{project}/{access}/{agent}/{granularity}/{start}/{end}"

# unique-devices
UD_ENDPOINT = "unique-devices"
UD_ARGS = "{project}/{access}/{granularity}/{start}/{end}"

# legacy pagecounts
PC_ENDPOINT = "legacy/pagecounts/aggregate"
PC_ARGS = "{project}/{access_site}/{granularity}/{start}/{end}"


class ZeroOrDataNotLoadedException(Exception):
    """Raised for 404 Error

    404 may happen when there is no data or data has not been filled yet.
    https://wikitech.wikimedia.org/wiki/Analytics/PageviewAPI#Gotchas
    """
    pass


class ThrottlingException(Exception):
    """Raise for 429 Error

    Client doing too many request may be subject to throttling.
    Requests in cache are not throttled (throttling is done at storage layer).
    https://wikitech.wikimedia.org/wiki/Analytics/PageviewAPI#Gotchas
    """


def per_article(project, page, start, end,
                access='all-access', agent='all-agents', granularity='daily'):
    """Per article API.

    >>> import pageviewapi
    >>> pageview.per_article('en.wikipedia', 'Paris', '20151106', '20151120')
    will requests views for Paris article between 2015-11-06 and 2015-11-20
    """
    args = PA_ARGS.format(project=project,
                          page=page,
                          start=start,
                          end=end,
                          access=access,
                          agent=agent,
                          granularity=granularity)
    return __api__(PA_ENDPOINT, args)


def top(project, year, month, day, access='all-access'):
    """Top 1000 most visited articles from project on a given date.

    >>> import pageviewapi
    >>> views = pageviewapi.top('fr.wikipedia', 2015, 11, 14)
    >>> views['items'][0]['articles'][0]
    {u'article': u'Wikip\xe9dia:Accueil_principal', u'rank': 1,
    u'views': 1600547}
    """
    args = TOP_ARGS.format(project=project,
                           access=access,
                           year=year,
                           month=month,
                           day=day)
    return __api__(TOP_ENDPOINT, args)


def aggregate(project, start, end,
              access='all-access', agent='all-agents', granularity='daily'):
    """Aggregate API.

    >>> import pageviewapi
    >>> pageviewapi.aggregate('fr.wikipedia', '2015100100', '2015103100')
    """
    args = AG_ARGS.format(project=project,
                          start=start,
                          end=end,
                          access=access,
                          agent=agent,
                          granularity=granularity)
    return __api__(AG_ENDPOINT, args)


def unique_devices(project, start, end,
                   access='all-access', granularity='daily'):
    """Unique devices."""
    args = UD_ARGS.format(project=project,
                          start=start,
                          end=end,
                          access=access,
                          granularity=granularity)
    return __api__(UD_ENDPOINT, args)


def legacy_pagecounts(project, start, end,
                      access_site='all-sites', granularity='daily'):
    """Legacy pagecounts

    >>> import pageviewapi
    >>> pageviewapi.legacy_pagecounts('fr.wikipedia', '2010010100', '2011010100')
    """
    project_arg = 'all-projects'
    if project != 'all-projects':
        project_arg = '{}.org'.format(project)
    args = PC_ARGS.format(project=project_arg,
                          start=start,
                          end=end,
                          access_site=access_site,
                          granularity=granularity)
    return __api__(PC_ENDPOINT, args)


def __api__(end_point, args, api_url=API_BASE_URL):
    """Calling API."""
    url = "/".join([api_url, end_point, args])
    response = requests.get(url, headers=USER_AGENT)
    if response.status_code == 200:
        # Everything went fine!
        return AttrDict(response.json())
    elif response.status_code == 404:
        raise ZeroOrDataNotLoadedException
    elif response.status_code == 429:
        raise ThrottlingException
    else:
        response.raise_for_status()
