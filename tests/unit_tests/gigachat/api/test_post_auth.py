import aiohttp
import pytest
from pytest_aiohttp import AiohttpClientMock

from gigachat.api import post_auth
from gigachat.exceptions import AuthenticationError, ResponseError
from gigachat.models import AccessToken

from ....utils import get_json

MOCK_URL = "http://testserver/foo"

ACCESS_TOKEN = get_json("access_token.json")


def test_sync(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(MOCK_URL, payload=ACCESS_TOKEN)

    with aiohttp.ClientSession() as client:
        response = post_auth.sync(client, url=MOCK_URL, credentials="credentials", scope="scope")

    assert isinstance(response, AccessToken)


def test_sync_value_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(MOCK_URL, payload={})

    with aiohttp.ClientSession() as client:
        with pytest.raises(ValueError, match="2 validation errors for AccessToken*"):
            post_auth.sync(client, url=MOCK_URL, credentials="credentials", scope="scope")


def test_sync_authentication_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(MOCK_URL, status=401)

    with aiohttp.ClientSession() as client:
        with pytest.raises(AuthenticationError):
            post_auth.sync(client, url=MOCK_URL, credentials="credentials", scope="scope")


def test_sync_response_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(MOCK_URL, status=400)

    with aiohttp.ClientSession() as client:
        with pytest.raises(ResponseError):
            post_auth.sync(client, url=MOCK_URL, credentials="credentials", scope="scope")


def test_sync_headers(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(MOCK_URL, payload=ACCESS_TOKEN)

    with aiohttp.ClientSession() as client:
        response = post_auth.sync(
            client,
            url=MOCK_URL,
            credentials="credentials",
            scope="scope",
        )

    assert isinstance(response, AccessToken)


@pytest.mark.asyncio()
async def test_asyncio(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(MOCK_URL, payload=ACCESS_TOKEN)

    async with aiohttp.ClientSession() as client:
        response = await post_auth.asyncio(client, url=MOCK_URL, credentials="credentials", scope="scope")

    assert isinstance(response, AccessToken)
