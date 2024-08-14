"""Environment Variable Configuration for Aithena Services."""

import os

OPENAI_KEY_ENV = os.getenv("OPENAI_API_KEY", None)
OLLAMA_URL_ENV = os.getenv("OLLAMA_URL", None)

# ----AzureOpenAI----
# ---required---
AZURE_OPENAI_KEY_ENV = os.environ.get("AZURE_OPENAI_API_KEY", None)
AZURE_OPENAI_ENDPOINT_ENV = os.environ.get("AZURE_OPENAI_ENDPOINT", None)
AZURE_OPENAI_API_VERSION_ENV = os.environ.get("AZURE_OPENAI_API_VERSION", None)
# ---optional---
AZURE_OPENAI_DEPLOYMENT_NAME_ENV = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", None)
AZURE_OPENAI_MODEL_ENV = os.environ.get("AZURE_OPENAI_MODEL", None)
AZURE_OPENAI_ENV_DICT = {
    "api_key": AZURE_OPENAI_KEY_ENV,
    "azure_endpoint": AZURE_OPENAI_ENDPOINT_ENV,
    "api_version": AZURE_OPENAI_API_VERSION_ENV,
    "model": AZURE_OPENAI_MODEL_ENV,
    "engine": AZURE_OPENAI_DEPLOYMENT_NAME_ENV,
}

OPENAI_AVAILABLE = OPENAI_KEY_ENV is not None
OLLAMA_AVAILABLE = OLLAMA_URL_ENV is not None
AZURE_OPENAI_AVAILABLE = (
    (AZURE_OPENAI_KEY_ENV is not None)
    and (AZURE_OPENAI_ENDPOINT_ENV is not None)
    and (AZURE_OPENAI_API_VERSION_ENV is not None)
)


__all__ = [
    "OPENAI_AVAILABLE",
    "OLLAMA_AVAILABLE",
    "OPENAI_KEY_ENV",
    "OLLAMA_URL_ENV",
    "AZURE_OPENAI_AVAILABLE",
    "AZURE_OPENAI_ENV_DICT",
]
