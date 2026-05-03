
from database import db

class Material(db.Model):
    __tablename__ = "materials"

    material_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    price = db.Column(db.Numeric(10,2))
    image = db.Column(db.String(255))
    type_id = db.Column(db.Integer)
