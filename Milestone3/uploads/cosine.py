# =========================================
# Milestone 3: Skill Gap Analysis Dashboard
# NO BERT | NO SEABORN | SINGLE FILE
# =========================================

from flask import Flask, render_template_string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import pandas as pd
import os

# -----------------------------------------
# 1. SKILLS (FROM MILESTONE 2 OUTPUT)
# -----------------------------------------
resume_skills = [
    "python", "sql", "machine learning",
    "communication", "data analysis", "nosql"
]

jd_skills = [
    "python", "sql", "deep learning",
    "aws cloud", "communication", "leadership"
]

# -----------------------------------------
# 2. TF-IDF VECTORIZATION
# -----------------------------------------
all_skills = resume_skills + jd_skills

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(all_skills)

resume_vectors = tfidf_matrix[:len(resume_skills)]
jd_vectors = tfidf_matrix[len(resume_skills):]

# -----------------------------------------
# 3. SIMILARITY MATRIX
# -----------------------------------------
similarity_matrix = cosine_similarity(jd_vectors, resume_vectors)

df = pd.DataFrame(
    similarity_matrix,
    index=jd_skills,
    columns=resume_skills
)

# -----------------------------------------
# 4. SKILL GAP ANALYSIS
# -----------------------------------------
matched, partial, missing = [], [], []

for skill, row in df.iterrows():
    max_score = row.max()
    if max_score >= 0.75:
        matched.append(skill)
    elif max_score >= 0.40:
        partial.append(skill)
    else:
        missing.append(skill)

overall_match = round(
    ((len(matched) + 0.5 * len(partial)) / len(jd_skills)) * 100, 2
)

# -----------------------------------------
# 5. CREATE STATIC FOLDER
# -----------------------------------------
os.makedirs("static", exist_ok=True)

# -----------------------------------------
# 6. SIMILARITY MATRIX PLOT (MATPLOTLIB)
# -----------------------------------------
plt.figure(figsize=(8,5))
plt.imshow(df, cmap="YlGn")
plt.colorbar()
plt.xticks(range(len(df.columns)), df.columns, rotation=45)
plt.yticks(range(len(df.index)), df.index)

for i in range(len(df.index)):
    for j in range(len(df.columns)):
        plt.text(j, i, round(df.iloc[i, j], 2),
                 ha="center", va="center")

plt.title("Skill Similarity Matrix")
plt.tight_layout()
plt.savefig("static/similarity_matrix.png")
plt.close()

# -----------------------------------------
# 7. DONUT CHART (MATCH OVERVIEW)
# -----------------------------------------
labels = ["Matched", "Partial", "Missing"]
sizes = [len(matched), len(partial), len(missing)]

plt.figure(figsize=(5,5))
plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
plt.title("Skill Match Overview")
plt.savefig("static/skill_match.png")
plt.close()

# -----------------------------------------
# 8. FLASK DASHBOARD
# -----------------------------------------
app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Milestone 3 Dashboard</title>
<style>
body { font-family: Arial; background:#f4f6f9; padding:20px }
h1 { color:#4b2aad }
.grid { display:flex; gap:20px; flex-wrap:wrap }
.card {
  background:white;
  padding:20px;
  border-radius:10px;
  width:220px;
  box-shadow:0 2px 8px rgba(0,0,0,0.1)
}
.big { font-size:30px; font-weight:bold }
img { width:100%; border-radius:10px }
</style>
</head>
<body>

<h1>Milestone 3: Skill Gap Analysis & Matching</h1>

<div class="grid">
  <div class="card"><p>Overall Match</p><div class="big">{{match}}%</div></div>
  <div class="card"><p>Matched Skills</p><div class="big">{{matched}}</div></div>
  <div class="card"><p>Partial Matches</p><div class="big">{{partial}}</div></div>
  <div class="card"><p>Missing Skills</p><div class="big">{{missing}}</div></div>
</div>

<br>

<div class="grid">
  <div class="card" style="width:48%">
    <h3>Similarity Matrix</h3>
    <img src="/static/similarity_matrix.png">
  </div>
  <div class="card" style="width:48%">
    <h3>Skill Match Overview</h3>
    <img src="/static/skill_match.png">
  </div>
</div>

<br>

<div class="card" style="width:100%">
<h3>Missing Skills</h3>
<ul>
{% for skill in missing_skills %}
<li>{{skill}}</li>
{% endfor %}
</ul>
</div>

</body>
</html>
"""

@app.route("/")
def dashboard():
    return render_template_string(
        HTML,
        match=overall_match,
        matched=len(matched),
        partial=len(partial),
        missing=len(missing),
        missing_skills=missing
    )

# -----------------------------------------
# 9. RUN APP
# -----------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
