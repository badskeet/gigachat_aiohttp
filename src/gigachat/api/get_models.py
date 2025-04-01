from typing import Any, Dict, Optional, Union

import aiohttp
import requests

from gigachat.api.utils import build_headers, build_response, build_response_async
from gigachat.models import Models


def _get_kwargs(
    *,
    access_token: Optional[str] = None,
) -> Dict[str, Any]:
    headers = build_headers(access_token)

    return {
        "method": "GET",
        "url": "/models",
        "headers": headers,
    }


def sync(
    client: Union[aiohttp.ClientSession, requests.Session],
    *,
    access_token: Optional[str] = None,
) -> Models:
    """Возвращает массив объектов с данными доступных моделей"""
    kwargs = _get_kwargs(access_token=access_token)
    response = client.request(**kwargs)
    return build_response(response, Models)


async def asyncio(
    client: aiohttp.ClientSession,
    *,
    access_token: Optional[str] = None,
) -> Models:
    """Возвращает массив объектов с данными доступных моделей"""
    kwargs = _get_kwargs(access_token=access_token)
    async with client.request(**kwargs) as response:
        return await build_response_async(response, Models)
