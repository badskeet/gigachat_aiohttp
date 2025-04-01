import ssl
from typing import List, Optional

import pytest
from aiohttp import ClientSession
from pytest_aiohttp import AiohttpClientMock
from pytest_mock import MockerFixture

from gigachat import GigaChat
from gigachat.client import (
    GIGACHAT_MODEL,
    GigaChatAsyncClient,
    GigaChatSyncClient,
    _get_auth_kwargs,
    _get_kwargs,
    _logger,
    _parse_chat,
)
from gigachat.exceptions import AuthenticationError
from gigachat.models import (
    Balance,
    Chat,
    ChatCompletion,
    ChatCompletionChunk,
    DeletedFile,
    Embedding,
    Embeddings,
    Function,
    Model,
    Models,
    OpenApiFunctions,
    TokensCount,
    UploadedFile,
    UploadedFiles,
)
from gigachat.models.balance import BalanceValue
from gigachat.settings import Settings

from ...utils import get_bytes, get_json

BASE_URL = "http://base_url"
AUTH_URL = "http://auth_url"
CHAT_URL = f"{BASE_URL}/chat/completions"
TOKEN_URL = f"{BASE_URL}/token"
MODELS_URL = f"{BASE_URL}/models"
MODEL_URL = f"{BASE_URL}/models/model"
TOKENS_COUNT_URL = f"{BASE_URL}/tokens/count"
EMBEDDINGS_URL = f"{BASE_URL}/embeddings"
FILES_URL = f"{BASE_URL}/files"
BALANCE_URL = f"{BASE_URL}/balance"
CONVERT_FUNCTIONS_URL = f"{BASE_URL}/functions/convert"
GET_FILE_URL = f"{BASE_URL}/files/1"
GET_FILES_URL = f"{BASE_URL}/files"
FILE_DELETE_URL = f"{BASE_URL}/files/1/delete"

ACCESS_TOKEN = get_json("access_token.json")
TOKEN = get_json("token.json")
CHAT = Chat.parse_obj(get_json("chat.json"))
CHAT_FUNCTION = Chat.parse_obj(get_json("chat_function.json"))
CHAT_COMPLETION = get_json("chat_completion.json")
CHAT_COMPLETION_FUNCTION = get_json("chat_completion_function.json")
CHAT_COMPLETION_STREAM = get_bytes("chat_completion.stream")
EMBEDDINGS = get_json("embeddings.json")
MODELS = get_json("models.json")
TOKENS_COUNT = get_json("tokens_count.json")
MODEL = get_json("model.json")
FILES = get_json("post_files.json")
BALANCE = get_json("balance.json")
CONVERT_FUNCTIONS = get_json("convert_functions.json")
GET_FILE = get_json("get_file.json")
GET_FILES = get_json("get_files.json")
FILE_DELETE = get_json("post_files_delete.json")

FILE = get_bytes("image.jpg")

HEADERS_STREAM = {"Content-Type": "text/event-stream"}

CREDENTIALS = "NmIwNzhlODgtNDlkNC00ZjFmLTljMjMtYjFiZTZjMjVmNTRlOmU3NWJlNjVhLTk4YjAtNGY0Ni1iOWVhLTljMDkwZGE4YTk4MQ=="


def _make_ssl_context() -> ssl.SSLContext:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    return context


def test__get_kwargs() -> None:
    settings = Settings(ca_bundle_file="ca.pem", cert_file="tls.pem", key_file="tls.key")
    assert _get_kwargs(settings)


def test__get_kwargs_ssl() -> None:
    context = _make_ssl_context()
    settings = Settings(ssl_context=context)
    assert _get_kwargs(settings)["verify"] == context


def test__get_auth_kwargs() -> None:
    settings = Settings(ca_bundle_file="ca.pem", cert_file="tls.pem", key_file="tls.key")
    assert _get_auth_kwargs(settings)


def test__get_auth_kwargs_ssl() -> None:
    context = _make_ssl_context()
    settings = Settings(ssl_context=context)
    assert _get_kwargs(settings)["verify"] == context


@pytest.mark.parametrize(
    ("payload_value", "setting_value", "expected"),
    [
        (None, None, GIGACHAT_MODEL),
        (None, "setting_model", "setting_model"),
        ("payload_model", None, "payload_model"),
        ("payload_model", "setting_model", "payload_model"),
    ],
)
def test__parse_chat_model(payload_value: Optional[str], setting_value: Optional[str], expected: str) -> None:
    actual = _parse_chat(Chat(messages=[], model=payload_value), Settings(model=setting_value))
    assert actual.model is expected


@pytest.mark.parametrize(
    ("payload_value", "setting_value", "expected"),
    [
        (None, None, None),
        (None, False, False),
        (None, True, True),
        (False, None, False),
        (False, False, False),
        (False, True, False),
        (True, None, True),
        (True, False, True),
        (True, True, True),
    ],
)
def test__parse_chat_profanity_check(
    payload_value: Optional[bool],
    setting_value: Optional[bool],
    expected: Optional[bool],
) -> None:
    actual = _parse_chat(
        Chat(messages=[], profanity_check=payload_value),
        Settings(profanity_check=setting_value),
    )
    assert actual.profanity_check is expected


def test__unknown_kwargs(mocker: MockerFixture) -> None:
    spy = mocker.spy(_logger, "warning")

    GigaChatSyncClient(foo="bar")

    assert spy.call_count == 1


@pytest.fixture
def aiohttp_mock() -> AiohttpClientMock:
    return AiohttpClientMock()


def test_get_tokens_count(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(TOKENS_COUNT_URL, payload=get_json("tokens_count.json"))
    client = GigaChatSyncClient(credentials="credentials")
    response = client.get_tokens_count("text")
    assert response == TokensCount.model_validate(get_json("tokens_count.json"))


def test_get_models(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(MODELS_URL, payload=get_json("models.json"))
    client = GigaChatSyncClient(credentials="credentials")
    response = client.get_models()
    assert response == Models.model_validate(get_json("models.json"))


def test_get_model(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(MODEL_URL, payload=get_json("model.json"))
    client = GigaChatSyncClient(credentials="credentials")
    response = client.get_model("model")
    assert response == Model.model_validate(get_json("model.json"))


def test_chat(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CHAT_URL, payload=get_json("chat.json"))
    client = GigaChatSyncClient(credentials="credentials")
    response = client.chat("text")
    assert response == ChatCompletion.model_validate(get_json("chat.json"))


def test_upload_file(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(FILES_URL, payload=get_json("uploaded_file.json"))
    client = GigaChatSyncClient(credentials="credentials")
    response = client.upload_file(get_bytes("file.txt"))
    assert response == UploadedFile.model_validate(get_json("uploaded_file.json"))


def test_chat_access_token(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CHAT_URL, payload=get_json("chat.json"))
    client = GigaChatSyncClient(access_token="access_token")
    response = client.chat("text")
    assert response == ChatCompletion.model_validate(get_json("chat.json"))


def test_chat_credentials(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CHAT_URL, payload=get_json("chat.json"))
    client = GigaChatSyncClient(credentials="credentials")
    response = client.chat("text")
    assert response == ChatCompletion.model_validate(get_json("chat.json"))


def test_chat_user_password(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CHAT_URL, payload=get_json("chat.json"))
    client = GigaChatSyncClient(user="user", password="password")
    response = client.chat("text")
    assert response == ChatCompletion.model_validate(get_json("chat.json"))


def test_chat_authentication_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CHAT_URL, status=401)
    client = GigaChatSyncClient(credentials="credentials")
    with pytest.raises(AuthenticationError):
        client.chat("text")


def test_chat_update_token_credentials(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(TOKEN_URL, payload=get_json("token.json"))
    aiohttp_mock.post(CHAT_URL, payload=get_json("chat.json"))
    client = GigaChatSyncClient(credentials="credentials", update_token=True)
    response = client.chat("text")
    assert response == ChatCompletion.model_validate(get_json("chat.json"))


def test_chat_update_token_user_password(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(TOKEN_URL, payload=get_json("token.json"))
    aiohttp_mock.post(CHAT_URL, payload=get_json("chat.json"))
    client = GigaChatSyncClient(user="user", password="password", update_token=True)
    response = client.chat("text")
    assert response == ChatCompletion.model_validate(get_json("chat.json"))


def test_chat_update_token_false(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CHAT_URL, status=401)
    client = GigaChatSyncClient(credentials="credentials", update_token=False)
    with pytest.raises(AuthenticationError):
        client.chat("text")


def test_chat_update_token_success(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(TOKEN_URL, payload=get_json("token.json"))
    aiohttp_mock.post(CHAT_URL, payload=get_json("chat.json"))
    client = GigaChatSyncClient(credentials="credentials", update_token=True)
    response = client.chat("text")
    assert response == ChatCompletion.model_validate(get_json("chat.json"))


def test_chat_update_token_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(TOKEN_URL, status=401)
    client = GigaChatSyncClient(credentials="credentials", update_token=True)
    with pytest.raises(AuthenticationError):
        client.chat("text")


def test_chat_with_functions(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CHAT_URL, payload=get_json("chat_with_functions.json"))
    client = GigaChatSyncClient(credentials="credentials")
    response = client.chat(
        "text",
        functions=[Function(name="function", description="description", parameters={"type": "object"})],
    )
    assert response == ChatCompletion.model_validate(get_json("chat_with_functions.json"))


def test_embeddings(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(EMBEDDINGS_URL, payload=get_json("embeddings.json"))
    client = GigaChatSyncClient(credentials="credentials")
    response = client.embeddings("text")
    assert response == Embeddings.model_validate(get_json("embeddings.json"))


def test_stream(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CHAT_URL, payload=get_json("stream.json"))
    client = GigaChatSyncClient(credentials="credentials")
    response = list(client.stream("text"))
    assert response == [ChatCompletionChunk.model_validate(get_json("stream.json"))]


def test_stream_access_token(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CHAT_URL, payload=get_json("stream.json"))
    client = GigaChatSyncClient(access_token="access_token")
    response = list(client.stream("text"))
    assert response == [ChatCompletionChunk.model_validate(get_json("stream.json"))]


def test_stream_authentication_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CHAT_URL, status=401)
    client = GigaChatSyncClient(credentials="credentials")
    with pytest.raises(AuthenticationError):
        list(client.stream("text"))


def test_stream_update_token_success(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(TOKEN_URL, payload=get_json("token.json"))
    aiohttp_mock.post(CHAT_URL, payload=get_json("stream.json"))
    client = GigaChatSyncClient(credentials="credentials", update_token=True)
    response = list(client.stream("text"))
    assert response == [ChatCompletionChunk.model_validate(get_json("stream.json"))]


def test_stream_update_token_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(TOKEN_URL, status=401)
    client = GigaChatSyncClient(credentials="credentials", update_token=True)
    with pytest.raises(AuthenticationError):
        list(client.stream("text"))


def test_get_token_credentials(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(TOKEN_URL, payload=get_json("token.json"))
    client = GigaChatSyncClient(credentials="credentials")
    response = client.get_token()
    assert response == "access_token"


def test_balance(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(BALANCE_URL, payload=get_json("balance.json"))
    client = GigaChatSyncClient(credentials="credentials")
    response = client.balance()
    assert response == Balance.model_validate(get_json("balance.json"))


def test_convert_functions(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CONVERT_FUNCTIONS_URL, payload=get_json("convert_functions.json"))
    client = GigaChatSyncClient(credentials="credentials")
    response = client.convert_functions([Function(name="function", description="description", parameters={"type": "object"})])
    assert response == OpenApiFunctions.model_validate(get_json("convert_functions.json"))


def test_get_file(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(f"{FILES_URL}/file_id", payload=get_json("uploaded_file.json"))
    client = GigaChatSyncClient(credentials="credentials")
    response = client.get_file("file_id")
    assert response == UploadedFile.model_validate(get_json("uploaded_file.json"))


def test_get_files(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(FILES_URL, payload=get_json("uploaded_files.json"))
    client = GigaChatSyncClient(credentials="credentials")
    response = client.get_files()
    assert response == UploadedFiles.model_validate(get_json("uploaded_files.json"))


def test_delete_file(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.delete(f"{FILES_URL}/file_id", payload=get_json("deleted_file.json"))
    client = GigaChatSyncClient(credentials="credentials")
    response = client.delete_file("file_id")
    assert response == DeletedFile.model_validate(get_json("deleted_file.json"))


@pytest.mark.asyncio()
async def test_aget_models(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(MODELS_URL, payload=get_json("models.json"))
    client = GigaChatAsyncClient(credentials="credentials")
    response = await client.aget_models()
    assert response == Models.model_validate(get_json("models.json"))


@pytest.mark.asyncio()
async def test_atokens_count(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(TOKENS_COUNT_URL, payload=get_json("tokens_count.json"))
    client = GigaChatAsyncClient(credentials="credentials")
    response = await client.aget_tokens_count("text")
    assert response == TokensCount.model_validate(get_json("tokens_count.json"))


@pytest.mark.asyncio()
async def test_aget_model(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(MODEL_URL, payload=get_json("model.json"))
    client = GigaChatAsyncClient(credentials="credentials")
    response = await client.aget_model("model")
    assert response == Model.model_validate(get_json("model.json"))


@pytest.mark.asyncio()
async def test_achat(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CHAT_URL, payload=get_json("chat.json"))
    client = GigaChatAsyncClient(credentials="credentials")
    response = await client.achat("text")
    assert response == ChatCompletion.model_validate(get_json("chat.json"))


@pytest.mark.asyncio()
async def test_achat_access_token(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CHAT_URL, payload=get_json("chat.json"))
    client = GigaChatAsyncClient(access_token="access_token")
    response = await client.achat("text")
    assert response == ChatCompletion.model_validate(get_json("chat.json"))


@pytest.mark.asyncio()
async def test_achat_credentials(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CHAT_URL, payload=get_json("chat.json"))
    client = GigaChatAsyncClient(credentials="credentials")
    response = await client.achat("text")
    assert response == ChatCompletion.model_validate(get_json("chat.json"))


@pytest.mark.asyncio()
async def test_achat_user_password(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CHAT_URL, payload=get_json("chat.json"))
    client = GigaChatAsyncClient(user="user", password="password")
    response = await client.achat("text")
    assert response == ChatCompletion.model_validate(get_json("chat.json"))


@pytest.mark.asyncio()
async def test_achat_authentication_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CHAT_URL, status=401)
    client = GigaChatAsyncClient(credentials="credentials")
    with pytest.raises(AuthenticationError):
        await client.achat("text")


@pytest.mark.asyncio()
async def test_achat_update_token_false(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CHAT_URL, status=401)
    client = GigaChatAsyncClient(credentials="credentials", update_token=False)
    with pytest.raises(AuthenticationError):
        await client.achat("text")


@pytest.mark.asyncio()
async def test_achat_update_token_credentials(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(TOKEN_URL, payload=get_json("token.json"))
    aiohttp_mock.post(CHAT_URL, payload=get_json("chat.json"))
    client = GigaChatAsyncClient(credentials="credentials", update_token=True)
    response = await client.achat("text")
    assert response == ChatCompletion.model_validate(get_json("chat.json"))


@pytest.mark.asyncio()
async def test_achat_update_token_user_password(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(TOKEN_URL, payload=get_json("token.json"))
    aiohttp_mock.post(CHAT_URL, payload=get_json("chat.json"))
    client = GigaChatAsyncClient(user="user", password="password", update_token=True)
    response = await client.achat("text")
    assert response == ChatCompletion.model_validate(get_json("chat.json"))


@pytest.mark.asyncio()
async def test_aembeddings(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(EMBEDDINGS_URL, payload=get_json("embeddings.json"))
    client = GigaChatAsyncClient(credentials="credentials")
    response = await client.aembeddings("text")
    assert response == Embeddings.model_validate(get_json("embeddings.json"))


@pytest.mark.asyncio()
async def test_abalance(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(BALANCE_URL, payload=get_json("balance.json"))
    client = GigaChatAsyncClient(credentials="credentials")
    response = await client.abalance()
    assert response == Balance.model_validate(get_json("balance.json"))


@pytest.mark.asyncio()
async def test_aconvert_functions(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CONVERT_FUNCTIONS_URL, payload=get_json("convert_functions.json"))
    client = GigaChatAsyncClient(credentials="credentials")
    response = await client.aconvert_functions([Function(name="function", description="description", parameters={"type": "object"})])
    assert response == OpenApiFunctions.model_validate(get_json("convert_functions.json"))


@pytest.mark.asyncio()
async def test_astream(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CHAT_URL, payload=get_json("stream.json"))
    client = GigaChatAsyncClient(credentials="credentials")
    response = [chunk async for chunk in client.astream("text")]
    assert response == [ChatCompletionChunk.model_validate(get_json("stream.json"))]


@pytest.mark.asyncio()
async def test_astream_access_token(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CHAT_URL, payload=get_json("stream.json"))
    client = GigaChatAsyncClient(access_token="access_token")
    response = [chunk async for chunk in client.astream("text")]
    assert response == [ChatCompletionChunk.model_validate(get_json("stream.json"))]


@pytest.mark.asyncio()
async def test_astream_authentication_error(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(CHAT_URL, status=401)
    client = GigaChatAsyncClient(credentials="credentials")
    with pytest.raises(AuthenticationError):
        async for _ in client.astream("text")


@pytest.mark.asyncio()
async def test_astream_update_token(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(TOKEN_URL, payload=get_json("token.json"))
    aiohttp_mock.post(CHAT_URL, payload=get_json("stream.json"))
    client = GigaChatAsyncClient(credentials="credentials", update_token=True)
    response = [chunk async for chunk in client.astream("text")]
    assert response == [ChatCompletionChunk.model_validate(get_json("stream.json"))]


@pytest.mark.asyncio()
async def test_aupload_file(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(FILES_URL, payload=get_json("uploaded_file.json"))
    client = GigaChatAsyncClient(credentials="credentials")
    response = await client.aupload_file(get_bytes("file.txt"))
    assert response == UploadedFile.model_validate(get_json("uploaded_file.json"))


@pytest.mark.asyncio()
async def test_aget_token_credentials(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.post(TOKEN_URL, payload=get_json("token.json"))
    client = GigaChatAsyncClient(credentials="credentials")
    response = await client.aget_token()
    assert response == "access_token"


@pytest.mark.asyncio()
async def test_aget_file(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(f"{FILES_URL}/file_id", payload=get_json("uploaded_file.json"))
    client = GigaChatAsyncClient(credentials="credentials")
    response = await client.aget_file("file_id")
    assert response == UploadedFile.model_validate(get_json("uploaded_file.json"))


@pytest.mark.asyncio()
async def test_aget_files(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.get(FILES_URL, payload=get_json("uploaded_files.json"))
    client = GigaChatAsyncClient(credentials="credentials")
    response = await client.aget_files()
    assert response == UploadedFiles.model_validate(get_json("uploaded_files.json"))


@pytest.mark.asyncio()
async def test_adelete_file(aiohttp_mock: AiohttpClientMock) -> None:
    aiohttp_mock.delete(f"{FILES_URL}/file_id", payload=get_json("deleted_file.json"))
    client = GigaChatAsyncClient(credentials="credentials")
    response = await client.adelete_file("file_id")
    assert response == DeletedFile.model_validate(get_json("deleted_file.json"))
