"""Tests for pageviewapi.period."""

from unittest.mock import patch

import pytest

from pageviewapi.period import _avg, _days_ago, _today, avg_last, sum_last

MOCK_VIEWS = {"items": [{"views": 100}, {"views": 200}, {"views": 300}]}


def test_today_format():
    result = _today()
    assert len(result) == 8
    assert result.isdigit()


def test_days_ago_format():
    result = _days_ago(30)
    assert len(result) == 8
    assert result.isdigit()


def test_days_ago_is_before_today():
    assert _days_ago(1) < _today()


def test_days_ago_zero_equals_today():
    assert _days_ago(0) == _today()


def test_avg_integers():
    assert _avg([10, 20, 30]) == 20.0


def test_avg_single_value():
    assert _avg([42]) == 42.0


def test_avg_floats():
    assert _avg([1.5, 2.5]) == pytest.approx(2.0)


def test_sum_last_returns_total():
    with patch("pageviewapi.client.per_article", return_value=MOCK_VIEWS):
        result = sum_last("en.wikipedia", "Python_(programming_language)")
    assert result == 600


def test_sum_last_passes_date_range():
    with patch("pageviewapi.client.per_article", return_value=MOCK_VIEWS) as mock_pa:
        sum_last("en.wikipedia", "Python_(programming_language)", last=7)
    call_args = mock_pa.call_args[0]
    start, end = call_args[2], call_args[3]
    assert start < end


def test_avg_last_returns_average():
    with patch("pageviewapi.client.per_article", return_value=MOCK_VIEWS):
        result = avg_last("en.wikipedia", "Python_(programming_language)")
    assert result == pytest.approx(200.0)


def test_avg_last_passes_access_and_agent():
    with patch("pageviewapi.client.per_article", return_value=MOCK_VIEWS) as mock_pa:
        avg_last("en.wikipedia", "Python", access="desktop", agent="user")
    _, kwargs = mock_pa.call_args
    assert kwargs["access"] == "desktop"
    assert kwargs["agent"] == "user"
