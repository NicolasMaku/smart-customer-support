from flask import Blueprint

from controllers.document_controller import DocumentController

document_bp = Blueprint("document", __name__, url_prefix="/admin/documents")

document_bp.add_url_rule("/", "index", DocumentController.index, methods=["GET"])
document_bp.add_url_rule("/create", "create_form", DocumentController.create_form, methods=["GET"])
document_bp.add_url_rule("/upload", "upload", DocumentController.upload, methods=["POST"])
document_bp.add_url_rule("/<int:document_id>/toggle", "toggle", DocumentController.toggle, methods=["POST"])
document_bp.add_url_rule("/<int:document_id>/delete", "delete", DocumentController.delete, methods=["POST"])
