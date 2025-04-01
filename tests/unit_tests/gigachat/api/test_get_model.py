import aiohttp
import pytest
from pytest_aiohttp import AiohttpClientMock

from gigachat.api import get_model
from gigachat.context import authorization_cvar, operation_id_cvar, request_id_cvar, service_id_cvar, session_id_cvar
from gigachat.exceptions import AuthenticationError, ResponseError
from gigachat.models import Model

from ....utils import get_json

BASE_URL = "http://testserver/api"
MODEL_URL = f"{BASE_URL}/models/model"

MODEL = get_json("model.json")


def test__kwargs_context_vars() -> None:
    token_authorization_cvar = authorization_cvar.set("authorization_cvar")
    token_request_id_cvar = request_id_cvar.set("request_id_cvar")
    token_session_id_cvar = session_id_cvar.set("session_id_cvar")
    token_service_id_cvar = service_id_cvar.set("service_id_cvar")
    token_operation_id_cvar = operation_id_cvar.set("operation_id_cvar")

    assert get_model._get_kwargs(model="model")

    authorization_cvar.reset(token_authorization_cvar)
    request_id_cvar.reset(token_request_id_cvar)
    session_id_cvar.reset(token_session_id_cvar)
    service_id_cvar.reset(token_service_id_cvar)
    operation_id_cvar.reset(token_operation_id_cvar)


def test_sync(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(MODEL_URL, payload=MODEL)

    with aiohttp.ClientSession(base_url=BASE_URL) as client:
        response = get_model.sync(client, model="model")

    assert isinstance(response, Model)


def test_sync_value_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(MODEL_URL, payload={})

    with aiohttp.ClientSession(base_url=BASE_URL) as client:
        with pytest.raises(ValueError, match="3 validation errors for Model*"):
            get_model.sync(client, model="model")


def test_sync_authentication_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(MODEL_URL, status=401)

    with aiohttp.ClientSession(base_url=BASE_URL) as client:
        with pytest.raises(AuthenticationError):
            get_model.sync(client, model="model")


def test_sync_response_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(MODEL_URL, status=400)

    with aiohttp.ClientSession(base_url=BASE_URL) as client:
        with pytest.raises(ResponseError):
            get_model.sync(client, model="model")


def test_sync_headers(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(MODEL_URL, payload=MODEL)

    with aiohttp.ClientSession(base_url=BASE_URL) as client:
        response = get_model.sync(
            client,
            model="model",
            access_token="access_token",
        )

    assert isinstance(response, Model)


@pytest.mark.asyncio()
async def test_asyncio(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(MODEL_URL, payload=MODEL)

    async with aiohttp.ClientSession(base_url=BASE_URL) as client:
        response = await get_model.asyncio(client, model="model")

    assert isinstance(response, Model)
