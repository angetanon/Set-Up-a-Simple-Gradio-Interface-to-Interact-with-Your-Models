# Gradio Chatbot

A small Gradio interface for sending a prompt to OpenAI's `gpt-4o-mini` model and displaying its response. The project also includes a basic Gradio greeting example in `demo.py`.

## Requirements

- Python 3.10 or newer
- An OpenAI API key

## Setup

Open PowerShell in the project directory and create a virtual environment:

```powershell
py -m venv my_env
.\my_env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in the project directory and add your API key:

```dotenv
OPENAI_API_KEY=your_openai_api_key
```

Keep the key private. The `.env` file is excluded from version control.

## Run the chatbot

```powershell
python llm_chat.py
```

Open [http://127.0.0.1:7860](http://127.0.0.1:7860) in your browser. Enter a question in the input box and submit it to see the model's response.

The chatbot runs locally on `127.0.0.1:7860`. It uses `gpt-4o-mini` with a maximum of 256 output tokens and a temperature of `0.5`. Each submission is a separate prompt; the app does not maintain conversation history.

## Run the PDF QA bot

```powershell
python qabot.py
```

Upload a PDF, enter a question, and submit it. The app loads and splits the
document, creates OpenAI embeddings, stores them in Chroma, and retrieves relevant
passages to answer with `gpt-4o-mini`. Embedding and chat requests use your OpenAI
API key and may incur charges; document text is sent to OpenAI.

The QA bot uses port 7860, so stop the other chatbot before starting it. It binds
to all network interfaces and enables a public Gradio share link. Do not upload
sensitive documents to a publicly shared instance. Stop it with `Ctrl+C`.

The dependencies target LangChain 1.x: text splitters come from
`langchain_text_splitters`, OpenAI integrations from `langchain_openai`, and the
legacy `RetrievalQA` chain from `langchain_classic.chains`. If you see import
errors after updating, reinstall the declared dependencies with
`python -m pip install -r requirements.txt` in the active virtual environment.

## Run the greeting demo

To start the simpler Gradio example instead:

```powershell
python demo.py
```

## Project files

- `llm_chat.py` — OpenAI-backed chatbot interface.
- `qabot.py` - PDF question-answering interface using retrieval-augmented generation.
- `demo.py` — Minimal greeting interface.
- `requirements.txt` — Python package requirements.
- `.env` — Local OpenAI API key configuration (not committed).
