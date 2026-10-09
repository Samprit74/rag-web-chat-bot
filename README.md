# Chat with Websites — RAG Question Answering

A Python-based Retrieval-Augmented Generation (RAG) application that lets users ask questions about website content and receive context-grounded answers. It combines semantic search, large language models, and text-to-speech to create an interactive website question-answering experience.

## Features

- **Website content ingestion:** Load web page content from a user-provided URL.
- **Text chunking:** Split extracted content into overlapping chunks for retrieval.
- **Semantic search:** Generate embeddings and store document chunks in Chroma.
- **Context-aware answers:** Retrieve relevant passages and use an LLM to generate answers grounded in website content.
- **Voice responses:** Convert generated answers into speech using ElevenLabs.
- **Interactive chat interface:** Use Streamlit to index websites, ask questions, and clear chat history.

## Architecture

```text
              Website URL
                   |
                   v
        LangChain WebBaseLoader
                   |
                   v
      Recursive Character Text Splitter
          Chunk size: 1000
          Overlap: 200
                   |
                   v
        Hugging Face Embeddings
        all-MiniLM-L6-v2
                   |
                   v
             Chroma Store
                   |
          User asks a question
                   |
                   v
       Similarity Search (top 4)
                   |
                   v
         Retrieved Website Context
                   |
                   v
        Groq — Llama 3.1 8B Instant
                   |
             Generated Answer
                   |
                   v
           ElevenLabs TTS
                   |
                   v
             Audio Playback
```

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| User interface | Streamlit |
| RAG framework | LangChain |
| Web content loading | WebBaseLoader |
| Text splitting | RecursiveCharacterTextSplitter |
| Embeddings | Hugging Face Sentence Transformers |
| Embedding model | `all-MiniLM-L6-v2` |
| Vector database | Chroma |
| LLM inference | Groq API |
| Language model | `llama-3.1-8b-instant` |
| Text-to-speech | ElevenLabs |
| Configuration | python-dotenv |

## Project Structure

```text
rag-web-chat-bot/
├── src/
│   ├── app.py
│   ├── chains_utils.py
│   ├── vectorstore_utils.py
│   └── tts_utils.py
├── .gitignore
└── README.md
```

- `app.py` — Streamlit interface, website input, chat history, and audio playback.
- `vectorstore_utils.py` — Loads website content, splits text, creates embeddings, and builds the Chroma vector store.
- `chains_utils.py` — Retrieves relevant document chunks and generates answers using the Groq-hosted language model.
- `tts_utils.py` — Converts generated answers into audio using ElevenLabs.

## How It Works

### 1. Website ingestion

The user submits a website URL through the Streamlit sidebar. LangChain's `WebBaseLoader` retrieves the page content for processing.

### 2. Text splitting

The loaded document is divided into smaller, overlapping chunks using `RecursiveCharacterTextSplitter`. The current configuration uses a chunk size of 1,000 characters and an overlap of 200 characters.

### 3. Embedding generation and indexing

The application uses the Hugging Face `all-MiniLM-L6-v2` embedding model to represent text chunks as vectors. Chroma stores the chunks and their embeddings for similarity-based retrieval.

### 4. Context retrieval

When the user asks a question, the application performs a similarity search and retrieves up to four relevant document chunks.

### 5. LLM-based answer generation

The retrieved text is passed to a Groq-hosted Llama model. The prompt instructs the model to answer only from the supplied website context and return *“Not found on this website.”* when the answer is unavailable in that context.

### 6. Speech generation

The generated answer is sent to ElevenLabs text-to-speech, which returns audio that the application plays in the chat interface.

## Getting Started

### Prerequisites

- Python 3.10 or newer recommended
- A Groq API key
- An ElevenLabs API key
- Internet access for website retrieval and API requests

### 1. Clone the repository

```bash
git clone https://github.com/Samprit74/rag-web-chat-bot.git
cd rag-web-chat-bot
```

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux or macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install streamlit python-dotenv langchain-core langchain-community langchain-text-splitters langchain-groq langchain-huggingface langchain-chroma chromadb sentence-transformers beautifulsoup4 requests elevenlabs
```

These are the packages associated with the current implementation. Depending on package versions, compatibility adjustments may be necessary. A pinned `requirements.txt` should be added after validating a clean installation.

### 4. Configure API keys

Create a `.env` file in the repository root:

```dotenv
GROQ_API_KEY=your_groq_api_key
ELEVEN_API_KEY=your_elevenlabs_api_key
```

Replace the placeholder values with your own API keys.

**Security:** Never commit your `.env` file or publish API keys. The repository's `.gitignore` already excludes `.env`.

### 5. Run the application

From the repository root:

```bash
streamlit run src/app.py
```

Open the local URL printed in your terminal, typically:

`http://localhost:8501`

## How to Use

1. Enter a publicly accessible website URL in the sidebar.
2. Click **Parse Website** and wait for indexing to finish.
3. Enter a question in the chat input.
4. Review the answer generated from retrieved website content.
5. Listen to the audio response when speech generation succeeds.
6. Use **Clear Chat** to reset the conversation display.

The interface also provides a **Re-Index** control. Its current behavior should be connected to an explicit index-rebuilding action before being relied on.

## Limitations

- The application loads the supplied page; it is not a complete website crawler that automatically indexes every page on a domain.
- Websites may block automated requests, require authentication, or depend on JavaScript rendering.
- Answer quality depends on the content retrieved and the relevance of the selected chunks.
- The current implementation does not display source citations alongside answers.
- Audio generation depends on ElevenLabs availability, API credentials, and account usage limits.
- Persistent vector storage and session-state behavior should be tested when switching between websites.

## Future Improvements

- Add URL validation, robust exception handling, and safeguards against unsafe URL requests.
- Provide source URLs or retrieved passages alongside answers.
- Add a reproducible `requirements.txt` with tested dependency versions.
- Improve re-indexing and vector-store lifecycle management.
- Add automated tests for ingestion, retrieval, and response generation.
- Support multi-page website crawling and document formats such as PDF.
- Add retrieval evaluation and configurable chunking and search parameters.

## License

No license is currently specified. Add a license file if you intend to define the terms under which others may use or modify this project.
