from flask import render_template

class ChatController:
    @staticmethod
    def index():
        return render_template("chat/index.html")
