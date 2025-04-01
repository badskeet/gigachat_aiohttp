import aiohttp
import pytest
from pytest_aiohttp import AiohttpClientMock

from gigachat.api import post_chat
from gigachat.context import authorization_cvar, operation_id_cvar, request_id_cvar, service_id_cvar, session_id_cvar
from gigachat.exceptions import AuthenticationError, ResponseError
from gigachat.models import Chat, ChatCompletion

from ....utils import get_json

BASE_URL = "http://testserver/api"
MOCK_URL = f"{BASE_URL}/chat/completions"

CHAT = Chat.parse_obj(get_json("chat.json"))
CHAT_COMPLETION = get_json("chat_completion.json")


def test__kwargs_context_vars() -> None:
    token_authorization_cvar = authorization_cvar.set("authorization_cvar")
    token_request_id_cvar = request_id_cvar.set("request_id_cvar")
    token_session_id_cvar = session_id_cvar.set("session_id_cvar")
    token_service_id_cvar = service_id_cvar.set("service_id_cvar")
    token_operation_id_cvar = operation_id_cvar.set("operation_id_cvar")

    assert post_chat._get_kwargs(chat=Chat(messages=[]))

    authorization_cvar.reset(token_authorization_cvar)
    request_id_cvar.reset(token_request_id_cvar)
    session_id_cvar.reset(token_session_id_cvar)
    service_id_cvar.reset(token_service_id_cvar)
    operation_id_cvar.reset(token_operation_id_cvar)


def test_sync(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(MOCK_URL, payload=CHAT_COMPLETION)

    with aiohttp.ClientSession(base_url=BASE_URL) as client:
        response = post_chat.sync(client, chat=CHAT)

    assert isinstance(response, ChatCompletion)


def test_sync_value_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(MOCK_URL, payload={})

    with aiohttp.ClientSession(base_url=BASE_URL) as client:
        with pytest.raises(ValueError, match="5 validation errors for ChatCompletion*"):
            post_chat.sync(client, chat=CHAT)


def test_sync_authentication_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(MOCK_URL, status=401)

    with aiohttp.ClientSession(base_url=BASE_URL) as client:
        with pytest.raises(AuthenticationError):
            post_chat.sync(client, chat=CHAT)


def test_sync_response_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(MOCK_URL, status=400)

    with aiohttp.ClientSession(base_url=BASE_URL) as client:
        with pytest.raises(ResponseError):
            post_chat.sync(client, chat=CHAT)


def test_sync_headers(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(MOCK_URL, payload=CHAT_COMPLETION)

    with aiohttp.ClientSession(base_url=BASE_URL) as client:
        response = post_chat.sync(
            client,
            chat=CHAT,
            access_token="access_token",
        )

    assert isinstance(response, ChatCompletion)


@pytest.mark.asyncio()
async def test_asyncio(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(MOCK_URL, payload=CHAT_COMPLETION)

    async with aiohttp.ClientSession(base_url=BASE_URL) as client:
        response = await post_chat.asyncio(client, chat=CHAT)

    assert isinstance(response, ChatCompletion)
