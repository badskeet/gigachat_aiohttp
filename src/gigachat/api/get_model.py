from typing import Any, Dict, Optional, Union

import aiohttp
import requests

from gigachat.api.utils import build_headers, build_response, build_response_async
from gigachat.models import Model


def _get_kwargs(
    *,
    model: str,
    access_token: Optional[str] = None,
) -> Dict[str, Any]:
    headers = build_headers(access_token)

    return {
        "method": "GET",
        "url": f"/models/{model}",
        "headers": headers,
    }


def sync(
    client: Union[aiohttp.ClientSession, requests.Session],
    *,
    model: str,
    access_token: Optional[str] = None,
) -> Model:
    """Возвращает объект с описанием указанной модели"""
    kwargs = _get_kwargs(model=model, access_token=access_token)
    response = client.request(**kwargs)
    return build_response(response, Model)


async def asyncio(
    client: aiohttp.ClientSession,
    *,
    model: str,
    access_token: Optional[str] = None,
) -> Model:
    """Возвращает объект с описанием указанной модели"""
    kwargs = _get_kwargs(model=model, access_token=access_token)
    async with client.request(**kwargs) as response:
        return await build_response_async(response, Model)
