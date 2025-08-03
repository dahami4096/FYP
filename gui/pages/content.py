import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import json
from prompts.prompt_template import build_prompt
from ai_chat_helper import ask_ai

with open("course_content.json") as f:
    course = json.load(f)

st.title("📘 AI Tutor")

# Get user name and level
user_name = st.text_input("What's your name?")
user_level = st.selectbox(
    "Select your Python level:", ["beginner", "intermediate", "advanced"]
)

# Display learning path
if user_name and user_level:
    st.markdown("### 📚 Your Learning Path")
    for idx, topic in enumerate(course[user_level], start=1):
        st.write(f"{idx}. {topic['title']} — {topic['goal']}")

    if st.button("Start First Lesson"):
        first_topic = course[user_level][0]
        prompt = build_prompt(
            user_level=user_level,
            topic_title=first_topic["title"],
            topic_goal=first_topic["goal"],
            user_name=user_name,
        )
        lesson = ask_ai(prompt)
        st.markdown("### 🧠 AI Tutor says:")
        st.write(lesson)

# Chat box
st.markdown("---")
st.markdown("### 💬 Ask your Python questions")

user_q = st.text_input("Type your question here:")
if user_q:
    answer = ask_ai(user_q)
    st.markdown("**AI Tutor says:**")
    st.write(answer)
