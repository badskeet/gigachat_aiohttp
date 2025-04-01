from typing import Any, Dict, Optional

import aiohttp

from gigachat.api.utils import build_headers, build_response, build_response_async
from gigachat.models.assistants import AssistantFileDelete


def _get_kwargs(
    *,
    assistant_id: str,
    file_id: str,
    access_token: Optional[str] = None,
) -> Dict[str, Any]:
    headers = build_headers(access_token)

    return {
        "method": "POST",
        "url": "/assistants/files/delete",
        "json": {
            "assistant_id": assistant_id,
            "file_id": file_id,
        },
        "headers": headers,
    }


def sync(
    client: aiohttp.ClientSession,
    *,
    assistant_id: str,
    file_id: str,
    access_token: Optional[str] = None,
) -> AssistantFileDelete:
    kwargs = _get_kwargs(assistant_id=assistant_id, file_id=file_id, access_token=access_token)
    response = client.request(**kwargs)
    return build_response(response, AssistantFileDelete)


async def asyncio(
    client: aiohttp.ClientSession,
    *,
    assistant_id: str,
    file_id: str,
    access_token: Optional[str] = None,
) -> AssistantFileDelete:
    """Удаляет файл ассистента"""
    kwargs = _get_kwargs(assistant_id=assistant_id, file_id=file_id, access_token=access_token)
    async with client.request(**kwargs) as response:
        return await build_response_async(response, AssistantFileDelete)
