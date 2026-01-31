import json
import numpy as np
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer

class QAAgent:
    def __init__(self):
        # Load sentence embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def retrieve(self, document_id: int, question: str, top_k: int = 5):
        # Resolve index and mapping paths
        index_path = Path("storage/indexes") / f"{document_id}.faiss"
        map_path = Path("storage/indexes") / f"{document_id}_map.json"

        # Ensure index exists
        if not index_path.exists() or not map_path.exists():
            raise ValueError("Vector index not found. Please index the document first.")

        # Load FAISS index and metadata
        index = faiss.read_index(str(index_path))
        mapping = json.loads(map_path.read_text())

        # Encode question embedding
        q_emb = self.model.encode([question])
        q_emb = np.array(q_emb).astype("float32")

        # Perform similarity search
        distances, indices = index.search(q_emb, top_k)

        # Build ranked result set
        results = []
        for rank, idx in enumerate(indices[0]):
            if idx == -1:
                continue
            results.append({
                "vector_id": int(idx),
                "distance": float(distances[0][rank]),
                "preview": mapping.get(str(idx), "")
            })

        # Return retrieval results
        return results

    def answer_from_context(self, question: str, contexts: list[str]) -> str:
        """
        Return a grounded, extractive answer without LLM generation.
        """
        # Handle empty context
        if not contexts:
            return "I don’t have enough information in the uploaded document to answer that."

        # Concatenate top context excerpts
        joined = "\n\n---\n\n".join(contexts[:3])
        return (
            "Based on the uploaded document, the most relevant excerpts are:\n\n"
            f"{joined}\n\n"
            "."
        )
