==============================================
Milestone 3: Skill Gap Analysis Dashboard
==============================================

Project Overview:
This Flask web application analyzes the skill gap between a candidate's resume and a job description (JD). 
It provides a visual dashboard showing matched, partial, and missing skills.

Features:
1. Generates a skill similarity matrix (heatmap) between resume and JD skills.
2. Creates a donut chart showing the overall skill match percentage.
3. Highlights matched, partial, and missing skills with emoji indicators.
4. Interactive Flask dashboard with colorful cards and visuals.

Technologies Used:
- Python
- Flask
- scikit-learn (TF-IDF, cosine similarity)
- pandas
- matplotlib

Usage:
1. Clone the repository.
2. Install dependencies:
   pip install flask scikit-learn pandas matplotlib
3. Run the app:
   python app.py
4. Open the dashboard in your browser at:
   http://127.0.0.1:5000/

