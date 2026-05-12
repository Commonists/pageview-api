"""Python client for the Wikimedia Pageview API."""

from pageviewapi.client import (
    PageviewResponse,
    ThrottlingException,
    ZeroOrDataNotLoadedException,
    __version__,
    aggregate,
    legacy_pagecounts,
    per_article,
    top,
    unique_devices,
)

__all__ = [
    "__version__",
    "aggregate",
    "PageviewResponse",
    "legacy_pagecounts",
    "per_article",
    "ThrottlingException",
    "top",
    "unique_devices",
    "ZeroOrDataNotLoadedException",
]
