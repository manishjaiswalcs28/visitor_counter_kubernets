import os
import socket
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template_string
import redis

app = Flask(__name__)
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
CLUSTER_NAME = os.getenv("CLUSTER_NAME", "local-cluster")

pool = redis.ConnectionPool(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB,
    socket_connect_timeout=2, socket_timeout=2,
    decode_responses=True, max_connections=30
)
redis_client = redis.Redis(connection_pool=pool)

PAGE = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>LOOP — Visitor Observatory</title>
<style>
:root{--ink:#18221f;--paper:#f3f0e8;--lime:#d5f36a;--muted:#75817a;--line:#d9ded4}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,sans-serif}
header{display:flex;justify-content:space-between;align-items:center;padding:24px 6vw;border-bottom:1px solid var(--line)}
.brand{font-size:20px;font-weight:900;letter-spacing:.16em}.status{font-size:11px;letter-spacing:.14em;text-transform:uppercase}
.dot{display:inline-block;width:8px;height:8px;background:#74ad42;border-radius:50%;margin-right:8px;box-shadow:0 0 0 4px #74ad4222}
main{max-width:1120px;margin:7vh auto;padding:0 28px}.eyebrow{font-size:11px;letter-spacing:.2em;color:var(--muted);text-transform:uppercase}
h1{font-size:clamp(42px,8vw,92px);line-height:.94;letter-spacing:-.075em;margin:20px 0 42px;max-width:800px}
h1 em{font-family:Georgia,serif;font-weight:400;color:#68766b}
.grid{display:grid;grid-template-columns:1.25fr .75fr;gap:18px}
.card{border:1px solid var(--line);border-radius:5px;padding:28px;background:#fbfaf6}
.hero{background:var(--lime);border-color:var(--lime);min-height:250px;display:flex;flex-direction:column;justify-content:space-between}
.label{font-size:11px;text-transform:uppercase;letter-spacing:.15em}.count{font-size:clamp(76px,12vw,132px);font-weight:850;letter-spacing:-.09em;line-height:.9}
.side{display:flex;flex-direction:column;gap:18px}.small{flex:1}.value{font-size:25px;font-weight:750;margin-top:20px}
footer{margin-top:22px;padding-top:18px;border-top:1px solid var(--line);display:flex;justify-content:space-between;gap:20px;color:var(--muted);font-size:12px}
.pill{display:inline-block;padding:7px 10px;border:1px solid var(--line);border-radius:20px;font-size:11px}
@media(max-width:700px){.grid{grid-template-columns:1fr}.hero{min-height:220px}header{padding:20px 24px}main{margin:48px auto}}
</style></head>
<body>
<header><div class="brand">LOOP<span style="color:#9dbb3d">/</span></div><div class="status"><span class="dot"></span>Live observatory</div></header>
<main>
<div class="eyebrow">Digital presence / public counter / {{ date }}</div>
<h1>Every visit<br>leaves a <em>trace.</em></h1>
<section class="grid">
<div class="card hero"><div class="label">Total page visits</div><div class="count">{{ count }}</div><div class="label">A little signal from every arrival ↗</div></div>
<div class="side">
<div class="card small"><div class="label">Runtime node</div><div class="value">{{ hostname }}</div><div class="label" style="margin-top:8px;color:var(--muted)">Container instance</div></div>
<div class="card small"><div class="label">Deployment lane</div><div class="value">{{ cluster }}</div><div style="margin-top:12px"><span class="pill">Flask {{ version }}</span> <span class="pill">Redis-backed</span></div></div>
</div></section>
<footer><span>LOOP / VISITOR OBSERVATORY</span><span>Refresh the page to register another visit.</span></footer>
</main></body></html>
"""

@app.get("/")
def home():
    try:
        count = redis_client.incr("visitor_count")
        return render_template_string(
            PAGE, count=count, hostname=socket.gethostname(),
            cluster=CLUSTER_NAME, version=APP_VERSION,
            date=datetime.now(timezone.utc).strftime("%d %b %Y · UTC")
        )
    except redis.RedisError:
        return ("Visitor counter storage is temporarily unavailable.", 503)

@app.get("/health")
def health():
    try:
        redis_client.ping()
        return jsonify(status="ok", redis="connected", cluster=CLUSTER_NAME), 200
    except redis.RedisError:
        return jsonify(status="degraded", redis="unavailable"), 503

@app.get("/ready")
def ready():
    try:
        redis_client.ping()
        return jsonify(ready=True), 200
    except redis.RedisError:
        return jsonify(ready=False), 503

@app.get("/api/stats")
def stats():
    try:
        return jsonify(
            visitors=int(redis_client.get("visitor_count") or 0),
            hostname=socket.gethostname(), cluster=CLUSTER_NAME,
            version=APP_VERSION
        )
    except redis.RedisError:
        return jsonify(error="Redis unavailable"), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
