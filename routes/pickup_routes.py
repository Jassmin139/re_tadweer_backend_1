
from flask import request, jsonify
from models.pickup import Pickup
from database import db
from datetime import datetime  # ✅ لازم هنا فوق

def pickup_routes(app):

    @app.route("/pickups", methods=["POST"])
    def create_pickup():
        try:
            data = request.json

            pickup = Pickup(
                pickup_date=datetime.strptime(
                    data.get("pickup_date"), "%Y-%m-%d"
                ).date(),   # ✅ مهم جدًا () هنا
                status="Scheduled",
                request_id=data.get("request_id")
            )

            db.session.add(pickup)
            db.session.commit()

            return jsonify({"message": "Pickup scheduled successfully"}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500