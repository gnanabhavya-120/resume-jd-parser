##1 to 3. Skill Cleaning, Deduplication, Dictionary Storage
def clean_skills(skills):
    return list(set([s.strip().lower() for s in skills if s.strip()]))

resume_skills = ["Python ", " ML", "Deep Learning", "Python"]
jd_skills = ["python", "machine learning", "data analysis"]

resume_skills = clean_skills(resume_skills)
jd_skills = clean_skills(jd_skills)

skills_dict = {
    "resume_skills": resume_skills,
    "job_description_skills": jd_skills
}
#----------------------------------------
#4. Load Sentence-BERT Model
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
#------------------------------------------
#5-7.Generate Embeddings
single_embedding = model.encode("python")
print(len(single_embedding))
#----------------------------------------------
resume_embeddings = model.encode(resume_skills)
jd_embeddings = model.encode(jd_skills)
#-----------------------------------------------
#8 to 10. Cosine Similarity & Similarity Matrix
from sklearn.metrics.pairwise import cosine_similarity
similarity_matrix = cosine_similarity(resume_embeddings, jd_embeddings)
#---------------------------------------------------------------------------------
#11. Store Similarity Matrix in DataFrame
import pandas as pd

df_similarity = pd.DataFrame(
    similarity_matrix,
    index=resume_skills,
    columns=jd_skills
)
#---------------------------------------------------------------------------
#12 to 14. Match, Partial, Missing Skills
matched, partial, missing = [], [], []

for jd in jd_skills:
    max_score = df_similarity[jd].max()
    best_match = df_similarity[jd].idxmax()

    if max_score >= 0.8:
        matched.append((jd, best_match, max_score))
    elif max_score >= 0.5:
        partial.append((jd, best_match, max_score))
    else:
        missing.append(jd)
#------------------------------------------------------------------
#15.Save Skill Gap Report (JSON)
import json

report = {
    "matched": matched,
    "partial": partial,
    "missing": missing
}

with open("skill_gap_report.json", "w") as f:
    json.dump(report, f, indent=4)
#-----------------------------------------------------------------------------
#16 to 18. Heatmap Visualization
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8, 6))
sns.heatmap(df_similarity, annot=True, cmap="viridis")
plt.xlabel("Job Description Skills")
plt.ylabel("Resume Skills")
plt.title("Skill Similarity Heatmap")
plt.show()
#--------------------------------------------------
#19.Handle Empty Skills
if not resume_skills or not jd_skills:
    raise ValueError("Skills list cannot be empty")
#-------------------------------------------------------------------------------------------------
#20.Normalize Abbreviations
abbr = {"ml": "machine learning", "dl": "deep learning", "ai": "artificial intelligence"}

def normalize(skill):
    return abbr.get(skill.lower(), skill.lower())
#-----------------------------------------------------------------------------------------------------------
#21.Compare Two Models
model2 = SentenceTransformer("paraphrase-MiniLM-L3-v2")
emb2 = model2.encode(resume_skills)
#--------------------------------------------------------------------------------------
#22. Cache Embeddings
embedding_cache = {}

def get_embedding(skill):
    if skill not in embedding_cache:
        embedding_cache[skill] = model.encode(skill)
    return embedding_cache[skill]
#-------------------------------------------------------------------------------------------
#23. Full Pipeline
def skill_gap_pipeline(resume_skills, jd_skills):
    resume_skills = clean_skills(resume_skills)
    jd_skills = clean_skills(jd_skills)

    res_emb = model.encode(resume_skills)
    jd_emb = model.encode(jd_skills)

    sim = cosine_similarity(res_emb, jd_emb)
    return pd.DataFrame(sim, index=resume_skills, columns=jd_skills)
#--------------------------------------------------------------------------------------------------
#24. Top-3 Resume Skills for Each JD Skill
top3 = {}

for jd in jd_skills:
    top3[jd] = df_similarity[jd].nlargest(3).to_dict()
#---------------------------------------------------------------------------------------
#25. Different Thresholds
tech_threshold = 0.75
soft_threshold = 0.6
#---------------------------------------------------------------------------------
#26. Overall Alignment Score
overall_score = df_similarity.max(axis=0).mean()
print("Overall Alignment Score:", overall_score)
#------------------------------------------------------------------------
#27. Export Report + Heatmap
df_similarity.to_csv("similarity_matrix.csv")
#-------------------------------------------------------------------------------
#28. Modular Architecture
#project/
#│
#├── preprocessing.py
#├── embeddings.py
#├── similarity.py
#├── reporting.py
#└── main.py


