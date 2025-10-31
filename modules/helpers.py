import streamlit as st

def set_page_styling():
    """
    Injects CSS to hide the first two sidebar pages (app and Login)
    and applies any other global styles.
    """
    hide_pages_css = """
    <style>
    /* Hide the main 'app' page link */
    [data-testid="stSidebarNav"] li:nth-child(1) {
        display: none !important;
    }
    /* Hide the 'Login' page link */
    [data-testid="stSidebarNav"] li:nth-child(2) {
        display: none !important;
    }
    </style>
    """
    st.markdown(hide_pages_css, unsafe_allow_html=True)

def hide_sidebar():
    """Hides the default Streamlit sidebar."""
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

def load_css(file_path):
    """Loads a CSS file into the Streamlit app."""
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def hide_streamlit_ui():
    """
    Hides Streamlit's toolbar, main menu, footer, and header including profile icon and repo link.
    """
    hide_ui_css = """
    <style>
    /* Hide the entire toolbar including Deploy button */
    div[data-testid="stToolbar"] {display: none !important;}
    /* Hide Streamlit main menu (three dots) */
    #MainMenu {visibility: hidden;}
    /* Hide Streamlit footer */
    footer {visibility: hidden;}
    /* Hide header including profile icon and repo link */
    header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_ui_css, unsafe_allow_html=True)
