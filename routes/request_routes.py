
from flask import request, jsonify
from models.recycle_request import RecycleRequest
from database import db
from datetime import date

def request_routes(app):

    @app.route("/recycle-requests", methods=["POST"])
    def create_request():
        try:
            data = request.get_json()

            # ✅ التحقق من البيانات
            if not data or not isinstance(data, dict):
                return jsonify({"error": "Invalid JSON format"}), 400

            if not data.get("quantity"):
                return jsonify({"error": "Quantity is required"}), 400

            if not data.get("total_price"):
                return jsonify({"error": "Total price is required"}), 400

            if not data.get("user_id"):
                return jsonify({"error": "User ID is required"}), 400

            if not data.get("reward_type"):
                return jsonify({"error": "Reward type is required"}), 400

            # ✅ التحقق إن reward_type صح
            if data.get("reward_type") not in ["cash", "gift"]:
                return jsonify({"error": "Reward must be 'cash' or 'gift'"}), 400

            # ✅ إنشاء الطلب
            req = RecycleRequest(
                quantity=data.get("quantity"),
                total_price=data.get("total_price"),
                request_date=date.today(),
                status="Pending",
                user_id=data.get("user_id"),
                reward_type=data.get("reward_type")  # ✅ الجديد
            )

            db.session.add(req)
            db.session.commit()

            return jsonify({
                "message": "Recycle request created",
                "request_id": req.request_id,
                "reward_type": req.reward_type
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

