"""Client to wikimedia pageview api."""

from attrdict import AttrDict
import requests


# User-agent
PROJECT_URL = "https://github.com/Commonists/pageview-api"
USER_AGENT = {
    'User-Agent': "Python pageview-api client <{url}>".format(url=PROJECT_URL)
}

API_BASE_URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews"
# Per article
PA_ENDPOINT = "per-article"
PA_ARGS = "{project}/{access}/{agent}/{page}/{granularity}/{start}/{end}"

# Top
TOP_ENDPOINT = "top"
TOP_ARGS = "{project}/{access}/{year}/{month}/{day}"


def per_article(project, page, start, end,
                access='all-access', agent='all-agents', granularity='daily'):
    """Per article API.

    >>> import pageviewapi as pv
    >>> pv.per_article('en.wikipedia', 'Paris', '20151106', '20151120')
    will requests views for Paris article between 2015-11-06 and 2015-11-20
    """
    args = PA_ARGS.format(project=project,
                          page=page,
                          start=start,
                          end=end,
                          access=access,
                          agent=agent,
                          granularity=granularity)
    url = "/".join([API_BASE_URL, PA_ENDPOINT, args])
    return AttrDict(requests.get(url, headers=USER_AGENT).json())


def top(project, year, month, day, access='all-access'):
    """Top 1000 most visited articles from project on a given date.

    >>> import pageviewapi
    >>> views = pageviewapi('fr.wikipedia', 2015, 11, 14)
    >>> views['items'][0]['articles'][0]
    {u'article': u'Wikip\xe9dia:Accueil_principal', u'rank': 1,
    u'views': 1600547}
    """
    args = TOP_ARGS.format(project=project,
                           access=access,
                           year=year,
                           month=month,
                           day=day)
    url = "/".join([API_BASE_URL, TOP_ENDPOINT, args])
    return AttrDict(requests.get(url, headers=USER_AGENT).json())
