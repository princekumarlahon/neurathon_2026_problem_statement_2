from flask import Flask
from app.models import init_db
from app.routes import app_routes

app = Flask(__name__)
app.register_blueprint(app_routes)

print("Starting Bharat Biz-Agent...")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
