import streamlit as st
import time
from utils.database import find_user_by_email, generate_and_save_otp, verify_otp, reset_password_with_otp


def forgot_password_page():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .auth-wrapper {
        min-height: 100vh;
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: radial-gradient(circle at 8% 12%, rgba(255,255,255,0.07), transparent 7%),
                    radial-gradient(circle at 92% 88%, rgba(255,255,255,0.03), transparent 10%),
                    linear-gradient(180deg, #f3fbff 0%, #dff7ff 40%, #c6eefc 100%);
        position: relative;
        overflow: hidden;
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

    .reset-container {
        width: 100%;
        max-width: 360px;
        margin: 0 auto;
        padding: 18px 18px;
        background: rgba(255, 255, 255, 0.98);
        border-radius: 16px;
        box-shadow: 0 12px 30px rgba(8, 15, 30, 0.08);
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

    .reset-header {
        text-align: center;
        margin-bottom: 32px;
    }

    .reset-header h1 {
        color: #0f172a;
        margin: 0;
        font-size: 24px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 8px;
    }

    .reset-header p {
        color: #64748b;
        margin: 0;
        font-size: 14px;
        font-weight: 400;
        line-height: 1.4;
    }

    .input-group {
        margin-bottom: 18px;
    }

    .input-group label {
        display: block;
        color: #374151;
        font-weight: 500;
        margin-bottom: 8px;
        font-size: 14px;
        letter-spacing: 0.2px;
    }

    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(0, 0, 0, 0.06) !important;
        border-radius: 10px !important;
        padding: 10px 12px !important;
        font-size: 14px !important;
        color: #1f2937 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-family: 'Inter', sans-serif !important;
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
        border-radius: 10px !important;
        padding: 12px 18px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3), 0 4px 10px rgba(0, 0, 0, 0.2) !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.4), 0 6px 15px rgba(0, 0, 0, 0.25) !important;
    }

    .stButton button:active {
        transform: translateY(0px) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    }

    .back-link {
        text-align: center;
        margin-top: 24px;
        padding-top: 24px;
        border-top: 1px solid #e2e8f0;
    }

    .back-link p {
        color: #475569;
        font-size: 14px;
        margin: 0;
    }

    .back-link a {
        color: #2563eb;
        text-decoration: none;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .back-link a:hover {
        color: #1d4ed8;
    }
    </style>
    """, unsafe_allow_html=True)

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
        <div class="reset-container">
            <div class="reset-header">
                <h1>Reset Your Password</h1>
                <p>Enter your email to receive an OTP</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        st.markdown('<label>Email Address</label>', unsafe_allow_html=True)
        email = st.text_input("Email", placeholder="name@company.com", label_visibility="collapsed", key="forgot_email")
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Send OTP", use_container_width=True, type="primary"):
            if not email:
                st.error("❌ Please enter your email address.")
            else:
                user = find_user_by_email(email)
                if user:
                    otp = generate_and_save_otp(email)
                    if otp:
                        st.session_state.otp_code = otp
                        st.session_state.reset_email = email
                        st.success(f"✅ OTP sent! Your OTP is: **{otp}**")
                        st.info("Keep this OTP safe. You'll need it in the next step.")
                        
                        progress_placeholder = st.empty()
                        status_placeholder = st.empty()
                        
                        otp_timeout = 10000
                        for i in range(otp_timeout, 0, -1000):
                            with progress_placeholder.container():
                                st.progress((otp_timeout - i) / otp_timeout)
                            minutes = i // 60000
                            seconds = (i // 10000) % 60
                            status_placeholder.info(f"⏱️ You have {minutes}:{seconds:02d} minutes to enter OTP")
                            time.sleep(60000)
                        
                        st.session_state.page = "reset_password"
                        st.rerun()
                    else:
                        st.error("❌ Error generating OTP. Please try again.")
                else:
                    st.info("ℹ️ If this email exists, you will receive an OTP.")

        st.markdown("""
        <div class="back-link">
            <p><span style="color: #2563eb; font-weight: 600; cursor: pointer;">Back to Login</span></p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Return to Login", use_container_width=False, key="back_to_login_from_forgot"):
            st.session_state.page = "login"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


def reset_password_page():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .auth-wrapper {
        min-height: 100vh;
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: radial-gradient(circle at 8% 12%, rgba(255,255,255,0.07), transparent 7%),
                    radial-gradient(circle at 92% 88%, rgba(255,255,255,0.03), transparent 10%),
                    linear-gradient(180deg, #f3fbff 0%, #dff7ff 40%, #c6eefc 100%);
        position: relative;
        overflow: hidden;
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

    .reset-container {
        width: 100%;
        max-width: 360px;
        margin: 0 auto;
        padding: 18px 18px;
        background: rgba(255, 255, 255, 0.98);
        border-radius: 16px;
        box-shadow: 0 12px 30px rgba(8, 15, 30, 0.08);
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

    .reset-header {
        text-align: center;
        margin-bottom: 32px;
    }

    .reset-header h1 {
        color: #0f172a;
        margin: 0;
        font-size: 24px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 8px;
    }

    .reset-header p {
        color: #64748b;
        margin: 0;
        font-size: 14px;
        font-weight: 400;
        line-height: 1.4;
    }

    .input-group {
        margin-bottom: 18px;
    }

    .input-group label {
        display: block;
        color: #374151;
        font-weight: 500;
        margin-bottom: 8px;
        font-size: 14px;
        letter-spacing: 0.2px;
    }

    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(0, 0, 0, 0.06) !important;
        border-radius: 10px !important;
        padding: 10px 12px !important;
        font-size: 14px !important;
        color: #1f2937 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-family: 'Inter', sans-serif !important;
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
        border-radius: 10px !important;
        padding: 12px 18px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3), 0 4px 10px rgba(0, 0, 0, 0.2) !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.4), 0 6px 15px rgba(0, 0, 0, 0.25) !important;
    }

    .back-link {
        text-align: center;
        margin-top: 24px;
        padding-top: 24px;
        border-top: 1px solid #e2e8f0;
    }

    .back-link p {
        color: #475569;
        font-size: 14px;
        margin: 0;
    }

    .back-link a {
        color: #2563eb;
        text-decoration: none;
        font-weight: 600;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

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
        reset_email = st.session_state.get("reset_email", "")
        
        if not reset_email:
            st.markdown("""
            <div class="reset-container">
                <div class="reset-header">
                    <h1>Reset Your Password</h1>
                    <p>Enter your email to receive an OTP</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="input-group">', unsafe_allow_html=True)
            st.markdown('<label>Email Address</label>', unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="name@company.com", label_visibility="collapsed", key="reset_email_input")
            st.markdown('</div>', unsafe_allow_html=True)

            if st.button("Send OTP", use_container_width=True, type="primary", key="send_otp_btn"):
                if not email:
                    st.error("❌ Please enter your email address.")
                else:
                    user = find_user_by_email(email)
                    if user:
                        otp = generate_and_save_otp(email)
                        if otp:
                            st.success(f"✅ OTP sent! Your OTP is: **{otp}**")
                            st.info("Keep this OTP safe. You'll need it in the next step.")
                            st.session_state.reset_email = email
                            st.rerun()
                        else:
                            st.error("❌ Error generating OTP. Please try again.")
                    else:
                        st.info("ℹ️ If this email exists, you will receive an OTP.")

            if st.button("Back to Login", use_container_width=False, key="back_to_login_from_reset_direct"):
                st.session_state.page = "login"
                st.rerun()
        else:
            st.markdown("""
            <div class="reset-container">
                <div class="reset-header">
                    <h1>Create New Password</h1>
                    <p>Verify OTP and set your new password</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="input-group">', unsafe_allow_html=True)
            st.markdown(f'<label>Email Address</label>', unsafe_allow_html=True)
            st.markdown(f'<div style="padding: 10px 12px; background-color: #f3f4f6; border-radius: 10px; border: 1px solid rgba(0,0,0,0.06); color: #6b7280; font-size: 14px;">{reset_email}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            otp_code = st.session_state.get("otp_code")
            if otp_code:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%); border: 2px solid #3b82f6; border-radius: 12px; padding: 24px; text-align: center; margin-bottom: 24px;">
                    <div style="color: #1e40af; font-size: 14px; font-weight: 600; margin-bottom: 12px;">Your OTP Code</div>
                    <div style="color: #0f172a; font-size: 40px; font-weight: 700; letter-spacing: 8px; font-family: 'Courier New', monospace; margin-bottom: 16px;">{otp_code}</div>
                    <div style="color: #dc2626; font-size: 16px; font-weight: 600;">
                        <span id="timer">30</span>s remaining
                    </div>
                </div>
                <script>
                let timeLeft = 30;
                const timerElement = document.getElementById('timer');
                const interval = setInterval(() => {{
                    timeLeft--;
                    timerElement.textContent = timeLeft;
                    if (timeLeft <= 0) {{
                        clearInterval(interval);
                        timerElement.textContent = '0';
                    }}
                }}, 1000);
                </script>
                """, unsafe_allow_html=True)
            
            st.markdown('<div class="input-group">', unsafe_allow_html=True)
            st.markdown('<label>OTP</label>', unsafe_allow_html=True)
            otp = st.text_input("OTP", placeholder="Enter the 6-digit OTP", label_visibility="collapsed", key="reset_otp")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="input-group">', unsafe_allow_html=True)
            st.markdown('<label>New Password</label>', unsafe_allow_html=True)
            new_password = st.text_input("New Password", type="password", placeholder="Enter new password", label_visibility="collapsed", key="reset_new_password")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="input-group">', unsafe_allow_html=True)
            st.markdown('<label>Confirm Password</label>', unsafe_allow_html=True)
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password", label_visibility="collapsed", key="reset_confirm_password")
            st.markdown('</div>', unsafe_allow_html=True)

            if st.button("Reset Password", use_container_width=True, type="primary", key="reset_password_btn"):
                if not all([otp, new_password, confirm_password]):
                    st.error("❌ Please fill in all fields.")
                elif new_password != confirm_password:
                    st.error("❌ Passwords do not match.")
                elif len(new_password) < 6:
                    st.error("❌ Password must be at least 6 characters.")
                else:
                    if verify_otp(reset_email, otp):
                        reset_password_with_otp(reset_email, new_password)
                        st.success("✅ Password reset successfully! Redirecting to login...")
                        st.session_state.page = "login"
                        st.session_state.reset_email = None
                        st.rerun()
                    else:
                        st.error("❌ Invalid OTP. Please try again.")

            st.markdown("""
            <div class="back-link">
                <p><span style="color: #2563eb; font-weight: 600; cursor: pointer;">Back to Login</span></p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Return to Login", use_container_width=False, key="back_to_login_from_reset"):
                st.session_state.page = "login"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
