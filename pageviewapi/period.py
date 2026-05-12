"""Helper functions for aggregating pageviews over a time period."""

import datetime

import pageviewapi.client


def sum_last(
    project: str,
    page: str,
    last: int = 30,
    agent: str = "all-agents",
    access: str = "all-access",
) -> int:
    """Total pageviews for a page over the last N days."""
    views = pageviewapi.client.per_article(project, page, _days_ago(last), _today(), access=access, agent=agent)
    return sum(daily["views"] for daily in views["items"])


def avg_last(
    project: str,
    page: str,
    last: int = 30,
    agent: str = "all-agents",
    access: str = "all-access",
) -> float:
    """Average daily pageviews for a page over the last N days."""
    views = pageviewapi.client.per_article(project, page, _days_ago(last), _today(), access=access, agent=agent)
    return _avg([daily["views"] for daily in views["items"]])


def _today() -> str:
    return datetime.date.today().strftime("%Y%m%d")


def _days_ago(days: int) -> str:
    return (datetime.date.today() - datetime.timedelta(days=days)).strftime("%Y%m%d")


def _avg(values: list[int | float]) -> float:
    return sum(values) / len(values)
