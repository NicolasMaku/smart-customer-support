from flask import flash, redirect, render_template, request, url_for

from extensions import db
from models.produit import Produit


class ProduitController:
    @staticmethod
    def index():
        produits = Produit.query.order_by(Produit.id.desc()).all()
        return render_template("index.html", produits=produits)

    @staticmethod
    def create_form():
        return render_template("create.html")

    @staticmethod
    def create():
        nom = request.form.get("nom", "").strip()
        description = request.form.get("description", "").strip()
        prix = request.form.get("prix", "0")

        if not nom:
            flash("Le nom est obligatoire.", "danger")
            return redirect(url_for("produit.create_form"))

        try:
            prix = float(prix)
        except ValueError:
            flash("Le prix doit etre un nombre valide.", "danger")
            return redirect(url_for("produit.create_form"))

        produit = Produit(nom=nom, description=description or None, prix=prix)
        db.session.add(produit)
        db.session.commit()

        flash("Produit cree avec succes.", "success")
        return redirect(url_for("produit.index"))

    @staticmethod
    def edit_form(produit_id):
        produit = db.session.get(Produit, produit_id)
        if not produit:
            flash("Produit introuvable.", "danger")
            return redirect(url_for("produit.index"))
        return render_template("edit.html", produit=produit)

    @staticmethod
    def update(produit_id):
        produit = db.session.get(Produit, produit_id)
        if not produit:
            flash("Produit introuvable.", "danger")
            return redirect(url_for("produit.index"))

        nom = request.form.get("nom", "").strip()
        description = request.form.get("description", "").strip()
        prix = request.form.get("prix", "0")

        if not nom:
            flash("Le nom est obligatoire.", "danger")
            return redirect(url_for("produit.edit_form", produit_id=produit_id))

        try:
            prix = float(prix)
        except ValueError:
            flash("Le prix doit etre un nombre valide.", "danger")
            return redirect(url_for("produit.edit_form", produit_id=produit_id))

        produit.nom = nom
        produit.description = description or None
        produit.prix = prix
        db.session.commit()

        flash("Produit modifie avec succes.", "success")
        return redirect(url_for("produit.index"))

    @staticmethod
    def delete(produit_id):
        produit = db.session.get(Produit, produit_id)
        if not produit:
            flash("Produit introuvable.", "danger")
            return redirect(url_for("produit.index"))

        db.session.delete(produit)
        db.session.commit()
        flash("Produit supprime avec succes.", "success")
        return redirect(url_for("produit.index"))
