from services.pdf_service import PDFservice
from sentence_transformers import SentenceTransformer
import os
import numpy as np
import faiss


class RAGservice:
    def __init__(self):
        self.embed_model = SentenceTransformer(os.environ.get("EMBED_MODEL", ""))
        self.top_k = 3

        self.documents = []    # Textes originaux
        self.index     = None  # Index FAISS
        print("✅ Modèle chargé.")

    
    def creer_index(self, chunks, embed_model):
        embeddings = embed_model.encode(chunks, show_progress_bar=True)
        embeddings = np.array(embeddings, dtype="float32")
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        return index


    def rag_pdf(self, question, chunks, index, embed_model, k=3):
        # Recherche
        q_vec = embed_model.encode([question])
        q_vec = np.array(q_vec, dtype="float32")
        distances, indices = index.search(q_vec, k)

        contexte = "\n\n".join(chunks[i] for i in indices[0])

        # # Prompt
        # prompt = f"""Voici des extraits d'un document PDF. Réponds à la question.

        #         EXTRAITS :
        #         {contexte}

        #         QUESTION : {question}

        #         RÉPONSE (basée uniquement sur les extraits ci-dessus) :"""

        # # Génération
        # resp = chat(
        #     model="qwen2.5:0.5b",
        #     messages=[{"role": "user", "content": prompt}]
        # )
        # return resp["message"]["content"]
        return contexte

    def rag_research(self, question, filepaths: list[str]):
        """
        Construit un index FAISS à partir de tous les PDFs fournis
        et retourne les chunks les plus pertinents pour la question.
        """
        if not filepaths:
            return ""

        # Lire et agréger les chunks de tous les documents
        all_chunks = []
        for path in filepaths:
            try:
                chunks = PDFservice.lire_pdf(path)
                all_chunks.extend(chunks)
            except Exception as e:
                print(f"[RAGservice] Erreur lecture {path}: {e}")

        if not all_chunks:
            return ""

        # Créer l'index sur l'ensemble des chunks
        index = self.creer_index(all_chunks, self.embed_model)

        contexte = self.rag_pdf(question, all_chunks, index, self.embed_model)
        return contexte