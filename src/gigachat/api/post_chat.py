import json
from typing import Any, Dict, Optional, Union

import aiohttp
import requests

from gigachat.api.utils import build_headers, build_response, build_response_async
from gigachat.models import Chat, ChatCompletion


def _get_kwargs(
    *,
    chat: Chat,
    access_token: Optional[str] = None,
) -> Dict[str, Any]:
    headers = build_headers(access_token)
    headers["Content-Type"] = "application/json"

    return {
        "method": "POST",
        "url": "/chat/completions",
        "json": chat.dict(exclude_none=True, by_alias=True, exclude={"stream"}),
        "headers": headers,
    }


def sync(
    client: Union[aiohttp.ClientSession, requests.Session],
    *,
    chat: Chat,
    access_token: Optional[str] = None,
) -> ChatCompletion:
    kwargs = _get_kwargs(chat=chat, access_token=access_token)
    response = client.request(**kwargs)
    return build_response(response, ChatCompletion)


async def asyncio(
    client: aiohttp.ClientSession,
    *,
    chat: Chat,
    access_token: Optional[str] = None,
) -> ChatCompletion:
    kwargs = _get_kwargs(chat=chat, access_token=access_token)
    async with client.request(**kwargs) as response:
        return await build_response_async(response, ChatCompletion)
