# Usability Testing Tool

This is a usability testing tool built with Streamlit, designed for collecting and analyzing user data across various phases of a usability test. The tool allows you to track user progress, save responses to multiple questionnaires, and visualize task success rates, demographics, and user feedback.

## Features

- **Consent Form**: Users must agree to terms before proceeding with the test.
- **Demographic Questionnaire**: Collects basic demographic information such as name, age, occupation, and familiarity with similar tools.
- **Task Tracking**: Users select and perform tasks, while the app tracks task duration and success status.
- **Exit Questionnaire**: Collects user feedback about their experience and overall satisfaction with the usability test.
- **Data Visualization**: Visualizes task success rates and aggregated user data in charts.

## Requirements

- Python 3.8+
- Streamlit
- Pandas
- Plotly

To install the necessary dependencies, you can use the following:

```
pip install -r requirements.txt
```

## How to Run
1. Clone the repository:
```
git clone https://github.com/your-username/usabilitytestingapp.git
cd usabilitytestingapp
```

2. Install the required packages:
```
pip install -r requirements.txt
```
3. Run the app:
```
streamlit run app.py
```
4. Open your browser and navigate to ```http://localhost:8501``` to access the app.

## App Flow
The app is divided into several tabs, each corresponding to a phase of the usability test:
1. **Home**: Introduction and instructions for the usability test.
2. **Consent**: Users must read and agree to the consent form before continuing.
3. **Demographics**: Users fill out a short demographic questionnaire, including name, age, occupation, and familiarity with similar tools.
4. **Task**: Users select and perform a task. The app tracks the time taken for the task and whether the task was completed successfully.
5. **Exit Questionnaire**: After completing the task, users fill out a questionnaire about their experience, including satisfaction and difficulty ratings.
6. **Report**: A summary of all collected data, including consent, demographics, task performance, and exit feedback, is presented in an easy-to-read format with charts.

## Data Storage

User data is saved in CSV files, which are stored in the ```data``` folder:
- ```consent_data.csv```: Stores consent-related responses.
- ```demographic_data.csv```: Stores demographic information.
- ```task_data.csv```: Stores task-related data, including task success and duration.
- ```exit_data.csv```: Stores exit questionnaire responses.

## Visualizations
**Task Success Counts**: A bar chart showing the number of users who successfully completed each task.
**Task Success Rates**: A stacked bar chart showing the success rate for each task.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, feel free to fork the repository, make your changes, and submit a pull request.

MIT License

Copyright (c) [2025] [MARIO CASAS]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contact
For questions or feedback, please reach out to [MCasas548@gmail.com].

### Key Sections:
1. **Features**: A brief overview of what the app can do.
2. **Requirements**: Specifies the dependencies for the project.
3. **How to Run**: Instructions on setting up the project.
4. **App Flow**: Describes the different sections of the app and what the user will encounter.
5. **Data Storage**: Explains how data is saved and where it’s stored.
6. **Visualizations**: A quick overview of what types of charts are generated.
7. **Contributing**: Encourages contributions and describes how others can participate.
8. **License**: Mentions the licensing for the project.
9. **Contact**: Provides an email for questions or feedback.




