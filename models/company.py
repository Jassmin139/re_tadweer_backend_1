
from database import db

class Company(db.Model):
    __tablename__ = "companies"

    company_id = db.Column(db.Integer, primary_key=True)

    # ✅ بيانات الشركة
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # ✅ لازم جوه الكلاس 👇
    password = db.Column(db.String(255))
    city = db.Column(db.String(100))

    tax_id = db.Column(db.String(50))
    established_year = db.Column(db.Integer)
    employees = db.Column(db.Integer)
    address = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    type = db.Column(db.String(50))
    registration_number = db.Column(db.String(100))

    def to_dict(self):
        return {
            "company_id": self.company_id,
            "name": self.name,
            "email": self.email
        }

