import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.interview_engine import get_interview_questions, evaluate_interview_answer, create_interview_report


def main():
    if not st.session_state.get('logged_in', False):
        st.warning("Please login first to access the mock interview.")
        st.stop()

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .interview-container {
        max-width: 900px;
        margin: 0 auto;
    }
    
    .setup-section {
        background: transparent;
        padding: 10px 40px 40px 40px;
        border-radius: 16px;
        box-shadow: none;
        margin-bottom: 28px;
        border: none;
    }
    
    .setup-title {
        color: #0f172a;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 28px;
        padding-bottom: 16px;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .setup-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }
    
    .setup-box {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .setup-box:hover {
        border-color: #2563eb;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    
    .setup-box.selected {
        border-color: #2563eb;
        background: linear-gradient(135deg, #f0f9ff 0%, #f9f5ff 100%);
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.3);
    }
    
    .setup-box-title {
        color: #1e293b;
        font-size: 15px;
        font-weight: 600;
        margin: 0;
    }
    
    .setup-box-desc {
        color: #64748b;
        font-size: 13px;
        margin: 8px 0 0 0;
    }
    
    .question-card {
        background: white;
        border-left: 5px solid #2563eb;
        border-radius: 12px;
        padding: 32px;
        margin: 28px 0;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid #e2e8f0;
    }
    
    .question-number {
        color: #64748b;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }
    
    .question-text {
        color: #0f172a;
        font-size: 20px;
        line-height: 1.6;
        margin: 0;
        font-weight: 600;
    }
    
    .answer-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
        border-left: 5px solid #10b981;
        border-radius: 12px;
        padding: 28px;
        margin: 20px 0 28px 0;
        box-shadow: 0 1px 8px rgba(0, 0, 0, 0.04);
        border: 1px solid #d1fae5;
    }
    
    .answer-label {
        color: #0f172a;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px;
        display: block;
    }
    
    .answer-text {
        color: #1e293b;
        font-size: 15px;
        line-height: 1.8;
        margin: 0;
        white-space: pre-wrap;
        word-break: break-word;
    }
    
    .feedback-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fef08a 100%);
        border-left: 5px solid #f59e0b;
        border-radius: 12px;
        padding: 28px;
        margin: 20px 0;
        box-shadow: 0 1px 8px rgba(0, 0, 0, 0.04);
        border: 1px solid #fcd34d;
    }
    
    .feedback-label {
        color: #78350f;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 12px;
        display: block;
    }
    
    .feedback-text {
        color: #451a03;
        font-size: 15px;
        line-height: 1.8;
        margin: 0;
    }
    
    .score-label {
        color: #78350f;
        font-size: 12px;
        font-weight: 600;
        margin-top: 16px;
        padding-top: 16px;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    .model-answer-card {
        background: linear-gradient(135deg, #f3f4f6 0%, #ffffff 100%);
        border-left: 5px solid #6366f1;
        border-radius: 12px;
        padding: 28px;
        margin: 20px 0;
        box-shadow: 0 1px 8px rgba(0, 0, 0, 0.04);
        border: 1px solid #e5e7eb;
    }
    
    .stTextArea textarea {
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-size: 15px !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1) !important;
    }
    
    .stButton button {
        font-size: 15px !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    }
    
    .analysis-container {
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .completion-header {
        background: white;
        padding: 40px;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 28px;
        text-align: center;
        border: 1px solid #e2e8f0;
    }
    
    .completion-title {
        color: #0f172a;
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 12px;
    }
    
    .completion-desc {
        color: #64748b;
        font-size: 16px;
    }
    
    .progress-bar {
        height: 8px;
        background: #e2e8f0;
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 20px;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%);
        transition: width 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="interview-container">', unsafe_allow_html=True)

    if 'interview_started' not in st.session_state:
        st.session_state.interview_started = False
    if 'interview_questions' not in st.session_state:
        st.session_state.interview_questions = []
    if 'interview_answers' not in st.session_state:
        st.session_state.interview_answers = {}
    if 'interview_results' not in st.session_state:
        st.session_state.interview_results = []
    if 'interview_completed' not in st.session_state:
        st.session_state.interview_completed = False
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'interview_topic' not in st.session_state:
        st.session_state.interview_topic = ""
    if 'interview_difficulty' not in st.session_state:
        st.session_state.interview_difficulty = ""
    if 'answer_submitted' not in st.session_state:
        st.session_state.answer_submitted = False

    if not st.session_state.interview_started:
        st.markdown('<h1 style="color: #0f172a; margin-bottom: 8px;">Mock Interview</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color: #64748b; font-size: 16px; margin: 0 0 8px 0;">Practice interview questions and receive AI-powered feedback</p>', unsafe_allow_html=True)

        st.markdown('<div class="setup-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="setup-title" style="margin-top: 0;">Select Interview Topic</h2>', unsafe_allow_html=True)

        topics = [
            {"label": "Python", "name": "Python"},
            {"label": "Data Structures & Algorithms", "name": "DSA"},
            {"label": "Web Development", "name": "Web Development"},
            {"label": "Database Management", "name": "DBMS"}
        ]

        st.markdown('<div class="setup-grid">', unsafe_allow_html=True)
        cols = st.columns(4)
        for idx, topic in enumerate(topics):
            with cols[idx]:
                is_selected = st.session_state.interview_topic == topic["name"]
                st.markdown(f"""
                <div class="{'setup-box selected' if is_selected else 'setup-box'}">
                    <p class="setup-box-title">{topic['label']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Select {topic['name']}", key=f"topic_{topic['name']}", use_container_width=True):
                    st.session_state.interview_topic = topic["name"]
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<h2 class="setup-title" style="margin-top: 28px;">Select Difficulty Level</h2>', unsafe_allow_html=True)

        difficulties = [
            {"label": "Easy", "name": "Easy"},
            {"label": "Medium", "name": "Medium"},
            {"label": "Hard", "name": "Hard"}
        ]

        st.markdown('<div class="setup-grid">', unsafe_allow_html=True)
        cols = st.columns(3)
        for idx, diff in enumerate(difficulties):
            with cols[idx]:
                is_selected = st.session_state.interview_difficulty == diff["name"]
                st.markdown(f"""
                <div class="{'setup-box selected' if is_selected else 'setup-box'}">
                    <p class="setup-box-title">{diff['label']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Select {diff['name']}", key=f"diff_{diff['name']}", use_container_width=True):
                    st.session_state.interview_difficulty = diff["name"]
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.interview_topic and st.session_state.interview_difficulty:
            if st.button("Start Interview", type="primary", use_container_width=True):
                questions = get_interview_questions(st.session_state.interview_topic, st.session_state.interview_difficulty, 5)
                if questions:
                    st.session_state.interview_questions = questions
                    st.session_state.interview_started = True
                    st.session_state.current_question_index = 0
                    st.session_state.interview_answers = {}
                    st.session_state.answer_submitted = False
                    st.rerun()

    elif st.session_state.interview_started and not st.session_state.interview_completed:
        if st.session_state.current_question_index < len(st.session_state.interview_questions):
            current_q = st.session_state.interview_questions[st.session_state.current_question_index]
            progress = (st.session_state.current_question_index + 1) / len(st.session_state.interview_questions)

            st.markdown(f"""
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress * 100}%"></div>
            </div>
            <p style="color: #64748b; font-size: 14px; margin: 0 0 28px 0;">
                Question {st.session_state.current_question_index + 1} of {len(st.session_state.interview_questions)}
            </p>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="question-card">
                <div class="question-number">Question {st.session_state.current_question_index + 1}</div>
                <p class="question-text">{current_q['question']}</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("💡 View Hint", use_container_width=True):
                    st.info(f"**Hint:** {current_q['hint']}")

            current_answer = st.session_state.interview_answers.get(st.session_state.current_question_index, "")
            user_answer = st.text_area(
                "Your Answer",
                value=current_answer,
                height=200,
                placeholder="Type your answer here...",
                label_visibility="collapsed"
            )
            st.session_state.interview_answers[st.session_state.current_question_index] = user_answer

            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("✓ Submit Answer", type="primary", use_container_width=True):
                    if not st.session_state.answer_submitted:
                        user_input = user_answer if user_answer.strip() else "No answer provided"
                        expected_points = current_q.get('expected_points', [])
                        evaluation = evaluate_interview_answer(
                            current_q['question'],
                            user_input,
                            expected_points
                        )

                        st.session_state.interview_results.append({
                            'question': current_q['question'],
                            'user_answer': user_answer,
                            'expected_points': expected_points,
                            'evaluation': evaluation
                        })
                        
                        st.session_state.answer_submitted = True
                        st.rerun()

            if st.session_state.answer_submitted:
                result = st.session_state.interview_results[-1]
                st.markdown(f"""
                <div class="feedback-card">
                    <span class="feedback-label">Feedback</span>
                    <p class="feedback-text">{result['evaluation']['feedback']}</p>
                    <div class="score-label">Score: {result['evaluation']['score']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("→ Next Question", use_container_width=True, key="next_q"):
                        st.session_state.current_question_index += 1
                        st.session_state.answer_submitted = False
                        if st.session_state.current_question_index >= len(st.session_state.interview_questions):
                            st.session_state.interview_completed = True
                        st.rerun()
                
                with col2:
                    if st.button("⏹ End Interview", use_container_width=True):
                        st.session_state.interview_completed = True
                        st.rerun()
            else:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("⊘ Skip Question", use_container_width=True):
                        st.session_state.current_question_index += 1
                        st.session_state.answer_submitted = False
                        if st.session_state.current_question_index >= len(st.session_state.interview_questions):
                            st.session_state.interview_completed = True
                        st.rerun()
                
                with col2:
                    if st.button("⏹ End Interview", use_container_width=True):
                        st.session_state.interview_completed = True
                        st.rerun()

    elif st.session_state.interview_completed:
        st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="completion-header">
            <h1 class="completion-title">Interview Complete ✓</h1>
            <p class="completion-desc">Here's your detailed performance analysis</p>
        </div>
        """, unsafe_allow_html=True)

        processed_results = []
        for result in st.session_state.interview_results:
            processed_results.append({
                'score': result['evaluation'].get('score', 0),
                'strengths': result['evaluation'].get('strengths', []),
                'weaknesses': result['evaluation'].get('weaknesses', [])
            })
        
        report = create_interview_report(processed_results)

        st.markdown(f"""
        <div class="question-card" style="border-left-color: #8b5cf6; background: linear-gradient(135deg, #f5f3ff 0%, #ffffff 100%);">
            <div class="question-number">Overall Performance</div>
            <p class="question-text" style="color: #8b5cf6; margin-bottom: 12px;">{report['performance']}</p>
            <p style="color: #6b21a8; font-size: 15px; line-height: 1.8; margin: 0;">{report['percentage']:.1f}% - {report['remarks']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h2 style='color: #0f172a; margin-top: 40px; margin-bottom: 28px;'>Detailed Results</h2>", unsafe_allow_html=True)
        
        for idx, result in enumerate(st.session_state.interview_results):
            # Question header
            st.markdown(f"""
            <div class="question-card">
                <div class="question-number">Question {idx + 1}</div>
                <p class="question-text">{result['question']}</p>
            </div>
            """, unsafe_allow_html=True)

            # Side-by-side comparison: User Answer (Left) and Model Answer (Right)
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="answer-card" style="height: 100%; min-height: 200px;">
                    <span class="answer-label">Your Answer</span>
                    <p class="answer-text">{result['user_answer'] if result['user_answer'].strip() else '(No answer provided)'}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                expected_pts = result.get('expected_points', [])
                if expected_pts:
                    def format_model_answer(points):
                        if not points:
                            return "No model answer available"
                        
                        if len(points) == 1:
                            return f"The key point to understand is: {points[0]}."
                        
                        intro = "A comprehensive answer should cover the following points: "
                        points_intro = points[0]
                        
                        if len(points) == 2:
                            formatted = f"{intro} {points_intro}, and {points[1]}. These concepts work together to provide a complete understanding of the topic."
                        else:
                            middle_points = ", ".join(points[1:-1])
                            formatted = f"{intro} {points_intro}, {middle_points}, and {points[-1]}. Understanding all these aspects is crucial for a thorough response."
                        
                        return formatted
                    
                    model_answer_text = format_model_answer(expected_pts)
                    st.markdown(f"""
                    <div class="model-answer-card" style="height: 100%; min-height: 200px;">
                        <span class="answer-label">Model's Ideal Answer</span>
                        <p class="answer-text">{model_answer_text}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="model-answer-card" style="height: 100%; min-height: 200px;">
                        <span class="answer-label">Model's Ideal Answer</span>
                        <p class="answer-text">No model answer available</p>
                    </div>
                    """, unsafe_allow_html=True)

            # Feedback section below the side-by-side comparison
            st.markdown(f"""
            <div class="feedback-card">
                <span class="feedback-label">AI Feedback & Evaluation</span>
                <p class="feedback-text">{result['evaluation']['feedback']}</p>
                <div class="score-label">Score: {result['evaluation']['score']}/10</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("↻ Start New Interview", type="primary", use_container_width=True):
                st.session_state.interview_started = False
                st.session_state.interview_questions = []
                st.session_state.interview_answers = {}
                st.session_state.interview_results = []
                st.session_state.interview_completed = False
                st.session_state.current_question_index = 0
                st.session_state.interview_topic = ""
                st.session_state.interview_difficulty = ""
                st.session_state.answer_submitted = False
                st.rerun()

        with col2:
            if st.button("→ Go to Dashboard", use_container_width=True):
                st.switch_page("pages/chatbot.py")

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
