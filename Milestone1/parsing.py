from flask import Flask, request, render_template_string
import os, re, json
import PyPDF2
import docx

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------------
# File type detection
# -------------------------------
def file_type(name):
    if name.endswith(".txt"):
        return "TXT"
    if name.endswith(".pdf"):
        return "PDF"
    if name.endswith(".docx"):
        return "DOCX"
    return "NA"

# -------------------------------
# Load file content
# -------------------------------
def read_file(path, ftype):
    text = ""
    if ftype == "TXT":
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

    elif ftype == "PDF":
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for p in reader.pages:
                if p.extract_text():
                    text += p.extract_text() + "\n"

    elif ftype == "DOCX":
        d = docx.Document(path)
        for p in d.paragraphs:
            text += p.text + "\n"

    return text

# -------------------------------
# Clean & split line by line
# -------------------------------
def clean_lines(text):
    result = []
    for line in text.split("\n"):
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            result.append(line)
    return result

# -------------------------------
# HTML UI (Colorful + Two Panels)
# -------------------------------
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Milestone 1 | Resume & JD Parser</title>
<style>
body {
    font-family: Arial;
    background: linear-gradient(to right, #e3f2fd, #fce4ec);
    padding:30px;
}

.header {
    background:#3949ab;
    color:white;
    padding:20px;
    border-radius:10px;
    margin-bottom:20px;
}

.upload-box {
    background:white;
    padding:20px;
    border-radius:10px;
    box-shadow:0 0 10px #bbb;
    margin-bottom:20px;
}

.container {
    display:flex;
    gap:20px;
}

.panel {
    width:50%;
    background:white;
    border-radius:10px;
    box-shadow:0 0 10px #bbb;
}

.panel-header {
    padding:12px;
    color:white;
    font-weight:bold;
    border-radius:10px 10px 0 0;
}

.resume-header { background:#1e88e5; }
.jd-header { background:#8e24aa; }

.panel-body {
    padding:15px;
    max-height:400px;
    overflow-y:auto;
    background:#f9f9f9;
}

p { margin:5px 0; font-size:14px; }

button {
    background:#3949ab;
    color:white;
    border:none;
    padding:10px 20px;
    border-radius:5px;
    cursor:pointer;
}
</style>
</head>

<body>

<div class="header">
    <h2>Milestone 1: Data Ingestion & Parsing (Weeks 1–2)</h2>
    <p>Resume & Job Description Upload | TXT • PDF • DOCX</p>
</div>

<div class="upload-box">
    <form method="POST" enctype="multipart/form-data">
        Resume:
        <input type="file" name="resume" required>
        &nbsp;&nbsp;
        Job Description:
        <input type="file" name="jd" required>
        <br><br>
        <button>Upload & Parse</button>
    </form>
</div>

{% if resume %}
<div class="container">

    <div class="panel">
        <div class="panel-header resume-header">📄 Resume Preview</div>
        <div class="panel-body">
            {% for line in resume %}
                <p>{{ line }}</p>
            {% endfor %}
        </div>
    </div>

    <div class="panel">
        <div class="panel-header jd-header">📋 Job Description Preview</div>
        <div class="panel-body">
            {% for line in jd %}
                <p>{{ line }}</p>
            {% endfor %}
        </div>
    </div>

</div>
{% endif %}

</body>
</html>
"""

# -------------------------------
# Flask route
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    resume = None
    jd = None

    if request.method == "POST":
        r = request.files["resume"]
        j = request.files["jd"]

        r_path = os.path.join(UPLOAD_FOLDER, r.filename)
        j_path = os.path.join(UPLOAD_FOLDER, j.filename)

        r.save(r_path)
        j.save(j_path)

        r_text = read_file(r_path, file_type(r.filename.lower()))
        j_text = read_file(j_path, file_type(j.filename.lower()))

        resume = clean_lines(r_text)
        jd = clean_lines(j_text)

        # Save JSON output
        with open("parsed_output.json", "w", encoding="utf-8") as f:
            json.dump({"resume": resume, "job_description": jd}, f, indent=4)

    return render_template_string(HTML, resume=resume, jd=jd)

if __name__ == "__main__":
    app.run(debug=True)
