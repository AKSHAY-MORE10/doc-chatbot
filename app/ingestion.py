"""Document ingestion — load, chunk, and store in the vectorstore."""

import logging
import os
import tempfile

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings
from app.vectorstore import get_vectorstore

logger = logging.getLogger(__name__)


async def ingest_file(file_bytes: bytes, filename: str, collection: str) -> int:
    """Write *file_bytes* to a temp file, split into chunks, and add to the vectorstore.

    Returns the number of chunks added.
    """
    suffix = ".pdf" if filename.lower().endswith(".pdf") else ".txt"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        loader = PyPDFLoader(tmp_path) if suffix == ".pdf" else TextLoader(tmp_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            add_start_index=True,
        )
        chunks = splitter.split_documents(docs)

        for chunk in chunks:
            chunk.metadata["source_file"] = filename

        vectorstore = get_vectorstore(collection)
        vectorstore.add_documents(chunks)

        logger.info(
            "Ingested %d chunks from %s into collection %s",
            len(chunks),
            filename,
            collection,
        )
        return len(chunks)
    finally:
        os.unlink(tmp_path)
