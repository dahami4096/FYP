import streamlit as st

st.set_page_config(page_title="Learn C Programming", page_icon="💻", layout="wide")

# Title
st.title("🧠 Learn C Programming with AI Agent")

# Introduction
st.markdown("""
Welcome to your personalized **C Programming Learning Agent**! 🚀  
This AI-powered assistant will help you learn C based on your current knowledge level.

---

### 📋 How It Works

1. **Start with a Quick Quiz** (5–10 short questions)
2. 📊 Based on your score, you will be assigned a level:
   - 🟢 Beginner
   - 🟡 Intermediate
   - 🔵 Advanced
3. 🤖 Then, the agent will generate lessons **custom-tailored** to your level.

---

Whether you're new to programming or brushing up for interviews, this tool will guide you step-by-step. Let's begin your C programming journey today! 🎯
""")

# Button to Start Quiz
if st.button("Start C Programming Quiz"):
    st.switch_page("pages/c_quiz.py")  # Make sure c_quiz.py exists in `pages/` folder
