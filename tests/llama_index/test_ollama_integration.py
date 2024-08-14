"""
Ollama integration with llama index.

NOTE all performance metrics are removed by the llama-index wrapper.
"""

from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage
import pytest
import logging

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__file__)

llm = Ollama(model="llama3.1:latest", request_timeout=120.0)


def test_chat(user_message: dict[str, str]):
    """Sync implementation of ollama chat integration."""
    messages = [ChatMessage(**user_message)]
    resp = llm.chat(messages)
    logger.info(f"output: {resp.content}")


def test_chat_sync_stream(user_message):
    """Sync stream implementation of ollama chat integration."""
    messages = [ChatMessage(**user_message)]
    chunks = llm.stream_chat(messages)
    for chunk in chunks:
         print(chunk.delta, end="", flush=True)
    logger.info(f"output: {chunk.content}")
     

@pytest.mark.asyncio
async def test_chat_async(user_message: dict[str, str]):
    """Async implementation of ollama chat integration."""
    messages = [ChatMessage(**user_message)]
    resp = await llm.achat(messages)
    logger.info(f"output: {resp.content}")


@pytest.mark.asyncio
async def test_chat_async_stream(user_message: dict[str, str]):
    """Async stream implementation of ollama chat integration."""
    messages = [ChatMessage(**user_message)]
    chunks = await llm.astream_chat(messages)
    async for chunk in chunks: # NOTE the async for iterating the async generator
         print(chunk.delta, end="", flush=True)



