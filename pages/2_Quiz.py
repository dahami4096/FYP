import streamlit as st
import json
import random
from modules import llm, db, helpers

helpers.set_page_styling()

st.set_page_config(page_title="Placement Quiz", page_icon="🧠", layout="centered")
if 'user_id' not in st.session_state or 'selected_subject' not in st.session_state:
    st.page_link("pages/0_Login.py", label="Go to Login", icon="🔑")
    st.stop()

subject = st.session_state['selected_subject']
progress = db.get_or_create_progress(st.session_state['user_id'], subject)

# Page Guard
if progress['level'] is not None:
    st.info("You have already completed the placement quiz for this subject.")
    if progress['status'] == 'learning':
        st.page_link("pages/3_Learning_Path.py", label="Continue Your Learning Path", icon="📚")
    elif progress['status'] == 'assessing':
        st.page_link("pages/4_Assignments.py", label="Go to Your Assignments", icon="📝")
    else: # 'completed'
        st.page_link("pages/5_Profile.py", label="View Your Progress on Your Profile", icon="👤")
    st.stop()

st.title(f"🧠 {subject} Placement Quiz")
st.write("This quiz will determine your starting point in our curriculum.")

try:
    with open(f"curriculum/{subject.lower()}_curriculum.json") as f:
        curriculum = json.load(f)['full_path']
except FileNotFoundError:
    st.error(f"Curriculum for {subject} not found.")
    st.stop()

def get_start_index(level):
    for i, topic in enumerate(curriculum):
        if topic['level'] == level:
            return i
    return 0

def generate_question(difficulty, programming_language):
    # Full, detailed prompt
    prompt = f"""
    Generate one multiple-choice question (MCQ) for the {programming_language} language at a **{difficulty}** difficulty level.
    
    **INSTRUCTIONS:**
    1. If the question involves a code snippet, embed it directly in the 'question' string using Markdown code fences.
    2. Return ONLY a valid JSON object with keys "question", "options" (a list of 4 strings), and "correct_answer" (the string of the correct option).
    """
    try:
        response = llm.ask_ai(prompt, language=programming_language)
        data = json.loads(response)
        random.shuffle(data["options"])
        return data
    except (json.JSONDecodeError, KeyError) as e:
        st.error(f"Error generating {difficulty} question. Please try again. Details: {e}")
        return None

if "quiz_questions" not in st.session_state:
    with st.spinner("Preparing your adaptive quiz..."):
        st.session_state.quiz_questions = {
            "beginner": [generate_question("beginner", subject) for _ in range(3)],
            "intermediate": [generate_question("intermediate", subject) for _ in range(3)],
            "advanced": [generate_question("advanced", subject) for _ in range(3)]
        }
        st.session_state.quiz_scores = {"beginner": -1, "intermediate": -1, "advanced": -1}
        st.session_state.user_answers = {}

scores = st.session_state.quiz_scores
final_level = "beginner"
quiz_is_over = False

if scores["beginner"] < 3 and scores["beginner"] != -1:
    final_level = "beginner"
    quiz_is_over = True
elif scores["beginner"] == 3 and scores["intermediate"] < 3 and scores["intermediate"] != -1:
    final_level = "intermediate"
    quiz_is_over = True
elif scores["intermediate"] == 3:
    final_level = "advanced"
    if scores["advanced"] != -1:
        quiz_is_over = True

if quiz_is_over:
    st.info(f"Beginner Score: {scores['beginner']}/3" if scores["beginner"] != -1 else "Beginner: Not Taken")
    st.info(f"Intermediate Score: {scores['intermediate']}/3" if scores["intermediate"] != -1 else "Intermediate: Not Taken")
    st.info(f"Advanced Score: {scores['advanced']}/3" if scores["advanced"] != -1 else "Advanced: Not Taken")
    
    start_index = get_start_index(final_level)
    
    db.update_progress(
        st.session_state['user_id'], 
        subject, 
        level=final_level, 
        topic_index=start_index,
        status='learning'
    )
    
    st.success(f"### 🎉 Quiz Complete! Your starting level is **{final_level.capitalize()}**.")
    st.page_link("pages/3_Learning_Path.py", label="Start Your Learning Path!", icon="🚀")
    st.stop()

levels = ["beginner", "intermediate", "advanced"]
for level in levels:
    if scores[level] == -1:
        st.header(f"🟢 {level.capitalize()} Level Questions")
        with st.form(key=f"{level}_form"):
            questions = st.session_state.quiz_questions[level]
            if any(q is None for q in questions):
                st.error("Some questions could not be loaded. Please refresh.")
                st.stop()

            for i, q in enumerate(questions):
                key = f"{level}_{i}"
                st.markdown(f"**Q{i+1}: {q['question']}**") 
                st.session_state.user_answers[key] = st.radio("Options:", q['options'], key=key, index=None)

            if st.form_submit_button("Submit Answers"):
                score = 0
                for i, q in enumerate(questions):
                    key = f"{level}_{i}"
                    if st.session_state.user_answers[key] == q['correct_answer']:
                        score += 1
                st.session_state.quiz_scores[level] = score
                st.rerun()
        break