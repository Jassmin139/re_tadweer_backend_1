
from flask import app, request, jsonify
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

        return jsonify([
            {
                "id": u.user_id,
                "name": u.name,
                "email": u.email,
                "phone": u.phone,
                "address": u.address
            } for u in users
        ]), 200




    # ✅ Register Company
    @app.route("/companies/register", methods=["POST"])
    def register_company():
        try:
            data = request.get_json()

            if not data.get("name"):
                return jsonify({"error": "Name is required"}), 400
            if not data.get("email"):
                return jsonify({"error": "Email is required"}), 400

            existing = Company.query.filter_by(email=data.get("email")).first()
            if existing:
                return jsonify({"error": "Company already exists"}), 400

            company = Company(
                name=data.get("name"),
                email=data.get("email"),
                tax_id=data.get("tax_id"),
                established_year=data.get("established_year"),
                employees=data.get("employees"),
                address=data.get("address"),
                phone=data.get("phone"),
                type=data.get("type"),
                registration_number=data.get("registration_number")
            )

            db.session.add(company)
            db.session.commit()

            return jsonify({
                "message": "Company registered successfully",
                "company_id": company.company_id
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500




    # ✅ Login (User + Company)
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


    # ✅ User Profile + Orders
    @app.route("/users/<int:user_id>", methods=["GET"])
    def get_user_profile(user_id):

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        requests = RecycleRequest.query.filter_by(user_id=user_id)\
            .order_by(RecycleRequest.request_id.desc())\
            .all()

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
            "orders": orders
        }), 200



    # ✅ User Requests
    @app.route("/users/<int:user_id>/requests", methods=["GET"])
    def get_user_requests(user_id):

        requests = RecycleRequest.query.filter_by(user_id=user_id).all()

        return jsonify([
            {
                "request_id": r.request_id,
                "quantity": r.quantity,
                "total_price": r.total_price,
                "status": r.status
            } for r in requests
        ]), 200


 

    # ✅ Company Profile
    @app.route("/companies/<int:company_id>", methods=["GET"])
    def get_company_profile(company_id):

        company = Company.query.get(company_id)

        if not company:
            return jsonify({"error": "Company not found"}), 404

        requests = RecycleRequest.query.filter_by(company_id=company_id).all()

        orders = []

        for r in requests:
            orders.append({
                "request_id": r.request_id,
                "quantity": r.quantity,
                "total_price": r.total_price,
                "status": r.status,
                "date": str(r.request_date)

            })

        return jsonify({
            "company_id": company.company_id,
            "name": company.name,
            "email": company.email,

            "tax_id": company.tax_id,
            "established_year": company.established_year,
            "employees": company.employees,
            "address": company.address,
            "phone": company.phone,
            "type": company.type,
            "registration_number": company.registration_number,

            "orders": orders
        }), 200

 