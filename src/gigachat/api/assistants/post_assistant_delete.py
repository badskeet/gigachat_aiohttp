from typing import Union

import aiohttp
import requests

from gigachat.api.utils import build_response_sync, build_response_async
from gigachat.models.assistants.assistant_delete import AssistantDelete


def _get_kwargs(assistant_id: str) -> dict:
    """Get kwargs for request."""
    url = "/assistants/delete"
    headers = {"Content-Type": "application/json"}
    kwargs = {
        "method": "POST",
        "url": url,
        "headers": headers,
        "json": {"assistant_id": assistant_id},
    }
    return kwargs


def sync(
    client: Union[aiohttp.ClientSession, requests.Session],
    assistant_id: str,
) -> AssistantDelete:
    """Delete assistant."""
    kwargs = _get_kwargs(assistant_id)
    response = client.request(**kwargs)
    return build_response_sync(response, AssistantDelete)


async def asyncio(
    client: aiohttp.ClientSession,
    assistant_id: str,
) -> AssistantDelete:
    """Delete assistant."""
    kwargs = _get_kwargs(assistant_id)
    response = await client.request(**kwargs)
    return await build_response_async(response, AssistantDelete)
