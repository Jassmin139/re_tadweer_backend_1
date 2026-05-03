
from database import db

class RecycleRequest(db.Model):
    __tablename__ = "recycle_request"

    request_id = db.Column(db.Integer, primary_key=True)

    quantity = db.Column(db.Integer)
    total_price = db.Column(db.Float)

    request_date = db.Column(db.Date)
    status = db.Column(db.String(50))

    # ✅ مربوط بالمستخدم
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    # ✅ مربوط بالشركة (اختياري)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=True)

    # 🔥 الجديد: نوع المكافأة
    reward_type = db.Column(db.String(10))  # "cash" أو "gift"

