import json
import numpy as np
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer

class IndexingAgent:
    def __init__(self):
        # Load sentence embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def chunk_text(self, text: str, chunk_size=800, overlap=150):
        # Split text into overlapping chunks
        chunks = []
        start = 0

        while start < len(text):
            # Define chunk boundaries
            end = start + chunk_size
            
            # Extract chunk
            chunk = text[start:end]
            chunks.append(chunk)
            
            # Advance with overlap
            start = end - overlap

        # Return all chunks
        return chunks

    def build_index(self, chunks: list[str], index_path: Path, map_path: Path):
        # Encode chunks into embeddings
        embeddings = self.model.encode(chunks, show_progress_bar=False)
        
        # Convert to float32 for FAISS
        embeddings = np.array(embeddings).astype("float32")

        # Create FAISS L2 index
        index = faiss.IndexFlatL2(embeddings.shape[1])
        
        # Add embeddings to index
        index.add(embeddings)

        # Persist index to disk
        faiss.write_index(index, str(index_path))

        # Create chunk index mapping
        mapping = {str(i): {"chunk_index": i} for i in range(len(chunks))}

        # Save mapping file
        map_path.write_text(json.dumps(mapping, indent=2))

        # Return chunk count
        return len(chunks)
