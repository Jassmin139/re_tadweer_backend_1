





from flask import jsonify
from models.material import Material

def material_routes(app):

    @app.route("/materials", methods=["GET"])
    def get_materials():
        materials = Material.query.limit(10).all()

        return jsonify([
            {
                "id": m.material_id,
                "name": m.name,
                "price": float(m.price),
                "description": m.description
            } for m in materials
        ])


