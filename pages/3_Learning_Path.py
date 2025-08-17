import streamlit as st
from modules import llm, db,helpers
import json

helpers.set_page_styling()

st.set_page_config(page_title="Learning Path", page_icon="📚", layout="wide")
if 'user_id' not in st.session_state or 'selected_subject' not in st.session_state:
    st.page_link("pages/0_Login.py", label="Go to Login", icon="🔑")
    st.stop()

subject = st.session_state['selected_subject']

try:
    with open(f"curriculum/{subject.lower()}_curriculum.json") as f:
        curriculum = json.load(f)['full_path']
except FileNotFoundError:
    st.error(f"Curriculum for {subject} not found.")
    st.stop()

topics = [item['topic'] for item in curriculum]
progress_data = db.get_or_create_progress(st.session_state['user_id'], subject)
topic_index = progress_data['topic_index']

failed_assignment = progress_data['assignment_score'] is not None and progress_data['status'] == 'learning'
revise_mode_flag = st.session_state.get('revise_mode', False)
review_mode = failed_assignment or revise_mode_flag

if review_mode:
    if revise_mode_flag:
        st.info("📖 You are in **Revise Mode**. All lessons are unlocked for your review.")
    else:
        st.info("📖 You are in **Review Mode**. Study what you need and retake the assignment when you're ready.")
else:
    st.title(f"🚀 Your {subject.capitalize()} Learning Path")

if not review_mode and topic_index >= len(topics):
    st.success("🎉 You've completed all the lessons in the learning path!")
    st.markdown("---")
    st.subheader("What would you like to do next?")
    cols = st.columns(2)
    with cols[0]:
        if st.button("Review Lessons", use_container_width=True):
            st.session_state['revise_mode'] = True
            st.rerun()
    with cols[1]:
        if st.button("Take Final Assignment", type="primary", use_container_width=True):
            db.update_progress(st.session_state['user_id'], subject, status='assessing')
            st.switch_page("pages/4_Assignments.py")
    st.stop()
    
if 'viewing_topic_index' not in st.session_state:
    if review_mode:
        st.session_state.viewing_topic_index = 0
    else:
        st.session_state.viewing_topic_index = topic_index

st.sidebar.header("Course Outline")
for i, topic_name in enumerate(topics):
    if review_mode:
        btn_type = "primary" if i == st.session_state.viewing_topic_index else "secondary"
        if st.sidebar.button(f"📖 {topic_name}", key=f"topic_{i}", type=btn_type):
            st.session_state.viewing_topic_index = i
            st.rerun()
    else:
        if i < topic_index: st.sidebar.button(f"✅ {topic_name}", disabled=True)
        elif i == topic_index: st.sidebar.button(f"▶️ {topic_name}", type="primary")
        else: st.sidebar.button(f"🔒 {topic_name}", disabled=True)

if failed_assignment:
    st.sidebar.markdown("---")
    if st.sidebar.button("Ready to Retake Assignment", type="primary"):
        db.update_progress(st.session_state['user_id'], subject, status='assessing')
        if 'assignment_questions' in st.session_state: del st.session_state.assignment_questions
        st.switch_page("pages/4_Assignments.py")

viewing_index = st.session_state.viewing_topic_index
current_topic = topics[viewing_index]
current_level = curriculum[viewing_index]['level']

st.header(f"Chapter {viewing_index + 1}: {current_topic}")
st.caption(f"Difficulty Level: {current_level.capitalize()}")

lesson_key = f"lesson_{viewing_index}"
if lesson_key not in st.session_state:
    with st.spinner("Loading lesson..."):
        prompt = f"Provide a detailed lesson for a '{current_level}' level {subject} student on the topic: '{current_topic}'. Include simple code examples."
        st.session_state[lesson_key] = llm.ask_ai(prompt, language=subject)
st.markdown(st.session_state[lesson_key])

if not review_mode:
    st.markdown("---")
    st.subheader("🌟 Check Your Understanding")
    quiz_key = f"quiz_{viewing_index}"
    if quiz_key not in st.session_state:
        with st.spinner("Creating a quick quiz..."):
            # Full, detailed prompt
            prompt = f"""
            Generate one multiple-choice question for the {subject} language on the topic '{current_topic}'.
            
            **INSTRUCTIONS:**
            1. If the question involves a code snippet, embed it directly in the 'question' string using Markdown.
            2. Return ONLY a valid JSON object with keys "question", "options" (a list of 4 strings), and "correct_answer" (the string of the correct option).
            """
            response = llm.ask_ai(prompt, language=subject)
            st.session_state[quiz_key] = json.loads(response)
    quiz_data = st.session_state[quiz_key]
    user_choice = st.radio(quiz_data['question'], quiz_data['options'], index=None)
    if st.button("Submit Answer"):
        if user_choice == quiz_data['correct_answer']:
            st.balloons(); st.success("Correct! You've unlocked the next topic!")
            db.update_progress(st.session_state['user_id'], subject, topic_index=topic_index + 1)
            st.session_state.viewing_topic_index = topic_index + 1
            st.rerun()
        else:
            st.error("Not quite. Try reviewing the lesson and answering again!")

st.markdown("---")
st.header("💬 AI Tutor Chat")
st.write(f"Ask any question about **{current_topic}** or general {subject} concepts.")

if 'chat_history' not in st.session_state: st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]): st.markdown(message["content"])

if user_prompt := st.chat_input(f"Ask me about {subject}..."):
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"): st.markdown(user_prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            chat_prompt = f"The user is currently studying the topic '{current_topic}' in a {subject} course. They are at a '{current_level}' level. Answer the following user question in this context. User question: \"{user_prompt}\""
            ai_response = llm.ask_ai(chat_prompt, language=subject)
            st.markdown(ai_response)
    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})