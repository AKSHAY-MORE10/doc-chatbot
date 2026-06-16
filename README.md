# Doc Chatbot

FastAPI + ChromaDB document chat app with a browser UI, safe markdown rendering, optional API-key protection for admin actions, and a switch between a self-hosted Ollama model, Groq, or Gemini.

## Run locally

```bash
pip install -r requirements.txt
set ADMIN_API_KEY=change-me
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000.

## Configuration

These environment variables are supported:

- `LLM_PROVIDER`: `ollama`, `groq`, or `gemini`.
- `OLLAMA_BASE_URL`: Ollama server URL.
- `LLM_MODEL`: chat model name.
- `LLM_API_KEY`: API key used when `LLM_PROVIDER` is `groq` or `gemini`.
- `LLM_API_BASE_URL`: Groq or other OpenAI-compatible API base URL.
- `GEMINI_API_BASE_URL`: Gemini REST API base URL.
- `EMBED_MODEL`: embedding model name.
- `EMBED_PROVIDER`: embedding backend used for retrieval; defaults to `ollama`, or `gemini` when the Gemini provider is selected.
- `CHROMA_PATH`: persistent vector store path.
- `ALLOWED_ORIGINS`: comma-separated CORS allowlist.
- `ADMIN_API_KEY`: protects ingest and collection delete endpoints when set.
- `MAX_UPLOAD_MB`: upload size limit.

The UI now includes a model settings panel. Choose the provider, paste the API key if needed, and save the settings to the server `.env` file. Groq uses an OpenAI-compatible chat endpoint. Gemini uses Google's REST API. Retrieval embeddings stay on Ollama unless the Gemini provider is selected, in which case Gemini embeddings are used.

## Security notes

- `POST /ingest` and `DELETE /collection/{name}` require `X-API-Key` when `ADMIN_API_KEY` is configured.
- The frontend stores the admin key only in the current browser session.
- Markdown output is sanitized before being inserted into the page.
