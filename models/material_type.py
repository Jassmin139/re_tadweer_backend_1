

from database import db

class MaterialType(db.Model):
    __tablename__ = "material_types"

    type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(100))


