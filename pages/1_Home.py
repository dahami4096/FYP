import streamlit as st
from modules import db, helpers

helpers.load_css("assets/style.css")
helpers.set_page_styling()
helpers.hide_sidebar()
helpers.hide_streamlit_ui() 
# --- Page configuration ---
st.set_page_config(
    page_title="Home", 
    page_icon="🏠", 
    layout="wide"
)


# --- Authentication check ---
if 'user_id' not in st.session_state:
    st.warning("You need to log in to access this page.")
    st.page_link("pages/0_Login.py", label="Go to Login", icon="🔑")
    st.stop()

# --- Page content ---
st.title(f"Welcome, {st.session_state['username']}! 👋")
st.header("💻 Choose a Programming Language")
st.write("Click on a subject to begin or continue your learning journey.")

# List of available languages
languages = ["C", "Python", "C++", "Java", "JavaScript", "Rust"]

# Create columns for a grid layout
cols = st.columns(4) 
col_index = 0

for lang in languages:
    with cols[col_index % 4]:
        if st.button(lang, use_container_width=True, key=f"lang_{lang}"):
            
            # If the selected subject is different from the one in session, reset course state
            if st.session_state.get('selected_subject') != lang:
                keys_to_clear = [
                    'quiz_questions', 'quiz_scores', 'user_answers', 'user_level', 
                    'learning_topics', 'current_topic_index', 'viewing_topic_index',
                    'chat_history', 'revise_mode' # Added 'revise_mode' here
                ]
                for key in keys_to_clear:
                    if key in st.session_state:
                        del st.session_state[key]
                
                for key in st.session_state.keys():
                    if key.startswith('lesson_') or key.startswith('quiz_'):
                        del st.session_state[key]

            st.session_state['selected_subject'] = lang
            progress = db.get_or_create_progress(st.session_state['user_id'], lang)

            # Navigator Logic
            if progress['level'] is None:
                st.switch_page("pages/2_Quiz.py")
            elif progress['status'] == 'assessing':
                st.switch_page("pages/4_Assignments.py")
            elif progress['status'] == 'completed':
                st.info(f"You have already completed the {lang} module. Check your profile for your results.")
                st.switch_page("pages/5_Profile.py")
            else: # status == 'learning'
                st.switch_page("pages/3_Learning_Path.py")
    col_index += 1

st.markdown("---")
if st.button("Logout"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()