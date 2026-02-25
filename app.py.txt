import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bac II Mock Exam Feedback", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Summary Feedback", "Detailed Analytics"])

# Load data
uploaded = st.sidebar.file_uploader("Upload mock exam CSV", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)
else:
    df = pd.read_csv("sample_data.csv")

# Compute metrics (groupby for scores, topics, etc.)

if page == "Summary Feedback":
    # show class average, distribution, weakest topics
    ...
else:
    # show topic-student matrix, item-level table
    ...
