"""Views during the last days."""
import datetime
import pageviewapi.client


def last30(project, page, agent='all-agents', access='all-access'):
    """Page views during last 30 days."""
    return __last__(project, page, 30, agent=agent, access=access)

def last60(project, page, agent='all-agents', access='all-access'):
    """Page views during last 60 days."""
    return __last__(project, page, 60, agent=agent, access=access)

def last90(project, page, agent='all-agents', access='all-access'):
    """Page views during last 90 days."""
    return __last__(project, page, 90, agent=agent, access=access)


def __last__(project, page, days, agent='all-agents', access='all-access'):
    """Page views during last days."""
    today = datetime.date.today()
    delta = datetime.timedelta(days=days)
    start_period = today - delta
    views = pageviewapi.client.per_article(project, page,
                                           start_period.strftime('%Y%m%d'),
                                           today.strftime('%Y%m%d'),
                                           access=access, agent=agent)
    return sum([daily['views'] for daily in views['items']])
