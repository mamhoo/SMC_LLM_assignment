import gzip
import json
import os
from pinecone import Pinecone, ServerlessSpec

PINECONE_API_KEY = "pcsk_5La4Zc_GcDwGPWQg1hqPVmmYTAYqiRw7oG31vD6UASDbVS12XLfLeazcxZd3jSAjqThxBs"
pc = Pinecone(api_key=PINECONE_API_KEY)

if "financial-10k" not in pc.list_indexes().names():
    pc.create_index(
        name="financial-10k",
        dimension=512,
        metric="cosine"
    )
    print("✅ Index created in cloud.")

index = pc.Index("financial-10k")

BATCH_SIZE = 50  # Small batch for speed
vectors = []

with gzip.open("data/pinecone_vectors.jsonl.gz", "rt") as f:
    for line in f:
        vector = json.loads(line)
        if 'namespace' in vector:
            del vector['namespace']
        vectors.append(vector)
        
        if len(vectors) >= BATCH_SIZE:
            index.upsert(vectors=vectors)
            vectors = []
            print(f"Loaded {BATCH_SIZE} vectors...")

if vectors:
    index.upsert(vectors=vectors)

print("✅ Pinecone vectors loaded to cloud!")
