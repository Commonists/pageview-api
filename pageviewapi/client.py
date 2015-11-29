"""Client to wikimedia pageview api."""

from attrdict import AttrDict
import requests


API_BASE_URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews"
# PER_ARTICLE = "/per-article/en.wikipedia/all-access/all-agents/Paris/daily/20151110/20151117"
PER_ARTICLE = "per-article"
PA_ARGS = "{project}/{access}/{agent}/{page}/{granularity}/{start}/{end}"


def per_article(project, page, start, end,
                access='all-access', agent='all-agents',granularity='daily'):
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
    url = "/".join([API_BASE_URL, PER_ARTICLE, args])
    return AttrDict(requests.get(url).json())
