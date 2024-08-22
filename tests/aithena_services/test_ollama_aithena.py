# mypy: disable-error-code="import-untyped"
"""Ollama Aithena Service Test Module."""

# pylint: disable=C0415, W0621, C0413, C0103
import pytest
import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(), override=True)
# this is after dotenv in case .env for tests
# defines different values for these variables
from aithena_services.envvars import OLLAMA_AVAILABLE, OLLAMA_HOST
from aithena_services.llms.types import ChatResponse, Message


def test_ollama_available():
    """Test OllamaAvailable from Aithena Services."""
    ol_av = OLLAMA_HOST is not None
    assert OLLAMA_AVAILABLE == ol_av


@pytest.fixture
def ollama_imp():
    """Return Ollama object from Aithena Services."""
    if not OLLAMA_AVAILABLE:
        pytest.skip("Ollama not available")
    from aithena_services.llms import Ollama

    return Ollama


def test_ollama_list_models(ollama_imp):
    """Test Aithena Services Ollama List Models."""

    Ollama = ollama_imp
    req = requests.get(OLLAMA_HOST + "/api/tags", timeout=40).json()["models"]
    names_req = [x["name"] for x in req]
    names_obj = Ollama.list_models()
    assert names_req == names_obj


def test_ollama_llama31_response_message(ollama_imp, math_question):
    """Test Aithena Services Ollama Llama3.1.

    Test response contains Message.
    """
    Ollama = ollama_imp
    llama = Ollama(model="llama3.1")
    response = llama.chat(math_question)
    assert isinstance(response.message, Message)


def test_ollama_llama31_response_message_content(ollama_imp, math_question):
    """Test Aithena Services Ollama Llama3.1.

    Test response contains Message.
    """
    Ollama = ollama_imp
    llama = Ollama(model="llama3.1")
    response = llama.chat(math_question)
    assert isinstance(response.message.content, str)


def test_ollama_llama31_response(ollama_imp, math_question):
    """Test Aithena Services Ollama Llama3.1.

    Test response object.
    """
    Ollama = ollama_imp
    llama = Ollama(model="llama3.1")
    response = llama.chat(math_question)
    assert isinstance(response, ChatResponse)


def test_ollama_llama31_vs_llamaindex(ollama_imp, math_question):
    """Test Aithena Services Ollama Llama3.1.

    Test response object of Aithena vs LlamaIndex.
    """
    from llama_index.core.llms import ChatMessage
    from llama_index.llms.ollama import Ollama as LlamaIndexOllama

    Ollama = ollama_imp
    llama = Ollama(model="llama3.1")
    response = llama.chat(math_question)
    llama2 = LlamaIndexOllama(model="llama3.1")
    response2 = llama2.chat([ChatMessage(**x) for x in math_question])
    assert isinstance(response.message, Message)
    assert isinstance(response2.message, ChatMessage)
    for arg in response2.__dict__:
        if arg == "message":
            assert (
                getattr(response, arg).content.__class__
                == getattr(response2, arg).content.__class__
            )
        else:
            assert getattr(response, arg).__class__ == getattr(response2, arg).__class__


def test_ollama_llama31_stream_story(ollama_imp, text_question_1):
    """Test Aithena Services Ollama Llama3.1.

    Test response object in stream chat.
    """
    Ollama = ollama_imp
    llama = Ollama(model="llama3.1")
    response = llama.stream_chat(text_question_1)
    for r in response:
        assert isinstance(r, ChatResponse)
        assert isinstance(r.message, Message)
        assert isinstance(r.message.content, str)
        assert isinstance(r.delta, str)


def test_ollama_llama31_args1(ollama_imp, text_question_1):
    """Test Aithena Services Ollama Llama3.1.

    Test response with specific params with two instances
    of Aithena Services Ollama Llama3.1.
    """
    Ollama = ollama_imp
    llama = Ollama(model="llama3.1", temperature=0, seed=82)
    response1 = llama.chat(text_question_1)
    llama2 = Ollama(model="llama3.1", temperature=0, seed=82)
    response2 = llama2.chat(text_question_1)
    assert response1.message == response2.message


def test_ollama_llama31_args2(ollama_imp, query_1):
    """Test Aithena Services Ollama Llama3.1.

    Test response with specific params with Aithena
    vs REST API.
    """
    Ollama = ollama_imp
    llama = Ollama(model="llama3.1", temperature=0, seed=12)
    response1 = llama.chat(query_1)
    data = {
        "model": "llama3.1",
        "messages": [x.as_json() for x in query_1],
        "options": {"seed": 12, "temperature": 0},
        "stream": False,
    }
    response2 = requests.post(OLLAMA_HOST + "/api/chat", json=data, timeout=40).json()[
        "message"
    ]["content"]

    assert response1.message.content == response2


def test_ollama_llama31_args3(ollama_imp, query_1):
    """Test Aithena Services Ollama Llama3.1.

    Test response with specific params with Aithena
    vs LlamaIndex.
    """
    from llama_index.core.llms import ChatMessage
    from llama_index.llms.ollama import Ollama as LlamaIndexOllama

    Ollama = ollama_imp
    llama = Ollama(model="llama3.1", temperature=0, seed=12)
    response1 = llama.chat(query_1)
    response2 = LlamaIndexOllama(model="llama3.1", temperature=0, seed=12).chat(
        [ChatMessage(**x.as_json()) for x in query_1]
    )

    assert response1.message.content == response2.message.content
