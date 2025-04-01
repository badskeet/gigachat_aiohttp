from typing import Any, Dict, Optional, Union

import aiohttp
import requests

from gigachat.api.utils import build_headers, build_response, build_response_async, build_response_sync
from gigachat.models.assistants import Assistants


def _get_kwargs(
    *,
    assistant_id: Optional[str] = None,
    access_token: Optional[str] = None,
) -> Dict[str, Any]:
    headers = build_headers(access_token)
    params = {
        "method": "GET",
        "url": "/assistants",
        "headers": headers,
    }
    if assistant_id:
        params["params"] = {"assistant_id": assistant_id}
    return params


def sync(
    client: Union[requests.Session, aiohttp.ClientSession],
    *,
    assistant_id: Optional[str] = None,
    access_token: Optional[str] = None,
) -> Assistants:
    """Возвращает массив объектов с данными доступных ассистентов"""
    kwargs = _get_kwargs(assistant_id=assistant_id, access_token=access_token)
    response = client.request(**kwargs)
    return build_response_sync(response, Assistants)


async def asyncio(
    client: aiohttp.ClientSession,
    *,
    assistant_id: Optional[str] = None,
    access_token: Optional[str] = None,
) -> Assistants:
    """Возвращает массив объектов с данными доступных ассистентов"""
    kwargs = _get_kwargs(assistant_id=assistant_id, access_token=access_token)
    async with client.request(**kwargs) as response:
        return await build_response_async(response, Assistants)
