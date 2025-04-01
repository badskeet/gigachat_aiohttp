from typing import Any, Dict, Literal, Optional, Union

import aiohttp
import requests

from gigachat._types import FileTypes
from gigachat.api.utils import build_headers, build_response, build_response_async
from gigachat.models import UploadedFile


def _get_kwargs(
    *,
    file: FileTypes,
    purpose: Literal["general", "assistant"] = "general",
    access_token: Optional[str] = None,
) -> Dict[str, Any]:
    headers = build_headers(access_token)

    return {
        "method": "POST",
        "url": "/files",
        "data": {"purpose": purpose},
        "files": {"file": file},
        "headers": headers,
    }


def sync(
    client: Union[aiohttp.ClientSession, requests.Session],
    *,
    file: FileTypes,
    purpose: Literal["general", "assistant"] = "general",
    access_token: Optional[str] = None,
) -> UploadedFile:
    kwargs = _get_kwargs(file=file, purpose=purpose, access_token=access_token)
    response = client.request(**kwargs)
    return build_response(response, UploadedFile)


async def asyncio(
    client: aiohttp.ClientSession,
    *,
    file: FileTypes,
    purpose: Literal["general", "assistant"] = "general",
    access_token: Optional[str] = None,
) -> UploadedFile:
    kwargs = _get_kwargs(file=file, purpose=purpose, access_token=access_token)
    async with client.request(**kwargs) as response:
        return await build_response_async(response, UploadedFile)
