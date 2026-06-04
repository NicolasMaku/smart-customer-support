import os
from flask import current_app, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from extensions import db
from models.document import Document
from services.rag_service import RAGservice


class DocumentController:
    @staticmethod
    def index():
        documents = Document.query.order_by(Document.id.desc()).all()
        return render_template("documents/index.html", documents=documents)

    @staticmethod
    def create_form():
        return render_template("documents/create.html")

    @staticmethod
    def upload():
        if 'file' not in request.files:
            flash("Aucun fichier sélectionné.", "danger")
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash("Aucun fichier sélectionné.", "danger")
            return redirect(url_for("document.create_form"))

        if file and file.filename.lower().endswith('.pdf'):
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']

            # Sauvegarder le fichier sur disque
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)

            # Sauvegarder en base
            document = Document(filename=filename, filepath=filepath)
            db.session.add(document)
            db.session.commit()

            # Construire et persister l'index vectoriel
            try:
                rag = RAGservice()
                rag.build_and_save(document.id, filepath)
            except Exception as e:
                print(f"[DocumentController] Erreur vectorisation {filepath}: {e}")

            flash("Document PDF ajouté avec succès.", "success")
            return redirect(url_for("document.index"))
        else:
            flash("Seuls les fichiers PDF sont autorisés.", "danger")
            return redirect(url_for("document.create_form"))

    @staticmethod
    def toggle(document_id):
        document = db.session.get(Document, document_id)
        if not document:
            flash("Document introuvable.", "danger")
            return redirect(url_for("document.index"))

        document.is_active = not document.is_active
        db.session.commit()

        # Supprimer le cache si désactivé, reconstruire si réactivé
        if not document.is_active:
            RAGservice.delete_cache(document_id)
        else:
            try:
                rag = RAGservice()
                rag.build_and_save(document.id, document.filepath)
            except Exception as e:
                print(f"[DocumentController] Erreur re-vectorisation: {e}")

        state = "activé" if document.is_active else "désactivé"
        flash(f"Document « {document.filename} » {state}.", "success")
        return redirect(url_for("document.index"))

    @staticmethod
    def delete(document_id):
        document = db.session.get(Document, document_id)
        if not document:
            flash("Document introuvable.", "danger")
            return redirect(url_for("document.index"))

        # Supprimer le cache vectoriel
        RAGservice.delete_cache(document_id)

        # Supprimer le fichier PDF du disque
        try:
            if os.path.exists(document.filepath):
                os.remove(document.filepath)
        except Exception as e:
            print(f"[DocumentController] Erreur suppression fichier {document.filepath}: {e}")

        db.session.delete(document)
        db.session.commit()
        flash("Document supprimé avec succès.", "success")
        return redirect(url_for("document.index"))
