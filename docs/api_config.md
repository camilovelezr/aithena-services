# AIthena Services
## API Configuration

It is through the `config.json` file that users will made the REST API of AIthena Services aware of which models are available.

### Structure
The `config.json` file is composed of two lists:
```json
{
    "chat_models": [],
    "embed_models": []
}
```
#### Models
Each element of the list sets up the configuration for one chat model or one embedding model. The basic structure is:
```json
{
    "name": <how you will refer to the model>,
    "model": <which LLM/Embedding is this model>,
    "backend": <where is this running? ollama/azure>,
    "config": {} # specific to each backend,
    "params": { # optional
        "temperature": 0.7 # example
    }
}
```
The `name` must be unique and can be any text you'd like.

The `model` refers to the LLM used, for example `gpt-4o` or `nomic-embed-text`.

The `backend` is where this model is being ran. It can be `ollama`, `azure`, or `openai`.

#### Configuration
* Ollama:
    Configuration dictionary can be left empty ({}).
    The only parameter is:

    * `url`: where is the Ollama server hosted.

    Since this can be specified for each model, you can potentially have different Ollama servers and you would differentiate them through this `url` parameter in the config.
    
    If left empty, the `url` used would default to the environment variable `OLLAMA_HOST`

* Azure:
    There are the following parameters:
    * `endpoint`: "https://nna.openai.azure.com/",
    * `api_version`: "2024-02-01",
    * `deployment`: "gpt-4o"

    Where `endpoint` and `api_version` can be `null` and the values would default to the environment variables `AZURE_OPENAI_ENDPOINT` AND `AZURE_OPENAI_API_VERSION`.

    `deployment` must be specified for each model.

#### Params
These are model-specific parameters like `temperature`. It can be left as `null`.