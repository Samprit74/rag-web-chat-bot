from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


def get_vectorstore_fromurl(url):
    loader = WebBaseLoader(
        url,
        requests_kwargs={
            "timeout": 20,
            "headers": {
                "User-Agent": "Mozilla/5.0"
            },
        },
    )

    document = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    documents_chunks = text_splitter.split_documents(document)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(
        documents_chunks,
        embeddings,
        persist_directory="./chroma_db"
    )

    return vectorstore
