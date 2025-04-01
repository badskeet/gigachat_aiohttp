from http import HTTPStatus
from typing import Any, AsyncIterator, Dict, Iterator, Optional

import aiohttp

from gigachat.api.utils import build_headers, build_x_headers, parse_chunk
from gigachat.exceptions import AuthenticationError, ResponseError
from gigachat.models.threads import ThreadCompletionChunk, ThreadRunOptions

EVENT_STREAM = "text/event-stream"


def _get_kwargs(
    *,
    thread_id: str,
    thread_options: Optional[ThreadRunOptions] = None,
    update_interval: Optional[int] = None,
    access_token: Optional[str] = None,
) -> Dict[str, Any]:
    headers = build_headers(access_token)
    thread_options_dict = {}
    if thread_options:
        thread_options_dict = thread_options.dict(exclude_none=True)
    params = {
        "method": "POST",
        "url": "/threads/messages/rerun",
        "headers": headers,
        "json": {
            **thread_options_dict,
            **{
                "thread_id": thread_id,
                "update_interval": update_interval,
                "stream": True,
            },
        },
    }
    return params


def _check_content_type(response: aiohttp.ClientResponse) -> None:
    content_type, _, _ = response.headers.get("content-type", "").partition(";")
    if content_type != EVENT_STREAM:
        raise aiohttp.ClientError(f"Expected response Content-Type to be '{EVENT_STREAM}', got {content_type!r}")


def _check_response(response: aiohttp.ClientResponse) -> None:
    if response.status == HTTPStatus.OK:
        _check_content_type(response)
    elif response.status == HTTPStatus.UNAUTHORIZED:
        raise AuthenticationError(str(response.url), response.status, response.content.read(), response.headers)
    else:
        raise ResponseError(str(response.url), response.status, response.content.read(), response.headers)


async def _acheck_response(response: aiohttp.ClientResponse) -> None:
    if response.status == HTTPStatus.OK:
        _check_content_type(response)
    elif response.status == HTTPStatus.UNAUTHORIZED:
        raise AuthenticationError(str(response.url), response.status, await response.read(), response.headers)
    else:
        raise ResponseError(str(response.url), response.status, await response.read(), response.headers)


def sync(
    client: aiohttp.ClientSession,
    *,
    thread_id: str,
    thread_options: Optional[ThreadRunOptions] = None,
    update_interval: Optional[int] = None,
    access_token: Optional[str] = None,
) -> Iterator[ThreadCompletionChunk]:
    """Перегенерация ответа модели"""
    kwargs = _get_kwargs(
        thread_id=thread_id,
        thread_options=thread_options,
        update_interval=update_interval,
        access_token=access_token,
    )
    response = client.request(**kwargs)
    _check_response(response)
    x_headers = build_x_headers(response)
    for line in response.content.iter_any():
        if chunk := parse_chunk(line.decode(), ThreadCompletionChunk):
            chunk.x_headers = x_headers
            yield chunk


async def asyncio(
    client: aiohttp.ClientSession,
    *,
    thread_id: str,
    thread_options: Optional[ThreadRunOptions] = None,
    update_interval: Optional[int] = None,
    access_token: Optional[str] = None,
) -> AsyncIterator[ThreadCompletionChunk]:
    """Перегенерация ответа модели"""
    kwargs = _get_kwargs(
        thread_id=thread_id,
        thread_options=thread_options,
        update_interval=update_interval,
        access_token=access_token,
    )
    async with client.request(**kwargs) as response:
        await _acheck_response(response)
        x_headers = build_x_headers(response)
        async for line in response.content.iter_any():
            if chunk := parse_chunk(line.decode(), ThreadCompletionChunk):
                chunk.x_headers = x_headers
                yield chunk
