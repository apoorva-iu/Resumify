import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import time
import re
import json
from difflib import SequenceMatcher
from collections import defaultdict


def safe_rerun():
    """Compat helper for programmatic rerun across Streamlit versions.

    - Tries `st.experimental_rerun()` first (common API).
    - If not available, attempts to raise the internal `RerunException`.
    - If that fails, falls back to changing a query param and stopping the script.
    """
    try:
        # Preferred API when available
        st.experimental_rerun()
        return
    except Exception:
        pass

    # Try to import and raise the internal rerun exception used by Streamlit
    try:
        from streamlit.runtime.scriptrunner import RerunException
        raise RerunException()
    except Exception:
        try:
            # Older/newer internal path fallback
            from streamlit.runtime.scriptrunner.script_runner import RerunException as RR
            raise RR()
        except Exception:
            # Last-resort fallback: nudge a query param so the page URL changes
            params = dict(st.query_params)
            params["_rerun"] = str(time.time())
            st.query_params = params
            st.stop()
import pdfplumber
import docx
import pandas as pd
import plotly.express as px

def main():
    # Check if user is logged in
    if not st.session_state.get('logged_in', False):
        st.warning("🔒 Please login first to access this page.")
        st.stop()
    
    # Professional UI Styling
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .card {
        background: white;
        padding: 28px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        margin-bottom: 24px;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    .card:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        transform: translateY(-4px);
    }
    .metric-card {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        padding: 24px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        margin: 12px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .skill-badge-present {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 10px 16px;
        border-radius: 8px;
        display: inline-block;
        margin: 6px;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }
    .skill-badge-missing {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        color: white;
        padding: 10px 16px;
        border-radius: 8px;
        display: inline-block;
        margin: 6px;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(249, 115, 22, 0.3);
    }
    .stSelectbox select {
        border-radius: 8px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 10px !important;
        font-size: 14px !important;
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

    st.markdown("""
    <h1 style="color: #0f172a; margin-bottom: 8px;">Upload & Analyze Resume</h1>
    <p style="color: #64748b; font-size: 16px; margin: 0;">Discover your skills and identify gaps for your target role</p>
    """, unsafe_allow_html=True)
    st.divider()

    role_skills_dict = {
        "Software Engineer": ["Python", "Java", "C++", "Git", "Algorithms", "Data Structures", "SQL"],
        "Data Analyst": ["Python", "SQL", "R", "Excel", "Statistics", "Tableau", "PowerBI"],
        "Frontend Developer": ["HTML", "CSS", "JavaScript", "React", "Git", "UI/UX", "TypeScript"],
        "Backend Developer": ["Python", "Java", "Node.js", "SQL", "APIs", "Docker", "Git"],
        "Machine Learning Engineer": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "Data Structures", "SQL"],
        "DevOps Engineer": ["Linux", "Docker", "Kubernetes", "AWS", "CI/CD", "Git", "Python"],
        "Cybersecurity Analyst": ["Cybersecurity", "Networking", "Linux", "Python", "Ethical Hacking", "Security Tools", "Incident Response"]
    }

    # Role Selection Card
    st.markdown("### 🎯 Step 1: Select Your Target Role")
    # Check reset flags (set by the Analyze Another Resume button) and clear
    # widget-backed keys before they are created. This guarantees the selectbox
    # and uploader start fresh on the next run.
    reset_target = st.session_state.pop('reset_target_role_select', False)
    reset_uploader = st.session_state.pop('reset_resume_uploader', False)
    if reset_target or reset_uploader:
        # Ensure selectbox shows the placeholder option on the next run by
        # setting the widget key before the selectbox is created.
        if reset_target:
            st.session_state['target_role_select'] = "-- Select Role --"
        # Remove uploader value so the file_uploader renders empty
        if reset_uploader:
            st.session_state.pop('resume_uploader', None)
        # Clear analysis values
        st.session_state.pop('target_role', None)
        st.session_state.pop('missing_skills', None)

    roles = list(role_skills_dict.keys())
    # Give the selectbox a stable key so we can reset it programmatically later
    target_role = st.selectbox(
        "Choose the role you're aiming for:",
        ["-- Select Role --"] + roles,
        help="Select the job role you want to analyze your resume against",
        key="target_role_select"
    )

    if target_role == "-- Select Role --":
        st.info("👆 Please select a target role to continue")
        st.stop()

    st.success(f"✅ Target Role: **{target_role}**")
    st.divider()

    # File Upload Card
    st.markdown("### 📄 Step 2: Upload Your Resume")
    # Use a fixed key so we can reset the uploader programmatically when the user
    # chooses to analyze another resume.
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF or DOCX format)",
        type=["pdf", "docx"],
        help="Supported formats: PDF, DOCX",
        key="resume_uploader"
    )

    def extract_text_from_pdf(file):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    def extract_text_from_docx(file):
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])

    def semantic_skill_analyzer(resume_text, required_skills, target_role):
        """
        AI Resume Intelligence Engine - Deep NLP Semantic Analysis
        
        Performs semantic understanding of resume text to detect skills,
        not just keyword matching. Understands synonyms, context, and meaning.
        
        Returns: JSON-compatible dictionary with skills_found, skills_missing, 
                 and recommended_extra_skills
        """
        
        # Skill synonyms and semantic variations database
        skill_synonyms = {
            "Python": ["python", "py", "python3", "python programming", "pythonic"],
            "Java": ["java", "java programming", "j2ee", "java ee", "core java"],
            "C++": ["c++", "cpp", "c plus plus", "cplusplus"],
            "JavaScript": ["javascript", "js", "ecmascript", "es6", "es7", "node.js", "nodejs"],
            "React": ["react", "reactjs", "react.js", "react native"],
            "Git": ["git", "github", "gitlab", "version control", "source control"],
            "SQL": ["sql", "mysql", "postgresql", "database", "rdbms", "t-sql", "pl/sql"],
            "Docker": ["docker", "containerization", "containers", "dockerfile"],
            "Kubernetes": ["kubernetes", "k8s", "container orchestration"],
            "AWS": ["aws", "amazon web services", "ec2", "s3", "lambda", "cloud computing"],
            "Python": ["python", "django", "flask", "fastapi"],
            "Machine Learning": ["machine learning", "ml", "supervised learning", "unsupervised learning", "deep learning", "neural networks"],
            "TensorFlow": ["tensorflow", "tf", "keras"],
            "PyTorch": ["pytorch", "torch"],
            "HTML": ["html", "html5", "markup"],
            "CSS": ["css", "css3", "styling", "sass", "scss", "less"],
            "TypeScript": ["typescript", "ts"],
            "Node.js": ["node.js", "nodejs", "node", "express", "express.js"],
            "APIs": ["api", "apis", "rest api", "restful", "graphql", "web services"],
            "CI/CD": ["ci/cd", "continuous integration", "continuous deployment", "jenkins", "github actions"],
            "Linux": ["linux", "unix", "ubuntu", "centos", "bash", "shell scripting"],
            "Algorithms": ["algorithms", "algorithmic", "problem solving", "competitive programming", "leetcode", "hackerrank"],
            "Data Structures": ["data structures", "arrays", "linked lists", "trees", "graphs", "hash tables"],
            "Statistics": ["statistics", "statistical analysis", "probability", "hypothesis testing"],
            "Tableau": ["tableau", "data visualization", "dashboards"],
            "PowerBI": ["powerbi", "power bi", "bi tools"],
            "Excel": ["excel", "spreadsheets", "vlookup", "pivot tables"],
            "R": ["r programming", "r language", "rstudio"],
            "UI/UX": ["ui/ux", "user interface", "user experience", "design", "figma", "sketch"],
            "Cybersecurity": ["cybersecurity", "security", "infosec", "information security"],
            "Networking": ["networking", "tcp/ip", "network protocols", "routing", "switching"],
            "Ethical Hacking": ["ethical hacking", "penetration testing", "pentest", "security testing"],
            "Security Tools": ["security tools", "nmap", "wireshark", "metasploit", "burp suite"],
            "Incident Response": ["incident response", "security incidents", "threat detection"]
        }
        
        # Related skills recommendations by role
        related_skills_by_role = {
            "Software Engineer": [
                {"skill": "Design Patterns", "reason": "Helps write maintainable and scalable code"},
                {"skill": "Testing (Unit/Integration)", "reason": "Essential for code quality and reliability"},
                {"skill": "Agile/Scrum", "reason": "Most teams use Agile methodologies"},
                {"skill": "REST APIs", "reason": "Critical for building modern applications"},
                {"skill": "Cloud Services (AWS/Azure)", "reason": "Cloud knowledge is increasingly important"}
            ],
            "Data Analyst": [
                {"skill": "Data Cleaning", "reason": "Core skill for preparing data for analysis"},
                {"skill": "A/B Testing", "reason": "Important for data-driven decision making"},
                {"skill": "Machine Learning Basics", "reason": "Adds predictive analytics capabilities"},
                {"skill": "Business Intelligence", "reason": "Helps communicate insights to stakeholders"},
                {"skill": "Big Data (Hadoop/Spark)", "reason": "Useful for handling large datasets"}
            ],
            "Frontend Developer": [
                {"skill": "Responsive Design", "reason": "Essential for mobile-friendly applications"},
                {"skill": "State Management (Redux)", "reason": "Critical for complex React applications"},
                {"skill": "CSS Preprocessors (Sass)", "reason": "Makes styling more maintainable"},
                {"skill": "Webpack/Build Tools", "reason": "Important for optimizing frontend applications"},
                {"skill": "Testing (Jest/Cypress)", "reason": "Ensures UI reliability"}
            ],
            "Backend Developer": [
                {"skill": "Microservices Architecture", "reason": "Modern approach to building scalable systems"},
                {"skill": "Message Queues (RabbitMQ/Kafka)", "reason": "Important for asynchronous processing"},
                {"skill": "Caching (Redis)", "reason": "Critical for performance optimization"},
                {"skill": "Database Design", "reason": "Core skill for efficient data storage"},
                {"skill": "Security Best Practices", "reason": "Essential for protecting applications"}
            ],
            "Machine Learning Engineer": [
                {"skill": "MLOps", "reason": "Critical for deploying ML models to production"},
                {"skill": "Computer Vision", "reason": "Expanding area in ML applications"},
                {"skill": "NLP (Natural Language Processing)", "reason": "High demand skill in ML"},
                {"skill": "Cloud ML Services", "reason": "Important for scalable ML solutions"},
                {"skill": "Model Optimization", "reason": "Essential for efficient ML systems"}
            ],
            "DevOps Engineer": [
                {"skill": "Infrastructure as Code (Terraform)", "reason": "Modern way to manage infrastructure"},
                {"skill": "Monitoring (Prometheus/Grafana)", "reason": "Critical for system reliability"},
                {"skill": "Security Automation", "reason": "Increasingly important in DevOps"},
                {"skill": "Cloud Networking", "reason": "Essential for cloud infrastructure"},
                {"skill": "Configuration Management (Ansible)", "reason": "Automates system configuration"}
            ],
            "Cybersecurity Analyst": [
                {"skill": "SIEM Tools", "reason": "Critical for security monitoring"},
                {"skill": "Cloud Security", "reason": "Growing area in cybersecurity"},
                {"skill": "Compliance (GDPR/ISO 27001)", "reason": "Important for enterprise security"},
                {"skill": "Threat Intelligence", "reason": "Proactive security approach"},
                {"skill": "Security Automation", "reason": "Efficiency in security operations"}
            ]
        }
        
        # Context patterns that boost confidence
        context_patterns = {
            "experience": r"(experience|worked|developed|built|created|implemented|designed)",
            "proficiency": r"(proficient|expert|skilled|advanced|experienced|familiar)",
            "projects": r"(project|application|system|solution|platform)",
            "duration": r"(\d+\s*(year|month|yr|mo)s?)",
        }
        
        resume_lower = resume_text.lower()
        
        # Tokenize resume for better matching
        words_in_resume = set(re.findall(r'\b\w+\b', resume_lower))
        
        skills_found = []
        skills_missing = []
        
        for skill in required_skills:
            # Get synonyms for this skill
            synonyms = skill_synonyms.get(skill, [skill.lower()])
            
            # Calculate confidence score
            confidence = 0.0
            matches = []
            
            # Check for exact and semantic matches
            for synonym in synonyms:
                synonym_lower = synonym.lower()
                
                # Exact match
                if synonym_lower in resume_lower:
                    matches.append(synonym)
                    
                    # Base confidence for finding the skill
                    confidence = max(confidence, 0.6)
                    
                    # Check for context around the skill mention
                    for context_type, pattern in context_patterns.items():
                        # Look for context within 50 characters of skill mention
                        context_search = re.search(
                            f"({pattern}).{{0,50}}{re.escape(synonym_lower)}|{re.escape(synonym_lower)}.{{0,50}}({pattern})",
                            resume_lower
                        )
                        if context_search:
                            if context_type == "experience":
                                confidence += 0.15
                            elif context_type == "proficiency":
                                confidence += 0.12
                            elif context_type == "projects":
                                confidence += 0.08
                            elif context_type == "duration":
                                confidence += 0.10
                
                # Partial fuzzy match for compound skills
                elif len(synonym_lower.split()) > 1:
                    # Check if all words in the skill are in resume
                    skill_words = set(synonym_lower.split())
                    if skill_words.issubset(words_in_resume):
                        matches.append(synonym)
                        confidence = max(confidence, 0.45)
            
            # Cap confidence at 0.95 (never 100% certain without manual review)
            confidence = min(confidence, 0.95)
            
            if confidence > 0.3:  # Threshold for considering skill as "found"
                skills_found.append({
                    "skill": skill,
                    "confidence": round(confidence, 2)
                })
            else:
                skills_missing.append(skill)
        
        # Sort found skills by confidence (highest first)
        skills_found.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Get recommended extra skills for this role
        recommended_extra_skills = related_skills_by_role.get(target_role, [])
        
        # Build the JSON response
        analysis_result = {
            "skills_found": skills_found,
            "skills_missing": skills_missing,
            "recommended_extra_skills": recommended_extra_skills
        }
        
        return analysis_result

    def extract_skills_from_resume(text, role_skills):
        """Legacy function - kept for backward compatibility"""
        text_lower = text.lower()
        found = [skill for skill in role_skills if skill.lower() in text_lower]
        missing = [skill for skill in role_skills if skill.lower() not in text_lower]
        return found, missing

    if uploaded_file:
        with st.spinner("🔍 Performing deep NLP semantic analysis on your resume..."):
            # Extract text based on file type
            if uploaded_file.type == "application/pdf":
                text = extract_text_from_pdf(uploaded_file)
            else:
                text = extract_text_from_docx(uploaded_file)

            role_skills = role_skills_dict[target_role]
            
            # Use the semantic analyzer for deep NLP analysis
            nlp_analysis = semantic_skill_analyzer(text, role_skills, target_role)
            
            # Extract results from NLP analysis
            skills_found_with_confidence = nlp_analysis['skills_found']
            missing_skills = nlp_analysis['skills_missing']
            recommended_skills = nlp_analysis['recommended_extra_skills']
            
            # For backward compatibility with UI
            found_skills = [s['skill'] for s in skills_found_with_confidence]

            # Store in session state for Skill Hub
            st.session_state['missing_skills'] = missing_skills
            st.session_state['target_role'] = target_role
            st.session_state['nlp_analysis'] = nlp_analysis  # Store full analysis

            st.success("✅ Resume analyzed successfully with AI-powered semantic understanding!")
            st.divider()

            # Score Card
            score = int((len(found_skills) / len(role_skills)) * 100)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h2 style="margin:0;">{score}%</h2>
                    <p style="margin:5px 0 0 0;">Skill Match Score</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h2 style="margin:0;">{len(found_skills)}</h2>
                    <p style="margin:5px 0 0 0;">Skills Found</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h2 style="margin:0;">{len(missing_skills)}</h2>
                    <p style="margin:5px 0 0 0;">Skills to Learn</p>
                </div>
                """, unsafe_allow_html=True)

            st.divider()

            # Skills Analysis
            col_left, col_right = st.columns(2)

            with col_left:
                st.markdown("### ✅ Skills Detected in Your Resume")
                if found_skills:
                    skills_html = "".join([f'<span class="skill-badge-present">{skill}</span>' for skill in found_skills])
                    st.markdown(skills_html, unsafe_allow_html=True)
                else:
                    st.warning("No matching skills detected in your resume.")

            with col_right:
                st.markdown("### ❌ Skills You Should Learn")
                if missing_skills:
                    skills_html = "".join([f'<span class="skill-badge-missing">{skill}</span>' for skill in missing_skills])
                    st.markdown(skills_html, unsafe_allow_html=True)
                    st.info("💡 Check out the **Skill Hub** page for learning resources!")
                else:
                    st.success("🎉 Great! You have all required skills!")

            st.divider()

            # Visualization
            st.markdown("### 📊 Visual Analysis")
            
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                # Progress bar
                st.markdown("#### Skill Coverage")
                st.progress(score / 100)
                st.caption(f"You have {len(found_skills)} out of {len(role_skills)} required skills")
            
            with col_chart2:
                # Pie chart
                pie_data = pd.DataFrame({
                    "Status": ["Skills Present", "Skills Missing"],
                    "Count": [len(found_skills), len(missing_skills)]
                })
                fig = px.pie(
                    pie_data,
                    names='Status',
                    values='Count',
                    color='Status',
                    color_discrete_map={'Skills Present': '#11998e', 'Skills Missing': '#ee0979'},
                    hole=0.4
                )
                fig.update_layout(
                    showlegend=True,
                    height=300,
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                st.plotly_chart(fig, use_container_width=True)

            st.divider()

            # Advanced NLP Analysis Section
            st.markdown("### 🤖 AI Semantic Analysis Details")
            
            with st.expander("🎯 Confidence Scores for Detected Skills"):
                st.markdown("**AI confidence levels for each detected skill:**")
                if skills_found_with_confidence:
                    for skill_data in skills_found_with_confidence:
                        confidence_pct = int(skill_data['confidence'] * 100)

                        
                        st.progress(skill_data['confidence'])
                        st.caption(f"**{skill_data['skill']}**: {confidence_pct}% confidence")
                else:
                    st.info("No skills detected in resume.")
            
            with st.expander("💡 Recommended Additional Skills"):
                st.markdown(f"**Skills that would strengthen your profile for {target_role}:**")
                if recommended_skills:
                    for rec in recommended_skills:
                        st.markdown(f"""
                        <div style="background: #f0f9ff; padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 4px solid #2563eb;">
                            <strong style="color: #1e40af;">🔹 {rec['skill']}</strong><br>
                            <span style="color: #64748b; font-size: 14px;">{rec['reason']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No additional skill recommendations available.")
           

            st.divider()

            # Resume Preview
            with st.expander("📄 View Resume Text Preview"):
                st.text_area("Extracted Resume Text", text, height=400, disabled=True)

            # Action Buttons
            st.divider()
            col_empty, col_btn, col_empty2 = st.columns([1, 1, 1])
            
            with col_btn:
                if st.button("🔄 Analyze Another Resume", use_container_width=True):
                    # Request a reset by setting flags; actual widget keys will be
                    # cleared at the top of the script before widgets are created.
                    st.session_state['reset_resume_uploader'] = True
                    st.session_state['reset_target_role_select'] = True
                    # Clear analysis results
                    st.session_state.pop('missing_skills', None)
                    st.session_state.pop('target_role', None)
                    # Force a rerun so the cleared state takes effect immediately
                    safe_rerun()

    else:
        # Empty state
        st.markdown("""
        <div class="card" style="text-align: center; padding: 3rem;">
            <h2>📂 No Resume Uploaded Yet</h2>
            <p style="font-size: 18px; color: #666;">
                Upload your resume above to get started with the analysis.<br>
                We'll help you identify your strengths and areas for improvement!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💡 What We Analyze:")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **🎯 Skill Matching**
            - Detect skills in your resume
            - Compare with target role
            - Calculate match percentage
            """)
        
        with col2:
            st.markdown("""
            **📊 Visual Reports**
            - Skill coverage charts
            - Gap analysis
            - Progress tracking
            """)
        
        with col3:
            st.markdown("""
            **🚀 Recommendations**
            - Identify missing skills
            - Get learning suggestions
            - Improve your profile
            """)