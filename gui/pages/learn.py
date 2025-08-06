import streamlit as st
import sys
import os
import json
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from prompts.prompt_template import build_prompt
from ai_chat_helper import ask_ai

st.set_page_config(page_title="Learn C Programming", page_icon="📘", layout="wide")

# Hide sidebar/header
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
header[data-testid="stHeader"] {
    display: none;
}
.block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Required session keys
required_keys = ["user_name", "user_level", "language", "selected_topic", "topic_index"]
if not all(k in st.session_state for k in required_keys):
    st.error("🚫 Please start from the quiz page.")
    if st.button("⬅️ Back to Quiz", key="back_to_quiz_bottom"):
        st.switch_page("pages/c_quiz.py")
    st.stop()

# Get session values
user_name = st.session_state.user_name
user_level = st.session_state.user_level
language = st.session_state.language
topic_index = st.session_state.topic_index

# Load course content
course_file = f"course_contents/course_{language}.json"
if not os.path.exists(course_file):
    st.error("Missing course content.")
    st.stop()

with open(course_file) as f:
    course = json.load(f)

topics = course[user_level]

# Check if all lessons completed
if topic_index >= len(topics):
    st.success("🎓 You've completed all lessons!")
    if st.button("⬅️ Back to Quiz", key="back_to_quiz_end"):
        st.switch_page("pages/c_quiz.py")
    st.stop()

# Get current topic
topic = topics[topic_index]

# Display lesson
st.title(f"📘 {topic['title']}")
st.subheader(f"🎯 Goal: {topic['goal']}")

# --- Lesson Caching ---
lesson_key = f"lesson_data_{topic_index}"

if lesson_key not in st.session_state:
    with st.spinner("Loading lesson..."):
        lesson_prompt = build_prompt(
            user_level=user_level,
            topic_title=topic["title"],
            topic_goal=topic["goal"],
            user_name=user_name,
            language=language,
        ) + "\n\nPlease provide only the lesson content. Do NOT include any quiz questions or exercises in the lesson."

    lesson = ask_ai(lesson_prompt, language=language)
    st.session_state[lesson_key] = lesson
else:
    lesson = st.session_state[lesson_key]

st.write(lesson)

# --- Quiz Caching ---
quiz_key = f"quiz_data_{topic_index}"

if quiz_key not in st.session_state:
    quiz_gen_prompt = f"""
    You are an expert C programming tutor.

    Create a multiple-choice question (MCQ) for the topic "{topic['title']}" at the {user_level} level.
    Base it on the goal: "{topic['goal']}".

    Provide:
    1. The quiz question
    2. Four answer options (strings)
    3. The correct answer (match exactly one of the options)

    Do NOT label them a–d. Just provide 4 options in a list.

    Format your response as:
    {{
      "question": "...",
      "options": ["...", "...", "...", "..."],
      "correct_answer": "..."
    }}
    """

    with st.spinner("Creating quiz question..."):
        quiz_json_str = ask_ai(quiz_gen_prompt, language="json")


    try:
        raw_quiz = json.loads(quiz_json_str)
        assert "question" in raw_quiz and "options" in raw_quiz and "correct_answer" in raw_quiz

        options_list = raw_quiz["options"]
        correct_answer = raw_quiz["correct_answer"]

        random.shuffle(options_list)
        option_keys = ["a", "b", "c", "d"]
        quiz_options = dict(zip(option_keys, options_list))

        correct_option_key = next(k for k, v in quiz_options.items() if v.strip() == correct_answer.strip())

        st.session_state[quiz_key] = {
            "question": raw_quiz["question"],
            "options": quiz_options,
            "correct_key": correct_option_key
        }

    except Exception as e:
        st.error("❌ Failed to generate quiz for this lesson.")
        if st.button("🔄 Try Again", key="retry_quiz"):
            st.rerun()
        st.stop()

# Use cached quiz data
quiz_data = st.session_state[quiz_key]
quiz_question = quiz_data["question"]
quiz_options = quiz_data["options"]
correct_option_key = quiz_data["correct_key"]

# --- Show Quiz ---
st.markdown("### 🌟 Quiz Time 🌟")
option_texts = [f"{key}) {quiz_options[key]}" for key in ["a", "b", "c", "d"]]
user_choice = st.radio(quiz_question, option_texts)

if "quiz_passed" not in st.session_state:
    st.session_state.quiz_passed = False

if st.button("Submit Answer", key="submit_answer"):
    selected_key = user_choice[0]  # First char = key
    if selected_key == correct_option_key:
        st.success("Correct! 🎉")
        st.session_state.quiz_passed = True
    else:
        st.error("Oops, that's not correct. Try again!")
        st.session_state.quiz_passed = False

# --- Proceed to Next Lesson ---
if st.session_state.quiz_passed:
    if topic_index + 1 < len(topics):
        if st.button("➡️ Continue to Next Lesson", key="next_lesson"):
            next_index = topic_index + 1
            st.session_state.topic_index = next_index
            st.session_state.selected_topic = topics[next_index]
            st.session_state.quiz_passed = False

            # Clear caches for next topic
            for key in [f"quiz_data_{next_index}", f"lesson_data_{next_index}"]:
                if key in st.session_state:
                    del st.session_state[key]

            st.rerun()
    else:
        st.success("🎓 You've completed all the lessons!")

# --- Ask AI anything ---
st.markdown("---")
st.markdown(f"### 💬 Ask any **{language.upper()}** question")
user_q = st.text_input("Type your question here:")
if user_q:
    with st.spinner("Thinking..."):
        answer = ask_ai(user_q, language=language)
    st.markdown("**AI Tutor says:**")
    st.write(answer)

# --- Back to Home ---
if st.button("⬅️ Back to Home", key="back_to_home_bottom"):
    st.switch_page("pages/home.py")
