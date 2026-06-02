from flask import Blueprint

from controllers.chat_controller import ChatController

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

chat_bp.add_url_rule("/", "index", ChatController.index, methods=["GET"])
