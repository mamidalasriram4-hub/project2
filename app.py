from flask import Flask, send_from_directory
import psycopg2
import os

app = Flask(__name__)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "devops"),
        user=os.environ.get("DB_USER", "ram"),
        password=os.environ.get("DB_PASS", "pavi123")
    )

def get_visitor_count():
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS visitors (id SERIAL PRIMARY KEY, time TIMESTAMP DEFAULT NOW())")
        cur.execute("INSERT INTO visitors DEFAULT VALUES")
        db.commit()
        cur.execute("SELECT COUNT(*) FROM visitors")
        return cur.fetchone()[0]
    except:
        return 0

@app.route("/")
def home():
    count = get_visitor_count()
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sriram Mamidala | DevOps Engineer</title>
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html {{ scroll-behavior: smooth; }}
        body {{ font-family: 'Syne', sans-serif; background: #050508; color: #fff; overflow-x: hidden; cursor: none; }}

        /* CUSTOM CURSOR */
        .cursor {{ position: fixed; width: 12px; height: 12px; background: #00d4ff; border-radius: 50%; pointer-events: none; z-index: 9999; transform: translate(-50%, -50%); transition: transform 0.1s; }}
        .cursor-follower {{ position: fixed; width: 40px; height: 40px; border: 1px solid rgba(0,212,255,0.5); border-radius: 50%; pointer-events: none; z-index: 9998; transform: translate(-50%, -50%); transition: all 0.15s ease; }}

        /* NAV */
        nav {{ position: fixed; top: 0; width: 100%; z-index: 1000; padding: 20px 80px; display: flex; justify-content: space-between; align-items: center; background: rgba(5,5,8,0.8); backdrop-filter: blur(30px); border-bottom: 1px solid rgba(255,255,255,0.05); transition: all 0.3s; }}
        .logo {{ font-family: 'JetBrains Mono', monospace; font-size: 18px; color: #00d4ff; letter-spacing: 2px; }}
        nav ul {{ list-style: none; display: flex; gap: 40px; }}
        nav ul a {{ color: #aaa; text-decoration: none; font-size: 14px; font-family: 'JetBrains Mono', monospace; transition: color 0.3s; position: relative; }}
        nav ul a::after {{ content: ''; position: absolute; bottom: -4px; left: 0; width: 0; height: 1px; background: #00d4ff; transition: width 0.3s; }}
        nav ul a:hover {{ color: #00d4ff; }}
        nav ul a:hover::after {{ width: 100%; }}
        .nav-cta {{ background: linear-gradient(135deg, #00d4ff, #0099bb); color: #000; padding: 10px 24px; border-radius: 50px; text-decoration: none; font-weight: 800; font-size: 13px; font-family: 'JetBrains Mono', monospace; transition: all 0.3s; }}
        .nav-cta:hover {{ transform: translateY(-2px); box-shadow: 0 10px 30px rgba(0,212,255,0.4); }}

        /* HERO */
        .hero {{ min-height: 100vh; position: relative; display: flex; align-items: center; justify-content: center; text-align: center; overflow: hidden; }}
        .hero-video {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; }}
        .hero-video video {{ width: 100%; height: 100%; object-fit: cover; filter: brightness(0.3); }}
        .hero-overlay {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(180deg, rgba(5,5,8,0.3) 0%, rgba(5,5,8,0.9) 100%); }}
        .hero-content {{ position: relative; z-index: 2; max-width: 1000px; padding: 20px; }}
        .hero-tag {{ display: inline-flex; align-items: center; gap: 8px; background: rgba(0,212,255,0.1); border: 1px solid rgba(0,212,255,0.3); color: #00d4ff; padding: 8px 20px; border-radius: 30px; font-size: 13px; font-family: 'JetBrains Mono', monospace; margin-bottom: 30px; animation: fadeDown 1s ease both; }}
        .hero-tag::before {{ content: ''; width: 8px; height: 8px; background: #00d4ff; border-radius: 50%; animation: pulse 1.5s infinite; }}
        .hero h1 {{ font-size: 80px; font-weight: 900; line-height: 1.05; margin-bottom: 24px; animation: fadeDown 1s ease 0.1s both; }}
        .hero h1 .line1 {{ display: block; color: white; }}
        .hero h1 .line2 {{ display: block; background: linear-gradient(135deg, #00d4ff, #f59e0b, #ff6b6b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; background-size: 200% auto; animation: gradientMove 3s linear infinite; }}
        @keyframes gradientMove {{ 0% {{ background-position: 0% center; }} 100% {{ background-position: 200% center; }} }}
        .hero p {{ font-size: 20px; color: #aaa; margin-bottom: 50px; line-height: 1.8; animation: fadeDown 1s ease 0.2s both; max-width: 600px; margin-left: auto; margin-right: auto; margin-bottom: 50px; }}
        .hero-btns {{ display: flex; gap: 15px; justify-content: center; animation: fadeDown 1s ease 0.3s both; }}
        .btn-glow {{ background: linear-gradient(135deg, #00d4ff, #0099bb); color: #000; padding: 18px 45px; border-radius: 50px; text-decoration: none; font-weight: 900; font-size: 16px; transition: all 0.3s; box-shadow: 0 0 30px rgba(0,212,255,0.4); }}
        .btn-glow:hover {{ transform: translateY(-4px) scale(1.05); box-shadow: 0 20px 60px rgba(0,212,255,0.6); }}
        .btn-ghost {{ border: 2px solid rgba(255,255,255,0.15); color: white; padding: 18px 45px; border-radius: 50px; text-decoration: none; font-weight: 700; font-size: 16px; transition: all 0.3s; backdrop-filter: blur(10px); }}
        .btn-ghost:hover {{ border-color: #00d4ff; color: #00d4ff; transform: translateY(-4px); }}

        /* FLOATING STATUS */
        .status-bar {{ display: flex; justify-content: center; gap: 15px; margin-top: 60px; flex-wrap: wrap; animation: fadeUp 1s ease 0.5s both; }}
        .status-item {{ background: rgba(10,10,20,0.8); border: 1px solid rgba(0,212,255,0.1); border-radius: 12px; padding: 10px 20px; display: flex; align-items: center; gap: 8px; font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #888; backdrop-filter: blur(10px); transition: all 0.3s; }}
        .status-item:hover {{ border-color: rgba(0,212,255,0.4); color: #00d4ff; transform: translateY(-3px); }}
        .status-dot {{ width: 8px; height: 8px; border-radius: 50%; background: #10b981; animation: pulse 1.5s infinite; flex-shrink: 0; }}

        /* MARQUEE */
        .marquee-section {{ padding: 30px 0; background: rgba(0,212,255,0.03); border-top: 1px solid rgba(0,212,255,0.05); border-bottom: 1px solid rgba(0,212,255,0.05); overflow: hidden; }}
        .marquee-track {{ display: flex; gap: 60px; animation: marquee 20s linear infinite; white-space: nowrap; }}
        .marquee-item {{ font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #444; display: flex; align-items: center; gap: 12px; flex-shrink: 0; }}
        .marquee-item span {{ color: #00d4ff; }}
        @keyframes marquee {{ 0% {{ transform: translateX(0); }} 100% {{ transform: translateX(-50%); }} }}

        /* STATS */
        .stats {{ padding: 100px 80px; background: #0a0a0f; }}
        .stats-inner {{ max-width: 1100px; margin: 0 auto; display: grid; grid-template-columns: repeat(4,1fr); gap: 24px; }}
        .stat-card {{ background: #0d0d14; border: 1px solid #1a1a2e; border-radius: 24px; padding: 40px 30px; text-align: center; position: relative; overflow: hidden; transition: all 0.4s; }}
        .stat-card::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #00d4ff, #f59e0b); transform: scaleX(0); transition: transform 0.4s; }}
        .stat-card:hover {{ transform: translateY(-10px); border-color: rgba(0,212,255,0.3); box-shadow: 0 30px 60px rgba(0,0,0,0.5); }}
        .stat-card:hover::before {{ transform: scaleX(1); }}
        .stat-icon {{ font-size: 36px; margin-bottom: 16px; }}
        .stat-number {{ font-size: 56px; font-weight: 900; font-family: 'JetBrains Mono', monospace; background: linear-gradient(135deg, #00d4ff, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
        .stat-label {{ color: #555; font-size: 13px; margin-top: 8px; text-transform: uppercase; letter-spacing: 2px; }}

        /* ABOUT */
        .about {{ padding: 100px 80px; background: #050508; }}
        .about-inner {{ max-width: 1100px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr; gap: 80px; align-items: center; }}
        .about-img-wrap {{ position: relative; }}
        .about-img-wrap::before {{ content: ''; position: absolute; inset: -2px; background: linear-gradient(135deg, #00d4ff, #f59e0b, #ff6b6b); border-radius: 24px; z-index: 0; opacity: 0.5; }}
        .about-img-wrap img {{ position: relative; z-index: 1; width: 100%; height: 550px; object-fit: cover; object-position: center top; border-radius: 22px; transition: transform 0.5s; }}
        .about-img-wrap:hover img {{ transform: scale(1.03); }}
        .about-tag {{ font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #00d4ff; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 20px; display: block; }}
        .about h2 {{ font-size: 48px; font-weight: 900; line-height: 1.15; margin-bottom: 24px; }}
        .about h2 span {{ background: linear-gradient(135deg, #f59e0b, #ff6b6b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
        .about p {{ color: #777; font-size: 16px; line-height: 1.9; margin-bottom: 16px; }}
        .about-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 36px; }}
        .about-stat {{ background: #0d0d14; border: 1px solid #1a1a2e; border-radius: 16px; padding: 20px; transition: all 0.3s; }}
        .about-stat:hover {{ border-color: rgba(245,158,11,0.4); transform: translateY(-4px); }}
        .about-stat-num {{ font-size: 32px; font-weight: 900; color: #f59e0b; font-family: 'JetBrains Mono', monospace; }}
        .about-stat-label {{ font-size: 12px; color: #555; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px; }}

        /* SKILLS */
        .skills {{ padding: 100px 80px; background: #0a0a0f; }}
        .section-header {{ text-align: center; margin-bottom: 70px; }}
        .section-eyebrow {{ font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #00d4ff; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 16px; display: block; }}
        .section-title {{ font-size: 52px; font-weight: 900; margin-bottom: 16px; line-height: 1.1; }}
        .section-sub {{ color: #555; font-size: 17px; max-width: 500px; margin: 0 auto; line-height: 1.7; }}
        .skills-grid {{ max-width: 1100px; margin: 0 auto; display: grid; grid-template-columns: repeat(3,1fr); gap: 24px; }}
        .skill-card {{ background: #0d0d14; border: 1px solid #1a1a2e; border-radius: 24px; padding: 36px; transition: all 0.4s; position: relative; overflow: hidden; group: true; }}
        .skill-card::after {{ content: ''; position: absolute; inset: 0; background: linear-gradient(135deg, rgba(0,212,255,0.05), transparent); opacity: 0; transition: opacity 0.4s; }}
        .skill-card:hover {{ border-color: rgba(0,212,255,0.3); transform: translateY(-10px) scale(1.02); box-shadow: 0 30px 60px rgba(0,0,0,0.4); }}
        .skill-card:hover::after {{ opacity: 1; }}
        .skill-icon {{ font-size: 40px; margin-bottom: 20px; display: block; transition: transform 0.3s; }}
        .skill-card:hover .skill-icon {{ transform: scale(1.2) rotate(-5deg); }}
        .skill-name {{ font-size: 20px; font-weight: 800; margin-bottom: 10px; }}
        .skill-desc {{ color: #666; font-size: 14px; line-height: 1.7; margin-bottom: 20px; }}
        .skill-bar {{ background: #1a1a2e; border-radius: 10px; height: 4px; overflow: hidden; }}
        .skill-fill {{ height: 100%; border-radius: 10px; background: linear-gradient(90deg, #00d4ff, #f59e0b); transform: scaleX(0); transform-origin: left; transition: transform 1s ease 0.3s; }}
        .skill-card.visible .skill-fill {{ transform: scaleX(1); }}
        .skill-percent {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #00d4ff; text-align: right; margin-top: 8px; }}

        /* PROJECTS */
        .projects {{ padding: 100px 80px; background: #050508; }}
        .projects-grid {{ max-width: 1100px; margin: 0 auto; display: grid; grid-template-columns: repeat(2,1fr); gap: 28px; }}
        .project-card {{ background: #0d0d14; border: 1px solid #1a1a2e; border-radius: 24px; padding: 40px; transition: all 0.4s; position: relative; overflow: hidden; }}
        .project-card::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #00d4ff, #7c3aed); transform: scaleX(0); transition: transform 0.4s; transform-origin: left; }}
        .project-card:hover {{ transform: translateY(-10px); border-color: rgba(0,212,255,0.2); box-shadow: 0 40px 80px rgba(0,0,0,0.5); }}
        .project-card:hover::before {{ transform: scaleX(1); }}
        .project-card.featured {{ border-color: rgba(0,212,255,0.15); background: linear-gradient(135deg, rgba(0,212,255,0.03), rgba(124,58,237,0.03)); }}
        .live-badge {{ display: inline-flex; align-items: center; gap: 6px; background: rgba(16,185,129,0.1); color: #10b981; border: 1px solid rgba(16,185,129,0.2); padding: 5px 14px; border-radius: 20px; font-size: 11px; margin-bottom: 16px; font-family: 'JetBrains Mono', monospace; }}
        .soon-badge {{ display: inline-flex; align-items: center; gap: 6px; background: rgba(245,158,11,0.1); color: #f59e0b; border: 1px solid rgba(245,158,11,0.2); padding: 5px 14px; border-radius: 20px; font-size: 11px; margin-bottom: 16px; font-family: 'JetBrains Mono', monospace; }}
        .project-num {{ font-size: 11px; color: #333; font-family: 'JetBrains Mono', monospace; letter-spacing: 2px; margin-bottom: 12px; }}
        .project-title {{ font-size: 24px; font-weight: 800; margin-bottom: 12px; transition: color 0.3s; }}
        .project-card:hover .project-title {{ color: #00d4ff; }}
        .project-desc {{ color: #555; font-size: 14px; line-height: 1.8; margin-bottom: 24px; }}
        .techs {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .tech {{ background: rgba(0,212,255,0.06); border: 1px solid rgba(0,212,255,0.12); color: #00d4ff; padding: 5px 14px; border-radius: 20px; font-size: 11px; font-family: 'JetBrains Mono', monospace; transition: all 0.3s; }}
        .tech:hover {{ background: rgba(0,212,255,0.15); border-color: rgba(0,212,255,0.4); }}

        /* VISITOR */
        .visitor {{ padding: 120px 80px; text-align: center; position: relative; overflow: hidden; }}
        .visitor-bg {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; }}
        .visitor-bg img {{ width: 100%; height: 100%; object-fit: cover; filter: brightness(0.1) saturate(0.5); }}
        .visitor-overlay {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(ellipse at center, rgba(0,212,255,0.08) 0%, rgba(5,5,8,0.95) 70%); }}
        .visitor-content {{ position: relative; z-index: 2; }}
        .visitor-eyebrow {{ font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #00d4ff; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 20px; display: block; }}
        .visitor h2 {{ font-size: 52px; font-weight: 900; margin-bottom: 20px; }}
        .visitor-count {{ font-size: 140px; font-weight: 900; background: linear-gradient(135deg, #00d4ff, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-family: 'JetBrains Mono', monospace; line-height: 1; margin: 10px 0 30px; }}
        .visitor p {{ color: #666; font-size: 18px; line-height: 1.7; max-width: 500px; margin: 0 auto; }}
        .visitor-badges {{ display: flex; justify-content: center; gap: 12px; margin-top: 30px; flex-wrap: wrap; }}
        .visitor-badge {{ background: rgba(0,212,255,0.08); border: 1px solid rgba(0,212,255,0.15); color: #888; padding: 8px 20px; border-radius: 20px; font-size: 13px; font-family: 'JetBrains Mono', monospace; transition: all 0.3s; }}
        .visitor-badge:hover {{ border-color: rgba(0,212,255,0.4); color: #00d4ff; }}

        /* FOOTER */
        footer {{ padding: 50px 80px; border-top: 1px solid #0d0d14; background: #050508; display: flex; justify-content: space-between; align-items: center; }}
        .footer-left {{ font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #444; }}
        .footer-left span {{ color: #00d4ff; }}
        .footer-links {{ display: flex; gap: 30px; }}
        .footer-links a {{ color: #444; text-decoration: none; font-size: 13px; font-family: 'JetBrains Mono', monospace; transition: color 0.3s; }}
        .footer-links a:hover {{ color: #00d4ff; }}

        /* ANIMATIONS */
        @keyframes fadeDown {{ from {{ opacity:0; transform:translateY(-30px); }} to {{ opacity:1; transform:translateY(0); }} }}
        @keyframes fadeUp {{ from {{ opacity:0; transform:translateY(30px); }} to {{ opacity:1; transform:translateY(0); }} }}
        @keyframes pulse {{ 0%,100% {{ opacity:1; transform:scale(1); }} 50% {{ opacity:0.5; transform:scale(0.8); }} }}

        .reveal {{ opacity: 0; transform: translateY(40px); transition: all 0.8s ease; }}
        .reveal.visible {{ opacity: 1; transform: translateY(0); }}
    </style>
</head>
<body>

<div class="cursor" id="cursor"></div>
<div class="cursor-follower" id="cursorFollower"></div>

<nav>
    <div class="logo">&lt;sriram.dev/&gt;</div>
    <ul>
        <li><a href="#about">About</a></li>
        <li><a href="#skills">Skills</a></li>
        <li><a href="#projects">Projects</a></li>
        <li><a href="#visitors">Live Count</a></li>
    </ul>
    <a href="#visitors" class="nav-cta">● Live Now</a>
</nav>

<section class="hero">
    <div class="hero-video">
        <video autoplay muted loop playsinline>
            <source src="/static/hero.mp4" type="video/mp4">
        </video>
    </div>
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <div class="hero-tag">DevOps Engineer · Los Angeles 🌴</div>
        <h1>
            <span class="line1">Infrastructure That</span>
            <span class="line2">Never Sleeps.</span>
        </h1>
        <p>Hi, I'm Sriram Mamidala. I build, automate and deploy production systems using Docker, AWS, Kubernetes and CI/CD pipelines.</p>
        <div class="hero-btns">
            <a href="#projects" class="btn-glow">View Projects →</a>
            <a href="#visitors" class="btn-ghost">Live Visitors</a>
        </div>
        <div class="status-bar">
            <div class="status-item"><div class="status-dot"></div> AWS Running</div>
            <div class="status-item"><div class="status-dot"></div> CI/CD Active</div>
            <div class="status-item"><div class="status-dot"></div> Docker Live</div>
            <div class="status-item"><div class="status-dot"></div> DB Connected</div>
            <div class="status-item"><div class="status-dot"></div> Auto Deploy ON</div>
        </div>
    </div>
</section>

<div class="marquee-section">
    <div class="marquee-track">
        <div class="marquee-item">🐳 <span>Docker</span></div>
        <div class="marquee-item">☁️ <span>AWS EC2</span></div>
        <div class="marquee-item">⚙️ <span>GitHub Actions</span></div>
        <div class="marquee-item">☸️ <span>Kubernetes</span></div>
        <div class="marquee-item">🏗️ <span>Terraform</span></div>
        <div class="marquee-item">🐍 <span>Python</span></div>
        <div class="marquee-item">📊 <span>Prometheus</span></div>
        <div class="marquee-item">🐘 <span>PostgreSQL</span></div>
        <div class="marquee-item">🔧 <span>Jenkins</span></div>
        <div class="marquee-item">🐳 <span>Docker</span></div>
        <div class="marquee-item">☁️ <span>AWS EC2</span></div>
        <div class="marquee-item">⚙️ <span>GitHub Actions</span></div>
        <div class="marquee-item">☸️ <span>Kubernetes</span></div>
        <div class="marquee-item">🏗️ <span>Terraform</span></div>
        <div class="marquee-item">🐍 <span>Python</span></div>
        <div class="marquee-item">📊 <span>Prometheus</span></div>
        <div class="marquee-item">🐘 <span>PostgreSQL</span></div>
        <div class="marquee-item">🔧 <span>Jenkins</span></div>
    </div>
</div>

<section class="stats">
    <div class="stats-inner">
        <div class="stat-card reveal">
            <div class="stat-icon">💼</div>
            <div class="stat-number" data-count="3">0</div><span style="font-size:40px;font-weight:900;color:#00d4ff;font-family:'JetBrains Mono',monospace;">+</span>
            <div class="stat-label">Years Experience</div>
        </div>
        <div class="stat-card reveal">
            <div class="stat-icon">🌍</div>
            <div class="stat-number" data-count="{count}">0</div>
            <div class="stat-label">Live Visitors</div>
        </div>
        <div class="stat-card reveal">
            <div class="stat-icon">🏢</div>
            <div class="stat-number" data-count="6">0</div><span style="font-size:40px;font-weight:900;color:#00d4ff;font-family:'JetBrains Mono',monospace;">+</span>
            <div class="stat-label">Companies</div>
        </div>
        <div class="stat-card reveal">
            <div class="stat-icon">🚀</div>
            <div class="stat-number" data-count="10">0</div><span style="font-size:40px;font-weight:900;color:#00d4ff;font-family:'JetBrains Mono',monospace;">+</span>
            <div class="stat-label">Projects</div>
        </div>
    </div>
</section>

<section class="about" id="about">
    <div class="about-inner">
        <div class="about-img-wrap reveal">
            <img src="/static/goku.jpg" alt="Sriram">
        </div>
        <div class="reveal">
            <span class="about-tag">// About Me</span>
            <h2>Training Like <span>Ultra Instinct</span> Every Day 💪</h2>
            <p>Just like Goku never stops pushing his limits, I never stop learning. Every project makes me faster, more reliable, and more powerful.</p>
            <p>From CI/CD pipelines to Kubernetes clusters — I make sure infrastructure runs at full power 24/7 with zero downtime.</p>
            <div class="about-grid">
                <div class="about-stat">
                    <div class="about-stat-num">99.9%</div>
                    <div class="about-stat-label">Uptime Goal</div>
                </div>
                <div class="about-stat">
                    <div class="about-stat-num">0</div>
                    <div class="about-stat-label">Manual Deploys</div>
                </div>
                <div class="about-stat">
                    <div class="about-stat-num">24/7</div>
                    <div class="about-stat-label">Monitoring</div>
                </div>
                <div class="about-stat">
                    <div class="about-stat-num">∞</div>
                    <div class="about-stat-label">Scalability</div>
                </div>
            </div>
        </div>
    </div>
</section>

<section class="skills" id="skills">
    <div class="section-header reveal">
        <span class="section-eyebrow">// expertise</span>
        <h2 class="section-title">What I Work With</h2>
        <p class="section-sub">Tools and technologies I use to build and scale infrastructure</p>
    </div>
    <div class="skills-grid">
        <div class="skill-card reveal">
            <span class="skill-icon">🐳</span>
            <div class="skill-name">Docker & Kubernetes</div>
            <div class="skill-desc">Container orchestration and microservices deployment at scale</div>
            <div class="skill-bar"><div class="skill-fill" style="width:88%"></div></div>
            <div class="skill-percent">88%</div>
        </div>
        <div class="skill-card reveal">
            <span class="skill-icon">☁️</span>
            <div class="skill-name">AWS Cloud</div>
            <div class="skill-desc">EC2, S3, RDS, EKS, Lambda — full cloud infrastructure</div>
            <div class="skill-bar"><div class="skill-fill" style="width:82%"></div></div>
            <div class="skill-percent">82%</div>
        </div>
        <div class="skill-card reveal">
            <span class="skill-icon">⚙️</span>
            <div class="skill-name">CI/CD Pipelines</div>
            <div class="skill-desc">GitHub Actions, Jenkins — automated zero-downtime deployments</div>
            <div class="skill-bar"><div class="skill-fill" style="width:92%"></div></div>
            <div class="skill-percent">92%</div>
        </div>
        <div class="skill-card reveal">
            <span class="skill-icon">🏗️</span>
            <div class="skill-name">Terraform</div>
            <div class="skill-desc">Infrastructure as Code for cloud resources</div>
            <div class="skill-bar"><div class="skill-fill" style="width:72%"></div></div>
            <div class="skill-percent">72%</div>
        </div>
        <div class="skill-card reveal">
            <span class="skill-icon">🐍</span>
            <div class="skill-name">Python & Bash</div>
            <div class="skill-desc">Scripting and automation for DevOps workflows</div>
            <div class="skill-bar"><div class="skill-fill" style="width:78%"></div></div>
            <div class="skill-percent">78%</div>
        </div>
        <div class="skill-card reveal">
            <span class="skill-icon">📊</span>
            <div class="skill-name">Monitoring</div>
            <div class="skill-desc">Prometheus, Grafana, ELK Stack observability</div>
            <div class="skill-bar"><div class="skill-fill" style="width:68%"></div></div>
            <div class="skill-percent">68%</div>
        </div>
    </div>
</section>

<section class="projects" id="projects">
    <div class="section-header reveal">
        <span class="section-eyebrow">// portfolio</span>
        <h2 class="section-title">Projects Built</h2>
        <p class="section-sub">Real infrastructure deployed to production on AWS</p>
    </div>
    <div class="projects-grid">
        <div class="project-card featured reveal">
            <div class="live-badge">● Live on AWS</div>
            <div class="project-num">// PROJECT 01</div>
            <div class="project-title">🚀 Flask DevOps Pipeline</div>
            <div class="project-desc">Flask web app containerized with Docker, deployed to AWS EC2 with a fully automated CI/CD pipeline using GitHub Actions. Zero manual deployment.</div>
            <div class="techs">
                <span class="tech">Python</span>
                <span class="tech">Docker</span>
                <span class="tech">AWS EC2</span>
                <span class="tech">GitHub Actions</span>
            </div>
        </div>
        <div class="project-card featured reveal">
            <div class="live-badge">● You Are Here!</div>
            <div class="project-num">// PROJECT 02</div>
            <div class="project-title">🐘 App + Database</div>
            <div class="project-desc">Flask + PostgreSQL running in Docker Compose. Fully automated CI/CD that deploys to AWS on every git push. Live visitor tracking in real database!</div>
            <div class="techs">
                <span class="tech">Flask</span>
                <span class="tech">PostgreSQL</span>
                <span class="tech">Docker Compose</span>
                <span class="tech">Auto Deploy</span>
            </div>
        </div>
        <div class="project-card reveal">
            <div class="soon-badge">🔜 Coming Soon</div>
            <div class="project-num">// PROJECT 03</div>
            <div class="project-title">☸️ Kubernetes Cluster</div>
            <div class="project-desc">Production Kubernetes on AWS EKS with auto-scaling, load balancing, health checks and full observability stack.</div>
            <div class="techs">
                <span class="tech">Kubernetes</span>
                <span class="tech">AWS EKS</span>
                <span class="tech">Helm</span>
                <span class="tech">Prometheus</span>
            </div>
        </div>
        <div class="project-card reveal">
            <div class="soon-badge">🔜 Coming Soon</div>
            <div class="project-num">// PROJECT 04</div>
            <div class="project-title">🏗️ Terraform IaC</div>
            <div class="project-desc">Complete AWS infrastructure as code — VPC, subnets, security groups, auto scaling groups and RDS databases.</div>
            <div class="techs">
                <span class="tech">Terraform</span>
                <span class="tech">AWS VPC</span>
                <span class="tech">IaC</span>
                <span class="tech">Ansible</span>
            </div>
        </div>
    </div>
</section>

<section class="visitor" id="visitors">
    <div class="visitor-bg">
        <img src="/static/bg.jpg" alt="bg">
    </div>
    <div class="visitor-overlay"></div>
    <div class="visitor-content reveal">
        <span class="visitor-eyebrow">// live database</span>
        <h2>Real Visitors. Real Data.</h2>
        <div class="visitor-count">{count}</div>
        <p>Every visit tracked in a PostgreSQL database running inside Docker on AWS EC2!</p>
        <div class="visitor-badges">
            <div class="visitor-badge">🐘 PostgreSQL</div>
            <div class="visitor-badge">🐳 Docker</div>
            <div class="visitor-badge">☁️ AWS EC2</div>
            <div class="visitor-badge">⚙️ Auto Deploy</div>
        </div>
    </div>
</section>

<footer>
    <div class="footer-left">Built by <span>Sriram Mamidala</span> · DevOps Engineer · Los Angeles 🌴</div>
    <div class="footer-links">
        <a href="https://github.com/mamidalasriram4-hub">GitHub</a>
        <a href="#">LinkedIn</a>
        <a href="/health">Status ●</a>
    </div>
</footer>

<script>
    // Custom cursor
    const cursor = document.getElementById('cursor');
    const follower = document.getElementById('cursorFollower');
    document.addEventListener('mousemove', e => {{
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
        setTimeout(() => {{
            follower.style.left = e.clientX + 'px';
            follower.style.top = e.clientY + 'px';
        }}, 80);
    }});

    // Hover effect on cursor
    document.querySelectorAll('a, button, .stat-card, .skill-card, .project-card').forEach(el => {{
        el.addEventListener('mouseenter', () => {{
            cursor.style.transform = 'translate(-50%, -50%) scale(2)';
            follower.style.transform = 'translate(-50%, -50%) scale(1.5)';
            follower.style.borderColor = 'rgba(0,212,255,0.8)';
        }});
        el.addEventListener('mouseleave', () => {{
            cursor.style.transform = 'translate(-50%, -50%) scale(1)';
            follower.style.transform = 'translate(-50%, -50%) scale(1)';
            follower.style.borderColor = 'rgba(0,212,255,0.5)';
        }});
    }});

    // Scroll reveal
    const reveals = document.querySelectorAll('.reveal');
    const observer = new IntersectionObserver(entries => {{
        entries.forEach(entry => {{
            if(entry.isIntersecting) {{
                entry.target.classList.add('visible');
                if(entry.target.classList.contains('skill-card')) {{
                    entry.target.classList.add('visible');
                }}
            }}
        }});
    }}, {{ threshold: 0.1 }});
    reveals.forEach(el => observer.observe(el));

    // Skill cards observer
    document.querySelectorAll('.skill-card').forEach(card => {{
        observer.observe(card);
    }});

    // Counter animation
    const counters = document.querySelectorAll('.stat-number[data-count]');
    const countObserver = new IntersectionObserver(entries => {{
        entries.forEach(entry => {{
            if(entry.isIntersecting) {{
                const target = parseInt(entry.target.getAttribute('data-count'));
                const duration = 2000;
                const step = target / (duration / 16);
                let current = 0;
                const timer = setInterval(() => {{
                    current += step;
                    if(current >= target) {{
                        current = target;
                        clearInterval(timer);
                    }}
                    entry.target.textContent = Math.floor(current);
                }}, 16);
                countObserver.unobserve(entry.target);
            }}
        }});
    }}, {{ threshold: 0.5 }});
    counters.forEach(counter => countObserver.observe(counter));
</script>

</body>
</html>
    """

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
