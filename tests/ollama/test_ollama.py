"""Tests for Ollama."""
import asyncio
from pathlib import Path
import httpx
import ollama
import pytest
import numpy as np

# pytest_plugins = ('pytest_asyncio',)

# OLLAMA_HOST use by ollama client

# create a single client
async_client = ollama.AsyncClient(host='http://localhost:11434')
client = ollama.Client(host='http://localhost:11434')

RUN_COUNT = 4
PERF_LOGFILE = Path("perf.log")

print(f"client created once.... {async_client._client._base_url}")


@pytest.fixture
def prompt():
    message = {'role': 'user', 'content': 'Why is the sky blue?'}
    return message


# chat asynchronously
async def async_chat(messages):
    """Async chat."""
    try:
        async for resp_chunk in await async_client.chat(model='llama3.1', messages=messages, stream=True):
            print(resp_chunk['message']['content'], end='', flush=True)
        return resp_chunk
    except ollama.ResponseError as e:
        print('Error:', e.error)


def chat(messages, stream=False):
    """Chat."""
    try:
        if stream:
            resp_chunks = client.chat(model='llama3.1', messages=messages, stream=stream)
            for chunk in resp_chunks:
                print(chunk['message']['content'], end='', flush=True)
            return chunk
        
        resp = client.chat(model='llama3.1', messages=messages, stream=stream)
        print(resp)
        return resp
    except ollama.ResponseError as e:
        print('Error:', e.error)


@pytest.mark.asyncio
async def test_chat(prompt):
    """Test async chat."""
    total_durations = []
    for i in range(RUN_COUNT):
        messages = [prompt]
        res = await async_chat(messages)
        print(res)
        assert res["done"] and res["done_reason"] == "stop"
        log_stats(res)
        total_durations.append(res["total_duration"])
    avg_total_duration = np.mean(np.array(total_durations)) * 10**-9
    with PERF_LOGFILE.open("a+") as fw:
        fw.write(f"async:True, stream:True, avg_total_duration: {avg_total_duration}s \n")


def test_chat_sync_stream(prompt):
    """Test synchronous chat as a stream."""
    total_durations = []
    for i in range(RUN_COUNT):
        messages = [prompt]
        res = chat(messages, stream=True)
        print(res)
        assert res["done"] and res["done_reason"] == "stop"
        log_stats(res)
        total_durations.append(res["total_duration"])
    avg_total_duration = np.mean(np.array(total_durations)) * 10**-9
    with PERF_LOGFILE.open("a+") as fw:
        fw.write(f"async:False, stream:True, avg_total_duration: {avg_total_duration}s \n")


def test_chat_sync(prompt):
    """Test synchronous chat."""
    total_durations = []
    for i in range(RUN_COUNT):
        messages = [prompt]
        res = chat(messages, stream=False)
        print(res)
        assert res["done"] and res["done_reason"] == "stop"
        log_stats(res)
        total_durations.append(res["total_duration"])
    avg_total_duration = np.mean(np.array(total_durations)) * 10**-9
    with PERF_LOGFILE.open("a+") as fw:
        fw.write(f"async:False, stream:False, avg_total_duration: {avg_total_duration}s \n")


def log_stats(res):
    token_per_second = res["eval_count"] / res["eval_duration"] * 10**9
    total_duration = res["total_duration"] / 10**9
    load_duration = res["load_duration"] / 10**9
    prompt_eval_duration = res["prompt_eval_duration"] / 10**9
    eval_duration = res["eval_duration"] / 10**9
    print(f"token per second: {token_per_second}")
    print(f"total duration: {total_duration}")
    print(f"load duration: {load_duration}")
    print(f"prompt eval duration: {prompt_eval_duration}")
    print(f"eval duration: {eval_duration}")
