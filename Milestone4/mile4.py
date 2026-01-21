import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import PyPDF2
import docx
import re
from collections import Counter
import io

# Page configuration
st.set_page_config(page_title="Skill Gap Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2rem;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4a90e2;
    }
    .metric-label {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    .proficiency-circle {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        font-size: 1.8rem;
        font-weight: bold;
        color: white;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Helper Functions
def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    doc = docx.Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_txt(file):
    """Extract text from TXT file"""
    return file.read().decode('utf-8')

def extract_text(file):
    """Extract text based on file type"""
    if file.name.endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif file.name.endswith('.docx'):
        return extract_text_from_docx(file)
    elif file.name.endswith('.txt'):
        return extract_text_from_txt(file)
    else:
        return ""

def extract_skills(text):
    """Extract skills from text"""
    # Common technical skills to look for
    skill_keywords = [
        'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift',
        'machine learning', 'deep learning', 'artificial intelligence', 'ai',
        'data science', 'data analysis', 'statistics', 'sql', 'nosql', 'mongodb',
        'postgresql', 'mysql', 'tensorflow', 'pytorch', 'keras', 'scikit-learn',
        'pandas', 'numpy', 'matplotlib', 'aws', 'azure', 'gcp', 'docker',
        'kubernetes', 'git', 'agile', 'scrum', 'project management', 'communication',
        'leadership', 'teamwork', 'problem solving', 'react', 'angular', 'vue',
        'node.js', 'django', 'flask', 'rest api', 'graphql', 'html', 'css',
        'excel', 'powerpoint', 'tableau', 'power bi', 'spark', 'hadoop',
        'nlp', 'computer vision', 'devops', 'ci/cd', 'jenkins', 'linux'
    ]
    
    text_lower = text.lower()
    found_skills = {}
    
    for skill in skill_keywords:
        # Count occurrences
        count = len(re.findall(r'\b' + re.escape(skill) + r'\b', text_lower))
        if count > 0:
            # Estimate proficiency based on frequency (normalized to 100)
            proficiency = min(100, 50 + (count * 10))
            found_skills[skill.title()] = proficiency
    
    return found_skills

def calculate_match_score(resume_skills, job_skills):
    """Calculate match score between resume and job description"""
    if not job_skills:
        return 0, [], []
    
    matched_skills = []
    missing_skills = []
    
    for skill in job_skills:
        if skill in resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)
    
    match_percentage = (len(matched_skills) / len(job_skills)) * 100 if job_skills else 0
    
    return match_percentage, matched_skills, missing_skills

def create_bar_chart(resume_skills, job_skills):
    """Create comparison bar chart"""
    all_skills = set(list(resume_skills.keys())[:8] + list(job_skills.keys())[:8])
    
    skills_list = list(all_skills)[:8]
    resume_values = [resume_skills.get(skill, 0) for skill in skills_list]
    job_values = [job_skills.get(skill, 0) for skill in skills_list]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Resume Skills',
        x=skills_list,
        y=resume_values,
        marker_color='#4a90e2'
    ))
    
    fig.add_trace(go.Bar(
        name='Job Requirements',
        x=skills_list,
        y=job_values,
        marker_color='#5cb85c'
    ))
    
    fig.update_layout(
        barmode='group',
        height=350,
        xaxis_title="Skills",
        yaxis_title="Match Percentage",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=40, b=80),
        plot_bgcolor='white',
        xaxis=dict(tickangle=-45)
    )
    
    return fig

def create_radar_chart(resume_skills, job_skills):
    """Create radar chart for role view"""
    categories = ['Technical Skills', 'Soft Skills', 'Experience', 'Education', 'Certifications']
    
    # Simplified calculation based on available skills
    tech_skills = ['Python', 'Machine Learning', 'Sql', 'Aws', 'Tensorflow']
    soft_skills = ['Communication', 'Leadership', 'Teamwork', 'Problem Solving']
    
    resume_tech = sum([resume_skills.get(s, 0) for s in tech_skills]) / len(tech_skills) if tech_skills else 0
    job_tech = sum([job_skills.get(s, 0) for s in tech_skills]) / len(tech_skills) if tech_skills else 0
    
    resume_soft = sum([resume_skills.get(s, 0) for s in soft_skills]) / len(soft_skills) if soft_skills else 0
    job_soft = sum([job_skills.get(s, 0) for s in soft_skills]) / len(soft_skills) if soft_skills else 0
    
    resume_values = [resume_tech, resume_soft, 70, 85, 60]
    job_values = [job_tech, job_soft, 85, 75, 80]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=resume_values,
        theta=categories,
        fill='toself',
        name='Current Profile',
        line_color='#4a90e2'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=job_values,
        theta=categories,
        fill='toself',
        name='Job Requirements',
        line_color='#5cb85c'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        height=350,
        margin=dict(l=80, r=80, t=40, b=40)
    )
    
    return fig

def get_proficiency_color(score):
    """Get color based on proficiency score"""
    if score >= 85:
        return '#5cb85c'
    elif score >= 70:
        return '#8bc34a'
    elif score >= 50:
        return '#f0ad4e'
    else:
        return '#d9534f'

def generate_recommendations(missing_skills, resume_skills):
    """Generate upskilling recommendations"""
    recommendations = []
    
    skill_courses = {
        'Aws': ('AWS Cloud Services', 'Complete AWS Certified Solutions Architect course'),
        'Machine Learning': ('Advanced Machine Learning', 'Enroll in Advanced ML for Data Science program'),
        'Project Management': ('Project Management', 'Consider PMP certification for leadership skills'),
        'Sql': ('Advanced SQL', 'Master SQL for data analysis and database management'),
        'Communication': ('Communication Skills', 'Improve presentation and communication skills'),
        'Docker': ('Docker & Containers', 'Learn containerization with Docker and Kubernetes'),
        'Tensorflow': ('TensorFlow Deep Learning', 'Master deep learning with TensorFlow'),
    }
    
    for skill in missing_skills[:3]:
        if skill in skill_courses:
            recommendations.append(skill_courses[skill])
        else:
            recommendations.append((skill, f'Learn {skill} to match job requirements'))
    
    return recommendations

# Main App
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>Milestone 4: Dashboard and Report Export Module (Weeks 7-8)</h1>
        <p>Module: Dashboard and Report Export • Streamlit interface for end-to-end comparison • Interactive graphs and scores • Downloadable reports in PDF/CSV formats</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for file uploads
    with st.sidebar:
        st.title("📁 Upload Files")
        st.markdown("---")
        
        resume_file = st.file_uploader(
            "Upload Resume",
            type=['pdf', 'docx', 'txt'],
            help="Upload your resume in PDF, DOCX, or TXT format"
        )
        
        job_file = st.file_uploader(
            "Upload Job Description",
            type=['pdf', 'docx', 'txt'],
            help="Upload job description in PDF, DOCX, or TXT format"
        )
        
        st.markdown("---")
        
        analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)
        
        st.markdown("---")
        st.info("💡 **Tip**: Upload both files and click Analyze to see the skill gap analysis")
    
    # Main content
    if analyze_button and resume_file and job_file:
        with st.spinner("Analyzing files..."):
            # Extract text
            resume_text = extract_text(resume_file)
            job_text = extract_text(job_file)
            
            # Extract skills
            resume_skills = extract_skills(resume_text)
            job_skills = extract_skills(job_text)
            
            # Calculate match
            match_score, matched_skills, missing_skills = calculate_match_score(resume_skills, job_skills)
            
            # Store in session state
            st.session_state['resume_skills'] = resume_skills
            st.session_state['job_skills'] = job_skills
            st.session_state['match_score'] = match_score
            st.session_state['matched_skills'] = matched_skills
            st.session_state['missing_skills'] = missing_skills
            st.session_state['analyzed'] = True
    
    if st.session_state.get('analyzed', False):
        resume_skills = st.session_state['resume_skills']
        job_skills = st.session_state['job_skills']
        match_score = st.session_state['match_score']
        matched_skills = st.session_state['matched_skills']
        missing_skills = st.session_state['missing_skills']
        
        # Dashboard Header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("## 📊 Skill Gap Analysis Dashboard")
        with col2:
            if st.button("🔄 Refresh"):
                st.rerun()
        
        st.markdown("---")
        
        # Main Layout
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            # Skill Match Overview Card
            st.markdown("### 📈 Skill Match Overview")
            
            # Metrics
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{int(match_score)}%</div>
                    <div class="metric-label">Overall Match</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(matched_skills)}</div>
                    <div class="metric-label">Matched Skills</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(missing_skills)}</div>
                    <div class="metric-label">Missing Skills</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Bar Chart
            fig_bar = create_bar_chart(resume_skills, job_skills)
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Proficiency Circles
            st.markdown("#### Top Skills Proficiency")
            top_skills = list(resume_skills.items())[:4]
            
            circle_cols = st.columns(4)
            for idx, (skill, score) in enumerate(top_skills):
                with circle_cols[idx]:
                    color = get_proficiency_color(score)
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <div class="proficiency-circle" style="background-color: {color};">
                            {int(score)}%
                        </div>
                        <p style="margin-top: 10px; font-size: 0.9rem; color: #666;">{skill}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Skill Comparison Bars
            st.markdown("### ⚖️ Skill Comparison")
            
            top_comparison_skills = list(set(list(resume_skills.keys())[:3] + list(job_skills.keys())[:3]))[:3]
            
            for skill in top_comparison_skills:
                resume_val = resume_skills.get(skill, 0)
                job_val = job_skills.get(skill, 0)
                
                st.markdown(f"**{skill}**")
                
                col_bar1, col_bar2 = st.columns([resume_val, 100-resume_val] if resume_val > 0 else [1, 99])
                with col_bar1:
                    st.markdown(f"""
                    <div style="background-color: #5cb85c; height: 30px; border-radius: 5px; 
                    display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                        {int(resume_val)}%
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
        
        with col_right:
            # Role View
            st.markdown("### 👥 Role View")
            
            tab1, tab2 = st.tabs(["Job Seeker", "Recruiter"])
            
            with tab1:
                st.markdown("#### Profile Comparison")
                fig_radar = create_radar_chart(resume_skills, job_skills)
                st.plotly_chart(fig_radar, use_container_width=True)
            
            with tab2:
                st.markdown("#### Candidate Fit Analysis")
                st.info(f"**Match Score**: {int(match_score)}%")
                st.success(f"**Matched Skills**: {len(matched_skills)}")
                st.warning(f"**Skills Gap**: {len(missing_skills)}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Upskilling Recommendations
            st.markdown("### 💡 Upskilling Recommendations")
            
            recommendations = generate_recommendations(missing_skills, resume_skills)
            
            for title, desc in recommendations:
                st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; 
                margin-bottom: 10px; border-left: 4px solid #4a90e2;">
                    <div style="font-weight: 600; color: #333; margin-bottom: 5px;">
                        💡 {title}
                    </div>
                    <div style="font-size: 0.85rem; color: #666;">
                        {desc}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Download Reports Section
        st.markdown("---")
        st.markdown("### 📥 Download Reports")
        
        download_col1, download_col2, download_col3 = st.columns(3)
        
        with download_col1:
            # Create CSV report
            report_data = {
                'Skill': list(resume_skills.keys())[:10],
                'Resume Score': [resume_skills.get(skill, 0) for skill in list(resume_skills.keys())[:10]],
                'Job Requirement': [job_skills.get(skill, 0) for skill in list(resume_skills.keys())[:10]]
            }
            df_report = pd.DataFrame(report_data)
            csv = df_report.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📄 Download CSV Report",
                data=csv,
                file_name="skill_gap_analysis.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with download_col2:
            # Summary report
            summary = f"""Skill Gap Analysis Report
            
Overall Match: {int(match_score)}%
Matched Skills: {len(matched_skills)}
Missing Skills: {len(missing_skills)}

Matched Skills:
{chr(10).join(['- ' + skill for skill in matched_skills[:10]])}

Missing Skills:
{chr(10).join(['- ' + skill for skill in missing_skills[:10]])}

Recommendations:
{chr(10).join(['- ' + title + ': ' + desc for title, desc in recommendations])}
"""
            st.download_button(
                label="📝 Download Summary",
                data=summary,
                file_name="skill_gap_summary.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with download_col3:
            st.info("📊 PDF export coming soon!")
    
    else:
        # Welcome screen
        st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <h2>Welcome to Skill Gap Analysis Dashboard</h2>
            <p style="font-size: 1.2rem; color: #666; margin-top: 20px;">
                Upload your resume and job description to get started
            </p>
            <p style="margin-top: 30px;">
                👈 Use the sidebar to upload your files
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()