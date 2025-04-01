import aiohttp
import pytest
from pytest_aiohttp import AiohttpClientMock

from gigachat.api import get_models
from gigachat.context import authorization_cvar, operation_id_cvar, request_id_cvar, service_id_cvar, session_id_cvar
from gigachat.exceptions import AuthenticationError, ResponseError
from gigachat.models import Models

from ....utils import get_json

BASE_URL = "http://testserver/api"
MODELS_URL = f"{BASE_URL}/models"

MODELS = get_json("models.json")


def test__kwargs_context_vars() -> None:
    token_authorization_cvar = authorization_cvar.set("authorization_cvar")
    token_request_id_cvar = request_id_cvar.set("request_id_cvar")
    token_session_id_cvar = session_id_cvar.set("session_id_cvar")
    token_service_id_cvar = service_id_cvar.set("service_id_cvar")
    token_operation_id_cvar = operation_id_cvar.set("operation_id_cvar")

    assert get_models._get_kwargs()

    authorization_cvar.reset(token_authorization_cvar)
    request_id_cvar.reset(token_request_id_cvar)
    session_id_cvar.reset(token_session_id_cvar)
    service_id_cvar.reset(token_service_id_cvar)
    operation_id_cvar.reset(token_operation_id_cvar)


def test_sync(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(MODELS_URL, payload=MODELS)

    with aiohttp.ClientSession(base_url=BASE_URL) as client:
        response = get_models.sync(client)

    assert isinstance(response, Models)


def test_sync_value_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(MODELS_URL, payload={})

    with aiohttp.ClientSession(base_url=BASE_URL) as client:
        with pytest.raises(ValueError, match="2 validation errors for Models*"):
            get_models.sync(client)


def test_sync_authentication_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(MODELS_URL, status=401)

    with aiohttp.ClientSession(base_url=BASE_URL) as client:
        with pytest.raises(AuthenticationError):
            get_models.sync(client)


def test_sync_response_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(MODELS_URL, status=400)

    with aiohttp.ClientSession(base_url=BASE_URL) as client:
        with pytest.raises(ResponseError):
            get_models.sync(client)


def test_sync_headers(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(MODELS_URL, payload=MODELS)

    with aiohttp.ClientSession(base_url=BASE_URL) as client:
        response = get_models.sync(
            client,
            access_token="access_token",
        )

    assert isinstance(response, Models)


@pytest.mark.asyncio()
async def test_asyncio(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(MODELS_URL, payload=MODELS)

    async with aiohttp.ClientSession(base_url=BASE_URL) as client:
        response = await get_models.asyncio(client)

    assert isinstance(response, Models)
