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
    except Exception:
        return 0


# Plain string (NOT an f-string) -- CSS braces need no escaping.
PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Sriram Mamidala — Senior Cloud Engineer</title>
<style>
  :root{
    --ink:#0a0a0b;
    --ink-2:#131316;
    --paper:#ffffff;
    --fog:#f5f6f8;
    --mist:#86868b;
    --mist-d:#6e6e73;
    --line-light:rgba(255,255,255,.12);
    --line-dark:rgba(0,0,0,.10);
    --accent:#2e8fff;
    --accent-soft:rgba(46,143,255,.14);
    --font:-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Helvetica,Arial,sans-serif;
    --ease:cubic-bezier(.22,.61,.36,1);
  }

  *{margin:0;padding:0;box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{
    font-family:var(--font);
    background:var(--ink);
    color:#fff;
    -webkit-font-smoothing:antialiased;
    overflow-x:hidden;
  }

  /* scroll-snap panels — the DJI stacked-reveal feel */
  .scroller{
    height:100vh;
    overflow-y:scroll;
    scroll-snap-type:y proximity;
    scroll-behavior:smooth;
  }
  .panel{
    position:relative;
    min-height:100vh;
    scroll-snap-align:start;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    text-align:center;
    padding:120px 24px 80px;
    overflow:hidden;
  }
  .panel.light{background:var(--paper);color:var(--ink)}
  .panel.fog{background:var(--fog);color:var(--ink)}
  .panel.dark{background:var(--ink)}
  .panel.ink2{background:var(--ink-2)}

  /* ---------- NAV ---------- */
  .nav{
    position:fixed;top:0;left:0;right:0;z-index:100;
    display:flex;align-items:center;justify-content:space-between;
    padding:0 34px;height:56px;
    background:rgba(10,10,11,0);
    backdrop-filter:blur(0px);
    transition:background .4s var(--ease),backdrop-filter .4s var(--ease),border-color .4s var(--ease);
    border-bottom:1px solid transparent;
  }
  .nav.scrolled{
    background:rgba(10,10,11,.72);
    backdrop-filter:blur(18px);
    border-bottom:1px solid var(--line-light);
  }
  .nav .brand{
    font-size:15px;font-weight:600;letter-spacing:.14em;color:#fff;text-decoration:none;
  }
  .nav .brand span{color:var(--accent)}
  .nav-links{display:flex;gap:30px;list-style:none}
  .nav-links a{
    color:rgba(255,255,255,.72);text-decoration:none;font-size:12.5px;
    letter-spacing:.04em;transition:color .25s var(--ease);
  }
  .nav-links a:hover{color:#fff}
  .nav-cta{
    font-size:12.5px;color:var(--ink);background:#fff;padding:7px 15px;border-radius:100px;
    text-decoration:none;font-weight:500;transition:transform .25s var(--ease),opacity .25s;
  }
  .nav-cta:hover{transform:scale(1.04)}
  .menu-btn{display:none;background:none;border:0;color:#fff;font-size:22px;cursor:pointer}

  /* ---------- HERO ---------- */
  #hero{background:radial-gradient(120% 90% at 50% -10%,#1a2a44 0%,#0a0a0b 55%)}
  .hero-glow{
    position:absolute;inset:0;pointer-events:none;
  }
  .hero-glow b{
    position:absolute;border-radius:50%;filter:blur(70px);opacity:.55;
    animation:drift 18s ease-in-out infinite alternate;
  }
  .hero-glow b:nth-child(1){width:440px;height:440px;background:#1f6feb;top:8%;left:12%}
  .hero-glow b:nth-child(2){width:380px;height:380px;background:#7b3ff2;bottom:6%;right:14%;animation-delay:-6s}
  .hero-glow b:nth-child(3){width:300px;height:300px;background:#00b3a4;top:38%;left:52%;animation-delay:-11s;opacity:.4}
  @keyframes drift{to{transform:translate3d(40px,-30px,0) scale(1.12)}}
  .grid-fade{
    position:absolute;inset:0;
    background-image:linear-gradient(var(--line-light) 1px,transparent 1px),linear-gradient(90deg,var(--line-light) 1px,transparent 1px);
    background-size:64px 64px;
    mask-image:radial-gradient(70% 60% at 50% 45%,#000 0%,transparent 78%);
    -webkit-mask-image:radial-gradient(70% 60% at 50% 45%,#000 0%,transparent 78%);
    opacity:.6;
  }
  .hero-inner{position:relative;z-index:2;max-width:900px}
  .eyebrow{
    font-size:12px;letter-spacing:.34em;text-transform:uppercase;color:var(--accent);
    font-weight:600;margin-bottom:22px;
  }
  #hero h1{
    font-size:clamp(44px,9vw,116px);font-weight:600;letter-spacing:-.03em;line-height:.96;
    background:linear-gradient(180deg,#fff 30%,#b9c4d4 100%);
    -webkit-background-clip:text;background-clip:text;color:transparent;
  }
  .hero-sub{
    margin-top:20px;font-size:clamp(17px,2.4vw,24px);font-weight:300;color:rgba(255,255,255,.72);
    letter-spacing:.01em;
  }
  .hero-tag{
    margin:26px auto 0;max-width:560px;font-size:15px;line-height:1.6;color:rgba(255,255,255,.55);font-weight:300;
  }
  .hero-btns{margin-top:38px;display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
  .btn{
    text-decoration:none;font-size:14px;font-weight:500;padding:13px 26px;border-radius:100px;
    transition:transform .25s var(--ease),background .25s,opacity .25s;letter-spacing:.01em;
  }
  .btn-primary{background:var(--accent);color:#fff}
  .btn-primary:hover{transform:scale(1.04);background:#4a9fff}
  .btn-ghost{background:rgba(255,255,255,.08);color:#fff;border:1px solid var(--line-light)}
  .btn-ghost:hover{background:rgba(255,255,255,.16)}
  .btn-dark{background:var(--ink);color:#fff}
  .btn-dark:hover{transform:scale(1.04)}
  .btn-outline-d{background:transparent;color:var(--ink);border:1px solid var(--line-dark)}
  .btn-outline-d:hover{background:rgba(0,0,0,.05)}
  .scroll-cue{
    position:absolute;bottom:30px;left:50%;transform:translateX(-50%);z-index:2;
    font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:rgba(255,255,255,.4);
    display:flex;flex-direction:column;align-items:center;gap:10px;
  }
  .scroll-cue i{
    width:1px;height:34px;background:linear-gradient(rgba(255,255,255,.6),transparent);
    animation:cue 1.8s var(--ease) infinite;
  }
  @keyframes cue{0%{transform:scaleY(.2);opacity:0}40%{opacity:1}100%{transform:scaleY(1);opacity:0}}

  /* ---------- PRODUCT / ROLE PANELS ---------- */
  .role-eyebrow{
    font-size:12px;letter-spacing:.24em;text-transform:uppercase;font-weight:600;margin-bottom:18px;
    color:var(--accent);
  }
  .light .role-eyebrow,.fog .role-eyebrow{color:var(--accent)}
  .role-title{
    font-size:clamp(32px,6vw,72px);font-weight:600;letter-spacing:-.025em;line-height:1.02;max-width:14ch;
  }
  .role-sub{
    margin-top:18px;font-size:clamp(16px,2vw,21px);font-weight:300;max-width:44ch;line-height:1.5;
  }
  .dark .role-sub,.ink2 .role-sub{color:rgba(255,255,255,.66)}
  .light .role-sub,.fog .role-sub{color:var(--mist-d)}
  .chips{
    margin-top:26px;display:flex;flex-wrap:wrap;gap:9px;justify-content:center;max-width:640px;
  }
  .chip{
    font-size:12.5px;padding:7px 14px;border-radius:100px;letter-spacing:.02em;font-weight:500;
  }
  .dark .chip,.ink2 .chip{background:rgba(255,255,255,.07);border:1px solid var(--line-light);color:rgba(255,255,255,.82)}
  .light .chip,.fog .chip{background:#fff;border:1px solid var(--line-dark);color:var(--ink)}
  .metrics{
    margin-top:34px;display:flex;gap:44px;justify-content:center;flex-wrap:wrap;
  }
  .metric b{display:block;font-size:clamp(30px,4.5vw,50px);font-weight:600;letter-spacing:-.02em}
  .metric span{font-size:12.5px;letter-spacing:.06em;text-transform:uppercase}
  .dark .metric span,.ink2 .metric span{color:var(--mist)}
  .light .metric span,.fog .metric span{color:var(--mist-d)}
  .metric b em{font-style:normal;color:var(--accent)}
  .role-links{margin-top:34px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap}

  /* ---------- TECH MARQUEE ("Built with") ---------- */
  #stack{padding:110px 0;gap:0;justify-content:center}
  .stack-label{
    font-size:12px;letter-spacing:.24em;text-transform:uppercase;color:var(--accent);font-weight:600;margin-bottom:8px;
  }
  .stack-h{
    font-size:clamp(26px,4vw,44px);font-weight:600;letter-spacing:-.02em;margin-bottom:48px;max-width:20ch;
  }
  .marquee{width:100%;overflow:hidden;-webkit-mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent);mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent)}
  .track{display:flex;width:max-content;animation:scroll 34s linear infinite;gap:0}
  .marquee:hover .track{animation-play-state:paused}
  .track .item{
    font-size:clamp(22px,3.4vw,40px);font-weight:500;letter-spacing:-.01em;color:rgba(255,255,255,.34);
    padding:0 30px;white-space:nowrap;transition:color .3s var(--ease);
  }
  .track .item:hover{color:#fff}
  .track .dot{color:var(--accent);padding:0 4px;align-self:center;font-size:22px}
  @keyframes scroll{to{transform:translateX(-50%)}}

  /* ---------- SKILLS GRID ---------- */
  #skills{justify-content:flex-start;padding-top:120px}
  .sec-head{max-width:900px;margin-bottom:52px}
  .sec-head .eyebrow{color:var(--accent)}
  .sec-head h2{font-size:clamp(30px,5vw,58px);font-weight:600;letter-spacing:-.025em;line-height:1.02}
  .light .sec-head h2,.fog .sec-head h2{color:var(--ink)}
  .skill-grid{
    display:grid;grid-template-columns:repeat(3,1fr);gap:18px;max-width:1040px;width:100%;text-align:left;
  }
  .skill-card{
    background:#fff;border:1px solid var(--line-dark);border-radius:18px;padding:26px 24px;
    transition:transform .35s var(--ease),box-shadow .35s var(--ease);
  }
  .skill-card:hover{transform:translateY(-6px);box-shadow:0 18px 44px rgba(0,0,0,.10)}
  .skill-card h3{font-size:16px;font-weight:600;margin-bottom:14px;color:var(--ink);display:flex;align-items:center;gap:9px}
  .skill-card h3::before{content:"";width:8px;height:8px;border-radius:2px;background:var(--accent)}
  .skill-card p{font-size:14px;line-height:1.75;color:var(--mist-d)}

  /* ---------- CONTACT ---------- */
  #contact{background:radial-gradient(120% 90% at 50% 120%,#1a2a44 0%,#0a0a0b 55%)}
  #contact h2{
    font-size:clamp(36px,7vw,88px);font-weight:600;letter-spacing:-.03em;line-height:1;
    background:linear-gradient(180deg,#fff 30%,#b9c4d4 100%);-webkit-background-clip:text;background-clip:text;color:transparent;
  }
  .contact-sub{margin-top:20px;font-size:17px;color:rgba(255,255,255,.6);font-weight:300}
  .contact-rows{margin-top:40px;display:flex;flex-direction:column;gap:2px;width:100%;max-width:520px}
  .crow{
    display:flex;align-items:center;justify-content:space-between;
    padding:18px 4px;border-bottom:1px solid var(--line-light);text-decoration:none;color:#fff;
    transition:padding .3s var(--ease);
  }
  .crow:hover{padding-left:14px;padding-right:0}
  .crow .k{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--mist)}
  .crow .v{font-size:15px;font-weight:500;display:flex;align-items:center;gap:10px}
  .crow .v::after{content:"→";color:var(--accent);opacity:0;transform:translateX(-6px);transition:.3s var(--ease)}
  .crow:hover .v::after{opacity:1;transform:translateX(0)}
  .placeholder{color:var(--mist)!important;font-style:italic;font-weight:400!important}
  .foot{margin-top:56px;font-size:12px;color:var(--mist);letter-spacing:.04em}

  /* ---------- reveal animation ---------- */
  .reveal{opacity:0;transform:translateY(34px);transition:opacity .9s var(--ease),transform .9s var(--ease)}
  .reveal.in{opacity:1;transform:none}
  .reveal.d1{transition-delay:.08s}
  .reveal.d2{transition-delay:.16s}
  .reveal.d3{transition-delay:.24s}
  .reveal.d4{transition-delay:.32s}

  /* live visitor count */
  .live-count{
    font-size:clamp(72px,16vw,180px);font-weight:600;line-height:.9;letter-spacing:-.04em;margin:22px 0 6px;
    background:linear-gradient(180deg,#fff 20%,#5ea6ff 110%);
    -webkit-background-clip:text;background-clip:text;color:transparent;
  }

  /* ---------- responsive ---------- */
  @media(max-width:760px){
    .nav-links,.nav-cta{display:none}
    .menu-btn{display:block}
    .metrics{gap:28px}
    .skill-grid{grid-template-columns:1fr}
    .panel{padding:100px 20px 70px}
    .crow{flex-direction:column;align-items:flex-start;gap:6px}
  }
  @media(prefers-reduced-motion:reduce){
    *{animation:none!important}
    .reveal{opacity:1;transform:none;transition:none}
    .scroller{scroll-snap-type:none}
  }
</style>
</head>
<body>

<nav class="nav" id="nav">
  <a href="#hero" class="brand">SRIRAM<span>.</span>M</a>
  <ul class="nav-links">
    <li><a href="#wf">Work</a></li>
    <li><a href="#stack">Stack</a></li>
    <li><a href="#skills">Skills</a></li>
    <li><a href="#live">Live</a></li>
    <li><a href="#contact">Contact</a></li>
  </ul>
  <a href="#contact" class="nav-cta">Get in touch</a>
  <button class="menu-btn" aria-label="menu">☰</button>
</nav>

<div class="scroller" id="scroller">

  <!-- HERO -->
  <section class="panel dark" id="hero">
    <div class="hero-glow"><b></b><b></b><b></b></div>
    <div class="grid-fade"></div>
    <div class="hero-inner">
      <p class="eyebrow reveal in">Senior Cloud Engineer · AWS · Kubernetes</p>
      <h1 class="reveal in d1">SRIRAM<br>MAMIDALA</h1>
      <p class="hero-sub reveal in d2">I build the platforms that ship software.</p>
      <p class="hero-tag reveal in d3">5+ years designing production Kubernetes and GitOps delivery on AWS across financial, healthcare, and enterprise systems.</p>
      <div class="hero-btns reveal in d4">
        <a href="#wf" class="btn btn-primary">Explore my work</a>
        <a href="#contact" class="btn btn-ghost">Get in touch</a>
      </div>
    </div>
    <div class="scroll-cue"><span>Scroll</span><i></i></div>
  </section>

  <!-- ROLE 1 — Wells Fargo -->
  <section class="panel light" id="wf">
    <p class="role-eyebrow reveal">Wells Fargo · 2025 – Present</p>
    <h2 class="role-title reveal d1">Core Banking,<br>Continuously Delivered</h2>
    <p class="role-sub reveal d2">Production Kubernetes clusters and GitOps pipelines running core banking microservices across dev, QA, and production.</p>
    <div class="metrics">
      <div class="metric reveal d2"><b>3</b><span>Environments</span></div>
      <div class="metric reveal d3"><b>EKS</b><span>Production clusters</span></div>
      <div class="metric reveal d4"><b>GitOps</b><span>Argo CD delivery</span></div>
    </div>
    <div class="chips">
      <span class="chip reveal d2">Amazon EKS</span>
      <span class="chip reveal d2">Argo CD</span>
      <span class="chip reveal d3">Terraform</span>
      <span class="chip reveal d3">Helm</span>
      <span class="chip reveal d3">GitHub Actions</span>
      <span class="chip reveal d4">NGINX Ingress</span>
      <span class="chip reveal d4">Splunk</span>
      <span class="chip reveal d4">Prometheus / Grafana</span>
    </div>
  </section>

  <!-- ROLE 2 — UnitedHealth -->
  <section class="panel dark" id="uhg">
    <p class="role-eyebrow reveal">UnitedHealth Group · 2023 – 2024</p>
    <h2 class="role-title reveal d1">Healthcare Claims,<br>at Scale</h2>
    <p class="role-sub reveal d2">CI/CD pipelines and AWS infrastructure automation for containerized healthcare claims-processing services.</p>
    <div class="metrics">
      <div class="metric reveal d2"><b>3</b><span>CI/CD toolchains</span></div>
      <div class="metric reveal d3"><b>IaC</b><span>Terraform + CFN</span></div>
      <div class="metric reveal d4"><b>ELK</b><span>Observability</span></div>
    </div>
    <div class="chips">
      <span class="chip reveal d2">Jenkins</span>
      <span class="chip reveal d2">GitHub Actions</span>
      <span class="chip reveal d3">Azure DevOps</span>
      <span class="chip reveal d3">ECS / EKS</span>
      <span class="chip reveal d3">CloudFormation</span>
      <span class="chip reveal d4">ELK Stack</span>
      <span class="chip reveal d4">CloudWatch</span>
    </div>
  </section>

  <!-- ROLE 3 — Tech Mahindra -->
  <section class="panel fog" id="tm">
    <p class="role-eyebrow reveal">Tech Mahindra · 2021 – 2023</p>
    <h2 class="role-title reveal d1">Where the<br>Pipeline Began</h2>
    <p class="role-sub reveal d2">Containerized build-and-deploy automation for telecom network management applications, and the foundation of a DevOps career.</p>
    <div class="metrics">
      <div class="metric reveal d2"><b>Docker</b><span>Containerized envs</span></div>
      <div class="metric reveal d3"><b>Jenkins</b><span>Release automation</span></div>
      <div class="metric reveal d4"><b>Agile</b><span>Delivery process</span></div>
    </div>
    <div class="chips">
      <span class="chip reveal d2">Docker</span>
      <span class="chip reveal d2">Jenkins</span>
      <span class="chip reveal d3">Shell Scripting</span>
      <span class="chip reveal d3">Git / Bitbucket</span>
      <span class="chip reveal d4">ELK Stack</span>
    </div>
  </section>

  <!-- STACK MARQUEE -->
  <section class="panel ink2" id="stack">
    <p class="stack-label reveal">Built with</p>
    <h2 class="stack-h reveal d1">The toolkit behind every deploy.</h2>
    <div class="marquee reveal d2">
      <div class="track">
        <span class="item">AWS</span><span class="dot">●</span>
        <span class="item">Kubernetes</span><span class="dot">●</span>
        <span class="item">Terraform</span><span class="dot">●</span>
        <span class="item">Argo CD</span><span class="dot">●</span>
        <span class="item">Docker</span><span class="dot">●</span>
        <span class="item">Helm</span><span class="dot">●</span>
        <span class="item">GitHub Actions</span><span class="dot">●</span>
        <span class="item">Jenkins</span><span class="dot">●</span>
        <span class="item">Prometheus</span><span class="dot">●</span>
        <span class="item">Grafana</span><span class="dot">●</span>
        <span class="item">Splunk</span><span class="dot">●</span>
        <!-- duplicate for seamless loop -->
        <span class="item">AWS</span><span class="dot">●</span>
        <span class="item">Kubernetes</span><span class="dot">●</span>
        <span class="item">Terraform</span><span class="dot">●</span>
        <span class="item">Argo CD</span><span class="dot">●</span>
        <span class="item">Docker</span><span class="dot">●</span>
        <span class="item">Helm</span><span class="dot">●</span>
        <span class="item">GitHub Actions</span><span class="dot">●</span>
        <span class="item">Jenkins</span><span class="dot">●</span>
        <span class="item">Prometheus</span><span class="dot">●</span>
        <span class="item">Grafana</span><span class="dot">●</span>
        <span class="item">Splunk</span><span class="dot">●</span>
      </div>
    </div>
  </section>

  <!-- SKILLS -->
  <section class="panel light" id="skills">
    <div class="sec-head">
      <p class="eyebrow reveal">Capabilities</p>
      <h2 class="reveal d1">Everything from the<br>cluster to the pipeline.</h2>
    </div>
    <div class="skill-grid">
      <div class="skill-card reveal d1">
        <h3>Cloud Platforms</h3>
        <p>AWS — EKS, ECS, EC2, VPC, S3, RDS, IAM, Lambda, CloudWatch, Route 53. Working knowledge of Azure and GCP.</p>
      </div>
      <div class="skill-card reveal d1">
        <h3>Kubernetes &amp; Orchestration</h3>
        <p>Amazon EKS, ECS, Helm, NGINX Ingress, RBAC, namespaces, rolling updates, Docker.</p>
      </div>
      <div class="skill-card reveal d2">
        <h3>GitOps &amp; CI/CD</h3>
        <p>Argo CD, GitHub Actions, Jenkins, Azure DevOps, GitOps workflows, Maven, Gradle.</p>
      </div>
      <div class="skill-card reveal d2">
        <h3>Infrastructure as Code</h3>
        <p>Terraform, Helm, CloudFormation — repeatable, version-controlled environments.</p>
      </div>
      <div class="skill-card reveal d3">
        <h3>Security &amp; Reliability</h3>
        <p>Kubernetes RBAC, AWS Secrets Manager, IAM policies, Kubernetes secrets, policy controls.</p>
      </div>
      <div class="skill-card reveal d3">
        <h3>Monitoring &amp; Observability</h3>
        <p>CloudWatch, Prometheus, Grafana, Splunk, ELK Stack, automated alerting and incident response.</p>
      </div>
    </div>
  </section>


  <!-- LIVE COUNT (real Postgres data) -->
  <section class="panel ink2" id="live">
    <p class="eyebrow reveal">Live &middot; PostgreSQL on AWS EC2</p>
    <h2 class="role-title reveal d1">Real Visitors.<br>Real Database.</h2>
    <div class="live-count reveal d2">__COUNT__</div>
    <p class="role-sub reveal d3">Every visit is written to a PostgreSQL database running in Docker on AWS EC2, auto-deployed on every push.</p>
    <div class="chips">
      <span class="chip reveal d3">PostgreSQL</span>
      <span class="chip reveal d3">Docker</span>
      <span class="chip reveal d4">AWS EC2</span>
      <span class="chip reveal d4">Auto Deploy</span>
    </div>
  </section>

  <!-- CONTACT -->
  <section class="panel dark" id="contact">
    <p class="eyebrow reveal">Let's talk</p>
    <h2 class="reveal d1">Get in touch.</h2>
    <p class="contact-sub reveal d2">Open to Senior Cloud / DevOps Engineer roles.</p>
    <div class="contact-rows">
      <a class="crow reveal d2" href="mailto:sriramdev1479@gmail.com">
        <span class="k">Email</span><span class="v">sriramdev1479@gmail.com</span>
      </a>
      <a class="crow reveal d2" href="tel:+15627687257">
        <span class="k">Phone</span><span class="v">+1 562-768-7257</span>
      </a>
      <a class="crow reveal d3" href="https://github.com/mamidalasriram4-hub" target="_blank" rel="noopener">
        <span class="k">GitHub</span><span class="v">github.com/mamidalasriram4-hub</span>
      </a>
      <!-- FILL IN your real LinkedIn URL below, then remove the "placeholder" class -->
      <a class="crow reveal d3" href="#" data-fill="linkedin">
        <span class="k">LinkedIn</span><span class="v placeholder">add your LinkedIn URL</span>
      </a>
    </div>
    <p class="foot reveal d4">© 2026 Sriram Mamidala · Senior Cloud Engineer · Long Beach, CA &middot; <a href="/health" style="color:inherit;text-decoration:none">Status &bull;</a></p>
  </section>

</div>

<script>
  const scroller = document.getElementById('scroller');
  const nav = document.getElementById('nav');

  // nav background on scroll
  scroller.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', scroller.scrollTop > 40);
  }, {passive:true});

  // scroll-triggered reveals (DJI-style enter animation)
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('in'); });
  }, {root: scroller, threshold: 0.18});
  document.querySelectorAll('.reveal').forEach(el => {
    if(!el.classList.contains('in')) io.observe(el);
  });

  // smooth in-scroller anchor jumps
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', ev => {
      const id = a.getAttribute('href');
      const t = document.querySelector(id);
      if(t){ ev.preventDefault(); scroller.scrollTo({top:t.offsetTop, behavior:'smooth'}); }
    });
  });
</script>
</body>
</html>
"""


@app.route("/")
def home():
    count = get_visitor_count()
    return PAGE.replace("__COUNT__", str(count))


@app.route("/health")
def health():
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
