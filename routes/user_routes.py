from flask import Blueprint

from controllers.user_controller import UserController

user_bp = Blueprint("user", __name__, url_prefix="/admin/users")

user_bp.add_url_rule("/", "index", UserController.index, methods=["GET"])
user_bp.add_url_rule(
    "/create", "create_form", UserController.create_form, methods=["GET"]
)
user_bp.add_url_rule("/create", "create", UserController.create, methods=["POST"])
user_bp.add_url_rule(
    "/<int:user_id>/edit",
    "edit_form",
    UserController.edit_form,
    methods=["GET"],
)
user_bp.add_url_rule(
    "/<int:user_id>/edit",
    "update",
    UserController.update,
    methods=["POST"],
)
user_bp.add_url_rule(
    "/<int:user_id>/delete",
    "delete",
    UserController.delete,
    methods=["POST"],
)
