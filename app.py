from flask import Flask
import psycopg2
import os
from datetime import datetime

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
        count = cur.fetchone()[0]
        return count
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
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', sans-serif; background: #0a0a0a; color: #fff; }}
            
            /* NAVBAR */
            nav {{ background: rgba(0,0,0,0.9); padding: 20px 40px; display: flex; justify-content: space-between; align-items: center; position: fixed; width: 100%; top: 0; z-index: 100; border-bottom: 1px solid #333; }}
            nav .logo {{ font-size: 22px; font-weight: bold; color: #667eea; }}
            nav ul {{ list-style: none; display: flex; gap: 30px; }}
            nav ul a {{ color: #ccc; text-decoration: none; font-size: 15px; }}
            nav ul a:hover {{ color: #667eea; }}

            /* HERO */
            .hero {{ min-height: 100vh; display: flex; align-items: center; justify-content: center; text-align: center; background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%); padding-top: 80px; }}
            .hero-content {{ max-width: 800px; padding: 20px; }}
            .hero-badge {{ background: rgba(102,126,234,0.2); border: 1px solid #667eea; color: #667eea; padding: 8px 20px; border-radius: 20px; font-size: 14px; display: inline-block; margin-bottom: 20px; }}
            .hero h1 {{ font-size: 60px; font-weight: 800; line-height: 1.1; margin-bottom: 20px; }}
            .hero h1 span {{ background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
            .hero p {{ font-size: 20px; color: #aaa; margin-bottom: 40px; line-height: 1.6; }}
            .hero-btns {{ display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; }}
            .btn-primary {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 15px 35px; border-radius: 30px; text-decoration: none; font-weight: bold; font-size: 16px; }}
            .btn-secondary {{ border: 2px solid #667eea; color: #667eea; padding: 15px 35px; border-radius: 30px; text-decoration: none; font-weight: bold; font-size: 16px; }}
            
            /* STATS */
            .stats {{ background: #111; padding: 60px 40px; }}
            .stats-grid {{ max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; text-align: center; }}
            .stat-card {{ background: #1a1a2e; padding: 30px 20px; border-radius: 15px; border: 1px solid #333; }}
            .stat-number {{ font-size: 40px; font-weight: 800; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
            .stat-label {{ color: #aaa; font-size: 14px; margin-top: 5px; }}

            /* SKILLS */
            .skills {{ padding: 80px 40px; background: #0a0a0a; }}
            .section-title {{ text-align: center; font-size: 36px; font-weight: 800; margin-bottom: 10px; }}
            .section-sub {{ text-align: center; color: #aaa; margin-bottom: 50px; font-size: 16px; }}
            .skills-grid {{ max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
            .skill-card {{ background: #111; border-radius: 15px; padding: 25px; border: 1px solid #222; transition: border-color 0.3s; }}
            .skill-card:hover {{ border-color: #667eea; }}
            .skill-icon {{ font-size: 36px; margin-bottom: 15px; }}
            .skill-name {{ font-size: 18px; font-weight: bold; margin-bottom: 8px; }}
            .skill-desc {{ color: #aaa; font-size: 14px; line-height: 1.5; }}
            .skill-bar {{ background: #222; border-radius: 10px; height: 6px; margin-top: 15px; }}
            .skill-fill {{ height: 100%; border-radius: 10px; background: linear-gradient(135deg, #667eea, #764ba2); }}

            /* PROJECTS */
            .projects {{ padding: 80px 40px; background: #111; }}
            .projects-grid {{ max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: repeat(2, 1fr); gap: 25px; }}
            .project-card {{ background: #1a1a2e; border-radius: 15px; padding: 30px; border: 1px solid #333; }}
            .project-tag {{ background: rgba(102,126,234,0.2); color: #667eea; padding: 4px 12px; border-radius: 10px; font-size: 12px; display: inline-block; margin-bottom: 15px; }}
            .project-title {{ font-size: 20px; font-weight: bold; margin-bottom: 10px; }}
            .project-desc {{ color: #aaa; font-size: 14px; line-height: 1.6; margin-bottom: 20px; }}
            .project-techs {{ display: flex; flex-wrap: wrap; gap: 8px; }}
            .tech-badge {{ background: #0f3460; padding: 4px 12px; border-radius: 10px; font-size: 12px; color: #ccc; }}

            /* VISITOR */
            .visitor {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 60px 40px; text-align: center; }}
            .visitor h2 {{ font-size: 36px; margin-bottom: 10px; }}
            .visitor-count {{ font-size: 80px; font-weight: 800; }}
            .visitor p {{ font-size: 18px; opacity: 0.8; margin-top: 10px; }}

            /* FOOTER */
            footer {{ background: #0a0a0a; padding: 40px; text-align: center; color: #555; border-top: 1px solid #222; }}
        </style>
    </head>
    <body>

        <!-- NAVBAR -->
        <nav>
            <div class="logo">Sriram.dev</div>
            <ul>
                <li><a href="#skills">Skills</a></li>
                <li><a href="#projects">Projects</a></li>
                <li><a href="#visitors">Visitors</a></li>
            </ul>
        </nav>

        <!-- HERO -->
        <section class="hero">
            <div class="hero-content">
                <div class="hero-badge">👋 Available for DevOps roles</div>
                <h1>Hi, I'm <span>Sriram Mamidala</span></h1>
                <p>DevOps Engineer based in Los Angeles 🌴<br>Building infrastructure that never sleeps</p>
                <div class="hero-btns">
                    <a href="#projects" class="btn-primary">View My Projects</a>
                    <a href="#visitors" class="btn-secondary">Live Visitor Count</a>
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
                    <div class="stat-number">10+</div>
                    <div class="stat-label">Projects Done</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">5+</div>
                    <div class="stat-label">Companies</div>
                </div>
            </div>
        </section>

        <!-- SKILLS -->
        <section class="skills" id="skills">
            <h2 class="section-title">My Skills</h2>
            <p class="section-sub">Tools and technologies I work with daily</p>
            <div class="skills-grid">
                <div class="skill-card">
                    <div class="skill-icon">🐳</div>
                    <div class="skill-name">Docker & Kubernetes</div>
                    <div class="skill-desc">Container orchestration and microservices deployment</div>
                    <div class="skill-bar"><div class="skill-fill" style="width:85%"></div></div>
                </div>
                <div class="skill-card">
                    <div class="skill-icon">☁️</div>
                    <div class="skill-name">AWS Cloud</div>
                    <div class="skill-desc">EC2, S3, RDS, EKS, Lambda and more</div>
                    <div class="skill-bar"><div class="skill-fill" style="width:80%"></div></div>
                </div>
                <div class="skill-card">
                    <div class="skill-icon">⚙️</div>
                    <div class="skill-name">CI/CD Pipelines</div>
                    <div class="skill-desc">GitHub Actions, Jenkins, automated deployments</div>
                    <div class="skill-bar"><div class="skill-fill" style="width:90%"></div></div>
                </div>
                <div class="skill-card">
                    <div class="skill-icon">📦</div>
                    <div class="skill-name">Terraform</div>
                    <div class="skill-desc">Infrastructure as Code for cloud resources</div>
                    <div class="skill-bar"><div class="skill-fill" style="width:70%"></div></div>
                </div>
                <div class="skill-card">
                    <div class="skill-icon">🐍</div>
                    <div class="skill-name">Python & Bash</div>
                    <div class="skill-desc">Scripting and automation for DevOps tasks</div>
                    <div class="skill-bar"><div class="skill-fill" style="width:75%"></div></div>
                </div>
                <div class="skill-card">
                    <div class="skill-icon">📊</div>
                    <div class="skill-name">Monitoring</div>
                    <div class="skill-desc">Prometheus, Grafana, ELK Stack</div>
                    <div class="skill-bar"><div class="skill-fill" style="width:65%"></div></div>
                </div>
            </div>
        </section>

        <!-- PROJECTS -->
        <section class="projects" id="projects">
            <h2 class="section-title">My Projects</h2>
            <p class="section-sub">Real projects built and deployed</p>
            <div class="projects-grid">
                <div class="project-card">
                    <span class="project-tag">Project 1</span>
                    <div class="project-title">🚀 Flask DevOps App</div>
                    <div class="project-desc">Built and deployed a Flask web application to AWS EC2 using Docker containers with automated CI/CD pipeline via GitHub Actions.</div>
                    <div class="project-techs">
                        <span class="tech-badge">Python</span>
                        <span class="tech-badge">Docker</span>
                        <span class="tech-badge">AWS EC2</span>
                        <span class="tech-badge">GitHub Actions</span>
                    </div>
                </div>
                <div class="project-card">
                    <span class="project-tag">Project 2</span>
                    <div class="project-title">🐘 App + Database</div>
                    <div class="project-desc">Multi-container application with Flask and PostgreSQL using Docker Compose with fully automated deployment pipeline to AWS.</div>
                    <div class="project-techs">
                        <span class="tech-badge">Flask</span>
                        <span class="tech-badge">PostgreSQL</span>
                        <span class="tech-badge">Docker Compose</span>
                        <span class="tech-badge">CI/CD</span>
                    </div>
                </div>
                <div class="project-card">
                    <span class="project-tag">Coming Soon</span>
                    <div class="project-title">☸️ Kubernetes Cluster</div>
                    <div class="project-desc">Production grade Kubernetes deployment on AWS EKS with auto scaling, load balancing and monitoring.</div>
                    <div class="project-techs">
                        <span class="tech-badge">Kubernetes</span>
                        <span class="tech-badge">AWS EKS</span>
                        <span class="tech-badge">Helm</span>
                        <span class="tech-badge">Prometheus</span>
                    </div>
                </div>
                <div class="project-card">
                    <span class="project-tag">Coming Soon</span>
                    <div class="project-title">🏗️ Terraform IaC</div>
                    <div class="project-desc">Complete AWS infrastructure provisioned with Terraform including VPC, subnets, security groups and auto scaling groups.</div>
                    <div class="project-techs">
                        <span class="tech-badge">Terraform</span>
                        <span class="tech-badge">AWS</span>
                        <span class="tech-badge">IaC</span>
                        <span class="tech-badge">Ansible</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- VISITOR COUNT -->
        <section class="visitor" id="visitors">
            <h2>Live Visitor Count 🌍</h2>
            <div class="visitor-count">{count}</div>
            <p>Real visitors tracked in PostgreSQL database on AWS!</p>
        </section>

        <!-- FOOTER -->
        <footer>
            <p>Built by Sriram Mamidala | DevOps Engineer | Los Angeles 🌴</p>
            <p style="margin-top:10px">Flask • PostgreSQL • Docker • AWS • GitHub Actions</p>
        </footer>

    </body>
    </html>
    """

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
