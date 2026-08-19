# Personal PDF Chatbot

A Streamlit app that lets you upload a PDF and ask questions about it. It uses a Retrieval-Augmented Generation (RAG) pipeline — the document is chunked, embedded, and stored in a vector store, and the most relevant chunks are pulled into the prompt so the model answers strictly from the PDF's content.

## Features

- Upload any PDF through a simple web UI
- Automatic text extraction, chunking, and embedding of the document
- Semantic search over the document to retrieve relevant context per question
- Streaming chat responses powered by OpenAI

## Tech Stack

- [Streamlit](https://streamlit.io/) — chat UI
- [LangChain](https://www.langchain.com/) — document loading, splitting, and vector store integration
- [Chroma](https://www.trychroma.com/) — in-memory vector store
- [OpenAI API](https://platform.openai.com/) — embeddings (`text-embedding-3-small`) and chat completions (`gpt-3.5-turbo`)

## Requirements

- Python 3.10–3.12
- An [OpenAI API key](https://platform.openai.com/api-keys)
- [uv](https://docs.astral.sh/uv/) for dependency management

## Installation

```bash
git clone https://github.com/Anka256/Personal-PDF-Chatbot.git
cd Personal-PDF-Chatbot
uv sync
```

## Configuration

Copy [.env.example](.env.example) to `.env` and fill in your OpenAI API key:

```bash
cp .env.example .env
```

```
OPENAI_API_KEY=your-api-key-here
```

## Usage

```bash
uv run streamlit run app.py
```

Then open the URL Streamlit prints (usually `http://localhost:8501`), upload a PDF, wait for it to finish processing, and start asking questions in the chat box.

## Project Structure

```
.
├── app.py    # Streamlit UI and chat loop
├── rag.py    # PDF loading, chunking, and vector store creation
└── pyproject.toml
```

## Limitations

- The vector store is held in memory (`st.session_state`) and is not persisted — reloading the page requires re-uploading the PDF.
- Only one PDF can be active per session.
- Answers are only as good as the retrieved context; very large or poorly structured PDFs may reduce answer quality.

## License

This project is licensed under the [MIT License](LICENSE).
