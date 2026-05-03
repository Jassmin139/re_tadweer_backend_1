
from flask import request, jsonify
from database import db
from models.contact import ContactMessage

def contact_routes(app):

    @app.route("/contact", methods=["POST"])
    def add_contact():
        data = request.get_json()

        if not data.get("name"):
            return jsonify({"error": "Name required"}), 400

        if not data.get("email"):
            return jsonify({"error": "Email required"}), 400

        if not data.get("message"):
            return jsonify({"error": "Message required"}), 400

        new_msg = ContactMessage(
            name=data["name"],
            email=data["email"],
            message=data["message"]
        )

        db.session.add(new_msg)
        db.session.commit()

        return jsonify({"message": "Message saved"}), 201


    @app.route("/contact", methods=["GET"])
    def get_messages():
        msgs = ContactMessage.query.all()

        result = []
        for m in msgs:
            result.append({
                "id": m.id,
                "name": m.name,
                "email": m.email,
                "message": m.message
            })

        return jsonify(result)
