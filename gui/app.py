import streamlit as st

# Page config
st.set_page_config(page_title="AI Learning Agent", page_icon="📘", layout="wide")

# Hide sidebar and other elements with CSS
st.markdown(
    """
    <style>
    /* Hide sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* Hide the blank left space where sidebar would be */
    .block-container {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* Center Streamlit button */
    div.stButton {
        display: flex !important;
        justify-content: center !important;
        margin-top: 30px;
    }

    /* Stylish button styles */
    div.stButton > button {
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%) !important;
        color: white !important;
        padding: 15px 40px !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        border-radius: 30px !important;
        box-shadow: 0 8px 15px rgba(37, 117, 252, 0.3) !important;
        border: none !important;
        cursor: pointer !important;
        transition: all 0.3s ease 0s !important;
        user-select: none !important;
        display: inline-block !important;
    }

    div.stButton > button:hover {
        box-shadow: 0 15px 20px rgba(37, 117, 252, 0.6) !important;
        transform: translateY(-3px) !important;
    }

    div.stButton > button:active {
        transform: translateY(1px) !important;
        box-shadow: 0 5px 10px rgba(37, 117, 252, 0.2) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Welcome message
st.markdown(
    """
    <div style='width: 100%; text-align: center; margin-top: 50px;'>
        <h1 style='font-size: 3rem;'>👋 Welcome to the AI Learning Assistant</h1>
        <p style='font-size: 1.3rem; max-width: 800px; margin: auto;'>
            This intelligent assistant is designed to guide you through personalized learning paths,
            offer interactive support, and adapt to your individual progress. Explore the tools, get feedback, 
            and take control of your learning journey!
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Button to start
if st.button("Let's get started"):
    st.switch_page("pages/home.py")
