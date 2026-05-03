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



