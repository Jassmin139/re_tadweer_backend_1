import os

from flask import Flask
from flask_cors import CORS
from config import Config
from database import db

# ✅ imports لازم في الأول
from routes.user_routes import user_routes
from routes.material_routes import material_routes
from routes.price_routes import price_routes
from routes.request_routes import request_routes
from routes.pickup_routes import pickup_routes
from routes.company_routes import company_routes
from routes.contact_routes import contact_routes
# ✅ إنشاء التطبيق (أول حاجة)
app = Flask(__name__)

# ✅ CORS
CORS(app)

# ✅ Config
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()


# ✅ ✅ ✅ الحل النهائي للماتريال (route manual)
@app.route("/add-materials", methods=["GET"])
def add_materials():
    from models.material_type import MaterialType
    from models.material import Material

    try:
        # ✅ types
        if MaterialType.query.count() == 0:
            t1 = MaterialType(type_name="Plastic")
            t2 = MaterialType(type_name="Paper")
            t3 = MaterialType(type_name="Electronics")

            db.session.add_all([t1, t2, t3])
            db.session.commit()

        # ✅ materials
        if Material.query.count() == 0:
            m1 = Material(name="Plastic", description="Plastic waste", price=5, image="img.png", type_id=1)
            m2 = Material(name="Paper", description="Paper waste", price=2, 

image="img.png", type_id=2)
            m3 = Material(name="Electronics", description="Electronic waste", price=7, image="img.png", type_id=3)

            db.session.add_all([m1, m2, m3])
            db.session.commit()

        return {"message": "Materials added ✅"}

    except Exception as e:
        return {"error": str(e)}


# ✅ ربط routes
user_routes(app)
material_routes(app)
price_routes(app)
request_routes(app)

pickup_routes(app)
company_routes(app)
contact_routes(app)

# ✅ test route
@app.route("/")
def home():
    return {"message": "RE Tadweer Backend Running"}

# ✅ تشغيل السيرفر
port = int(os.environ.get("PORT", 8080))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
