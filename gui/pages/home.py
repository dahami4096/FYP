import streamlit as st

st.set_page_config(
    page_title="Home - AI Learning Assistant", page_icon="💻", layout="wide"
)

# Title
st.markdown(
    """
    <h2 style='text-align: center; margin-top: 30px;'>💻 Choose a Programming Language</h2>
    <p style='text-align: center; color: grey;'>Click on any language to start learning</p>
    """,
    unsafe_allow_html=True,
)

# Custom CSS for same-sized buttons
st.markdown(
    """
    <style>
    .stButton > button {
        background: linear-gradient(to right, #ff7e5f, #feb47b);
        border: none;
        color: white;
        width: 150px;  /* fixed width */
        height: 70px; /* fixed height */
        font-size: 1rem;
        font-weight: 600;
        border-radius: 12px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,0,0,0.8);
        transition: all 0.3s ease;
        margin: auto; /* center inside column */
        display: block;
    }
    .stButton > button:hover {
        background: linear-gradient(to right, #feb47b, #ff7e5f);
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Language buttons list
languages = [
    "C Programming",
    "Python",
    "C++",
    "C#",
    "Java",
    "JavaScript",
    "Go",
    "Rust",
    "TypeScript",
    "Kotlin",
    "Ruby",
    "Swift",
]

# Layout: 4 buttons per row
cols_per_row = 4

# Display buttons in rows
for i in range(0, len(languages), cols_per_row):
    cols = st.columns(cols_per_row)
    for idx, lang in enumerate(languages[i : i + cols_per_row]):
        with cols[idx]:
            if st.button(lang):
                if lang == "Python":
                    st.switch_page("pages/python.py")
                elif lang == "C Programming":
                    st.switch_page("pages/home_c.py")
                else:
                    st.success(f"You clicked {lang}")
