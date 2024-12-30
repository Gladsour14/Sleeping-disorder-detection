import streamlit as st

st.title("Feedback Form")

st.text_area('Enter Your Feedback', max_chars=200)

st.button("Submit", type="primary")