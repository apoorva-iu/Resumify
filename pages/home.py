import streamlit as st


def home():
   # --- CSS Styles ---
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&display=swap');
    
    /* Center the main container text */
    .hero-title { 
        font-size: 56px; 
        font-weight: 800; 
        color: #0f172a; 
        line-height: 1.15; 
        letter-spacing: -2px; 
        margin: 40px auto 24px auto; 
        text-align: center; 
        font-family: 'Poppins', sans-serif;
        display: block;
        width: 100%;
    }

    .hero-description { 
        font-size: 20px; 
        color: #475569; 
        line-height: 1.6; /* Increased for better readability */
        margin: 0 auto 40px auto; 
        max-width: 850px; 
        text-align: center; 
        font-family: 'Inter', sans-serif;
        display: block; /* Ensures margin auto works */
    }

    /* Keep your existing button and feature styles below */
    .stButton > button { 
        font-weight: 700 !important; font-size: 13px !important; border-radius: 10px !important;
        padding: 10px 22px !important; transition: all 0.3s ease !important; height: auto !important;
        font-family: 'Poppins', sans-serif !important; background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%) !important;
        color: white !important; box-shadow: 0 8px 20px rgba(14, 165, 233, 0.3) !important;
    }
    .header-button-style .stButton > button { 
        background: #0f172a !important; border: 2px solid #38bdf8 !important; color: #38bdf8 !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.3) !important; padding: 8px 18px !important; border-radius: 8px !important;
        transform: none !important;
    }
    .key-features-title { text-align: center; font-size: 32px; font-weight: 800; color: #0f172a; margin: 30px 0 28px 0; letter-spacing: -1px; font-family: 'Poppins', sans-serif; }
    .feature-box { background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px); padding: 32px; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.6); transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); text-align: center; height: 280px; width: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08); }
    .feature-icon { font-size: 40px; margin-bottom: 12px; }
    .feature-name { font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 10px; font-family: 'Poppins', sans-serif; }
    .feature-desc { font-size: 15px; color: #64748b; line-height: 1.5; margin: 0; }
    .divider-light { border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(14, 165, 233, 0.2), transparent); margin: 16px 0; }
    </style>
    """, unsafe_allow_html=True)

    # --- Header Layout ---
    col_logo, col_spacer, btn_col1, btn_col2 = st.columns([1.5, 6, 1, 1])

    with col_logo:
        st.markdown('<p class="logo-brand">Resumify</p>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="header-button-style">', unsafe_allow_html=True)
        
        with btn_col1:
            if st.button("Sign In", use_container_width=True, key="home_signin_btn_01"):
                st.session_state.page = "login"
                st.rerun()

        with btn_col2:
            if st.button("Sign Up", use_container_width=True, key="home_header_signup_btn"):
                st.session_state.page = "signup"
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)
    # --- End Header Layout ---
    
    st.markdown('<div class="divider-light"></div>', unsafe_allow_html=True)
    
    # --- Hero Section ---
    st.markdown('<h1 class="hero-title">Resumify – Your Career\'s Smartest Companion</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="hero-description">
    Step into a workspace where building your future feels effortless. Resumify blends clean design with smart automation to help you create professional resumes, discover personalized job insights, and prepare confidently for interviews.
    </p>
    """, unsafe_allow_html=True)
    # --- End Hero Section ---
    st.write("")
    st.markdown('<div class="key-features-title">Key Features</div>', unsafe_allow_html=True)
    
    # --- Features Section ---
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">✨</div>
            <div class="feature-name">AI-Crafted Resumes</div>
            <div class="feature-desc">Create polished, industry-ready resumes in minutes.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🎯</div>
            <div class="feature-name">Smart Job Recommendations</div>
            <div class="feature-desc">Discover roles that match your skills and goals.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🎤</div>
            <div class="feature-name">Interview Prep Engine</div>
            <div class="feature-desc">Practice with tailored questions and meaningful feedback.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">📊</div>
            <div class="feature-name">Dashboard Overview</div>
            <div class="feature-desc">Access all your tools from one simple, intuitive place.</div>
        </div>
        """, unsafe_allow_html=True)
    # --- End Features Section ---
    
    st.markdown('<div class="divider-light"></div>', unsafe_allow_html=True)
    
    # --- CTA Section ---
    col_l, col_center, col_r = st.columns([1, 2, 1])
    with col_center:
        if st.button("🚀 Get Started", use_container_width=True, key="home_cta"):
            st.session_state.page = "login"
            st.rerun()
    # --- End CTA Section ---