import gzip
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

INDEX_NAME = "financial-10k"
DIMENSION = 512          

# Load .env from backend/app/.env
env_path = Path(__file__).parent.parent / "backend" / "app" / ".env"
load_dotenv(dotenv_path=env_path)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if not PINECONE_API_KEY:
    raise ValueError(f"PINECONE_API_KEY not found in {env_path}")

pc = Pinecone(api_key=PINECONE_API_KEY)

# === Handle index creation / dimension mismatch ===
existing_indexes = [idx.name for idx in pc.list_indexes()]

if INDEX_NAME in existing_indexes:
    # Check current dimension
    index_info = pc.describe_index(INDEX_NAME)
    current_dim = index_info.dimension
    
    if current_dim != DIMENSION:
        print(f"Dimension mismatch: Index has {current_dim}, but vectors are {DIMENSION}")
        print("Deleting existing index...")
        pc.delete_index(INDEX_NAME)
        print("Index deleted.")
        existing_indexes.remove(INDEX_NAME)

if INDEX_NAME not in existing_indexes:
    print(f"Creating new index with dimension {DIMENSION}...")
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    print("Index created successfully.")

index = pc.Index(INDEX_NAME)
print(f"Connected to index '{INDEX_NAME}' (dimension={DIMENSION})")

# ====================== LOAD VECTORS ======================
BATCH_SIZE = 50
vectors = []

print("📤 Loading vectors from data/pinecone_vectors.jsonl.gz ...")

with gzip.open("data/pinecone_vectors.jsonl.gz", "rt", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
        vector = json.loads(line)
        if 'namespace' in vector:
            del vector['namespace']
        vectors.append(vector)
        
        if len(vectors) >= BATCH_SIZE:
            index.upsert(vectors=vectors)
            vectors = []
            print(f"Uploaded batch of {BATCH_SIZE} vectors (Total: {line_num})")

if vectors:
    index.upsert(vectors=vectors)
    print(f"Uploaded final batch of {len(vectors)} vectors")

print("\nAll Pinecone vectors loaded successfully!")
