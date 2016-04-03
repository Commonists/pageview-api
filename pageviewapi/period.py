"""Helper functions on period."""
import datetime
import pageviewapi.client


def sum_last(project, page, last=30, agent='all-agents', access='all-access'):
    """Page views during last days."""
    views = pageviewapi.client.per_article(project, page,
                                           __days_ago__(last),
                                           __today__(),
                                           access=access, agent=agent)
    return sum([daily['views'] for daily in views['items']])


def avg_last(project, page, last=30, agent='all-agents', access='all-access'):
    """Page views during last days."""
    views = pageviewapi.client.per_article(project, page,
                                           __days_ago__(last),
                                           __today__(),
                                           access=access, agent=agent)
    return __avg__([daily['views'] for daily in views['items']])


def __today__():
    """Date of the day as YYYYmmdd format."""
    return datetime.date.today().strftime('%Y%m%d')


def __days_ago__(days):
    """Days ago as YYYYmmdd format."""
    today = datetime.date.today()
    delta = datetime.timedelta(days=days)
    ago = today - delta
    return ago.strftime('%Y%m%d')


def __avg__(numericlist):
    """Basic average function."""
    return sum(numericlist) / float(len(numericlist))
