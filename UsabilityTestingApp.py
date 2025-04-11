import streamlit as st
import pandas as pd
import time
import os
import plotly.express as px

# Create a folder called data in the main project folder (only create if not exists)
DATA_FOLDER = "data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# Define CSV file paths for each part of the usability testing
CONSENT_CSV = os.path.join(DATA_FOLDER, "consent_data.csv")
DEMOGRAPHIC_CSV = os.path.join(DATA_FOLDER, "demographic_data.csv")
TASK_CSV = os.path.join(DATA_FOLDER, "task_data.csv")
EXIT_CSV = os.path.join(DATA_FOLDER, "exit_data.csv")

@st.cache_data
def load_from_csv(csv_file):
    """
    Load data from a CSV file and return a pandas DataFrame.
    Uses caching to speed up subsequent reads.
    """
    if os.path.isfile(csv_file):
        return pd.read_csv(csv_file)
    else:
        return pd.DataFrame()

@st.cache_data
def save_to_csv(data_dict, csv_file):
    """
    Save data dictionary to a CSV file, either appending to an existing file
    or creating a new one if it doesn't exist. Caching used to prevent redundant
    writes.
    """
    df_new = pd.DataFrame([data_dict])
    if not os.path.isfile(csv_file):
        # If CSV doesn't exist, write with headers
        df_new.to_csv(csv_file, mode='w', header=True, index=False)
    else:
        # Append without writing the header
        df_new.to_csv(csv_file, mode='a', header=False, index=False)


def main():
    st.set_page_config(page_title="Usability Testing Tool", layout="wide")

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
                save_to_csv(data_dict, CONSENT_CSV)
                st.success("Your consent has been recorded. Thank you!")

    with demographics:
        st.header("Demographic Questionnaire")

        with st.form("demographic_form"):
            with st.container():
                name = st.text_input("Name (optional)")
                age = st.number_input("Age:", min_value=0, max_value=100, step=1, format="%d")
                occupation = st.text_input("Occupation")
                familiarity = st.selectbox("Familiarity with similar tools?",options=["", "Not Familiar", "Somewhat Familiar", "Very Familiar"])

            submitted = st.form_submit_button("Submit Demographics")
            if submitted:
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "name": name,
                    "age": age,
                    "occupation": occupation,
                    "familiarity": familiarity
                }
                save_to_csv(data_dict, DEMOGRAPHIC_CSV)
                if not age or not occupation or not familiarity:
                    st.warning("Please fill out the form")
                else:
                    st.success("Demographic data saved.")

    with tasks:
        st.header("Task Page")

        st.write("Please select a task and record your experience completing it.")

        # For this template, we assume there's only one task, in project 3, we will have to include the actual tasks
        selected_task = st.selectbox("Select Task", options=["","Task 1: Wait for User Input",
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
        st.write("Task Description: Perform the example task in our system...")

        # Track success, completion time, etc.
        if "previous_task" not in st.session_state or st.session_state["previous_task"] != selected_task:
            st.session_state["previous_task"] = selected_task
            st.session_state["task_completed"] = False  # Reset when a new task is selected
            st.session_state["start_time"] = None   # Reset start time when a new task is selected

        success = ""    # Default value for success

        if selected_task:
            if not st.session_state.get("task_completed", False):
                start_button = st.button("Start Task Timer")
                if start_button:
                    st.session_state["start_time"] = time.time()
                    st.info("Task timer started. Complete your task and then click 'Stop Task Timer.'")

                stop_button = st.button("Stop Task Timer")
                if stop_button:
                    if "start_time" in st.session_state and st.session_state["start_time"] is not None:
                        # Record task completion duration and mark task as completed
                        duration = time.time() - st.session_state["start_time"]
                        st.session_state["task_duration"] = duration
                        st.session_state["task_completed"] = True   # Mark task as completed
                        st.success(f"Task completed in {duration:.2f} seconds!")

                        # Reset to allow starting again immediately after stop
                        st.session_state["start_time"] = None   # Reset start time after stopping the task
                        st.session_state["task_completed"] = False

            success = st.radio("Was the task completed successfully?", ["No", "Yes", "Partial"])
            notes = st.text_area("Observer Notes")

        else:
            st.info("Please select a task.")

        # Disable the "Save Task Results" button if no task is selected
        if selected_task:
            if st.button("Save Task Results"):
                duration_val = st.session_state.get("task_duration", None)

                # Only save if the task is completed
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
                    save_to_csv(data_dict, TASK_CSV)
                    st.success("Task data saved.")

                    # Reset any stored time in session_state if you'd like
                    if "start_time" in st.session_state:
                        del st.session_state["start_time"]
                    if "task_duration" in st.session_state:
                        del st.session_state["task_duration"]

    with exit:
        st.header("Exit Questionnaire")

        with st.form("exit_form"):
            with st.container():
                satisfaction = st.slider("Overall Satisfaction (1=Very Low,5=Very High)", 1, 5)
                difficulty = st.slider("Overall Difficulty (1=Very Easy,5=Very Hard)", 1, 5)
                open_feedback = st.text_area("Additional feedback or comments:")

            submitted_exit = st.form_submit_button("Submit Exit Questionnaire")
            if submitted_exit:
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "satisfaction": satisfaction,
                    "difficulty": difficulty,
                    "open_feedback": open_feedback
                }
                save_to_csv(data_dict, EXIT_CSV)
                st.success("Exit questionnaire data saved.")

    with report:
        st.header("Usability Report - Aggregated Results")

        st.write("**Consent Data**")
        consent_df = load_from_csv(CONSENT_CSV)
        if not consent_df.empty:
            st.dataframe(consent_df)
        else:
            st.info("No consent data available yet.")

        st.write("**Demographic Data**")
        demographic_df = load_from_csv(DEMOGRAPHIC_CSV)
        if not demographic_df.empty:
            st.dataframe(demographic_df)
        else:
            st.info("No demographic data available yet.")

        st.write("**Task Performance Data**")
        task_df = load_from_csv(TASK_CSV)
        if not task_df.empty:
            st.dataframe(task_df)
        else:
            st.info("No task data available yet.")

        st.write("**Exit Questionnaire Data**")
        exit_df = load_from_csv(EXIT_CSV)
        if not exit_df.empty:
            st.dataframe(exit_df)
        else:
            st.info("No exit questionnaire data available yet.")

        if not task_df.empty:
            # Create a bar chart of task success counts
            task_success_counts = task_df['success'].value_counts()
            fig = px.bar(task_success_counts, x=task_success_counts.index, y=task_success_counts.values,
                         labels={'x': 'Success Status', 'y': 'Count'}, title="Task Success Counts")
            fig.update_xaxes(tickangle=0)  # Rotate x-axis labels horizontally
            st.plotly_chart(fig)

            # Create success rates per task (stacked bar chart)
            task_success_per_task = task_df.groupby('task_name')['success'].value_counts().unstack().fillna(0)
            task_success_per_task = task_success_per_task.div(task_success_per_task.sum(axis=1), axis=0) * 100
            fig = px.bar(task_success_per_task, x=task_success_per_task.index, y=task_success_per_task.columns,
                         title="Success Rates per Task", labels={'x': 'Task Name', 'y': 'Percentage'})
            fig.update_xaxes(tickangle=0)  # Rotate x-axis labels horizontally
            st.plotly_chart(fig)
        else:
            st.info("No task data available yet.")


if __name__ == "__main__":
    main()