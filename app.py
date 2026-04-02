import streamlit as st
from utils.database import init_db
from auth.login import login
from auth.signup import signup
from auth.forgot_password import forgot_password_page, reset_password_page
from pages import upload_analyze, skill_hub, chatbot, mock_interview, job_recomm, home

# Initialize database
init_db()

# Page configuration
st.set_page_config(
    page_title="Resumify - Career Development Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "home"
if "username" not in st.session_state:
    st.session_state.username = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# Global CSS for professional UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .main {
        background: #f0f4f9;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid #334155;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white !important;
    }
    
    hr {
        border: none;
        height: 1px;
        background: rgba(255, 255, 255, 0.1);
        margin: 1.5rem 0;
    }
    
    .stRadio > label {
        font-weight: 500;
        font-size: 15px;
        transition: all 0.2s ease;
    }
    
    .stRadio > div {
        gap: 10px;
    }
    
    .stButton button {
        transition: all 0.3s ease !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
    }
    
    .metric-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        transform: translateY(-4px);
    }
    
    h1, h2, h3 {
        color: #0f172a !important;
        font-weight: 700 !important;
    }
    
    h1 {
        font-size: 36px !important;
        letter-spacing: -1px !important;
    }
    
    h2 {
        font-size: 28px !important;
    }
    
    h3 {
        font-size: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Routing logic ---
if not st.session_state.logged_in:
    # Home page
    if st.session_state.page == "home":
        home.home()
    # Authentication pages
    elif st.session_state.page == "login":
        login()
        st.divider()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✨ New user? Create Account", use_container_width=True):
                st.session_state.page = "signup"
                st.rerun()

    elif st.session_state.page == "signup":
        signup()
        st.divider()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔐 Already have an account? Login", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()

    elif st.session_state.page == "reset_password":
        reset_password_page()

else:
    # Logged in - Show dashboard with sidebar navigation
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem 1rem 1rem 1rem;">
            <div style="font-size: 28px; font-weight: 700; background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 8px;">Resumify</div>
            <p style="margin: 0; font-size: 13px; opacity: 0.8; letter-spacing: 1px; text-transform: uppercase;">Career Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown(f"""
        <div style="text-align: center; padding: 16px; background: rgba(255,255,255,0.05); border-radius: 12px; margin-bottom: 24px; border: 1px solid rgba(255,255,255,0.1);">
            <div style="font-weight: 600; font-size: 15px; margin-bottom: 4px;">Welcome, {st.session_state.username}!</div>
            <div style="font-size: 13px; opacity: 0.8; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{st.session_state.email}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Navigation**")
        page = st.radio(
            "Go to",
            ["Dashboard", "Upload & Analyze", "Skill Hub", "Job Recommendation", "AI Chatbot", "Mock Interview", "Logout"],
            label_visibility="collapsed"
        )

    # Page routing
    if page == "Dashboard":
        st.markdown("""
        <style>
        .dashboard-header {
            margin-bottom: 40px;
            animation: fadeIn 0.6s ease-out;
        }
        
        .dashboard-title {
            font-size: 40px;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: -1.5px;
            margin-bottom: 12px;
        }
        
        .dashboard-subtitle {
            font-size: 16px;
            color: #64748b;
            font-weight: 400;
        }
        
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
            margin: 32px 0;
        }
        
        .feature-card {
            background: white;
            padding: 28px;
            border-radius: 16px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            border: 1px solid #e2e8f0;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%);
        }
        
        .feature-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.12);
            border-color: #2563eb;
        }
        
        .feature-icon {
            font-size: 40px;
            margin-bottom: 16px;
        }
        
        .feature-title {
            font-size: 18px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 8px;
        }
        
        .feature-desc {
            font-size: 14px;
            color: #64748b;
            line-height: 1.5;
        }
        
        .section-divider {
            height: 1px;
            background: linear-gradient(90deg, #e2e8f0 0%, transparent 50%, #e2e8f0 100%);
            margin: 48px 0;
        }
        
        .info-box {
            background: linear-gradient(135deg, #f0f9ff 0%, #f9f5ff 100%);
            border: 1px solid #e2e8f0;
            border-left: 4px solid #2563eb;
            padding: 24px;
            border-radius: 12px;
            margin-bottom: 24px;
        }
        
        .info-box h4 {
            color: #1e40af;
            margin: 0 0 12px 0;
            font-size: 16px;
        }
        
        .info-box p {
            color: #334155;
            margin: 8px 0;
            font-size: 14px;
            line-height: 1.6;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        </style>
        
        <div class="dashboard-header">
            <div class="dashboard-title">Dashboard</div>
            <div class="dashboard-subtitle">Manage your career development journey</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # First row - 3 cards (centered)
        col_empty1, col1, col2, col3, col_empty2 = st.columns([0.5, 1, 1, 1, 0.5])
        with col1:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🎤</div>
                <div class="feature-title">Mock Interview</div>
                <div class="feature-desc">Practice technical interviews with AI-powered feedback</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">💼</div>
                <div class="feature-title">Upload & Analyze</div>
                <div class="feature-desc">Analyze your resume and identify skill gaps</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Skill Hub</div>
                <div class="feature-desc">Curated learning resources for skill development</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Second row - 2 cards (centered)
        col_empty1, col1, col2, col_empty2 = st.columns([0.75, 1, 1, 0.75])
        with col1:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">AI Chatbot</div>
                <div class="feature-desc">Get personalized career guidance and advice</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Job Recommendation</div>
                <div class="feature-desc">Discover roles that match your skills and goals</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="info-box">
                <h4>📘 Getting Started</h4>
                <p><strong>1. Upload Your Resume</strong> - Start with Upload & Analyze to identify your current skills</p>
                <p><strong>2. Learn New Skills</strong> - Use Skill Hub to access curated resources for missing skills</p>
                <p><strong>3. Build Resume</strong> - Create professional resumes with our Resume Builder</p>
                <p><strong>4. Practice Interviews</strong> - Use Mock Interview to prepare for interviews</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-box">
                <h4>✨ Key Features</h4>
                <p><strong>AI-Powered Analysis</strong> - Get intelligent feedback on your career development</p>
                <p><strong>Real-time Preview</strong> - See changes instantly as you build your resume</p>
                <p><strong>Personalized Recommendations</strong> - Tailored guidance based on your profile</p>
                <p><strong>Professional Templates</strong> - Industry-standard resume designs</p>
            </div>
            """, unsafe_allow_html=True)
        
    elif page == "Upload & Analyze":
        upload_analyze.main()
    elif page == "Skill Hub":
        skill_hub.main()
    elif page == "Job Recommendation":
        job_recomm.run()
    elif page == "AI Chatbot":
        chatbot.main()
    elif page == "Mock Interview":
        mock_interview.main()
    elif page == "Logout":
        # Clear session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.logged_in = False
        st.session_state.page = "home"
        st.success("✅ Logged out successfully!")
        st.rerun()
