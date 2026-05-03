
from flask import request, jsonify
from models.company import Company
from database import db

def company_routes(app):

    # ✅ Register Company
    @app.route("/companies/register", methods=["POST"])
    def register_company():
        try:
            data = request.get_json()

            # ✅ validation
            if not data.get("name"):
                return jsonify({"error": "Name is required"}), 400

            if not data.get("email"):
                return jsonify({"error": "Email is required"}), 400

            # ✅ check if exists
            existing = Company.query.filter_by(email=data.get("email")).first()
            if existing:
                return jsonify({"error": "Company already exists"}), 400

            # ✅ create company
            company = Company(
                name=data.get("name"),
                email=data.get("email")

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

    # ✅ Login Company
    @app.route("/companies/login", methods=["POST"])
    def login_company():
        try:
            data = request.get_json()

            if not data.get("email"):
                return jsonify({"error": "Email is required"}), 400

            company = Company.query.filter_by(email=data.get("email")).first()

            if not company:
                return jsonify({"error": "Company not found"}), 401

            return jsonify({
                "message": "Login successful",
                "company_id": company.company_id,
                "name": company.name
            }), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

