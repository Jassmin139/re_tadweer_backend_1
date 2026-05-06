
from flask import request, jsonify
from models.user import User
from models.company import Company
from models.recycle_request import RecycleRequest
from database import db

def user_routes(app):

    # ✅ Register User
    @app.route("/users/register", methods=["POST"])
    def register_user():
        try:
            data = request.get_json()

            if not data.get("name"):
                return jsonify({"error": "Name is required"}), 400
            if not data.get("email"):
                return jsonify({"error": "Email is required"}), 400
            if not data.get("phone"):
                return jsonify({"error": "Phone is required"}), 400
            if not data.get("address"):
                return jsonify({"error": "Address is required"}), 400

            existing = User.query.filter_by(email=data.get("email")).first()
            if existing:
                return jsonify({"error": "User already exists"}), 400

            user = User(
                name=data.get("name"),
                email=data.get("email"),
                phone=data.get("phone"),
                address=data.get("address")
            )

            db.session.add(user)
            db.session.commit()

            return jsonify({
                "message": "User registered successfully",
                "user_id": user.user_id
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500


    # ✅ GET All Users
    @app.route("/users", methods=["GET"])

    def get_users():
        users = User.query.all()

        result = []
        for u in users:
            result.append({
                "id": u.user_id,
                "name": u.name,
                "email": u.email,
                "phone": u.phone,
                "address": u.address
            })

        return jsonify(result), 200


    # ✅ Login
    @app.route("/login", methods=["POST"])
    def login():
        try:
            data = request.get_json()

            if not data.get("email"):
                return jsonify({"error": "Email is required"}), 400

            email = data.get("email")

            user = User.query.filter_by(email=email).first()
            if user:
                return jsonify({
                    "type": "user",
                    "user_id": user.user_id,
                    "name": user.name
                }), 200

            company = Company.query.filter_by(email=email).first()
            if company:
                return jsonify({
                    "type": "company",
                    "company_id": company.company_id,
                    "name": company.name
                }), 200

            return jsonify({"error": "User not found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500


    # ✅ ✅ GET User Profile + Orders (المهم 🔥🔥)

    @app.route("/users/<int:user_id>", methods=["GET"])
    def get_user_profile(user_id):

        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        # ✅ نجيب كل الطلبات
        requests = RecycleRequest.query.filter_by(user_id=user_id).all()

        orders = []

        for r in requests:
            orders.append({
                "request_id": r.request_id,
                "quantity": r.quantity,
                "total_price": r.total_price,
                "status": r.status,
                "date": str(r.request_date),
                "reward_type": r.reward_type,
                "image": r.image_path
            })

        return jsonify({

            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "address": user.address,
            "orders": orders   # ✅ أهم تعديل
        }), 200


    # ✅ (اختياري) GET requests فقط
    @app.route("/users/<int:user_id>/requests", methods=["GET"])
    def get_user_requests(user_id):

        requests = RecycleRequest.query.filter_by(user_id=user_id).all()

        result = []

        for r in requests:
            result.append({
                "request_id": r.request_id,
                "quantity": r.quantity,
                "total_price": r.total_price,

                "status": r.status
            })

        return jsonify(result), 200



