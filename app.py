
import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(
    page_title="AI Exam Preparation Planner",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Exam Preparation Planner")
st.write("Personalized Study Planning for College Students")

st.sidebar.header("Student Details")
name = st.sidebar.text_input("Student Name")
course = st.sidebar.text_input("Course / Department")
exam_date = st.sidebar.date_input(
    "Exam Date",
    min_value=date.today()
)

st.header("Enter Your Subjects")

subjects = st.text_area(
    "Subject Names (one per line)",
    "Mathematics\nPython\nDBMS\nComputer Networks"
)

study_hours = st.slider(
    "Daily Study Hours",
    min_value=1,
    max_value=10,
    value=4
)

plan_type = st.selectbox(
    "Choose Study Plan",
    ["Relaxed", "Balanced", "Intensive"]
)

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if st.button("Generate Study Plan"):
    subject_list = [
        s.strip()
        for s in subjects.splitlines()
        if s.strip()
    ]

    days = (exam_date - date.today()).days + 1

    if not subject_list:
        st.error("Please enter at least one subject.")
    else:
        factor = {
            "Relaxed": 0.6,
            "Balanced": 0.8,
            "Intensive": 1.0
        }[plan_type]

        daily_hours = max(1, round(study_hours * factor))

        tasks = []

        for i in range(days):
            current_date = date.today() + timedelta(days=i)
            subject = subject_list[i % len(subject_list)]

            activity = (
                "Revision and Practice"
                if i >= max(0, days - 2)
                else "Study and Practice"
            )

            tasks.append({
                "Date": str(current_date),
                "Subject": subject,
                "Activity": activity,
                "Hours": daily_hours,
                "Completed": False
            })

        st.session_state.tasks = tasks
        st.success("Study Plan Generated Successfully!")

if st.session_state.tasks:
    st.header("Your Study Timetable")

    df = pd.DataFrame(st.session_state.tasks)

    edited_df = st.data_editor(
        df,
        hide_index=True,
        disabled=["Date", "Subject", "Activity", "Hours"],
        key="study_editor"
    )

    st.session_state.tasks = edited_df.to_dict("records")

    progress = edited_df["Completed"].mean()

    st.subheader("Study Progress")
    st.progress(float(progress))
    st.write(f"{progress * 100:.1f}% Completed")

    st.subheader("Study Hours by Subject")
    chart_data = edited_df.groupby("Subject")["Hours"].sum()
    st.bar_chart(chart_data)

    csv = edited_df.to_csv(index=False)

    st.download_button(
        "Download Timetable",
        csv,
        "study_timetable.csv",
        "text/csv"
    )

st.info("Tip: Take short breaks between study sessions.")
