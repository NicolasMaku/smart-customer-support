import os
from dotenv import load_dotenv
load_dotenv()  # Load .env before anything else

from flask import Flask, redirect, url_for

from config import Config
from database import ensure_database_exists, init_db
from routes.user_routes import user_bp
from routes.chat_routes import chat_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)
    app.register_blueprint(user_bp)
    app.register_blueprint(chat_bp)
    
    from routes.document_routes import document_bp
    app.register_blueprint(document_bp)
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    @app.route("/")
    def home():
        return redirect(url_for("chat.index"))

    return app


if __name__ == "__main__":
    ensure_database_exists()
    application = create_app()
    application.run(debug=True)
