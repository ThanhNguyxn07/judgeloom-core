"""
JudgeLoom — Root conftest for pytest.

Provides shared fixtures available to all test modules.
"""

from __future__ import annotations

import pytest
from django.test import RequestFactory


@pytest.fixture
def request_factory() -> RequestFactory:
    """Provide a Django RequestFactory instance."""
    return RequestFactory()


@pytest.fixture
def api_client():
    """Provide a Django Ninja test client."""
    from ninja.testing import TestClient

    from config.urls import api

    return TestClient(api)
