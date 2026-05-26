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
    return """
    <html>
    <body style="font-family:Arial; text-align:center; padding:50px; background:#f0f0f0">
        <h1>🚀 Ram and Pavi DevOps App</h1>
        <p>Built with Flask + PostgreSQL + Docker + AWS</p>
        <h3>Visitors:</h3>
        <a href="/add">Add Visit</a> | 
        <a href="/list">See All Visits</a>
    </body>
    </html>
    """

@app.route("/add")
def add():
    db = get_db()
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, name TEXT)")
    cur.execute("INSERT INTO visits (name) VALUES ('Ram and Pavi visited! 💕')")
    db.commit()
    return "<h2>Visit added! <a href='/list'>See list</a></h2>"

@app.route("/list")
def list_visits():
    db = get_db()
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, name TEXT)")
    cur.execute("SELECT * FROM visits")
    rows = cur.fetchall()
    result = "<h1>All Visits:</h1><ul>"
    for row in rows:
        result += f"<li>{row[0]} — {row[1]}</li>"
    result += "</ul><a href='/'>Back</a>"
    return result

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
