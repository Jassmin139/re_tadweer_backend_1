
from flask import request, jsonify
from models.pickup import Pickup
from database import db
from datetime import datetime

def pickup_routes(app):

    @app.route("/pickups", methods=["POST"])
    def create_pickup():
        try:

            #  يدعم JSON و FormData
            pickup_date = request.form.get("pickup_date") or request.json.get("pickup_date")
            pickup_time = request.form.get("pickup_time") or request.json.get("pickup_time")
            request_id = request.form.get("request_id") or request.json.get("request_id")

            #  validation
            if not pickup_date:
                return jsonify({"error": "pickup_date is required"}), 400

            if not request_id:
                return jsonify({"error": "request_id is required"}), 400

            # تحويل التاريخ
            parsed_date = datetime.strptime(
                pickup_date, "%Y-%m-%d"
            ).date()

            #  إنشاء pickup
            pickup = Pickup(
                pickup_date=parsed_date,
                pickup_time=pickup_time,   #  الجديد 
                status="Scheduled",
                request_id=request_id
            )

            db.session.add(pickup)
            db.session.commit()

            return jsonify({
                "message": "Pickup scheduled successfully",
                "pickup_date": pickup_date,
                "pickup_time": pickup_time
            }), 201

        except Exception as e:

            db.session.rollback()
            return jsonify({"error": str(e)}), 500

