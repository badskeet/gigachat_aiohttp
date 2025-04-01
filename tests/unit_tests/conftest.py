import os

import pytest
from aioresponses import aioresponses


@pytest.fixture(autouse=True)
def _delenv(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(os, "environ", {})


@pytest.fixture
def aioresponses_mock() -> aioresponses:
    with aioresponses() as mock:
        yield mock
