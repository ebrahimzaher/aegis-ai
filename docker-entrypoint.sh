set -e

CHROMA_DIR="${CHROMA_PERSIST_DIR:-./data/chroma}"

if [ ! -d "$CHROMA_DIR" ] || [ -z "$(ls -A "$CHROMA_DIR" 2>/dev/null)" ]; then
    echo "Vector store empty at $CHROMA_DIR -- running ingestion..."
    python -m rag.ingest
else
    echo "Vector store already populated at $CHROMA_DIR -- skipping ingestion."
fi

exec uvicorn main:app --host 0.0.0.0 --port 8000