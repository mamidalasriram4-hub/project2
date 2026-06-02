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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #fff; color: #111; }}

        /* NAV */
        nav {{ padding: 20px 80px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; position: sticky; top: 0; background: white; z-index: 100; box-shadow: 0 2px 20px rgba(0,0,0,0.05); }}
        .logo {{ font-size: 20px; font-weight: 800; color: #3f59f6; }}
        nav ul {{ list-style: none; display: flex; gap: 35px; }}
        nav ul a {{ color: #555; text-decoration: none; font-size: 14px; font-weight: 500; transition: color 0.2s; }}
        nav ul a:hover {{ color: #3f59f6; }}
        .nav-btn {{ background: #3f59f6; color: white; padding: 10px 24px; border-radius: 8px; text-decoration: none; font-size: 14px; font-weight: 600; transition: background 0.2s; }}
        .nav-btn:hover {{ background: #2d47e0; }}

        /* HERO */
        .hero {{ padding: 100px 80px; text-align: center; background: linear-gradient(180deg, #f8f9ff 0%, #ffffff 100%); }}
        .hero-badge {{ display: inline-block; background: #eef0ff; color: #3f59f6; padding: 8px 20px; border-radius: 50px; font-size: 13px; font-weight: 600; margin-bottom: 24px; }}
        .hero h1 {{ font-size: 64px; font-weight: 800; line-height: 1.1; margin-bottom: 24px; color: #111; }}
        .hero h1 span {{ color: #3f59f6; }}
        .hero p {{ font-size: 20px; color: #666; max-width: 600px; margin: 0 auto 40px; line-height: 1.7; }}
        .hero-btns {{ display: flex; gap: 15px; justify-content: center; }}
        .btn-blue {{ background: #3f59f6; color: white; padding: 16px 36px; border-radius: 10px; text-decoration: none; font-weight: 700; font-size: 16px; transition: all 0.2s; box-shadow: 0 4px 20px rgba(63,89,246,0.3); }}
        .btn-blue:hover {{ background: #2d47e0; transform: translateY(-2px); }}
        .btn-outline {{ border: 2px solid #e0e0e0; color: #333; padding: 16px 36px; border-radius: 10px; text-decoration: none; font-weight: 700; font-size: 16px; transition: all 0.2s; }}
        .btn-outline:hover {{ border-color: #3f59f6; color: #3f59f6; }}

        /* STATS */
        .stats {{ padding: 60px 80px; background: white; }}
        .stats-grid {{ max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }}
        .stat-card {{ background: #f8f9ff; border-radius: 16px; padding: 30px; text-align: center; border: 1px solid #eef0ff; transition: transform 0.2s; }}
        .stat-card:hover {{ transform: translateY(-4px); }}
        .stat-number {{ font-size: 42px; font-weight: 800; color: #3f59f6; }}
        .stat-label {{ color: #888; font-size: 13px; margin-top: 6px; font-weight: 500; }}

        /* SKILLS */
        .skills {{ padding: 80px; background: #f8f9ff; }}
        .section-header {{ text-align: center; margin-bottom: 50px; }}
        .section-label {{ font-size: 13px; font-weight: 600; color: #3f59f6; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px; }}
        .section-title {{ font-size: 40px; font-weight: 800; color: #111; margin-bottom: 12px; }}
        .section-sub {{ color: #888; font-size: 16px; }}
        .skills-grid {{ max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
        .skill-card {{ background: white; border-radius: 16px; padding: 28px; border: 1px solid #eee; transition: all 0.2s; }}
        .skill-card:hover {{ border-color: #3f59f6; transform: translateY(-4px); box-shadow: 0 10px 30px rgba(63,89,246,0.1); }}
        .skill-icon {{ font-size: 32px; margin-bottom: 14px; }}
        .skill-name {{ font-size: 17px; font-weight: 700; margin-bottom: 8px; color: #111; }}
        .skill-desc {{ color: #888; font-size: 13px; line-height: 1.6; margin-bottom: 16px; }}
        .skill-bar {{ background: #f0f0f0; border-radius: 10px; height: 6px; }}
        .skill-fill {{ height: 100%; border-radius: 10px; background: linear-gradient(90deg, #3f59f6, #8b5cf6); }}

        /* PROJECTS */
        .projects {{ padding: 80px; background: white; }}
        .projects-grid {{ max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }}
        .project-card {{ background: #f8f9ff; border-radius: 16px; padding: 32px; border: 1px solid #eef0ff; transition: all 0.2s; }}
        .project-card:hover {{ border-color: #3f59f6; transform: translateY(-4px); box-shadow: 0 10px 30px rgba(63,89,246,0.1); }}
        .project-card.live {{ background: linear-gradient(135deg, #f0f4ff, #f8f0ff); border-color: #c7d0ff; }}
        .project-num {{ font-size: 12px; font-weight: 600; color: #3f59f6; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }}
        .project-title {{ font-size: 20px; font-weight: 700; margin-bottom: 10px; color: #111; }}
        .project-desc {{ color: #777; font-size: 14px; line-height: 1.7; margin-bottom: 20px; }}
        .techs {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .tech {{ background: white; border: 1px solid #e0e0e0; color: #555; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 500; }}
        .live-badge {{ display: inline-block; background: #dcfce7; color: #16a34a; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; margin-bottom: 12px; }}
        .soon-badge {{ display: inline-block; background: #fef9c3; color: #ca8a04; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; margin-bottom: 12px; }}

        /* VISITOR */
        .visitor {{ padding: 80px; background: linear-gradient(135deg, #3f59f6, #8b5cf6); text-align: center; color: white; }}
        .visitor h2 {{ font-size: 36px; font-weight: 800; margin-bottom: 10px; }}
        .visitor-count {{ font-size: 100px; font-weight: 800; line-height: 1; margin: 20px 0; }}
        .visitor p {{ font-size: 18px; opacity: 0.85; }}
        .visitor-badge {{ display: inline-block; background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.3); padding: 8px 20px; border-radius: 20px; font-size: 13px; margin-top: 20px; }}

        /* FOOTER */
        footer {{ padding: 40px 80px; background: #111; color: #888; display: flex; justify-content: space-between; align-items: center; }}
        footer .left {{ font-size: 14px; }}
        footer .left span {{ color: #3f59f6; font-weight: 600; }}
        footer .right {{ display: flex; gap: 24px; }}
        footer .right a {{ color: #888; text-decoration: none; font-size: 13px; transition: color 0.2s; }}
        footer .right a:hover {{ color: white; }}

        @media (max-width: 768px) {{
            nav {{ padding: 15px 20px; }}
            .hero {{ padding: 60px 20px; }}
            .hero h1 {{ font-size: 36px; }}
            .stats, .skills, .projects, .visitor {{ padding: 40px 20px; }}
            .stats-grid, .skills-grid, .projects-grid {{ grid-template-columns: 1fr; }}
            footer {{ padding: 30px 20px; flex-direction: column; gap: 15px; text-align: center; }}
        }}
    </style>
</head>
<body>

<!-- NAV -->
<nav>
    <div class="logo">Sriram.dev</div>
    <ul>
        <li><a href="#skills">Skills</a></li>
        <li><a href="#projects">Projects</a></li>
        <li><a href="#visitors">Visitors</a></li>
    </ul>
    <a href="#visitors" class="nav-btn">Live Count →</a>
</nav>

<!-- HERO -->
<section class="hero">
    <div class="hero-badge">👋 Available for DevOps roles in LA</div>
    <h1>Hi, I'm <span>Sriram Mamidala</span><br>DevOps Engineer</h1>
    <p>Building reliable infrastructure that powers modern applications. Based in Los Angeles 🌴</p>
    <div class="hero-btns">
        <a href="#projects" class="btn-blue">View My Projects →</a>
        <a href="#visitors" class="btn-outline">Live Visitor Count</a>
    </div>
</section>

<!-- STATS -->
<section class="stats">
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">3+</div>
            <div class="stat-label">Years Experience</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{count}</div>
            <div class="stat-label">Live Visitors</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">6+</div>
            <div class="stat-label">Companies</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">10+</div>
            <div class="stat-label">Projects</div>
        </div>
    </div>
</section>

<!-- SKILLS -->
<section class="skills" id="skills">
    <div class="section-header">
        <div class="section-label">Expertise</div>
        <h2 class="section-title">What I Work With</h2>
        <p class="section-sub">Tools and technologies I use daily</p>
    </div>
    <div class="skills-grid">
        <div class="skill-card">
            <div class="skill-icon">🐳</div>
            <div class="skill-name">Docker & Kubernetes</div>
            <div class="skill-desc">Container orchestration and microservices deployment at scale</div>
            <div class="skill-bar"><div class="skill-fill" style="width:88%"></div></div>
        </div>
        <div class="skill-card">
            <div class="skill-icon">☁️</div>
            <div class="skill-name">AWS Cloud</div>
            <div class="skill-desc">EC2, S3, RDS, EKS, Lambda — full cloud infrastructure</div>
            <div class="skill-bar"><div class="skill-fill" style="width:82%"></div></div>
        </div>
        <div class="skill-card">
            <div class="skill-icon">⚙️</div>
            <div class="skill-name">CI/CD Pipelines</div>
            <div class="skill-desc">GitHub Actions, Jenkins — automated deployments</div>
            <div class="skill-bar"><div class="skill-fill" style="width:92%"></div></div>
        </div>
        <div class="skill-card">
            <div class="skill-icon">🏗️</div>
            <div class="skill-name">Terraform</div>
            <div class="skill-desc">Infrastructure as Code for cloud resources</div>
            <div class="skill-bar"><div class="skill-fill" style="width:72%"></div></div>
        </div>
        <div class="skill-card">
            <div class="skill-icon">🐍</div>
            <div class="skill-name">Python & Bash</div>
            <div class="skill-desc">Scripting and automation for DevOps workflows</div>
            <div class="skill-bar"><div class="skill-fill" style="width:78%"></div></div>
        </div>
        <div class="skill-card">
            <div class="skill-icon">📊</div>
            <div class="skill-name">Monitoring</div>
            <div class="skill-desc">Prometheus, Grafana, ELK Stack observability</div>
            <div class="skill-bar"><div class="skill-fill" style="width:68%"></div></div>
        </div>
    </div>
</section>

<!-- PROJECTS -->
<section class="projects" id="projects">
    <div class="section-header">
        <div class="section-label">Portfolio</div>
        <h2 class="section-title">Projects Built</h2>
        <p class="section-sub">Real infrastructure deployed to production</p>
    </div>
    <div class="projects-grid">
        <div class="project-card live">
            <div class="live-badge">🟢 Live on AWS</div>
            <div class="project-num">Project 01</div>
            <div class="project-title">🚀 Flask DevOps Pipeline</div>
            <div class="project-desc"
