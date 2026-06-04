from services.pdf_service import PDFservice
from sentence_transformers import SentenceTransformer
import os
import pickle
import numpy as np
import faiss


VECTORS_DIR = os.path.join("uploads", "vectors")


class RAGservice:
    def __init__(self):
        self.embed_model = SentenceTransformer(os.environ.get("EMBED_MODEL", ""))
        self.top_k = 3
        os.makedirs(VECTORS_DIR, exist_ok=True)
        print("✅ Modèle chargé.")

    # ------------------------------------------------------------------
    # Chemins de cache pour un document donné
    # ------------------------------------------------------------------
    @staticmethod
    def _cache_paths(doc_id: int):
        folder = os.path.join(VECTORS_DIR, str(doc_id))
        return folder, os.path.join(folder, "index.faiss"), os.path.join(folder, "chunks.pkl")

    # ------------------------------------------------------------------
    # Construire et sauvegarder l'index d'un seul document
    # ------------------------------------------------------------------
    def build_and_save(self, doc_id: int, filepath: str):
        """Lit le PDF, crée l'index FAISS et le persiste sur disque."""
        chunks = PDFservice.lire_pdf(filepath)
        if not chunks:
            return

        embeddings = self.embed_model.encode(chunks, show_progress_bar=False)
        embeddings = np.array(embeddings, dtype="float32")

        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)

        folder, index_path, chunks_path = self._cache_paths(doc_id)
        os.makedirs(folder, exist_ok=True)
        faiss.write_index(index, index_path)
        with open(chunks_path, "wb") as f:
            pickle.dump(chunks, f)

        print(f"[RAGservice] Index sauvegardé pour doc {doc_id} ({len(chunks)} chunks)")

    # ------------------------------------------------------------------
    # Supprimer le cache d'un document (suppression ou toggle off)
    # ------------------------------------------------------------------
    @staticmethod
    def delete_cache(doc_id: int):
        folder, index_path, chunks_path = RAGservice._cache_paths(doc_id)
        for path in (index_path, chunks_path):
            if os.path.exists(path):
                os.remove(path)
        if os.path.isdir(folder) and not os.listdir(folder):
            os.rmdir(folder)
        print(f"[RAGservice] Cache supprimé pour doc {doc_id}")

    # ------------------------------------------------------------------
    # Recherche sur tous les documents actifs
    # ------------------------------------------------------------------
    def rag_research(self, question: str, doc_ids_filepaths: list[tuple]):
        """
        doc_ids_filepaths : liste de (doc_id, filepath) pour les docs actifs.
        Charge les index FAISS persistés (ou les reconstruit si absents),
        fusionne tout et retourne les top-k chunks les plus pertinents.
        """
        if not doc_ids_filepaths:
            return ""

        all_chunks = []
        all_embeddings = []

        for doc_id, filepath in doc_ids_filepaths:
            folder, index_path, chunks_path = self._cache_paths(doc_id)

            # Reconstruire le cache si absent
            if not os.path.exists(index_path) or not os.path.exists(chunks_path):
                print(f"[RAGservice] Cache absent pour doc {doc_id}, reconstruction…")
                self.build_and_save(doc_id, filepath)

            if not os.path.exists(chunks_path):
                continue  # PDF illisible, on saute

            with open(chunks_path, "rb") as f:
                chunks = pickle.load(f)

            cached_index = faiss.read_index(index_path)

            # Extraire les vecteurs de l'index pour la fusion
            n = cached_index.ntotal
            dim = cached_index.d
            vecs = np.zeros((n, dim), dtype="float32")
            faiss.extract_index_ivf  # juste pour vérifier l'import
            # IndexFlatL2 supporte reconstruct_n
            cached_index.reconstruct_n(0, n, vecs)

            all_chunks.extend(chunks)
            all_embeddings.append(vecs)

        if not all_chunks:
            return ""

        # Fusionner tous les embeddings dans un seul index
        all_vecs = np.vstack(all_embeddings).astype("float32")
        merged_index = faiss.IndexFlatL2(all_vecs.shape[1])
        merged_index.add(all_vecs)

        # Recherche
        q_vec = self.embed_model.encode([question])
        q_vec = np.array(q_vec, dtype="float32")
        k = min(self.top_k, len(all_chunks))
        distances, indices = merged_index.search(q_vec, k)

        contexte = "\n\n".join(all_chunks[i] for i in indices[0])
        return contexte
