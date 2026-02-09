"""Ingest embeddings into Pinecone vector index.

Batch upsert: 100 vectors per call.
Metadata: text truncated to 1000 chars (40KB limit).
"""

import json
import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from pinecone import Pinecone
from tqdm import tqdm

load_dotenv()

RAW_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "processed"

BATCH_SIZE = 100
TEXT_LIMIT = 1000  # metadata text truncation


def ingest(progress_callback=None):
    """Batch upsert embeddings into Pinecone vector index.

    Args:
        progress_callback: Optional callback(current, total) for progress updates.

    Returns:
        int: Number of vectors upserted.

    Hints:
        - Load embeddings from PROCESSED_DIR / "embeddings.npy"
        - Load IDs from PROCESSED_DIR / "embedding_ids.json"
        - Load texts from RAW_DIR / "corpus.jsonl" for metadata
        - Connect: Pinecone(api_key=...) → pc.Index(index_name)
        - Upsert format: {"id": ..., "values": [...], "metadata": {"text": ...}}
        - Batch size: BATCH_SIZE (100), truncate text to TEXT_LIMIT (1000) chars
    """
    # TODO: Implement Pinecone upsert
    # 파일 로드 (임베딩, ID, 원본 텍스트)
    embeddings = np.load(PROCESSED_DIR / "embeddings.npy")
    with open(PROCESSED_DIR / "embedding_ids.json", "r") as f:
        ids = json.load(f)
    
    # 원본 텍스트 로드 (metadata용)
    texts = {}
    with open(RAW_DIR / "corpus.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            doc = json.loads(line)
            texts[doc["id"]] = doc["text"]

    # Pinecone 연결
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = os.getenv("PINECONE_INDEX")
    index = pc.Index(index_name)

    # 배치 업서트 (BATCH_SIZE = 100)
    total = len(ids)
    for i in tqdm(range(0, total, BATCH_SIZE), desc="Upserting to Pinecone"):
        batch_end = i + BATCH_SIZE
        batch_ids = ids[i:batch_end]
        batch_vectors = embeddings[i:batch_end].tolist()  
        
        records = []
        for doc_id, vector in zip(batch_ids, batch_vectors):
            metadata = {"text": texts[doc_id][:TEXT_LIMIT]}
            records.append({
                "id": doc_id, 
                "values": vector, 
                "metadata": metadata
            })
        
        # Pinecone에 적재
        index.upsert(vectors=records)
        
        if progress_callback:
            progress_callback(min(batch_end, total), total)

    print(f"Successfully upserted {total} vectors to Pinecone.")
    return total


if __name__ == "__main__":
    ingest()
