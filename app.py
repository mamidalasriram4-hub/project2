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
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Syne', sans-serif; background: #050508; color: #fff; overflow-x: hidden; }}

        /* NAV */
        nav {{ position: fixed; top: 0; width: 100%; z-index: 100; padding: 20px 60px; display: flex; justify-content: space-between; align-items: center; background: rgba(5,5,8,0.7); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255,255,255,0.05); }}
        .logo {{ font-family: 'JetBrains Mono', monospace; font-size: 18px; color: #00d4ff; }}
        nav ul {{ list-style: none; display: flex; gap: 40px; }}
        nav ul a {{ color: #aaa; text-decoration: none; font-size: 14px; transition: color 0.3s; font-family: 'JetBrains Mono', monospace; }}
        nav ul a:hover {{ color: #00d4ff; }}
        .nav-badge {{ background: rgba(0,212,255,0.1); border: 1px solid rgba(0,212,255,0.3); color: #00d4ff; padding: 6px 16px; border-radius: 20px; font-size: 12px; font-family: 'JetBrains Mono', monospace; }}

        /* HERO */
        .hero {{ min-height: 100vh; position: relative; display: flex; align-items: center; justify-content: center; text-align: center; overflow: hidden; }}
        .hero-bg {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: url('/static/bg.jpg'); background-size: cover; background-position: center; filter: brightness(0.3); }}
        .hero-overlay {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(180deg, rgba(5,5,8,0.3) 0%, rgba(5,5,8,0.8) 100%); }}
        .hero-content {{ position: relative; z-index: 2; max-width: 900px; padding: 20px; }}
        .hero-badge {{ display: inline-block; background: rgba(0,212,255,0.15); border: 1px solid rgba(0,212,255,0.3); color: #00d4ff; padding: 8px 20px; border-radius: 30px; font-size: 13px; margin-bottom: 24px; font-family: 'JetBrains Mono', monospace; }}
        .hero h1 {{ font-size: 72px; font-weight: 800; line-height: 1.1; margin-bottom: 20px; }}
        .hero h1 span {{ background: linear-gradient(135deg, #00d4ff, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
        .hero p {{ font-size: 20px; color: #ccc; margin-bottom: 40px; line-height: 1.7; }}
        .hero-btns {{ display: flex; gap: 15px; justify-content: center; }}
        .btn-primary {{ background: linear-gradient(135deg, #00d4ff, #0099bb); color: #000; padding: 16px 40px; border-radius: 50px; text-decoration: none; font-weight: 800; font-size: 15px; }}
        .btn-secondary {{ border: 2px solid rgba(255,255,255,0.2); color: white; padding: 16px 40px; border-radius: 50px; text-decoration: none; font-weight: 700; font-size: 15px; }}

        /* STATS */
        .stats {{ padding: 80px 60px; background: #0a0a0f; }}
        .stats-grid {{ max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: repeat(4,1fr); gap: 20px; }}
        .stat-card {{ background: #111; border: 1px solid #222; border-radius: 20px; padding: 30px; text-align: center; }}
        .stat-number {{ font-size: 48px; font-weight: 800; color: #00d4ff; font-family: 'JetBrains Mono', monospace; }}
        .stat-label {{ color: #666; font-size: 13px; margin-top: 8px; }}

        /* GOKU SECTION */
        .goku-section {{ padding: 80px 60px; background: #050508; display: flex; align-items: center; max-width: 1100px; margin: 0 auto; gap: 60px; }}
        .goku-image {{ flex: 1; border-radius: 20px; overflow: hidden; border: 2px solid rgba(245,158,11,0.3); box-shadow: 0 0 60px rgba(245,158,11,0.2); }}
        .goku-image img {{ width: 100%; height: 500px; object-fit: cover; object-position: center top; }}
        .goku-text {{ flex: 1; }}
        .goku-text .tag {{ font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #f59e0b; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 16px; display: block; }}
        .goku-text h2 {{ font-size: 42px; font-weight: 800; line-height: 1.2; margin-bottom: 20px; }}
        .goku-text h2 span {{ color: #f59e0b; }}
        .goku-text p {{ color: #888; font-size: 16px; line-height: 1.8; margin-bottom: 30px; }}
        .goku-stats {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
        .goku-stat {{ background: #111; border: 1px solid #222; border-radius: 12px; padding: 16px; }}
        .goku-stat-num {{ font-size: 28px; font-weight: 800; color: #f59e0b; font-family: 'JetBrains Mono', monospace; }}
        .goku-stat-label {{ font-size: 12px; color: #666; margin-top: 4px; }}

        /* SKILLS */
        .skills {{ padding: 80px 60px; background: #0a0a0f; }}
        .section-header {{ text-align: center; margin-bottom: 50px; }}
        .section-tag {{ font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #00d4ff; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 12px; display: block; }}
        .section-title {{ font-size: 42px; font-weight: 800; margin-bottom: 12px; }}
        .section-sub {{ color: #666; font-size: 16px; }}
        .skills-grid {{ max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: repeat(3,1fr); gap: 20px; }}
        .skill-card {{ background: #111; border: 1px solid #1a1a1a; border-radius: 20px; padding: 28px; transition: all 0.3s; }}
        .skill-card:hover {{ border-color: rgba(0,212,255,0.3); transform: translateY(-5px); }}
        .skill-icon {{ font-size: 32px; margin-bottom: 14px; }}
        .skill-name {{ font-size: 17px; font-weight: 700; margin-bottom: 8px; }}
        .skill-desc {{ color: #666; font-size: 13px; line-height: 1.6; margin-bottom: 16px; }}
        .skill-bar {{ background: #222; border-radius: 10px; height: 4px; }}
        .skill-fill {{ height: 100%; border-radius: 10px; background: linear-gradient(90deg, #00d4ff, #f59e0b); }}

        /* PROJECTS */
        .projects {{ padding: 80px 60px; background: #050508; }}
        .projects-grid {{ max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: repeat(2,1fr); gap: 24px; }}
        .project-card {{ background: #111; border: 1px solid #1a1a1a; border-radius: 20px; padding: 32px; transition: all 0.3s; }}
        .project-card:hover {{ border-color: rgba(0,212,255,0.3); transform: translateY(-5px); }}
        .project-card.live {{ border-color: rgba(0,212,255,0.2); }}
        .live-badge {{ display: inline-block; background: rgba(16,185,129,0.1); color: #10b981; border: 1px solid rgba(16,185,129,0.3); padding: 4px 12px; border-radius: 20px; font-size: 11px; margin-bottom: 12px; font-family: 'JetBrains Mono', monospace; }}
        .soon-badge {{ display: inline-block; background: rgba(245,158,11,0.1); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); padding: 4px 12px; border-radius: 20px; font-size: 11px; margin-bottom: 12px; font-family: 'JetBrains Mono', monospace; }}
        .project-num {{ font-size: 11px; color: #00d4ff; font-family: 'JetBrains Mono', monospace; letter-spacing: 2px; margin-bottom: 12px; }}
        .project-title {{ font-size: 20px; font-weight: 700; margin-bottom: 10px; }}
        .project-desc {{ color: #666; font-size: 14px; line-height: 1.7; margin-bottom: 20px; }}
        .techs {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .tech {{ background: rgba(0,212,255,0.08); border: 1px solid rgba(0,212,255,0.15); color: #00d4ff; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-family: 'JetBrains Mono', monospace; }}

        /* VISITOR */
        .visitor {{ padding: 80px 60px; text-align: center; position: relative; overflow: hidden; }}
        .visitor-bg {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: url('/static/goku.jpg'); background-size: cover; background-position: center; filter: brightness(0.15); }}
        .visitor-overlay {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(5,5,8,0.7); }}
        .visitor-content {{ position: relative; z-index: 2; }}
        .visitor h2 {{ font-size: 42px; font-weight: 800; margin-bottom: 10px; }}
        .visitor-count {{ font-size: 120px; font-weight: 800; background: linear-gradient(135deg, #00d4ff, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-family: 'JetBrains Mono', monospace; line-height: 1; margin: 20px 0; }}
        .visitor p {{ color: #888; font-size: 18px; }}
        .visitor-badge {{ display: inline-block; background: rgba(0,212,255,0.1); border: 1px solid rgba(0,212,255,0.2); color: #aaa; padding: 8px 20px; border-radius: 20px; font-size: 13px; margin-top: 20px; font-family: 'JetBrains Mono', monospace; }}

        /* FOOTER */
        footer {{ padding: 40px 60px; border-top: 1px solid #111; display: flex; justify-content: space-between; align-items: center; background: #050508; }}
        footer .left {{ font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #555; }}
        footer .left span {{ color: #00d4ff; }}
        footer .right a {{ color: #555; text-decoration: none; font-size: 13px; margin-left: 24px; font-family: 'JetBrains Mono', monospace; transition: color 0.3s; }}
        footer .right a:hover {{ color: #00d4ff; }}
    </style>
</head>
<body>

<!-- NAV -->
<nav>
    <div class="logo">&lt;sriram.dev/&gt;</div>
    <ul>
        <li><a href="#skills">Skills</a></li>
        <li><a href="#projects">Projects</a></li>
        <li><a href="#visitors">Visitors</a></li>
    </ul>
    <div class="nav-badge">● Available for hire</div>
</nav>

<!-- HERO with BG.JPG -->
<section class="hero">
    <div class="hero-bg"></div>
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <div class="hero-badge">DevOps Engineer · Los Angeles 🌴</div>
        <h1>Hi, I'm <span>Sriram Mamidala</span></h1>
        <p>Building infrastructure that never sleeps.<br>Docker · AWS · Kubernetes · CI/CD</p>
        <div class="hero-btns">
            <a href="#projects" class="btn-primary">View Projects →</a>
            <a href="#visitors" class="btn-secondary">Live Visitors</a>
        </div>
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

<!-- GOKU SECTION with GOKU.JPG -->
<section style="padding: 80px 60px; background: #050508;">
    <div class="goku-section" style="padding: 0;">
        <div class="goku-image">
            <img src="/static/goku.jpg" alt="Power">
        </div>
        <div class="goku-text">
            <span class="tag">// About Me</span>
            <h2>Powering Apps Like <span>Ultra Instinct</span> 😄</h2>
            <p>Just like Goku never stops training, I never stop learning. Every project I build is faster, more reliable, and more powerful than the last.</p>
            <p style="margin-top: 16px;">From setting up CI/CD pipelines to deploying Kubernetes clusters — I make sure your app runs at full power 24/7!</p>
            <div class="goku-stats" style="margin-top: 30px;">
                <div class="goku-stat">
                    <div class="goku-stat-num">99.9%</div>
                    <div class="goku-stat-label">Uptime Goal</div>
                </div>
                <div class="goku-stat">
                    <div class="goku-stat-num">0</div>
                    <div class="goku-stat-label">Manual Deploys</div>
                </div>
                <div class="goku-stat">
                    <div class="goku-stat-num">24/7</div>
                    <div class="goku-stat-label">Monitoring</div>
                </div>
                <div class="goku-stat">
                    <div class="goku-stat-num">∞</div>
                    <div class="goku-stat-label">Scalability</div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- SKILLS -->
<section class="skills" id="skills">
    <div class="section-header">
        <span class="section-tag">// expertise</span>
        <h2 class="section-title">What I Work With</h2>
        <p class="section-sub">Tools and technologies I use daily</p>
    </div>
    <div class="skills-grid">
        <div class="skill-card">
            <div class="skill-icon">🐳</div>
            <div class="skill-name">Docker & Kubernetes</div>
            <div class="skill-desc">Container orchestration and microservices at scale</div>
            <div class="skill-bar"><div class="skill-fill" style="width:88%"></div></div>
        </div>
        <div class="skill-card">
            <div class="skill-icon">☁️</div>
            <div class="skill-name">AWS Cloud</div>
            <div class="skill-desc">EC2, S3, RDS, EKS, Lambda and more</div>
            <div class="skill-bar"><div class="skill-fill" style="width:82%"></div></div>
        </div>
        <div class="skill-card">
            <div class="skill-icon">⚙️</div>
            <div class="skill-name">CI/CD Pipelines</div>
            <div class="skill-desc">GitHub Actions, Jenkins — zero manual deploys</div>
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
            <div class="skill-desc">Scripting and automation for DevOps</div>
            <div class="skill-bar"><div class="skill-fill" style="width:78%"></div></div>
        </div>
        <div class="skill-card">
            <div class="skill-icon">📊</div>
            <div class="skill-name">Monitoring</div>
            <div class="skill-desc">Prometheus, Grafana, ELK Stack</div>
            <div class="skill-bar"><div class="skill-fill" style="width:68%"></div></div>
        </div>
    </div>
</section>

<!-- PROJECTS -->
<section class="projects" id="projects">
    <div class="section-header">
        <span class="section-tag">// portfolio</span>
        <h2 class="section-title">Projects Built</h2>
        <p class="section-sub">Real infrastructure deployed to production</p>
    </div>
    <div class="projects-grid">
        <div class="project-card live">
            <div class="live-badge">🟢 Live on AWS</div>
            <div class="project-num">// PROJECT 01</div>
            <div class="project-title">🚀 Flask DevOps Pipeline</div>
            <div class="project-desc">Flask app deployed to AWS EC2 with Docker and automated CI/CD pipeline using GitHub Actions.</div>
            <div class="techs">
                <span class="tech">Python</span>
                <span class="tech">Docker</span>
                <span class="tech">AWS EC2</span>
                <span class="tech">GitHub Actions</span>
            </div>
        </div>
        <div class="project-card live">
            <div class="live-badge">🟢 You Are Here!</div>
            <div class="project-num">// PROJECT 02</div>
            <div class="project-title">🐘 App + Database</div>
            <div class="project-desc">Flask + PostgreSQL in Docker Compose. Auto-deploys to AWS on every git push!</div>
            <div class="techs">
                <span class="tech">Flask</span>
                <span class="tech">PostgreSQL</span>
                <span class="tech">Docker Compose</span>
                <span class="tech">Auto Deploy</span>
            </div>
        </div>
        <div class="project-card">
            <div class="soon-badge">🔜 Coming Soon</div>
            <div class="project-num">// PROJECT 03</div>
            <div class="project-title">☸️ Kubernetes Cluster</div>
            <div class="project-desc">Production Kubernetes on AWS EKS with auto-scaling and monitoring.</div>
            <div class="techs">
                <span class="tech">Kubernetes</span>
                <span class="tech">AWS EKS</span>
                <span class="tech">Helm</span>
                <span class="tech">Prometheus</span>
            </div>
        </div>
        <div class="project-card">
            <div class="soon-badge">🔜 Coming Soon</div>
            <div class="project-num">// PROJECT 04</div>
            <div class="project-title">🏗️ Terraform IaC</div>
            <div class="project-desc">Complete AWS infrastructure as code — VPC, subnets, RDS and auto scaling.</div>
            <div class="techs">
                <span class="tech">Terraform</span>
                <span class="tech">AWS VPC</span>
                <span class="tech">IaC</span>
                <span class="tech">Ansible</span>
            </div>
        </div>
    </div>
</section>

<!-- VISITOR with GOKU BG -->
<section class="visitor" id="visitors">
    <div class="visitor-bg"></div>
    <div class="visitor-overlay"></div>
    <div class="visitor-content">
        <h2>🌍 Live Visitor Count</h2>
        <div class="visitor-count">{count}</div>
        <p>Tracked in PostgreSQL database on AWS!</p>
        <div class="visitor-badge">🐘 PostgreSQL · 🐳 Docker · ☁️ AWS EC2</div>
    </div>
</section>

<!-- FOOTER -->
<footer>
    <div class="left">Built by <span>Sriram Mamidala</span> · DevOps Engineer · Los Angeles 🌴</div>
    <div class="right">
        <a href="https://github.com/mamidalasriram4-hub">GitHub</a>
        <a href="#">LinkedIn</a>
        <a href="/health">Status</a>
    </div>
</footer>

</body>
</html>
    """

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
