import streamlit as st
import re

# ------------------- Helper Functions -------------------

def extract_youtube_id(url):
    """Extract YouTube video ID from a YouTube URL."""
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})(?:\?|&|$)"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def get_thumbnail(link):
    """Return appropriate thumbnail URL for YouTube or a website."""
    video_id = extract_youtube_id(link)
    if "youtube.com" in link and video_id:
        return f"https://img.youtube.com/vi/{video_id}/0.jpg"
    else:
        # Use thum.io for website previews
        return f"https://image.thum.io/get/width/600/crop/600/noanimate/{link}"


def display_resource_grid(resources):
    """Display resource thumbnails in responsive 3-column grid."""
    cols = st.columns(3)
    idx = 0
    for title, link in resources.items():
        thumbnail_url = get_thumbnail(link)
        col = cols[idx % 3]
        with col:
            st.markdown(
                f"""
                <div style="text-align:center; margin-bottom:25px;">
                    <a href="{link}" target="_blank">
                        <img src="{thumbnail_url}" 
                             alt="{title}" 
                             style="width:100%; border-radius:12px; box-shadow:0 2px 10px rgba(0,0,0,0.2); transition:transform 0.2s;"
                             onmouseover="this.style.transform='scale(1.05)'" 
                             onmouseout="this.style.transform='scale(1)'">
                    </a>
                    <p style="margin-top:8px;">
                        <a href="{link}" target="_blank" 
                           style="text-decoration:none; color:#2E8BFF; font-weight:600;">
                           {title}
                        </a>
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        idx += 1


# ------------------- Main App -------------------

def main():
    # Check if user is logged in
    if not st.session_state.get('logged_in', False):
        st.warning("🔒 Please login first to access this page.")
        st.stop()
    
    # Modern UI Styling
    st.markdown("""
    <style>
    .skill-section {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    .skill-section:hover {
        box-shadow: 0 12px 48px rgba(0,0,0,0.15);
        transform: translateX(5px);
    }
    .resource-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 12px;
        margin: 10px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    .resource-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    .info-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(240, 147, 251, 0.3);
        margin: 2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("⚡ Skill Hub - Learning Resources")
    st.markdown("### Curated learning paths to boost your career")
    st.divider()

    if "missing_skills" not in st.session_state or "target_role" not in st.session_state:
        st.markdown("""
        <div class="info-card">
            <h2>📚 Get Started</h2>
            <p style="font-size: 18px;">
                Upload your resume in the <strong>Upload & Analyze</strong> page first<br>
                to get personalized skill recommendations!
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    target_role = st.session_state["target_role"]

    role_skills_dict = {
        "Software Engineer": ["Python", "Java", "C++", "Git", "Algorithms", "Data Structures", "SQL"],
        "Data Analyst": ["Python", "SQL", "R", "Excel", "Statistics", "Tableau", "PowerBI"],
        "Frontend Developer": ["HTML", "CSS", "JavaScript", "React", "Git", "UI/UX", "TypeScript"],
        "Backend Developer": ["Python", "Java", "Node.js", "SQL", "APIs", "Docker", "Git"],
        "Machine Learning Engineer": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "Data Structures", "SQL"],
        "DevOps Engineer": ["Linux", "Docker", "Kubernetes", "AWS", "CI/CD", "Git", "Python"],
        "Cybersecurity Analyst": ["Cybersecurity", "Networking", "Linux", "Python", "Ethical Hacking", "Incident Response"],
    }

    # 25+ skill resources
    free_resources = {
        "Python": {
            "Python Advanced Course": "https://www.youtube.com/watch?v=t1fQBD4B7xk",
            "Python Full Course": "https://www.youtube.com/watch?v=rfscVS0vtbw"
        },
        "SQL": {
            "SQL Full Course for Beginners": "https://www.youtube.com/watch?v=HXV3zeQKqGY",
            "Advanced SQL Tutorial": "https://www.youtube.com/watch?v=9Pzj7Aj25lw"
        },
        "Git": {
            "Git and GitHub Crash Course for Beginners": "https://www.youtube.com/watch?v=RGOj5yH7evk",
            "Advanced Git Tutorial": "https://www.youtube.com/watch?v=qsTthZi23VE"
        },
        "Linux": {
            "Linux Full Course for Beginners": "https://www.youtube.com/watch?v=v392lEyM29A",
            "Linux Command Line Crash Course": "https://www.youtube.com/watch?v=oxuRxtrO2Ag"
        },
        "Data Structures": {
            "Data Structures and Algorithms Full Course": "https://www.youtube.com/watch?v=8hly31xKli0",
            "Free Full Course: Data Structures & Algorithms": "https://www.youtube.com/watch?v=CBYHwZcbD-s"
        },
        "Algorithms": {
            "Introduction to Algorithms": "https://www.youtube.com/watch?v=HtSuA80QTyo",
            "Algorithms & Data Structures Full Course": "https://www.youtube.com/watch?v=8hly31xKli0"
        },
        "Statistics": {
            "Statistics Full Course": "https://www.youtube.com/watch?v=xxpc-HPKN28",
            "Statistics Crash Course": "https://www.youtube.com/watch?v=Vfo5le26IhY"
        },
        "C": {
            "C Programming Full Course": "https://www.youtube.com/watch?v=KJgsSFOSQv0",
            "C Programming Crash Course": "https://www.youtube.com/watch?v=86cQqHFyauc"
        },
        "Machine Learning": {
            "Machine Learning Full Course": "https://www.youtube.com/watch?v=GwIo3gDZCVQ",
            "Machine Learning Crash Course": "https://www.youtube.com/watch?v=ukzFI9rgwfU"
        },
        "React": {
            "React JS Full Course": "https://www.youtube.com/watch?v=bMknfKXIFA8",
            "React Crash Course 2024": "https://www.youtube.com/watch?v=w7ejDZ8SWv8"
        },
        "Docker": {
            "Docker Full Course": "https://www.youtube.com/watch?v=fqMOX6JJhGo",
            "Docker Crash Course": "https://www.youtube.com/watch?v=3c-iBn73dDE"
        },
        "Kubernetes": {
            "Kubernetes Full Course": "https://www.youtube.com/watch?v=X48VuDVv0do",
            "Kubernetes Crash Course": "https://www.youtube.com/watch?v=d6WC5n9G_sM"
        },
        "Java": {
            "Java Full Course": "https://www.youtube.com/watch?v=xk4_1vDrzzo",
            "Java Tutorial for Beginners": "https://www.youtube.com/watch?v=grEKMHGYyns"
        },
        "C++": {
            "C++ Full Course": "https://www.youtube.com/watch?v=vLnPwxZdW4Y",
            "C++ Programming Tutorial": "https://www.youtube.com/watch?v=-TkoO8Z07hI"
        },
        "Node.js": {
            "Node.js Full Course": "https://www.youtube.com/watch?v=RLtyhwFtXQA",
            "Node.js Crash Course": "https://www.youtube.com/watch?v=fBNz5xF-Kx4"
        },
        "HTML": {
            "HTML Full Course": "https://www.youtube.com/watch?v=pQN-pnXPaVg",
            "HTML Crash Course": "https://www.youtube.com/watch?v=UB1O30fR-EE"
        },
        "CSS": {
            "CSS Full Course": "https://www.youtube.com/watch?v=ieTHC78giGQ",
            "CSS Crash Course": "https://www.youtube.com/watch?v=yfoY53QXEnI"
        },
        "JavaScript": {
            "JavaScript Full Course": "https://www.youtube.com/watch?v=PkZNo7MFNFg",
            "JavaScript Crash Course": "https://www.youtube.com/watch?v=hdI2bqOjy3c"
        },
        "R": {
            "R Programming Full Course": "https://www.youtube.com/watch?v=_V8eKsto3Ug",
            "R Programming Tutorial": "https://www.youtube.com/watch?v=_V8eKsto3Ug"
        },
        "Excel": {
            "Excel Full Course": "https://www.youtube.com/watch?v=Vl0H-qTclOg",
            "Excel Tutorial for Beginners": "https://www.youtube.com/watch?v=Vl0H-qTclOg"
        },
        "Tableau": {
            "Tableau": "https://www.youtube.com/watch?v=TPMlZxRRaBQ",
            "Tableau Tutorial for Beginners": "https://www.youtube.com/watch?v=aHaOIvR00So"
        },
        "PowerBI": {
            "Power BI": "https://www.youtube.com/watch?v=AGrl-H87pRU",
            "Power BI Full Course": "https://www.youtube.com/watch?v=ag9E8Nl5G0I"
        },
        "APIs": {
            "REST API Full Course": "https://www.youtube.com/watch?v=7YcW25PHnAA",
            "API Development with Node.js": "https://www.youtube.com/watch?v=l8WPWK9mS5M"
        },
        "CI/CD": {
            "CI/CD Full Course": "https://www.youtube.com/watch?v=R8_veQiYBjI",
            "DevOps CI/CD Crash Course": "https://www.youtube.com/watch?v=scEDHsr3APg"
        },
        "Cybersecurity": {
            "Cybersecurity Full Course": "https://www.youtube.com/watch?v=xKaQHBbtaX0",
            "Cybersecurity for Beginners": "https://www.youtube.com/watch?v=0uvWRwLs5Zo"
        },
        "Networking": {
            "Networking Full Course": "https://www.youtube.com/watch?v=qiQR5rTSshw",
            "Computer Networking Crash Course": "https://www.youtube.com/watch?v=qiQR5rTSshw"
        },
        "Ethical Hacking": {
            "Ethical Hacking Full Course": "https://www.youtube.com/watch?v=3Kq1MIfTWCE",
            "Ethical Hacking for Beginners": "https://www.youtube.com/watch?v=fNzpcB7ODxQ"
        },
        "UI/UX": {
            "UI/UX Design Fundamentals": "https://www.youtube.com/watch?v=c9Wg6Cb_YlU",
            "User Experience Design Basics": "https://www.youtube.com/watch?v=jwCmIBJ8Jtc"
        },
        "TypeScript": {
            "TypeScript Full Course": "https://www.youtube.com/watch?v=30LWjhZzg50",
            "TypeScript Crash Course": "https://www.youtube.com/watch?v=BCg4U1FzODs"
        },
        "Incident Response": {
            "Incident Response Tutorial": "https://www.youtube.com/watch?v=2BOOl8_nwjQ",
            "Digital Forensics and Incident Response": "https://www.youtube.com/watch?v=mKUZx1z9dxo"
        },
        "TensorFlow": {
            "TensorFlow Full Course": "https://www.youtube.com/watch?v=Q5_knerjMS0",
            "TensorFlow Crash Course for Beginners": "https://www.youtube.com/watch?v=gWvwu7qLjJs"
        },
        "PyTorch": {
            "PyTorch for Deep Learning & Machine Learning": "https://www.youtube.com/watch?v=V_xro1bcAuA",
            "Deep Learning With PyTorch": "https://www.youtube.com/watch?v=c36lUUr864M"
        },
        "AWS": {
            "AWS Full Course 2025 | AWS Cloud Computing Tutorial for Beginners": "https://www.youtube.com/watch?v=UmQnenLf_Cs",
            "AWS Cloud Engineer Full Course for Beginners": "https://www.youtube.com/watch?v=j_StCjwpfmk"
        }
    }

    all_skills = role_skills_dict.get(target_role, [])
    st.subheader(f"📚 Learning Resources for {target_role}")

    for skill in all_skills:
        st.markdown(f"### 🏷 {skill}")
        if skill in free_resources:
            display_resource_grid(free_resources[skill])
        else:
            st.markdown(f"- [YouTube Tutorials](https://www.youtube.com/results?search_query={skill}+tutorial)")
        st.divider()


if __name__ == "__main__":
    main()
