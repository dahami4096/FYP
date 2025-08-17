import streamlit as st
import json
from modules import db,helpers

helpers.set_page_styling()

st.set_page_config(page_title="My Profile", page_icon="👤", layout="wide")
if 'user_id' not in st.session_state:
    st.page_link("pages/0_Login.py", label="Go to Login", icon="🔑")
    st.stop()

st.title(f"📊 {st.session_state['username']}'s Progress Dashboard")
all_progress = db.get_all_user_progress(st.session_state['user_id'])

if not all_progress:
    st.info("You haven't started any subjects yet. Go to the Home page to begin!")
    st.stop()

for p in all_progress:
    subject = p['subject']
    with st.container(border=True):
        st.subheader(f"{subject} ({p['status'].capitalize()})")
        try:
            with open(f"curriculum/{subject.lower()}_curriculum.json") as f:
                total_topics = len(json.load(f)['full_path'])
        except FileNotFoundError:
            st.error(f"Curriculum file for {subject} not found.")
            continue
        current_topic_index = p['topic_index']
        progress_percent = (current_topic_index / total_topics) if total_topics > 0 else 0
        st.progress(progress_percent, text=f"Topics Completed: {current_topic_index} of {total_topics}")
        cols = st.columns(3)
        with cols[0]:
            diagnosed_level = p['level'] if p['level'] else "Not Set"
            st.metric(label="Diagnosed Level", value=diagnosed_level.capitalize())
        with cols[1]:
            score = p['assignment_score']
            display_score = f"{score}%" if score is not None else "Not Taken"
            st.metric(label="Latest Assignment Score", value=display_score)
        with cols[2]:
            st.metric(label="Mastery Status", value=p['status'].capitalize())
        if p['status'] == 'completed':
            action_cols = st.columns(2)
            with action_cols[0]:
                if st.button(f"Revise {subject} Lessons", key=f"revise_{subject}"):
                    st.session_state['selected_subject'] = subject
                    st.session_state['revise_mode'] = True
                    st.switch_page("pages/3_Learning_Path.py")
            with action_cols[1]:
                 st.page_link("pages/1_Home.py", label="Select Another Module", icon="🏠")