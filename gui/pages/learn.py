import streamlit as st
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from prompts.prompt_template import build_prompt
from helpers.ai_chat_helper import ask_ai
import json

st.title("📚 Learn Python")

user_name = st.text_input("What's your name?")
user_level = st.selectbox(
    "Select your Python level:", ["beginner", "intermediate", "advanced"]
)

if user_name and user_level:
    with open("course_content.json") as f:
        course = json.load(f)

    topic = course[user_level][0]
    prompt = build_prompt(user_level, topic["title"], topic["goal"], user_name)

    if st.button("Start Lesson"):
        response = ask_ai(prompt)
        st.markdown("### AI Tutor says:")
        st.write(response)
