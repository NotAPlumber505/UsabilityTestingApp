import streamlit as st
import pandas as pd
import sqlite3
import time
import plotly.express as px

# Create a SQLite database (if not already exists)
DB_FILE = "usability_data.db"


def create_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    return conn


def create_tables():
    """Create necessary tables in the database."""
    conn = create_connection()
    cursor = conn.cursor()

    # Create tables if they don't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consent (
            timestamp TEXT,
            consent_given BOOLEAN
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS demographics (
            timestamp TEXT,
            name TEXT,
            age INTEGER,
            occupation TEXT,
            familiarity TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            timestamp TEXT,
            task_name TEXT,
            success TEXT,
            duration_seconds REAL,
            notes TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exit (
            timestamp TEXT,
            satisfaction INTEGER,
            difficulty INTEGER,
            open_feedback TEXT
        )
    ''')

    conn.commit()
    conn.close()


def save_to_db(data_dict, table_name):
    """Save data to the appropriate table in the database."""
    conn = create_connection()
    cursor = conn.cursor()

    columns = ', '.join(data_dict.keys())
    placeholders = ', '.join(['?'] * len(data_dict))

    cursor.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})', tuple(data_dict.values()))
    conn.commit()
    conn.close()


def load_from_db(query, limit=None):
    """Load data from the database using a query."""
    conn = create_connection()
    if limit:
        query = f"{query} LIMIT {limit}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def main():
    st.set_page_config(page_title="Usability Testing Tool", layout="wide")

    # Create tables if not exist
    create_tables()

    home, consent, demographics, tasks, exit, report = st.tabs(
        ["Home", "Consent", "Demographics", "Task", "Exit Questionnaire", "Report"])

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
                # Save the consent acceptance time
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "consent_given": consent_given
                }
                save_to_db(data_dict, "consent")
                st.success("Your consent has been recorded. Thank you!")

    with demographics:
        st.header("Demographic Questionnaire")

        with st.form("demographic_form"):
            with st.container():
                name = st.text_input("Name (optional)")
                age = st.number_input("Age:", min_value=0, max_value=100, step=1, format="%d")
                occupation = st.text_input("Occupation")
                familiarity = st.selectbox("Familiarity with similar tools?",
                                           options=["", "Not Familiar", "Somewhat Familiar", "Very Familiar"])

            submitted = st.form_submit_button("Submit Demographics")
            if submitted:
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "name": name,
                    "age": age,
                    "occupation": occupation,
                    "familiarity": familiarity
                }
                if not age or not occupation or not familiarity:
                    st.warning("Please fill out the form")
                else:
                    save_to_db(data_dict, "demographics")
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
                                                             "Task 10: Generate Report"
                                                             ])

        if "previous_task" not in st.session_state or st.session_state["previous_task"] != selected_task:
            st.session_state["previous_task"] = selected_task
            st.session_state["task_completed"] = False
            st.session_state["start_time"] = None

        success = ""

        if selected_task:
            if not st.session_state.get("task_completed", False):
                start_button = st.button("Start Task Timer")
                if start_button:
                    st.session_state["start_time"] = time.time()
                    st.info("Task timer started. Complete your task and then click 'Stop Task Timer.'")

                stop_button = st.button("Stop Task Timer")
                if stop_button:
                    if "start_time" in st.session_state and st.session_state["start_time"] is not None:
                        duration = time.time() - st.session_state["start_time"]
                        st.session_state["task_duration"] = duration
                        st.session_state["task_completed"] = True
                        st.success(f"Task completed in {duration:.2f} seconds!")

                        # Reset after task completion
                        st.session_state["start_time"] = None
                        st.session_state["task_completed"] = False

            success = st.radio("Was the task completed successfully?", ["No", "Yes", "Partial"])
            notes = st.text_area("Observer Notes")

        if selected_task:
            if st.button("Save Task Results"):
                duration_val = st.session_state.get("task_duration", None)

                if not success:
                    st.warning("Please select a success status before saving.")
                else:
                    data_dict = {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "task_name": selected_task,
                        "success": success,
                        "duration_seconds": duration_val if duration_val else "",
                        "notes": notes
                    }
                    save_to_db(data_dict, "tasks")
                    st.success("Task data saved.")

    with exit:
        st.header("Exit Questionnaire")

        # Wrap the exit form inside `st.form()`
        with st.form("exit_form"):
            satisfaction = st.slider("Overall Satisfaction (1=Very Low,5=Very High)", 1, 5)
            difficulty = st.slider("Overall Difficulty (1=Very Easy,5=Very Hard)", 1, 5)
            open_feedback = st.text_area("Additional feedback or comments:")

            # This button should now be inside the form
            submitted_exit = st.form_submit_button("Submit Exit Questionnaire")

        if submitted_exit:
            data_dict = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "satisfaction": satisfaction,
                "difficulty": difficulty,
                "open_feedback": open_feedback
            }
            save_to_db(data_dict, "exit")
            st.success("Exit questionnaire data saved.")

    with report:
        st.header("Usability Report - Aggregated Results")

        # Limit data to 100 rows to improve performance
        st.write("**Consent Data**")
        consent_df = load_from_db('SELECT * FROM consent', limit=100)
        if not consent_df.empty:
            st.dataframe(consent_df)
        else:
            st.info("No consent data available yet.")

        st.write("**Demographic Data**")
        demographic_df = load_from_db('SELECT * FROM demographics', limit=100)
        if not demographic_df.empty:
            st.dataframe(demographic_df)
        else:
            st.info("No demographic data available yet.")

        st.write("**Task Performance Data**")
        task_df = load_from_db('SELECT * FROM tasks', limit=100)
        if not task_df.empty:
            st.dataframe(task_df)
        else:
            st.info("No task data available yet.")

        st.write("**Exit Questionnaire Data**")
        exit_df = load_from_db('SELECT * FROM exit', limit=100)
        if not exit_df.empty:
            st.dataframe(exit_df)
        else:
            st.info("No exit questionnaire data available yet.")

        if not task_df.empty:
            task_success_counts = task_df['success'].value_counts()
            fig = px.bar(task_success_counts, x=task_success_counts.index, y=task_success_counts.values,
                         labels={'x': 'Success Status', 'y': 'Task Count'},
                         title="Task Success Summary")
            st.plotly_chart(fig)


if __name__ == "__main__":
    main()
