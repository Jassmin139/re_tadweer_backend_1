
from flask import Flask
from flask_cors import CORS   # ✅ الجديد

from config import Config
from database import db

# ✅ استيراد كل الـ routes
from routes.user_routes import user_routes
from routes.material_routes import material_routes
from routes.price_routes import price_routes
from routes.request_routes import request_routes
from routes.pickup_routes import pickup_routes
from routes.company_routes import company_routes

# ✅ إنشاء التطبيق
app = Flask(__name__)

# ✅ تفعيل CORS (مهم جدًا 🔥)
CORS(app)

# ✅ إعدادات الداتابيز
app.config.from_object(Config)
db.init_app(app)

# ✅ ربط الـ routes بالتطبيق
user_routes(app)

material_routes(app)
price_routes(app)
request_routes(app)
pickup_routes(app)
company_routes(app)

# ✅ route لتأكيد إن السيرفر شغال
@app.route("/")
def home():
    return {"message": "RE Tadweer Backend Running"}

# ✅ تشغيل التطبيق
if __name__ == "__main__":
    app.run(debug=True)

