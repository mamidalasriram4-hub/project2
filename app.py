from flask import Flask
import psycopg2
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "devops"),
        user=os.environ.get("DB_USER", "ram"),
        password=os.environ.get("DB_PASS", "pavi123")
    )

@app.route("/")
def home():
    return "Auto Deploy Working! Ram and Pavi 💕🚀"
@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
