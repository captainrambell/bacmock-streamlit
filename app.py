import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bac II Mock Exam Feedback", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Summary Feedback", "Detailed Analytics"])

# Load data
uploaded = st.sidebar.file_uploader("Upload mock exam CSV", type=["csv"])
if uploaded is not None:
    df = pd.read_csv(uploaded)
else:
    df = pd.read_csv("sample_data.csv")

# Basic preprocessing
df["is_correct"] = df["is_correct"].astype(int)

# Compute per-student score
student_scores = df.groupby("student_id")["is_correct"].sum().reset_index()
student_scores.rename(columns={"is_correct": "score"}, inplace=True)

# Compute per-topic accuracy
topic_stats = df.groupby("topic")["is_correct"].agg(["mean", "count"]).reset_index()
topic_stats.rename(columns={"mean": "accuracy"}, inplace=True)
topic_stats["accuracy_pct"] = (topic_stats["accuracy"] * 100).round(1)

# Identify weakest topics (lowest accuracy)
weakest_topics = topic_stats.sort_values("accuracy").head(5)

if page == "Summary Feedback":
    st.header("Summary Feedback")

    col1, col2 = st.columns(2)
    with col1:
        class_avg = student_scores["score"].mean().round(2)
        st.metric("Average score (items correct)", class_avg)
    with col2:
        st.metric("Number of students", student_scores["student_id"].nunique())

    st.subheader("Score distribution")
    st.bar_chart(student_scores.set_index("student_id")["score"])

    st.subheader("Topic accuracy (%)")
    st.bar_chart(topic_stats.set_index("topic")["accuracy_pct"])

    st.subheader("Top 5 weakest topics")
    st.table(weakest_topics[["topic", "accuracy_pct", "count"]])

else:
    st.header("Detailed Analytics")

    st.subheader("Student–Topic performance matrix")
    pivot = df.pivot_table(
        index="student_id",
        columns="topic",
        values="is_correct",
        aggfunc="mean"
    )
    st.dataframe(pivot.style.format("{:.2f}"))

    st.subheader("Item-level results")
    st.dataframe(df)
