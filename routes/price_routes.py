

from flask import request, jsonify
from models.material import Material

def price_routes(app):

    @app.route("/estimate-price", methods=["POST"])
    def estimate_price():
        data = request.json

        material = Material.query.get(data.get("material_id"))

        if not material:
            return jsonify({"error": "Material not found"}), 404

        total = material.price * data.get("quantity")
        return jsonify({"estimated_price": float(total)})

