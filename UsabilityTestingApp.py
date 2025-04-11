import streamlit as st
import pandas as pd
import time
import sqlite3
import plotly.express as px

# Database initialization
DB_NAME = "usability_data.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS consent_data (
            timestamp TEXT,
            consent_given BOOLEAN)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS demographic_data (
            timestamp TEXT,
            name TEXT,
            age INTEGER,
            occupation TEXT,
            familiarity TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS task_data (
            timestamp TEXT,
            task_name TEXT,
            success TEXT,
            duration_seconds REAL,
            notes TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS exit_data (
            timestamp TEXT,
            satisfaction INTEGER,
            difficulty INTEGER,
            open_feedback TEXT)''')
        conn.commit()

def insert_data(table, data_dict):
    with get_connection() as conn:
        df = pd.DataFrame([data_dict])
        df.to_sql(table, conn, if_exists='append', index=False)

def load_data(table):
    with get_connection() as conn:
        return pd.read_sql_query(f"SELECT * FROM {table}", conn)

@st.cache_data
def cached_load_data(table):
    return load_data(table)

def main():
    st.set_page_config(page_title="Usability Testing Tool", layout="wide")
    init_db()

    home, consent, demographics, tasks, exit, report = st.tabs(
        ["Home", "Consent", "Demographics", "Task", "Exit Questionnaire", "Report"]
    )

    with home:
        st.header("Introduction")
        st.write("""
        Welcome to the Usability Testing Tool for HCI.
        In this app, you will:
        1. Provide consent for data collection.
        2. Fill out a short demographic questionnaire.
        3. Perform a specific task (or tasks).
        4. Answer an exit questionnaire about your experience.
        5. View a summary report (for demonstration purposes).
        """)

    with consent:
        st.header("Consent Form")
        st.write("Please read the consent form below and confirm your agreement:")
        st.subheader("Consent Agreement:")
        st.write("- I understand the purpose of this usability study.")
        st.write("- I am aware that my data will be collected solely for research and improvement purposes.")
        st.write("- I can withdraw at any time.")
        consent_given = st.checkbox("I agree to the terms above")

        if st.button("Submit Consent"):
            if not consent_given:
                st.warning("You must agree to the consent terms before proceeding.")
            else:
                insert_data("consent_data", {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "consent_given": consent_given
                })
                st.success("Your consent has been recorded. Thank you!")

    with demographics:
        st.header("Demographic Questionnaire")
        with st.form("demographic_form"):
            name = st.text_input("Name (optional)")
            age = st.number_input("Age:", min_value=0, max_value=100, step=1, format="%d")
            occupation = st.text_input("Occupation")
            familiarity = st.selectbox("Familiarity with similar tools?",
                                       options=["", "Not Familiar", "Somewhat Familiar", "Very Familiar"])
            submitted = st.form_submit_button("Submit Demographics")
            if submitted:
                if not age or not occupation or not familiarity:
                    st.warning("Please fill out the form")
                else:
                    insert_data("demographic_data", {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "name": name,
                        "age": age,
                        "occupation": occupation,
                        "familiarity": familiarity
                    })
                    st.success("Demographic data saved.")

    with tasks:
        st.header("Task Page")
        st.write("Please select a task and record your experience completing it.")

        selected_task = st.selectbox("Select Task", options=["", "Task 1: Wait for User Input",
                                                             "Task 2: Process Data",
                                                             "Task 3: Save to Database",
                                                             "Task 4: Fetch Data from API",
                                                             "Task 5: Execute a Scheduled Task",
                                                             "Task 6: Log System Events",
                                                             "Task 7: Retry on Failure",
                                                             "Task 8: Trigger Alert on Timeout",
                                                             "Task 9: Cache Expiry",
                                                             "Task 10: Generate Report"])
        st.write("Task Description: Perform the example task in our system...")

        if "previous_task" not in st.session_state or st.session_state["previous_task"] != selected_task:
            st.session_state["previous_task"] = selected_task
            st.session_state["task_completed"] = False
            st.session_state["start_time"] = None

        success = ""

        if selected_task:
            if not st.session_state.get("task_completed", False):
                if st.button("Start Task Timer"):
                    st.session_state["start_time"] = time.time()
                    st.info("Task timer started. Complete your task and then click 'Stop Task Timer.'")

                if st.button("Stop Task Timer"):
                    if st.session_state.get("start_time"):
                        duration = time.time() - st.session_state["start_time"]
                        st.session_state["task_duration"] = duration
                        st.session_state["task_completed"] = True
                        st.success(f"Task completed in {duration:.2f} seconds!")
                        st.session_state["start_time"] = None
                        st.session_state["task_completed"] = False

            success = st.radio("Was the task completed successfully?", ["No", "Yes", "Partial"])
            notes = st.text_area("Observer Notes")

            if st.button("Save Task Results"):
                if not success:
                    st.warning("Please select a success status before saving.")
                else:
                    insert_data("task_data", {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "task_name": selected_task,
                        "success": success,
                        "duration_seconds": st.session_state.get("task_duration", None),
                        "notes": notes
                    })
                    st.success("Task data saved.")
                    st.session_state.pop("task_duration", None)

    with exit:
        st.header("Exit Questionnaire")
        with st.form("exit_form"):
            satisfaction = st.slider("Overall Satisfaction (1=Very Low,5=Very High)", 1, 5)
            difficulty = st.slider("Overall Difficulty (1=Very Easy,5=Very Hard)", 1, 5)
            open_feedback = st.text_area("Additional feedback or comments:")
            if st.form_submit_button("Submit Exit Questionnaire"):
                insert_data("exit_data", {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "satisfaction": satisfaction,
                    "difficulty": difficulty,
                    "open_feedback": open_feedback
                })
                st.success("Exit questionnaire data saved.")

    with report:
        st.header("Usability Report - Aggregated Results")

        def render_table_and_info(title, table_name):
            st.write(f"**{title}**")
            df = load_data(table_name)
            if not df.empty:
                st.dataframe(df)
            else:
                st.info(f"No {title.lower()} available yet.")
            return df

        consent_df = render_table_and_info("Consent Data", "consent_data")
        demo_df = render_table_and_info("Demographic Data", "demographic_data")
        task_df = render_table_and_info("Task Performance Data", "task_data")
        exit_df = render_table_and_info("Exit Questionnaire Data", "exit_data")

        if not task_df.empty:
            task_success_counts = task_df['success'].value_counts()
            fig = px.bar(task_success_counts, x=task_success_counts.index, y=task_success_counts.values,
                         labels={'x': 'Success Status', 'y': 'Count'}, title="Task Success Counts")
            st.plotly_chart(fig)

            task_success_per_task = task_df.groupby('task_name')['success'].value_counts().unstack().fillna(0)
            task_success_per_task = task_success_per_task.div(task_success_per_task.sum(axis=1), axis=0) * 100
            fig = px.bar(task_success_per_task, x=task_success_per_task.index, y=task_success_per_task.columns,
                         title="Success Rates per Task", labels={'x': 'Task Name', 'y': 'Percentage'})
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
