import streamlit as st
from utils.database import add_user


def signup():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    /* Fill viewport so centering works */
    html, body, [data-testid="stAppViewContainer"], .stApp, .main, .block-container {
        height: 100% !important;
        margin: 0;
        padding: 0 !important;
    }

    .auth-wrapper {
        min-height: 100vh;
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: radial-gradient(circle at 8% 12%, rgba(255,255,255,0.06), transparent 7%),
                    radial-gradient(circle at 92% 88%, rgba(255,255,255,0.03), transparent 10%),
                    linear-gradient(180deg, #f3fbff 0%, #e5f8ff 40%, #cfeefd 100%);
        position: relative;
        overflow: hidden;
    }

    .auth-wrapper::before {
        content: '';
        position: absolute;
        top: 10%;
        left: 10%;
        width: 200px;
        height: 200px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        filter: blur(40px);
        animation: float 6s ease-in-out infinite;
    }

    .auth-wrapper::after {
        content: '';
        position: absolute;
        bottom: 15%;
        right: 15%;
        width: 150px;
        height: 150px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        filter: blur(30px);
        animation: float 8s ease-in-out infinite reverse;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }

    .top-left-icon {
        position: absolute;
        top: 30px;
        left: 30px;
        z-index: 10;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .top-left-icon:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    }

    .signup-container {
        width: 100%;
        max-width: 320px;
        margin: 0 auto;
        padding: 8px 10px;
        background: rgba(255, 255, 255, 0.98);
        border-radius: 16px;
        box-shadow: 0 12px 30px rgba(8, 15, 30, 0.06);
        animation: slideIn 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(8px);
        position: relative;
        z-index: 5;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .signup-header {
        text-align: center;
        margin-bottom: 6px;
        animation: fadeInDown 0.35s ease-out;
        position: relative;
    }

    .logo {
        font-size: 22px;
        margin-bottom: 4px;
        font-weight: 700;
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 50%, #0369a1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.6px;
        font-family: 'Poppins', 'Inter', sans-serif;
    }

    .signup-header h1 {
        color: #0f172a;
        margin: 0;
        font-size: 18px;
        font-weight: 700;
        letter-spacing: -0.4px;
        margin-bottom: 4px;
    }

    .signup-header p {
        color: #64748b;
        margin: 0;
        font-size: 11px;
        font-weight: 400;
        line-height: 1.25;
    }
    
    .input-group {
        margin-bottom: 4px;
        animation: fadeInUp 0.35s ease-out forwards;
    }

    .input-group:nth-child(1) {
        animation-delay: 0.2s;
    }

    .input-group:nth-child(2) {
        animation-delay: 0.4s;
    }

    .input-group:nth-child(3) {
        animation-delay: 0.6s;
    }

    .input-group:nth-child(4) {
        animation-delay: 0.8s;
    }

    .input-group label {
        display: block;
        color: #374151;
        font-weight: 500;
        margin-bottom: 4px;
        font-size: 12px;
        letter-spacing: 0.12px;
    }

    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 1px solid rgba(0, 0, 0, 0.06) !important;
        border-radius: 6px !important;
        padding: 6px 8px !important;
        font-size: 12px !important;
        color: #1f2937 !important;
        transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.1px;
        backdrop-filter: blur(6px) !important;
    }

    .stTextInput input:hover {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-color: rgba(14, 165, 233, 0.3) !important;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.1) !important;
    }

    .stTextInput input:focus {
        background-color: #ffffff !important;
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1), 0 4px 12px rgba(14, 165, 233, 0.15) !important;
        outline: none !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #0f172a 0%, #111827 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 8px 10px !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3), 0 4px 10px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        letter-spacing: 0.3px;
        font-family: 'Inter', sans-serif !important;
        position: relative;
        overflow: hidden;
    }

    .stButton button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }

    .stButton button:hover::before {
        left: 100%;
    }

    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.4), 0 6px 15px rgba(0, 0, 0, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    }

    .stButton button:active {
        transform: translateY(0px) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    }

    .social-login {
        margin: 32px 0;
        text-align: center;
    }

    .social-login-title {
        color: #6b7280;
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 20px;
        position: relative;
    }

    .social-login-title::before,
    .social-login-title::after {
        content: '';
        position: absolute;
        top: 50%;
        width: 80px;
        height: 1px;
        background: #e5e7eb;
    }

    .social-login-title::before {
        left: -100px;
    }

    .social-login-title::after {
        right: -100px;
    }

    .social-buttons {
        display: flex;
        gap: 12px;
        justify-content: center;
    }

    .social-btn {
        flex: 1;
        max-width: 120px;
        padding: 12px 16px;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        font-size: 14px;
        font-weight: 500;
        color: #374151;
        text-decoration: none;
    }

    .social-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        border-color: #d1d5db;
    }

    .social-btn.google {
        color: #374151;
    }

    .social-btn.github {
        color: #374151;
    }
    
    .password-requirements {
        background-color: #f0f9ff;
        border-left: 4px solid #2563eb;
        padding: 10px 12px;
        border-radius: 8px;
        margin-top: 12px;
        font-size: 13px;
        color: #1e40af;
        font-weight: 500;
    }
    
    .login-link {
        text-align: center;
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid #e2e8f0;
    }
    
    .login-link p {
        color: #475569;
        font-size: 13px;
        margin: 0;
    }
    
    .login-link a {
        color: #2563eb;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .login-link a:hover {
        color: #1d4ed8;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .stSuccess, .stError, .stWarning {
        animation: slideIn 0.5s ease-out !important;
        border-radius: 12px !important;
        border: none !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%) !important;
        color: #15803d !important;
    }

    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%) !important;
        color: #991b1b !important;
    }

    .stWarning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%) !important;
        color: #92400e !important;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .signup-container {
            margin: 20px;
            padding: 32px 24px;
            max-width: none;
        }

        .signup-header h1 {
            font-size: 24px;
        }

        .logo {
            font-size: 36px;
        }

        .social-login-title::before,
        .social-login-title::after {
            width: 40px;
        }

        .social-login-title::before {
            left: -50px;
        }

        .social-login-title::after {
            right: -50px;
        }

        .top-left-icon {
            top: 20px;
            left: 20px;
            padding: 10px;
        }

        .auth-wrapper::before,
        .auth-wrapper::after {
            display: none;
        }
    }

    @media (max-width: 480px) {
        .signup-container {
            margin: 10px;
            padding: 24px 20px;
        }

        .social-buttons {
            flex-direction: column;
            gap: 8px;
        }

        .social-btn {
            max-width: none;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Top left icon
    st.markdown("""
    <div class="top-left-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#0ea5e9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 17L12 22L22 17" stroke="#0ea5e9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="#0ea5e9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        st.markdown("""
        <div class="signup-container">
            <div class="signup-header">
                <div class="logo">Resumify</div>
                <h1>Get Started</h1>
                <p>Create your professional career account</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        st.markdown('<label>Username</label>', unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="Choose a username", label_visibility="collapsed", key="signup_username")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        st.markdown('<label>Email Address</label>', unsafe_allow_html=True)
        email = st.text_input("Email", placeholder="name@company.com", label_visibility="collapsed", key="signup_email")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        st.markdown('<label>Password</label>', unsafe_allow_html=True)
        password = st.text_input("Password", type="password", placeholder="Create a strong password", label_visibility="collapsed", key="signup_password")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        st.markdown('<label>Confirm Password</label>', unsafe_allow_html=True)
        password_confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", label_visibility="collapsed", key="signup_password_confirm")
        st.markdown('</div>', unsafe_allow_html=True)

        # Password requirements removed per request

        # Social login section with divider
        # Social/OAuth removed per request

        if st.button("Sign Up", use_container_width=True, type="primary"):
            if not all([username, email, password, password_confirm]):
                st.error("❌ Please fill in all fields.")
            elif password != password_confirm:
                st.error("❌ Passwords do not match.")
            elif len(password) < 6:
                st.error("❌ Password must be at least 6 characters long.")
            else:
                success = add_user(username, email, password)
                if success:
                    st.success("✅ Account created successfully! Please login.")
                    st.balloons()
                else:
                    st.error("❌ Username or email already exists.")

        st.markdown("""
        <div class="login-link">
            <p>Already have an account? <span style="color: #2563eb; font-weight: 600;">Sign in here</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
