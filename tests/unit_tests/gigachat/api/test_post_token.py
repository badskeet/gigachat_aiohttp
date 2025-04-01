import aiohttp
import pytest
from pytest_aiohttp import AiohttpClientMock

from gigachat.api import post_token
from gigachat.context import operation_id_cvar, request_id_cvar, service_id_cvar, session_id_cvar
from gigachat.exceptions import AuthenticationError, ResponseError
from gigachat.models import Token

from ....utils import get_json

BASE_URL = "http://testserver/api"
MOCK_URL = f"{BASE_URL}/token"

TOKEN = get_json("token.json")


def test__kwargs_context_vars() -> None:
    token_request_id_cvar = request_id_cvar.set("request_id_cvar")
    token_session_id_cvar = session_id_cvar.set("session_id_cvar")
    token_service_id_cvar = service_id_cvar.set("service_id_cvar")
    token_operation_id_cvar = operation_id_cvar.set("operation_id_cvar")

    assert post_token._get_kwargs(user="user", password="password")

    request_id_cvar.reset(token_request_id_cvar)
    session_id_cvar.reset(token_session_id_cvar)
    service_id_cvar.reset(token_service_id_cvar)
    operation_id_cvar.reset(token_operation_id_cvar)


def test_sync(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(MOCK_URL, payload=TOKEN)

    with aiohttp.ClientSession(base_url=BASE_URL) as client:
        response = post_token.sync(client, user="user", password="password")

    assert isinstance(response, Token)


def test_sync_value_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(MOCK_URL, payload={})

    with aiohttp.ClientSession(base_url=BASE_URL) as client:
        with pytest.raises(ValueError, match="2 validation errors for Token*"):
            post_token.sync(client, user="user", password="password")


def test_sync_authentication_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(MOCK_URL, status=401)

    with aiohttp.ClientSession(base_url=BASE_URL) as client:
        with pytest.raises(AuthenticationError):
            post_token.sync(client, user="user", password="password")


def test_sync_response_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(MOCK_URL, status=400)

    with aiohttp.ClientSession(base_url=BASE_URL) as client:
        with pytest.raises(ResponseError):
            post_token.sync(client, user="user", password="password")


def test_sync_headers(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(MOCK_URL, payload=TOKEN)

    with aiohttp.ClientSession(base_url=BASE_URL) as client:
        response = post_token.sync(
            client,
            user="user",
            password="password",
        )

    assert isinstance(response, Token)


@pytest.mark.asyncio()
async def test_asyncio(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(MOCK_URL, payload=TOKEN)

    async with aiohttp.ClientSession(base_url=BASE_URL) as client:
        response = await post_token.asyncio(client, user="user", password="password")

    assert isinstance(response, Token)
