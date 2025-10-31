import streamlit as st
from modules import llm, db, helpers
import json
import re

helpers.set_page_styling()
helpers.hide_streamlit_ui() 

LEARNING_PATH_PAGE = "pages/3_Learning_Path.py"
PROFILE_PAGE = "pages/5_Profile.py"

st.set_page_config(page_title="Assignments", page_icon="📝", layout="centered")
if 'user_id' not in st.session_state or 'selected_subject' not in st.session_state:
    st.page_link("pages/0_Login.py", label="Go to Login", icon="🔑")
    st.stop()

subject = st.session_state['selected_subject']
st.title(f"📝 Final Assignments for {subject}")

progress = db.get_or_create_progress(st.session_state['user_id'], subject)

if progress['status'] == 'completed':
    st.success(f"You have already mastered the {subject} module!")
    st.metric(label="Your Final Score", value=f"{progress['assignment_score']}%")
    st.page_link(PROFILE_PAGE, label="View Your Profile", icon="👤")
    st.stop()

if progress['assignment_score'] is not None and progress['status'] == 'learning':
    st.warning(f"Your previous score was {progress['assignment_score']}%. Review the lessons and try again when you're ready.")
    if st.button("Try a New Assignment", type="primary"):
        db.update_progress(st.session_state['user_id'], subject, status='assessing')
        st.rerun()
    st.page_link(LEARNING_PATH_PAGE, label="Go to Review Mode", icon="📖")
    st.stop()

if progress['status'] != 'assessing':
    st.info("You must complete the learning path before taking the final assignment.")
    st.page_link(LEARNING_PATH_PAGE, label="Back to Learning Path")
    st.stop()

if 'assignment_questions' not in st.session_state:
    if st.button("Generate Your Assignment", type="primary", use_container_width=True):
        with st.spinner("Generating your assignment..."):
            # Full, detailed, few-shot prompt
            prompt = f"""
            Generate 3 diverse MULTIPLE-CHOICE questions for a {subject} assignment, covering beginner, intermediate, and advanced topics.

            **CRITICAL INSTRUCTIONS:**
            1. All questions MUST be multiple-choice with 4 options.
            2. If a question refers to a code snippet, that snippet MUST be embedded directly within the 'question' string using Markdown code fences (```c ... ```).
            3. Return a SINGLE, valid JSON array where each element is an object with keys "question", "options", "correct_answer", and "related_topic".
            4. Provide ONLY the JSON array, with no other text.

            **EXAMPLE of a perfect response format:**
            [
              {{
                "question": "What is the output of the following C code?\\n```c\\n#include <stdio.h>\\nint main() {{ int x = 10; printf(\\"%d\\", x++); return 0; }}\\n```",
                "options": ["10", "11", "12", "Compilation Error"],
                "correct_answer": "10",
                "related_topic": "Operators"
              }},
              {{
                "question": "Which function is used to allocate memory for an array in C?",
                "options": ["malloc", "calloc", "realloc", "free"],
                "correct_answer": "calloc",
                "related_topic": "Memory Management"
              }}
            ]
            """
            response = llm.ask_ai(prompt, language=subject)
            try:
                json_match = re.search(r'\[.*\]', response, re.DOTALL)
                if json_match:
                    json_string = json_match.group(0)
                    st.session_state.assignment_questions = json.loads(json_string)
                    st.rerun()
                else:
                    st.error("Could not find a valid JSON array in the AI's response."); st.code(response)
            except json.JSONDecodeError:
                st.error("Failed to decode the JSON from the AI's response."); st.code(response)
    st.stop()

questions = st.session_state.assignment_questions
user_answers = {}

st.info("Answer the following questions to complete your assessment.")
with st.form("assignment_form"):
    for i, q in enumerate(questions):
        if isinstance(q, dict) and all(key in q for key in ['question', 'options', 'correct_answer', 'related_topic']):
             st.markdown(f"**Question {i+1}:** {q['question']}")
             user_answers[i] = st.radio("Options:", q['options'], key=f"assign_{i}", index=None)
        else:
            st.warning(f"Question {i+1} is not formatted correctly and will be skipped."); user_answers[i] = None
    submitted = st.form_submit_button("Submit Final Assignment")

if submitted:
    score = 0
    wrong_answers_topics = []
    valid_questions = [q for i, q in enumerate(questions) if user_answers[i] is not None]
    for i, q in enumerate(valid_questions):
        if user_answers[i] == q['correct_answer']:
            score += 1
        else: wrong_answers_topics.append(q['related_topic'])
    score_percent = int((score / len(valid_questions)) * 100) if valid_questions else 0
    if score_percent >= 80:
        st.success(f"### Congratulations! You passed with a score of {score_percent}%.")
        db.update_progress(st.session_state['user_id'], subject, status='completed', score=score_percent)
        st.page_link(PROFILE_PAGE, label="View Your Profile")
    else:
        st.error(f"### Your score is {score_percent}%. You need more practice.")
        db.update_progress(st.session_state['user_id'], subject, status='learning', score=score_percent)
        if wrong_answers_topics:
            with st.spinner("Analyzing your results..."):
                topics_str = ", ".join(set(wrong_answers_topics))
                feedback_prompt = f"A student needs to improve their understanding of these {subject} topics: {topics_str}. Briefly and encouragingly explain what they should focus on when reviewing these topics."
                feedback = llm.ask_ai(feedback_prompt, language=subject)
                st.warning("💡 AI Tutor Feedback: What to Focus On"); st.info(feedback)
        st.page_link(LEARNING_PATH_PAGE, label="Go to Review Mode", icon="📖")
    if 'assignment_questions' in st.session_state: del st.session_state.assignment_questions