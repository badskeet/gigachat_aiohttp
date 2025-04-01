from gigachat.api.get_balance import asyncio as get_balance_asyncio, sync as get_balance_sync
from gigachat.api.get_file import asyncio as get_file_asyncio, sync as get_file_sync
from gigachat.api.get_files import asyncio as get_files_asyncio, sync as get_files_sync
from gigachat.api.get_image import asyncio as get_image_asyncio, sync as get_image_sync
from gigachat.api.get_model import asyncio as get_model_asyncio, sync as get_model_sync
from gigachat.api.get_models import asyncio as get_models_asyncio, sync as get_models_sync
from gigachat.api.post_auth import asyncio as post_auth_asyncio, sync as post_auth_sync
from gigachat.api.post_chat import asyncio as post_chat_asyncio, sync as post_chat_sync
from gigachat.api.post_embeddings import asyncio as post_embeddings_asyncio, sync as post_embeddings_sync
from gigachat.api.post_files import asyncio as post_files_asyncio, sync as post_files_sync
from gigachat.api.post_files_delete import asyncio as post_files_delete_asyncio, sync as post_files_delete_sync
from gigachat.api.post_functions_convert import asyncio as post_functions_convert_asyncio, sync as post_functions_convert_sync
from gigachat.api.post_token import asyncio as post_token_asyncio, sync as post_token_sync
from gigachat.api.post_tokens_count import asyncio as post_tokens_count_asyncio, sync as post_tokens_count_sync
from gigachat.api.stream_chat import asyncio as stream_chat_asyncio, sync as stream_chat_sync

__all__ = [
    "get_balance",
    "get_file",
    "get_files",
    "get_image",
    "get_model",
    "get_models",
    "post_auth",
    "post_chat",
    "post_embeddings",
    "post_files",
    "post_files_delete",
    "post_functions_convert",
    "post_token",
    "post_tokens_count",
    "stream_chat",
]

get_balance = type("get_balance", (), {"sync": get_balance_sync, "asyncio": get_balance_asyncio})
get_file = type("get_file", (), {"sync": get_file_sync, "asyncio": get_file_asyncio})
get_files = type("get_files", (), {"sync": get_files_sync, "asyncio": get_files_asyncio})
get_image = type("get_image", (), {"sync": get_image_sync, "asyncio": get_image_asyncio})
get_model = type("get_model", (), {"sync": get_model_sync, "asyncio": get_model_asyncio})
get_models = type("get_models", (), {"sync": get_models_sync, "asyncio": get_models_asyncio})
post_auth = type("post_auth", (), {"sync": post_auth_sync, "asyncio": post_auth_asyncio})
post_chat = type("post_chat", (), {"sync": post_chat_sync, "asyncio": post_chat_asyncio})
post_embeddings = type("post_embeddings", (), {"sync": post_embeddings_sync, "asyncio": post_embeddings_asyncio})
post_files = type("post_files", (), {"sync": post_files_sync, "asyncio": post_files_asyncio})
post_files_delete = type("post_files_delete", (), {"sync": post_files_delete_sync, "asyncio": post_files_delete_asyncio})
post_functions_convert = type("post_functions_convert", (), {"sync": post_functions_convert_sync, "asyncio": post_functions_convert_asyncio})
post_token = type("post_token", (), {"sync": post_token_sync, "asyncio": post_token_asyncio})
post_tokens_count = type("post_tokens_count", (), {"sync": post_tokens_count_sync, "asyncio": post_tokens_count_asyncio})
stream_chat = type("stream_chat", (), {"sync": stream_chat_sync, "asyncio": stream_chat_asyncio})
