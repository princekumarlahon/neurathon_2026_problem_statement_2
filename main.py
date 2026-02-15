from flask import Flask
from app.routes import app_routes


app = Flask(__name__)
app.secret_key = "supersecretkey"


app.register_blueprint(app_routes)

if __name__ == "__main__":
    print("Starting Bharat Biz-Agent...")
    app.run(host="0.0.0.0", port=5000, debug=True)
