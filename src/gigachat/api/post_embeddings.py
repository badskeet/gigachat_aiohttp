import json
from typing import Any, Dict, List, Optional, Union

import aiohttp
import requests

from gigachat.api.utils import build_headers, build_response, build_response_async
from gigachat.models import Embeddings


def _get_kwargs(
    *,
    input_: List[str],
    model: str,
    access_token: Optional[str] = None,
) -> Dict[str, Any]:
    headers = build_headers(access_token)
    headers["Content-Type"] = "application/json"

    return {
        "method": "POST",
        "url": "/embeddings",
        "json": {"input": input_, "model": model},
        "headers": headers,
    }


def sync(
    client: Union[aiohttp.ClientSession, requests.Session],
    *,
    input_: List[str],
    model: str,
    access_token: Optional[str] = None,
) -> Embeddings:
    kwargs = _get_kwargs(input_=input_, model=model, access_token=access_token)
    response = client.request(**kwargs)
    return build_response(response, Embeddings)


async def asyncio(
    client: aiohttp.ClientSession,
    *,
    input_: List[str],
    model: str,
    access_token: Optional[str] = None,
) -> Embeddings:
    kwargs = _get_kwargs(input_=input_, model=model, access_token=access_token)
    async with client.request(**kwargs) as response:
        return await build_response_async(response, Embeddings)
