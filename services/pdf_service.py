from PyPDF2 import PdfReader

class PDFservice:
    def lire_pdf(chemin_pdf, taille_chunk=300, overlap=50):
        """Lit un PDF et le découpe en chunks de ~taille_chunk mots."""
        reader = PdfReader(chemin_pdf)

        # Extraire tout le texte du PDF
        texte_complet = ""
        for page in reader.pages:
            texte_complet += page.extract_text() + " "

        # Découper en chunks
        mots = texte_complet.split()
        chunks = []

        for i in range(0, len(mots), taille_chunk - overlap):
            chunk = " ".join(mots[i : i + taille_chunk])
            if len(chunk.strip()) > 50:   # ignorer les chunks trop courts
                chunks.append(chunk.strip())

        print(f"📄 PDF lu : {len(reader.pages)} pages → {len(chunks)} chunks")
        return chunks