import pytest
from aioresponses import aioresponses
import responses

from gigachat.client import GigaChatAsyncClient, GigaChatSyncClient
from gigachat.models.assistants import (
    Assistant,
    AssistantDelete,
    AssistantFileDelete,
    Assistants,
    CreateAssistant,
)

from ...utils import get_json

BASE_URL = "http://base_url"

GET_ASSISTANTS_URL = f"{BASE_URL}/assistants"
POST_ASSISTANTS_URL = f"{BASE_URL}/assistants"
POST_ASSISTANT_MODIFY_URL = f"{BASE_URL}/assistants/modify"
POST_ASSISTANT_FILES_DELETE_URL = f"{BASE_URL}/assistants/files/delete"
POST_ASSISTANT_DELETE_URL = f"{BASE_URL}/assistants/delete"

GET_ASSISTANTS = get_json("assistants/get_assistants.json")
POST_ASSISTANTS = get_json("assistants/post_assistants.json")
POST_ASSISTANT_MODIFY = get_json("assistants/post_assistant_modify.json")
POST_ASSISTANT_FILES_DELETE = get_json("assistants/post_assistant_files_delete.json")
POST_ASSISTANT_DELETE = get_json("assistants/post_assistant_delete.json")


@responses.activate
def test_get_assistants() -> None:
    responses.add(responses.GET, GET_ASSISTANTS_URL, json=GET_ASSISTANTS)
    with GigaChatSyncClient(base_url=BASE_URL) as client:
        response = client.assistants.get()

    assert isinstance(response, Assistants)
    assert len(response.data) == 2


@pytest.mark.asyncio()
async def test_aget_assistants(aioresponses_mock: aioresponses) -> None:
    aioresponses_mock.get(GET_ASSISTANTS_URL, payload=GET_ASSISTANTS)
    async with GigaChatAsyncClient(base_url=BASE_URL) as client:
        response = await client.assistants.get()

    assert isinstance(response, Assistants)
    assert len(response.data) == 2


@responses.activate
def test_post_assistants() -> None:
    responses.add(responses.POST, POST_ASSISTANTS_URL, json=POST_ASSISTANTS)
    with GigaChatSyncClient(base_url=BASE_URL) as client:
        response = client.assistants.create(model="GigaChat", name="name", instructions="123")

    assert isinstance(response, CreateAssistant)
    assert response.assistant_id == "111"


@pytest.mark.asyncio()
async def test_apost_assistants(aioresponses_mock: aioresponses) -> None:
    aioresponses_mock.post(POST_ASSISTANTS_URL, payload=POST_ASSISTANTS)
    async with GigaChatAsyncClient(base_url=BASE_URL) as client:
        response = await client.assistants.create(model="GigaChat", name="name", instructions="123")

    assert isinstance(response, CreateAssistant)
    assert response.assistant_id == "111"


@responses.activate
def test_post_assistant_modify() -> None:
    responses.add(responses.POST, POST_ASSISTANT_MODIFY_URL, json=POST_ASSISTANT_MODIFY)
    with GigaChatSyncClient(base_url=BASE_URL) as client:
        response = client.assistants.update(assistant_id="111")

    assert isinstance(response, Assistant)


@pytest.mark.asyncio()
async def test_apost_assistant_modify(aioresponses_mock: aioresponses) -> None:
    aioresponses_mock.post(POST_ASSISTANT_MODIFY_URL, payload=POST_ASSISTANT_MODIFY)
    async with GigaChatAsyncClient(base_url=BASE_URL) as client:
        response = await client.assistants.update(assistant_id="111")

    assert isinstance(response, Assistant)


@responses.activate
def test_post_assistant_files_delete() -> None:
    responses.add(responses.POST, POST_ASSISTANT_FILES_DELETE_URL, json=POST_ASSISTANT_FILES_DELETE)
    with GigaChatSyncClient(base_url=BASE_URL) as client:
        response = client.assistants.delete_file(assistant_id="111", file_id="222")

    assert isinstance(response, AssistantFileDelete)


@pytest.mark.asyncio()
async def test_apost_assistant_files_delete(aioresponses_mock: aioresponses) -> None:
    aioresponses_mock.post(POST_ASSISTANT_FILES_DELETE_URL, payload=POST_ASSISTANT_FILES_DELETE)
    async with GigaChatAsyncClient(base_url=BASE_URL) as client:
        response = await client.assistants.delete_file(assistant_id="111", file_id="222")

    assert isinstance(response, AssistantFileDelete)


@responses.activate
def test_post_assistant_delete() -> None:
    responses.add(responses.POST, POST_ASSISTANT_DELETE_URL, json=POST_ASSISTANT_DELETE)
    with GigaChatSyncClient(base_url=BASE_URL) as client:
        response = client.assistants.delete(assistant_id="111")

    assert isinstance(response, AssistantDelete)


@pytest.mark.asyncio()
async def test_apost_assistant_delete(aioresponses_mock: aioresponses) -> None:
    aioresponses_mock.post(POST_ASSISTANT_DELETE_URL, payload=POST_ASSISTANT_DELETE)
    async with GigaChatAsyncClient(base_url=BASE_URL) as client:
        response = await client.assistants.delete(assistant_id="111")

    assert isinstance(response, AssistantDelete)
