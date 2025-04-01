from typing import Any, Dict, Optional, Union

import aiohttp
import requests

from gigachat.api.utils import build_headers, build_response, build_response_async
from gigachat.models.open_api_functions import OpenApiFunctions


def _get_kwargs(
    *,
    openapi_function: str,
    access_token: Optional[str] = None,
) -> Dict[str, Any]:
    headers = build_headers(access_token)

    return {
        "method": "POST",
        "url": "/functions/convert",
        "text": openapi_function,
        "headers": headers,
    }


def sync(
    client: Union[aiohttp.ClientSession, requests.Session],
    *,
    openapi_function: str,
    access_token: Optional[str] = None,
) -> OpenApiFunctions:
    """Конвертация описание функции в формате OpenAPI в gigachat функцию"""
    kwargs = _get_kwargs(openapi_function=openapi_function, access_token=access_token)
    response = client.request(**kwargs)
    return build_response(response, OpenApiFunctions)


async def asyncio(
    client: aiohttp.ClientSession,
    *,
    openapi_function: str,
    access_token: Optional[str] = None,
) -> OpenApiFunctions:
    """Конвертация описание функции в формате OpenAPI в gigachat функцию"""
    kwargs = _get_kwargs(openapi_function=openapi_function, access_token=access_token)
    async with client.request(**kwargs) as response:
        return await build_response_async(response, OpenApiFunctions)
