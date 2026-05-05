
from flask import request, jsonify
from models.recycle_request import RecycleRequest
from database import db
from datetime import date
import os
import uuid

def request_routes(app):

    # ✅ فولدر الصور
    UPLOAD_FOLDER = "uploads"
    BASE_URL = "https://retadweerbackend1-production.up.railway.app/"

    # ✅ ✅ Upload Image (لسه موجود لو احتجتيه)
    @app.route("/upload-image", methods=["POST"])
    def upload_image():

        if 'image' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['image']

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        image_url = BASE_URL + "uploads/" + filename

        return jsonify({
            "message": "Image uploaded successfully",
            "image_url": image_url
        })


    # ✅ ✅ ✅ Create Recycle Request (معدل عشان FormData + Image)
    @app.route("/recycle-requests", methods=["POST"])
    def create_request():
        try:

            # ✅ استلام البيانات من form-data
            quantity = request.form.get("quantity")

            total_price = request.form.get("total_price")
            user_id = request.form.get("user_id")
            reward_type = request.form.get("reward_type")

            # ✅ validation
            if not quantity:
                return jsonify({"error": "Quantity is required"}), 400

            if not total_price:
                return jsonify({"error": "Total price is required"}), 400

            if not user_id:
                return jsonify({"error": "User ID is required"}), 400

            if not reward_type:
                return jsonify({"error": "Reward type is required"}), 400

            if reward_type not in ["cash", "gift"]:

                return jsonify({"error": "Reward must be 'cash' or 'gift'"}), 400

            # ✅ استلام الصورة
            file = request.files.get("image")

            image_url = None

            if file:
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)

                filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)

                image_url = BASE_URL + "uploads/" + filename

            # ✅ إنشاء الطلب
            req = RecycleRequest(
                quantity=quantity,
                total_price=total_price,

                request_date=date.today(),
                status="Pending",
                user_id=user_id,
                reward_type=reward_type,
                image_path=image_url
            )

            db.session.add(req)
            db.session.commit()

            return jsonify({
                "message": "Recycle request created",
                "request_id": req.request_id,
                "image_url": image_url
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500


