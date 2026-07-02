import gzip
import json
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY", "dummy"), host="http://localhost:5080")
index = pc.Index("financial-10k")

with gzip.open("data/pinecone_vectors.jsonl.gz", "rt") as f:
    for line in f:
        vector = json.loads(line)
        index.upsert([vector])

print("Pinecone vectors loaded successfully!")