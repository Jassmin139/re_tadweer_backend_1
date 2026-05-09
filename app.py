
import os

from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from database import db

#  imports لازم في الأول
from routes.user_routes import user_routes
from routes.material_routes import material_routes
from routes.price_routes import price_routes
from routes.request_routes import request_routes
from routes.pickup_routes import pickup_routes
from routes.company_routes import company_routes
from routes.contact_routes import contact_routes

#  مهم جدًا: استيراد كل الموديلز
from models import material_type, material, user, company, recycle_request, pickup, contact, gift

#  إنشاء التطبيق
app = Flask(__name__)

#  CORS
CORS(app)

#  Config

app.config.from_object(Config)

#  Database URL
database_url = os.getenv("DATABASE_URL")

if not database_url:
    database_url = "sqlite:///app.db"

if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#  init DB
db.init_app(app)

#  إنشاء الجداول عند التشغيل
with app.app_context():
    db.create_all()

#  route لإنشاء الجداول يدوي
@app.route("/init-db")

def init_db():
    db.create_all()
    return "Database created ✅"


#  route إضافة ماتريال
@app.route("/add-materials", methods=["GET"])
def add_materials():
    from models.material_type import MaterialType
    from models.material import Material

    try:
        if MaterialType.query.count() == 0:
            t1 = MaterialType(type_name="Plastic")
            t2 = MaterialType(type_name="Paper")
            t3 = MaterialType(type_name="Electronics")

            db.session.add_all([t1, t2, t3])
            db.session.commit()

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


#  ربط routes
user_routes(app)
material_routes(app)
price_routes(app)
request_routes(app)
pickup_routes(app)
company_routes(app)
contact_routes(app)


# عرض الصور 
@app.route('/uploads/<filename>')

def get_image(filename):
    return send_from_directory('uploads', filename)



from flask import render_template

@app.route("/")
def home():
    return render_template("index.html")



#  تشغيل السيرفر
port = int(os.environ.get("PORT", 8080))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)

