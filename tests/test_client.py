"""Tests for pageviewapi.client."""

from unittest.mock import MagicMock, patch

import pytest

from pageviewapi.client import (
    API_BASE_URL,
    USER_AGENT,
    PageviewResponse,
    ThrottlingException,
    ZeroOrDataNotLoadedException,
    _api,
    _quote_article_name,
    aggregate,
    legacy_pagecounts,
    per_article,
    top,
    unique_devices,
)

ITEMS_RESPONSE = {"items": [{"views": 1234}]}


@pytest.fixture
def ok_response() -> MagicMock:
    r = MagicMock()
    r.status_code = 200
    r.json.return_value = ITEMS_RESPONSE
    return r


@pytest.fixture
def not_found_response() -> MagicMock:
    r = MagicMock()
    r.status_code = 404
    return r


@pytest.fixture
def throttled_response() -> MagicMock:
    r = MagicMock()
    r.status_code = 429
    return r


def test_per_article_returns_json(ok_response):
    with patch("requests.get", return_value=ok_response) as mock_get:
        result = per_article("en.wikipedia", "Paris", "20151106", "20151120")
    assert result == ITEMS_RESPONSE
    url = mock_get.call_args[0][0]
    assert "pageviews/per-article" in url
    assert "en.wikipedia" in url
    assert "Paris" in url
    assert "20151106" in url
    assert "20151120" in url


def test_per_article_default_args_in_url(ok_response):
    with patch("requests.get", return_value=ok_response) as mock_get:
        per_article("en.wikipedia", "Paris", "20151106", "20151120")
    url = mock_get.call_args[0][0]
    assert "all-access" in url
    assert "all-agents" in url
    assert "daily" in url


def test_per_article_custom_args(ok_response):
    with patch("requests.get", return_value=ok_response) as mock_get:
        per_article(
            "en.wikipedia", "Paris", "20151106", "20151120", access="desktop", agent="user", granularity="monthly"
        )
    url = mock_get.call_args[0][0]
    assert "desktop" in url
    assert "user" in url
    assert "monthly" in url


def test_per_article_404_raises(not_found_response):
    with patch("requests.get", return_value=not_found_response):
        with pytest.raises(ZeroOrDataNotLoadedException):
            per_article("en.wikipedia", "Paris", "20151106", "20151120")


def test_per_article_429_raises(throttled_response):
    with patch("requests.get", return_value=throttled_response):
        with pytest.raises(ThrottlingException):
            per_article("en.wikipedia", "Paris", "20151106", "20151120")


def test_top_returns_json(ok_response):
    with patch("requests.get", return_value=ok_response) as mock_get:
        result = top("fr.wikipedia", 2015, 11, 14)
    assert result == ITEMS_RESPONSE
    url = mock_get.call_args[0][0]
    assert "pageviews/top" in url
    assert "fr.wikipedia" in url


def test_top_url_contains_date(ok_response):
    with patch("requests.get", return_value=ok_response) as mock_get:
        top("fr.wikipedia", 2015, 11, 14)
    url = mock_get.call_args[0][0]
    assert "2015" in url
    assert "11" in url
    assert "14" in url


def test_aggregate_returns_json(ok_response):
    with patch("requests.get", return_value=ok_response) as mock_get:
        result = aggregate("fr.wikipedia", "2015100100", "2015103100")
    assert result == ITEMS_RESPONSE
    url = mock_get.call_args[0][0]
    assert "pageviews/aggregate" in url


def test_unique_devices_returns_json(ok_response):
    with patch("requests.get", return_value=ok_response) as mock_get:
        result = unique_devices("en.wikipedia", "20200101", "20200131")
    assert result == ITEMS_RESPONSE
    url = mock_get.call_args[0][0]
    assert "unique-devices" in url


def test_legacy_pagecounts_returns_json(ok_response):
    with patch("requests.get", return_value=ok_response) as mock_get:
        result = legacy_pagecounts("fr.wikipedia", "2010010100", "2011010100")
    assert result == ITEMS_RESPONSE
    url = mock_get.call_args[0][0]
    assert "legacy/pagecounts" in url
    assert "fr.wikipedia.org" in url


def test_legacy_pagecounts_all_projects(ok_response):
    with patch("requests.get", return_value=ok_response) as mock_get:
        legacy_pagecounts("all-projects", "2010010100", "2011010100")
    url = mock_get.call_args[0][0]
    assert "all-projects" in url
    assert "all-projects.org" not in url


def test_api_sends_user_agent(ok_response):
    with patch("requests.get", return_value=ok_response) as mock_get:
        _api("pageviews/per-article", "en.wikipedia/all-access/all-agents/Paris/daily/20200101/20200131")
    _, kwargs = mock_get.call_args
    assert kwargs["headers"] == USER_AGENT


def test_api_other_error_raises(ok_response):
    ok_response.status_code = 500
    ok_response.raise_for_status.side_effect = Exception("server error")
    with patch("requests.get", return_value=ok_response):
        with pytest.raises(Exception, match="server error"):
            _api("pageviews/per-article", "bad/args")


def test_api_constructs_url_correctly(ok_response):
    with patch("requests.get", return_value=ok_response) as mock_get:
        _api("my/endpoint", "arg1/arg2")
    url = mock_get.call_args[0][0]
    assert url == f"{API_BASE_URL}/my/endpoint/arg1/arg2"


def test_pageview_response_attribute_access():
    d = PageviewResponse({"rank": 1, "views": 42})
    assert d.rank == 1
    assert d.views == 42


def test_pageview_response_dict_access_still_works():
    d = PageviewResponse({"rank": 1})
    assert d["rank"] == 1


def test_pageview_response_missing_key_raises_attribute_error():
    d = PageviewResponse({"a": 1})
    with pytest.raises(AttributeError):
        _ = d.missing


def test_pageview_response_items_key_accessible_as_attribute():
    d = PageviewResponse.from_json({"items": [{"views": 1}]})
    assert isinstance(d.items, list)
    assert d.items[0].views == 1


def test_pageview_response_keys_key_accessible_as_attribute():
    d = PageviewResponse({"keys": ["a", "b"]})
    assert d.keys == ["a", "b"]


def test_pageview_response_dict_method_accessible_when_key_absent():
    d = PageviewResponse({"rank": 1})
    assert callable(d.items)


def test_pageview_response_nested_dict_is_wrapped():
    d = PageviewResponse.from_json({"outer": {"inner": 99}})
    assert isinstance(d.outer, PageviewResponse)
    assert d.outer.inner == 99


def test_pageview_response_nested_list_of_dicts_is_wrapped():
    d = PageviewResponse.from_json({"articles": [{"title": "Paris", "views": 10}]})
    assert isinstance(d["articles"][0], PageviewResponse)
    assert d["articles"][0].title == "Paris"


def test_api_returns_pageview_response(ok_response):
    with patch("requests.get", return_value=ok_response):
        result = per_article("en.wikipedia", "Paris", "20151106", "20151120")
    assert isinstance(result, PageviewResponse)


def test_quote_article_name_plain():
    assert _quote_article_name("Paris") == "Paris"


def test_quote_article_name_slash():
    assert _quote_article_name("AC/DC") == "AC%2FDC"


def test_per_article_encodes_space_in_page_name(ok_response):
    with patch("requests.get", return_value=ok_response) as mock_get:
        per_article("en.wikipedia", "New York", "20200101", "20200131")
    url = mock_get.call_args[0][0]
    assert "New%20York" in url
    assert "New York" not in url


def test_per_article_encodes_slash_in_page_name(ok_response):
    with patch("requests.get", return_value=ok_response) as mock_get:
        per_article("en.wikipedia", "AC/DC", "20200101", "20200131")
    url = mock_get.call_args[0][0]
    assert "AC%2FDC" in url
