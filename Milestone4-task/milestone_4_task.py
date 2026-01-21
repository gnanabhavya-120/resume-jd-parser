# ============================================================
# Milestone 4 – Streamlit Practical Problems
# Skill Gap Analysis Dashboard
# ============================================================

import streamlit as st
import pandas as pd

# ------------------------------------------------------------
# 1. Basic Streamlit App: Title & Description
# ------------------------------------------------------------
st.title("Skill Gap Analysis Dashboard")
st.write("This application analyzes skill gaps between a resume and a job description.")

# ------------------------------------------------------------
# 2. Sidebar Navigation
# ------------------------------------------------------------
st.sidebar.title("Navigation")
st.sidebar.write("Upload Files")
st.sidebar.write("Analysis")
st.sidebar.write("Results")

# ------------------------------------------------------------
# 3. File Uploaders (PDF, DOCX, TXT only)
# ------------------------------------------------------------
resume_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx", "txt"]
)

jd_file = st.file_uploader(
    "Upload Job Description",
    type=["pdf", "docx", "txt"]
)

# ------------------------------------------------------------
# 12. Session State to Preserve Uploaded Data
# ------------------------------------------------------------
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""

# ------------------------------------------------------------
# 13. Error Handling & File Reading
# ------------------------------------------------------------
def read_file(file):
    if file is None:
        return ""
    return file.read().decode("utf-8", errors="ignore")

if resume_file:
    st.write("Uploaded Resume:", resume_file.name)
    st.session_state.resume_text = read_file(resume_file)

if jd_file:
    st.write("Uploaded Job Description:", jd_file.name)
    st.session_state.jd_text = read_file(jd_file)

# ------------------------------------------------------------
# 5. Show First 300 Characters of Uploaded Files
# ------------------------------------------------------------
if st.session_state.resume_text:
    st.subheader("Resume Preview (First 300 Characters)")
    st.write(st.session_state.resume_text[:300])

if st.session_state.jd_text:
    st.subheader("Job Description Preview (First 300 Characters)")
    st.write(st.session_state.jd_text[:300])

# ------------------------------------------------------------
# 6. Button to Trigger Processing
# ------------------------------------------------------------
if st.button("Analyze Skills"):

    # --------------------------------------------------------
    # Dummy Skill Analysis (Example Data)
    # --------------------------------------------------------
    matched_skills = ["Python", "SQL", "Communication"]
    missing_skills = ["AWS", "Deep Learning"]

    skill_match_percentage = 75

    # --------------------------------------------------------
    # 8. Skill Match Percentage Metric
    # --------------------------------------------------------
    st.metric(
        label="Overall Skill Match Percentage",
        value=f"{skill_match_percentage}%"
    )

    # --------------------------------------------------------
    # 7. Resume & JD Display in Separate Sections
    # --------------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Resume Section")
        st.write(st.session_state.resume_text[:300])

    with col2:
        st.subheader("Job Description Section")
        st.write(st.session_state.jd_text[:300])

    # --------------------------------------------------------
    # 9. Matched & Missing Skills Lists
    # --------------------------------------------------------
    st.subheader("Matched Skills")
    st.write(matched_skills)

    st.subheader("Missing Skills")
    st.write(missing_skills)

    # --------------------------------------------------------
    # 10. Bar Chart: Matched vs Missing Skills
    # --------------------------------------------------------
    bar_data = pd.DataFrame({
        "Category": ["Matched Skills", "Missing Skills"],
        "Count": [len(matched_skills), len(missing_skills)]
    })

    st.subheader("Skill Comparison Chart")
    st.bar_chart(bar_data.set_index("Category"))

    # --------------------------------------------------------
    # 11. Table of Skills with Similarity Scores
    # --------------------------------------------------------
    similarity_table = pd.DataFrame({
        "Skill": ["Python", "SQL", "Communication", "AWS", "Deep Learning"],
        "Similarity Score": [0.95, 0.88, 0.80, 0.30, 0.25]
    })

    st.subheader("Skill Similarity Table")
    st.table(similarity_table)

    # --------------------------------------------------------
    # 14. Download Skill Gap Results as CSV
    # --------------------------------------------------------
    csv_data = similarity_table.to_csv(index=False)

    st.download_button(
        label="Download Skill Gap Report (CSV)",
        data=csv_data,
        file_name="skill_gap_report.csv",
        mime="text/csv"
    )

# ------------------------------------------------------------
# 15. End-to-End Streamlit Dashboard Completed
# ------------------------------------------------------------
