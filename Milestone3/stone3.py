# =========================================
# Milestone 3: Skill Gap Analysis Dashboard
# Colorful & Emoji-enhanced version
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
df = pd.DataFrame(similarity_matrix, index=jd_skills, columns=resume_skills)

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


overall_match = round(df.max(axis=1).sum() / len(jd_skills) * 100, 2)

# -----------------------------------------
# 5. CREATE STATIC FOLDER
# -----------------------------------------
os.makedirs("static", exist_ok=True)

# -----------------------------------------
# 6. SIMILARITY MATRIX PLOT
# -----------------------------------------
plt.figure(figsize=(8,5))
plt.imshow(df, cmap="coolwarm")
plt.colorbar()
plt.xticks(range(len(df.columns)), df.columns, rotation=45, fontsize=10, color="#333333")
plt.yticks(range(len(df.index)), df.index, fontsize=10, color="#333333")
for i in range(len(df.index)):
    for j in range(len(df.columns)):
        plt.text(j, i, round(df.iloc[i,j],2), ha="center", va="center", color="black", fontweight="bold")
plt.title("📊 Skill Similarity Matrix", fontsize=16, fontweight="bold", color="#4b2aad")
plt.tight_layout()
plt.savefig("static/similarity_matrix.png")
plt.close()

# -----------------------------------------
# 7. DONUT CHART
# -----------------------------------------
labels = ["✅ Matched", "⚠️ Partial", "❌ Missing"]
sizes = [len(matched), len(partial), len(missing)]
colors = ["#4CAF50", "#FFC107", "#F44336"]

plt.figure(figsize=(5,5))
plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors, textprops={'fontsize':12, 'weight':'bold'})
plt.title("🎯 Skill Match Overview", fontsize=14, fontweight="bold")
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
body { font-family: 'Arial', sans-serif; background:#f0f4f8; padding:20px; }
h1 { color:#4b2aad; text-align:center; margin-bottom:30px; }
.grid { display:flex; gap:20px; flex-wrap:wrap; justify-content:center; }
.card {
  background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
  padding:20px; border-radius:15px;
  width:220px; text-align:center;
  box-shadow:0 5px 15px rgba(0,0,0,0.2);
  transition: transform 0.2s;
}
.card:hover { transform: translateY(-5px); }
.big { font-size:32px; font-weight:bold; }
img { width:100%; border-radius:10px; margin-top:10px; }
ul { padding-left:20px; }
</style>
</head>
<body>

<h1>🌟 Milestone 3: Skill Gap Analysis & Matching 🌟</h1>

<div class="grid">
  <div class="card" style="background:#d4edda"><p>🎯 Overall Match</p><div class="big">{{match}}%</div></div>
  <div class="card" style="background:#cce5ff"><p>✅ Matched Skills</p><div class="big">{{matched}}</div></div>
  <div class="card" style="background:#fff3cd"><p>⚠️ Partial Matches</p><div class="big">{{partial}}</div></div>
  <div class="card" style="background:#f8d7da"><p>❌ Missing Skills</p><div class="big">{{missing}}</div></div>
</div>

<br>

<div class="grid">
  <div class="card" style="width:48%">
    <h3>📊 Similarity Matrix</h3>
    <img src="/static/similarity_matrix.png">
  </div>
  <div class="card" style="width:48%">
    <h3>🎯 Skill Match Overview</h3>
    <img src="/static/skill_match.png">
  </div>
</div>

<br>

<div class="card" style="width:100%">
<h3>❌ Missing Skills</h3>
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
