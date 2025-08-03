import streamlit as st

st.set_page_config(page_title="AI Learning Agent", page_icon="📘", layout="wide")

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

#side bar------------------------
with st.sidebar:
    st.write("Navigation")
    if st.button("Home"):
        st.switch_page("pages/home.py")
        

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
    /* Center Streamlit button by making its container a flexbox */
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

if st.button("Let's get started"):
    st.switch_page("pages/home.py")
