"""Ingest corpus into Elasticsearch BM25 index (wiki-bm25).

Index mapping: text field only (no vectors).
Bulk chunk_size=500 (lightweight without vectors).
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from tqdm import tqdm

load_dotenv()

INDEX_NAME = "wiki-bm25"
RAW_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"

INDEX_MAPPINGS = {
    "properties": {
        "text": {"type": "text", "analyzer": "standard"},
    }
}


def get_es_client() -> Elasticsearch:
    return Elasticsearch(
        os.getenv("ELASTIC_ENDPOINT"),
        api_key=os.getenv("ELASTIC_API_KEY"),
        request_timeout=60,
    )


def _generate_actions(corpus_path: Path):
    with open(corpus_path, encoding="utf-8") as f:
        for line in f:
            doc = json.loads(line)
            yield {
                "_index": INDEX_NAME,
                "_id": doc["id"],
                "_source": {
                    "text": doc["text"],
                },
            }


def ingest(progress_callback=None):
    """Create BM25 index and bulk-ingest corpus into Elasticsearch.

    Args:
        progress_callback: Optional callback(count) called after completion.

    Returns:
        int: Number of documents indexed.

    Hints:
        - Use get_es_client() to get ES client
        - Delete existing index if it exists, then create with INDEX_MAPPINGS
        - Corpus is at RAW_DIR / "corpus.jsonl"
        - Use _generate_actions(corpus_path) for bulk data
        - Use elasticsearch.helpers.bulk() with chunk_size=500
        - Call es.indices.refresh() after bulk ingest
    """
    # TODO: Implement ES BM25 ingestion
    es = get_es_client()
    corpus_path = RAW_DIR / "corpus.jsonl"

    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
        print(f"Existing index '{INDEX_NAME}' deleted.")

    # 새로운 인덱스 생성 (INDEX_MAPPINGS 적용)
    es.indices.create(index=INDEX_NAME, mappings=INDEX_MAPPINGS)
    print(f"New index '{INDEX_NAME}' created.")

    # 벌크 적재 (chunk_size=500 설정)
    success_count, _ = bulk(
        client=es,
        actions=_generate_actions(corpus_path),
        chunk_size=500,
        stats_only=True
    )

    # 인덱스 리프레시 
    es.indices.refresh(index=INDEX_NAME)

    if progress_callback:
        progress_callback(success_count)
    
    print(f"Successfully indexed {success_count} documents to {INDEX_NAME}.")
    return success_count


if __name__ == "__main__":
    ingest()
