
from database import db

class Company(db.Model):
    __tablename__ = "companies"

    company_id = db.Column(db.Integer, primary_key=True)

    # ✅ بيانات الشركة
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # ✅ علشان نرجعها بسهولة
    def to_dict(self):
        return {
            "company_id": self.company_id,
            "name": self.name,
            "email": self.email
        }
