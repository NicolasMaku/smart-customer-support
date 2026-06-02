from flask import flash, redirect, render_template, request, url_for

from extensions import db
from models.users import User


class UserController:
    @staticmethod
    def index():
        users = User.query.order_by(User.id.desc()).all()
        return render_template("users/index.html", users=users)

    @staticmethod
    def create_form():
        return render_template("users/create.html")

    @staticmethod
    def create():
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        role = request.form.get("role", "user").strip()

        if not username or not email or not password:
            flash("Tous les champs obligatoires doivent être remplis.", "danger")
            return redirect(url_for("user.create_form"))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Cet email est déjà utilisé.", "danger")
            return redirect(url_for("user.create_form"))

        # Note: In a real app, hash the password before saving!
        user = User(username=username, email=email, password=password, role=role)
        db.session.add(user)
        db.session.commit()

        flash("Utilisateur créé avec succès.", "success")
        return redirect(url_for("user.index"))

    @staticmethod
    def edit_form(user_id):
        user = db.session.get(User, user_id)
        if not user:
            flash("Utilisateur introuvable.", "danger")
            return redirect(url_for("user.index"))
        return render_template("users/edit.html", user=user)

    @staticmethod
    def update(user_id):
        user = db.session.get(User, user_id)
        if not user:
            flash("Utilisateur introuvable.", "danger")
            return redirect(url_for("user.index"))

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        role = request.form.get("role", "user").strip()
        password = request.form.get("password", "").strip()

        if not username or not email:
            flash("Le nom d'utilisateur et l'email sont obligatoires.", "danger")
            return redirect(url_for("user.edit_form", user_id=user_id))
            
        existing_user = User.query.filter(User.email == email, User.id != user_id).first()
        if existing_user:
            flash("Cet email est déjà utilisé par un autre utilisateur.", "danger")
            return redirect(url_for("user.edit_form", user_id=user_id))

        user.username = username
        user.email = email
        user.role = role
        if password:
            # Note: Hash password here
            user.password = password
            
        db.session.commit()

        flash("Utilisateur modifié avec succès.", "success")
        return redirect(url_for("user.index"))

    @staticmethod
    def delete(user_id):
        user = db.session.get(User, user_id)
        if not user:
            flash("Utilisateur introuvable.", "danger")
            return redirect(url_for("user.index"))

        db.session.delete(user)
        db.session.commit()
        flash("Utilisateur supprimé avec succès.", "success")
        return redirect(url_for("user.index"))
