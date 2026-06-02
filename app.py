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
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ram & Pavi DevOps App</title>
        <style>
            body { font-family: Arial; margin: 0; background: #1a1a2e; color: white; }
            .header { background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px; text-align: center; }
            .header h1 { font-size: 40px; margin: 0; }
            .header p { font-size: 18px; opacity: 0.8; }
            .container { max-width: 800px; margin: 40px auto; padding: 20px; }
            .card { background: #16213e; border-radius: 15px; padding: 30px; margin: 20px 0; border: 1px solid #0f3460; }
            .btn { display: inline-block; padding: 12px 30px; border-radius: 25px; text-decoration: none; font-weight: bold; margin: 10px; }
            .btn-add { background: #667eea; color: white; }
            .btn-list { background: #764ba2; color: white; }
            .badge { background: #0f3460; padding: 5px 15px; border-radius: 20px; font-size: 13px; margin: 5px; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🚀 Ram & Pavi DevOps App</h1>
            <p>Built with Flask • PostgreSQL • Docker • AWS</p>
        </div>
        <div class="container">
            <div class="card">
                <h2>Welcome! 💕</h2>
                <p>This is a real DevOps project running on AWS with a live database!</p>
                <a href="/add" class="btn btn-add">➕ Add Visit</a>
                <a href="/list" class="btn btn-list">📋 See All Visits</a>
            </div>
            <div class="card">
                <h3>Tech Stack:</h3>
                <span class="badge">🐍 Python Flask</span>
                <span class="badge">🐳 Docker</span>
                <span class="badge">🐘 PostgreSQL</span>
                <span class="badge">⚙️ GitHub Actions</span>
                <span class="badge">☁️ AWS EC2</span>
            </div>
        </div>
    </body>
    </html>
    """

@app.route("/add")
def add():
    db = get_db()
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, name TEXT, time TIMESTAMP DEFAULT NOW())")
    cur.execute("INSERT INTO visits (name) VALUES ('Ram and Pavi visited! 💕')")
    db.commit()
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Visit Added!</title>
        <style>
            body { font-family: Arial; margin: 0; background: #1a1a2e; color: white; text-align: center; padding: 100px; }
            .success { background: #16213e; border-radius: 15px; padding: 40px; max-width: 500px; margin: 0 auto; border: 2px solid #667eea; }
            .btn { display: inline-block; padding: 12px 30px; border-radius: 25px; text-decoration: none; font-weight: bold; margin: 10px; background: #667eea; color: white; }
        </style>
    </head>
    <body>
        <div class="success">
            <h1>✅ Visit Added!</h1>
            <p>Your visit was saved to PostgreSQL database on AWS!</p>
            <a href="/list" class="btn">📋 See All Visits</a>
            <a href="/" class="btn">🏠 Home</a>
        </div>
    </body>
    </html>
    """

@app.route("/list")
def list_visits():
    db = get_db()
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, name TEXT, time TIMESTAMP DEFAULT NOW())")
    cur.execute("SELECT * FROM visits ORDER BY id DESC")
    rows = cur.fetchall()
    rows_html = ""
    for row in rows:
        rows_html += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
        </tr>
        """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>All Visits</title>
        <style>
            body {{ font-family: Arial; margin: 0; background: #1a1a2e; color: white; }}
            .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 30px; text-align: center; }}
            .container {{ max-width: 900px; margin: 40px auto; padding: 20px; }}
            table {{ width: 100%; border-collapse: collapse; background: #16213e; border-radius: 15px; overflow: hidden; }}
            th {{ background: #0f3460; padding: 15px; text-align: left; }}
            td {{ padding: 12px 15px; border-bottom: 1px solid #0f3460; }}
            tr:hover {{ background: #0f3460; }}
            .btn {{ display: inline-block; padding: 12px 30px; border-radius: 25px; text-decoration: none; font-weight: bold; margin: 10px; background: #667eea; color: white; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📋 All Visits</h1>
            <p>Data stored in PostgreSQL database on AWS!</p>
        </div>
        <div class="container">
            <a href="/add" class="btn">➕ Add Visit</a>
            <a href="/" class="btn">🏠 Home</a>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Time</th>
                </tr>
                {rows_html}
            </table>
        </div>
    </body>
    </html>
    """

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
