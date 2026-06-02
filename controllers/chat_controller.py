import os
from flask import current_app, jsonify, render_template, request

import google.generativeai as genai

from models.document import Document


class ChatController:
    @staticmethod
    def index():
        return render_template("chat/index.html")

    @staticmethod
    def send_message():
        data = request.get_json()
        user_message = (data or {}).get("message", "").strip()
        if not user_message:
            return jsonify({"error": "Message vide."}), 400

        api_key = current_app.config.get("GEMINI_API_KEY", "")
        if not api_key:
            return jsonify({
                "reply": "⚠️ Clé API Gemini non configurée. Veuillez définir la variable d'environnement `GEMINI_API_KEY`."
            }), 200

        genai.configure(api_key=api_key)

        # Retrieve all PDFs from DB and upload them to Gemini File API
        documents = Document.query.all()
        uploaded_files = []
        for doc in documents:
            if os.path.exists(doc.filepath):
                try:
                    uploaded_file = genai.upload_file(
                        doc.filepath,
                        mime_type="application/pdf"
                    )
                    uploaded_files.append(uploaded_file)
                except Exception as e:
                    print(f"[ChatController] Error uploading {doc.filepath}: {e}")

        print('Cleee Gemini: ', api_key)

        # Build system instruction
        system_instruction = (
            "Tu es un assistant virtuel de support client expert et serviable. "
            "Réponds toujours en français de manière claire et professionnelle. "
        )
        if uploaded_files:
            system_instruction += (
                "Tu as accès à une base de connaissances constituée de documents PDF fournis ci-dessous. "
                "Appuie-toi EXCLUSIVEMENT sur ces documents pour répondre aux questions. "
                "Si la réponse ne se trouve pas dans les documents, dis-le clairement à l'utilisateur."
            )
        else:
            system_instruction += (
                "Aucun document de référence n'est disponible pour le moment. "
                "Réponds de manière générale et informe l'utilisateur que des documents "
                "peuvent être ajoutés dans la section 'Documents IA' pour améliorer tes réponses."
            )

        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction,
        )

        # Build the content list: PDFs first, then the user question
        content = uploaded_files + [user_message]

        try:
            response = model.generate_content(content)
            reply = response.text
        except Exception as e:
            print(f"[ChatController] Gemini API error: {e}")
            return jsonify({"error": str(e)}), 500

        return jsonify({"reply": reply})
