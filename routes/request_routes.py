
from flask import request, jsonify
from models.recycle_request import RecycleRequest
from database import db
from datetime import date
import os

def request_routes(app):

    # ✅ فولدر الصور
    UPLOAD_FOLDER = "uploads"

    # ✅ ✅ Upload Image
    @app.route("/upload-image", methods=["POST"])
    def upload_image():
        if 'image' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['image']

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        # ✅ اعمل فولدر لو مش موجود
        if not os.path.exists(UPLOAD_FOLDER):

            os.makedirs(UPLOAD_FOLDER)

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        return jsonify({
            "message": "Image uploaded successfully",
            "image_path": file_path
        })


    # ✅ ✅ Create Recycle Request
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

            if data.get("reward_type") not in ["cash", "gift"]:
                return jsonify({"error": "Reward must be 'cash' or 'gift'"}), 400

            # ✅ الصورة (اختياري)
            image_path = data.get("image_path")

            # ✅ إنشاء الطلب
            req = RecycleRequest(
                quantity=data.get("quantity"),

                total_price=data.get("total_price"),
                request_date=date.today(),
                status="Pending",
                user_id=data.get("user_id"),
                reward_type=data.get("reward_type"),
                # ✅ هنخزن مسار الصورة هنا
                image_path=image_path
            )

            db.session.add(req)
            db.session.commit()

            return jsonify({
                "message": "Recycle request created",
                "request_id": req.request_id,
                "image": image_path
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

