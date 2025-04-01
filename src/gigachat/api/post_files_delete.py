from typing import Any, Dict, Optional, Union

import aiohttp
import requests

from gigachat.api.utils import build_headers, build_response, build_response_async
from gigachat.models import DeletedFile


def _get_kwargs(
    *,
    file: str,
    access_token: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "method": "POST",
        "url": f"/files/{file}/delete",
        "files": {"file": file},
        "data": {},
        "headers": build_headers(access_token),
    }


def sync(
    client: Union[aiohttp.ClientSession, requests.Session],
    *,
    file: str,
    access_token: Optional[str] = None,
) -> DeletedFile:
    kwargs = _get_kwargs(file=file, access_token=access_token)
    response = client.request(**kwargs)
    return build_response(response, DeletedFile)


async def asyncio(
    client: aiohttp.ClientSession,
    *,
    file: str,
    access_token: Optional[str] = None,
) -> DeletedFile:
    kwargs = _get_kwargs(file=file, access_token=access_token)
    async with client.request(**kwargs) as response:
        return await build_response_async(response, DeletedFile)
