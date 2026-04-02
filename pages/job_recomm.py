import streamlit as st
import pickle
import pandas as pd
import os
from pathlib import Path

def recommend(job_title, data, similarity):
    """Generate top 5 job recommendations based on similarity."""
    try:
        # Find job in data
        matching_jobs = data[data['jobtitle'] == job_title]
        if matching_jobs.empty:
            return None
        
        job_index = matching_jobs.index[0]
        
        # Get similarity scores
        if job_index >= len(similarity):
            return None
            
        distances = similarity[job_index]
        
        # Get top 5 recommendations (excluding the job itself at index 0)
        job_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        if not job_list:
            return None

        recommended_jobs = []
        for i in job_list:
            idx = i[0]
            if idx < len(data):
                recommended_jobs.append(data.iloc[idx][['company', 'employmenttype_jobstatus', 'joblocation_address', 'jobtitle', 'skills']])
        
        return recommended_jobs if recommended_jobs else None
    except Exception as e:
        return None

def load_data():
    """Load and cache pickle files safely from project root."""
    try:
        project_root = Path(__file__).parent.parent
        job_recom_path = project_root / 'Job_recom.pkl'
        job_similar_path = project_root / 'job_similiar.pkl'
        
        if not job_recom_path.exists():
            st.error(f"❌ File not found: {job_recom_path}")
            return None, None
        
        if not job_similar_path.exists():
            st.error(f"❌ File not found: {job_similar_path}")
            return None, None
        
        with open(job_recom_path, 'rb') as f:
            Job_dict = pickle.load(f)
        
        data = pd.DataFrame(Job_dict)
        
        with open(job_similar_path, 'rb') as f:
            similarity = pickle.load(f)
        
        return data, similarity
    except Exception as e:
        st.error(f"❌ Error loading data files: {str(e)}")
        return None, None

def run():
    """Main function for Job Recommendation page."""
    # Check if user is logged in
    if not st.session_state.get('logged_in', False):
        st.warning("🔒 Please login first to access this page.")
        st.stop()
    
    # Professional UI Styling consistent with dashboard
    st.markdown("""
    <style>
    .job-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 16px;
        border-left: 4px solid #2563eb;
        transition: all 0.3s ease;
    }
    .job-card:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    .job-title {
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 12px;
    }
    .job-detail {
        font-size: 14px;
        color: #475569;
        margin: 8px 0;
    }
    .job-detail strong {
        color: #0f172a;
    }
    .intro-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #f9f5ff 100%);
        border: 1px solid #e2e8f0;
        border-left: 4px solid #2563eb;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 24px;
    }
    .intro-box h3 {
        color: #1e40af;
        margin-top: 0;
    }
    .intro-box p {
        color: #334155;
        line-height: 1.6;
        margin: 8px 0;
    }
    .stSelectbox {
        color: #0f172a !important;
    }
    .stSelectbox > div > div {
        color: #0f172a !important;
        background-color: white !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("💼 Job Recommendation System")
    
    st.markdown("""
    <div class="intro-box">
        <h3>🔍 Find Your Next Opportunity</h3>
        <p>Select a job title to discover similar positions tailored to your interests. This system uses advanced machine learning to analyze job characteristics and recommend the most relevant opportunities based on title, company, location, and required skills.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Load data
    data, similarity = load_data()
    
    if data is None or similarity is None:
        st.stop()
    
    # Initialize session state for recommendations
    if 'show_recommendations' not in st.session_state:
        st.session_state.show_recommendations = False
    if 'last_selected_job' not in st.session_state:
        st.session_state.last_selected_job = None
    
    st.markdown("### 🔎 Select Job Title")
    
    # Job selection in main page with placeholder
    job_options = ["-- Select Role --"] + sorted(data['jobtitle'].unique())
    select_job_name = st.selectbox(
        "Choose a job title",
        job_options,
        index=0,
        help="Choose a job title to get similar recommendations.",
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        button_clicked = st.button('🎯 Get Recommendations', use_container_width=True)
    
    # Recommendation results section
    if button_clicked and select_job_name != "-- Select Role --":
        st.session_state.show_recommendations = True
        st.session_state.last_selected_job = select_job_name
    elif button_clicked and select_job_name == "-- Select Role --":
        st.warning("⚠️ Please select a job title first.")
    
    if st.session_state.show_recommendations and st.session_state.last_selected_job:
        st.markdown(f"### 📌 Top 5 Jobs Similar to '{st.session_state.last_selected_job}'")
        st.divider()
        
        recommendations = recommend(st.session_state.last_selected_job, data, similarity)
        
        if recommendations and len(recommendations) > 0:
            for idx, rec in enumerate(recommendations, 1):
                st.markdown(f"""
                <div class="job-card">
                    <div class="job-title">{idx}. {rec['jobtitle']}</div>
                    <div class="job-detail"><strong>🏢 Company:</strong> {rec['company']}</div>
                    <div class="job-detail"><strong>📋 Employment Type:</strong> {rec['employmenttype_jobstatus']}</div>
                    <div class="job-detail"><strong>📍 Location:</strong> {rec['joblocation_address']}</div>
                    <div class="job-detail"><strong>🛠️ Required Skills:</strong> {rec['skills']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("ℹ️ No recommendations available for this job title at the moment. Please try another role.")
    
    st.caption("💡 Tip: Select a job title and click 'Get Recommendations' to see similar positions.")