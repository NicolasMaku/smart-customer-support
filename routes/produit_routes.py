from flask import Blueprint

from controllers.produit_controller import ProduitController

produit_bp = Blueprint("produit", __name__, url_prefix="/produits")

produit_bp.add_url_rule("/", "index", ProduitController.index, methods=["GET"])
produit_bp.add_url_rule(
    "/create", "create_form", ProduitController.create_form, methods=["GET"]
)
produit_bp.add_url_rule("/create", "create", ProduitController.create, methods=["POST"])
produit_bp.add_url_rule(
    "/<int:produit_id>/edit",
    "edit_form",
    ProduitController.edit_form,
    methods=["GET"],
)
produit_bp.add_url_rule(
    "/<int:produit_id>/edit",
    "update",
    ProduitController.update,
    methods=["POST"],
)
produit_bp.add_url_rule(
    "/<int:produit_id>/delete",
    "delete",
    ProduitController.delete,
    methods=["POST"],
)
