
from database import db

class Pickup(db.Model):
    __tablename__ = "pickups"

    pickup_id = db.Column(db.Integer, primary_key=True)

    pickup_date = db.Column(db.Date)

    pickup_time = db.Column(db.String(20))

    status = db.Column(db.String(50))

    request_id = db.Column(db.Integer)
