
from flask import request, jsonify
from models.pickup import Pickup
from database import db

def pickup_routes(app):

    @app.route("/pickups", methods=["POST"])
    def create_pickup():
        try:
            data = request.json

            pickup = Pickup(
                pickup_date=data.get("pickup_date"),
                status="Scheduled",
                request_id=data.get("request_id")
            )

            db.session.add(pickup)
            db.session.commit()
            
            return jsonify({"message": "Pickup scheduled successfully"}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500


   