from flask import Flask, jsonify, request, send_file, render_template_string
import os, glob, json, subprocess
from main import generate

app = Flask(__name__)

OUTPUT = "output"
MUSIC = "music"
CONFIG = "config.json"

# ---------- config helpers ----------
def load_config():
    if os.path.exists(CONFIG):
        return json.load(open(CONFIG))
    return {"cron_enabled": False}

def save_config(cfg):
    with open(CONFIG,"w") as f:
        json.dump(cfg,f)

def update_cron(enable):
    cron_line = "0 6 * * * curl -s http://localhost:8084/generate > /dev/null 2>&1\n"
    try:
        existing = subprocess.getoutput("crontab -l 2>/dev/null")
        lines = [l for l in existing.splitlines() if "8095/generate" not in l]
        if enable:
            lines.append(cron_line.strip())
        cmd = "\n".join(lines) + "\n"
        p = subprocess.Popen(["crontab","-"],stdin=subprocess.PIPE,text=True)
        p.communicate(cmd)
    except Exception as e:
        print("cron error", e)

# ---------- UI ----------
HTML = '''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Devotional Radio</title>
<style>
body{margin:0;font-family:system-ui;background:#0f172a;color:#fff;transition:.3s}
.light{background:#f1f5f9;color:#111}
header{padding:14px;background:#020617;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.light header{background:#fff}
button,select,input{padding:10px;border-radius:10px;border:none}
.grid{display:grid;grid-template-columns:1fr;gap:18px;padding:18px}
@media(min-width:700px){.grid{grid-template-columns:1fr 1fr}}
.card{background:#020617;border-radius:16px;padding:16px}
.light .card{background:#fff}
img{width:100%;border-radius:12px;margin-top:6px}
audio{width:100%;margin-top:8px}
small{opacity:.7}
</style>
</head>

<body id="body">

<header>
🌙 <input type="checkbox" onchange="toggleTheme(this)">
<select id="voice">
<option>en-US-AriaNeural</option>
<option>en-US-GuyNeural</option>
<option>en-US-DavisNeural</option>
<option>en-GB-RyanNeural</option>
</select>

<button onclick="gen()">Generate Today</button>

<label>
<input type="checkbox" id="cronToggle" onchange="toggleCron(this)">
Auto 6am
</label>

<form action="/upload" method="post" enctype="multipart/form-data">
<input type="file" name="music">
<button>Upload Music</button>
</form>
</header>

<div class="grid" id="grid"></div>

<script>
function toggleTheme(cb){
document.body.className = cb.checked ? "light" : ""
}

async function load(){
let r = await fetch("/list")
let j = await r.json()

let html=""
j.forEach(d=>{
html+=`
<div class="card">
<h3>${d.date} - ${d.topic}</h3>
<small>Voice: ${d.voice || ""}</small>
<img src="${d.image}">
<p>${(d.text||"").substring(0,350)}...</p>
<audio controls src="/audio/${d.date}"></audio>
</div>`
})
document.getElementById("grid").innerHTML=html
}

async function gen(){
let v=document.getElementById("voice").value
await fetch("/generate?voice="+v)
load()
}

async function toggleCron(cb){
await fetch("/cron?enable="+cb.checked)
}

load()
</script>
</body>
</html>
'''

# ---------- routes ----------
@app.route("/")
def home():
    cfg = load_config()
    return render_template_string(HTML, cfg=cfg)

@app.route("/generate")
def gen():
    voice = request.args.get("voice","en-US-AriaNeural")
    topic = os.getenv("WEEKLY_TOPIC","Hope")

    data = generate(topic, voice)
    data["voice"] = voice

    with open(f"{OUTPUT}/{data['date']}.json","w") as f:
        json.dump(data,f)

    return jsonify(data)

@app.route("/list")
def list_devos():
    files = sorted(glob.glob(f"{OUTPUT}/*.json"), reverse=True)
    out=[]
    for f in files:
        out.append(json.load(open(f)))
    return jsonify(out)

@app.route("/audio/<d>")
def audio(d):
    return send_file(f"{OUTPUT}/{d}.mp3")

@app.route("/upload",methods=["POST"])
def upload():
    f = request.files["music"]
    os.makedirs(MUSIC, exist_ok=True)
    f.save(f"{MUSIC}/{f.filename}")
    return "uploaded"

@app.route("/cron")
def cron():
    enable = request.args.get("enable","false") == "true"
    cfg = load_config()
    cfg["cron_enabled"] = enable
    save_config(cfg)
    update_cron(enable)
    return "ok"

app.run(host="0.0.0.0", port=8080)
