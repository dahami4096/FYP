import streamlit as st
hide_streamlit_style = """
    <style>
    /* Hide hamburger menu */
    #MainMenu {visibility: hidden;}
    /* Hide footer */
    footer {visibility: hidden;}
    /* Optional: hide header (title bar) */
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# Immediately redirect to the login page
st.switch_page("pages/0_Login.py")
