from flask import Flask, request, jsonify, render_template_string
import io, zipfile, base64, re, os, json, subprocess

app = Flask(__name__)

PRESETS = [
    {"key": "nextjs", "label": "Next.js Starter", "files": {"pages/index.tsx": "export default function Home() { return <h1>Next.js Starter</h1>; }"}},
    {"key": "solidity", "label": "Solidity Starter", "files": {"contracts/MyContract.sol": "pragma solidity ^0.8.0;\ncontract MyContract {}"}},
    {"key": "rust", "label": "Rust Starter", "files": {"src/main.rs": "fn main() { println!(\"Hello Rust\"); }"}}
]

def parse_files(text):
    lines = text.splitlines()
    files, current_name, current_content = [], None, []
    for line in lines:
        if re.match(r"^[\w\-/\.]+\.[a-zA-Z0-9]+$", line.strip()):
            if current_name and current_content:
                files.append((current_name, "\n".join(current_content).strip()))
            current_name = line.strip()
            current_content = []
        else:
            if line.strip().lower() in ["tsx","ts","js","jsx","download","copy code","wrap"]:
                continue
            if current_name:
                current_content.append(line)
    if current_name and current_content:
        files.append((current_name, "\n".join(current_content).strip()))
    return files

def format_code(filename, code):
    ext = filename.split(".")[-1]
    try:
        if ext in ["ts","tsx","js","jsx"]:
            proc = subprocess.run(["npx","prettier","--parser","typescript"], input=code.encode(), capture_output=True)
            return proc.stdout.decode() if proc.returncode==0 else code
        if ext=="rs":
            proc = subprocess.run(["rustfmt"], input=code.encode(), capture_output=True)
            return proc.stdout.decode() if proc.returncode==0 else code
        if ext=="sol":
            return code
    except Exception:
        return code
    return code

@app.route("/generate", methods=["POST"])
def generate_zip():
    content = request.json.get("code","")
    preset_key = request.json.get("preset")
    files = parse_files(content)

    preset_files = {}
    if preset_key:
        for p in PRESETS:
            if p["key"]==preset_key:
                preset_files=p["files"]
    for k,v in preset_files.items():
        files.append((k,v))

    if not files:
        return jsonify({"error":"No files found"}),400

    mem = io.BytesIO()
    report = {}
    total_size = 0
    language_count = {}

    with zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED) as zf:
        for filename, code in files:
            code = format_code(filename, code)
            zf.writestr(filename, code)
            total_size += len(code.encode())
            lang = filename.split(".")[-1]
            language_count[lang] = language_count.get(lang,0)+1
            report[filename]={"lines":len(code.splitlines()),"lang":lang}

    mem.seek(0)
    encoded = base64.b64encode(mem.read()).decode()
    return jsonify({
        "zip_base64":encoded,
        "filename":"project.zip",
        "total_files":len(files),
        "total_size":total_size,
        "languages":language_count,
        "report":report
    })

@app.route("/", methods=["GET"])
def index():
    return render_template_string("""
<!doctype html>
<html>
<head>
<title>Mono Repo Zipper</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Fira+Code&display=swap" rel="stylesheet">
<style>
:root { --bg:#f5f5f5; --card:#fff; --text:#333; --primary:#4f46e5; --success:#10b981; }
[data-theme="dark"] { --bg:#181818; --card:#242424; --text:#eee; --primary:#8b5cf6; --success:#22c55e; }
body { margin:0; font-family:'Inter',sans-serif; background:var(--bg); color:var(--text); transition:0.3s; }
.container { max-width:1000px; margin:50px auto; padding:30px; background:var(--card); border-radius:16px; box-shadow:0 10px 25px rgba(0,0,0,0.1); transition:0.3s; overflow:hidden; }
h1 { color:var(--primary); margin-bottom:10px;}
textarea { width:100%; max-width:100%; box-sizing:border-box; height:300px; font-family:'Fira Code', monospace; padding:16px; border-radius:12px; border:1px solid #ccc; background:#f9f9f9; resize:vertical; transition:0.2s; margin-top:10px; overflow:auto; }
textarea:focus { border-color:var(--primary); outline:none; }
button { padding:12px 24px; font-weight:600; border-radius:10px; border:none; cursor:pointer; transition:0.2s; }
#generateBtn { background:var(--primary); color:#fff; margin-top:10px;}
#generateBtn:hover { background:#4338ca; }
#downloadBtn { background:var(--success); color:#fff; display:none; margin-left:10px;}
#downloadBtn:hover { background:#0f9d75; }
.theme-toggle { padding:6px 10px; font-size:12px; background:#ddd; border-radius:8px; cursor:pointer; float:right; margin-top:5px; }
.preview { margin-top:20px; background:#f3f3f3; padding:12px; border-radius:10px; max-height:200px; overflow:auto; font-family:'Fira Code', monospace; word-break:break-word; }
.preview::before { content:"Preview & Info (file stats, snippet, languages)"; display:block; font-weight:600; margin-bottom:6px; color:#555; }
select { margin-top:10px; padding:8px 12px; border-radius:8px; border:1px solid #ccc; }
.buttons { margin-top:10px; display:flex; gap:10px; flex-wrap:wrap; }
.clearfix::after { content:""; display:table; clear:both;}
</style>
</head>
<body data-theme="light">
<div class="container">
<h1>Mono Repo Zipper</h1>
<p>Paste your project files below, optionally select a starter preset, then generate a ZIP.</p>
<div class="clearfix">
<select id="presetSelect">
<option value="">-- Choose a Starter Preset --</option>
{% for p in presets %}
<option value="{{p['key']}}">{{p['label']}}</option>
{% endfor %}
</select>
<button class="theme-toggle" onclick="toggleTheme()">Toggle Dark/Light</button>
</div>

<textarea id="code" placeholder="Paste your files here..."></textarea>
<div class="buttons">
<button id="generateBtn">Generate ZIP</button>
<button id="downloadBtn">Download ZIP</button>
</div>
<div class="preview" id="preview"></div>
</div>

<script>
let zipData=null;
const generateBtn=document.getElementById("generateBtn");
const downloadBtn=document.getElementById("downloadBtn");
const preview=document.getElementById("preview");

function toggleTheme(){
    const t=document.body.getAttribute("data-theme");
    document.body.setAttribute("data-theme", t==="light"?"dark":"light");
}

generateBtn.addEventListener("click", async ()=>{
    const code=document.getElementById("code").value;
    const preset=document.getElementById("presetSelect").value;
    generateBtn.innerText="Generating..."; generateBtn.disabled=true;
    const res=await fetch("/generate",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({code,preset})});
    generateBtn.innerText="Generate ZIP"; generateBtn.disabled=false;
    if(!res.ok){ alert("Error generating ZIP"); return; }
    const data=await res.json();
    zipData=data.zip_base64;
    downloadBtn.style.display="inline-block";

    let html=`<strong>Total files:</strong> ${data.total_files} | <strong>Total size:</strong> ${Math.round(data.total_size/1024)} KB<br><strong>Languages:</strong> `;
    html+=Object.entries(data.languages).map(e=>e[0]+"("+e[1]+")").join(", ");
    html+=`<br><strong>File Report:</strong><br><pre>${JSON.stringify(data.report,null,2)}</pre>`;
    preview.innerHTML=html;
});

downloadBtn.addEventListener("click", ()=>{
    if(!zipData) return;
    const link=document.createElement("a");
    link.href="data:application/zip;base64,"+zipData;
    link.download="project.zip";
    link.click();
});
</script>
</body>
</html>
""", presets=PRESETS)

if __name__=="__main__":
    app.run(debug=True)
