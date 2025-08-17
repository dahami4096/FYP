# 🤖 AI Personalized Learning Assistant

This is  multi-page web application built with Streamlit that acts as a personalized AI tutor. It assesses a user's skill level in a chosen programming language, provides a full curriculum with an AI-powered chatbot, and evaluates their mastery through final assignments.

---
## ✨ Features

- **User Authentication:** Secure login and signup system.
- **Dynamic Subject Selection:** Easily extendable to new subjects by adding a curriculum file.
- **Adaptive Placement Quiz:** A multi-stage quiz to determine the user's entry point into the curriculum.
- **Full Learning Curriculum:** Structured, topic-by-topic learning path with progress tracking.
- **AI Tutor Chatbot:** An interactive chatbot on each lesson page for asking questions.
- **Final Assignments & Re-evaluation:** AI-generated assignments to test mastery.
- **Personalized Feedback:** If a user fails an assignment, the AI provides feedback on which topics to review.
- **Review Mode:** Completed lessons can be freely reviewed at any time.
- **Progress Dashboard:** A profile page to visualize progress and scores across all subjects.

---
## 🛠️ Tech Stack

- **Framework:** Python, Streamlit
- **Database:** SQLite
- **AI/LLM:** OpenAI API compatible (using OpenRouter.ai)

---
## 🚀 Setup and Installation

Follow these steps to set up and run the project on your local machine.

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd <your-repository-name>
```

### 2. Create and Activate Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies.

- **Windows:**
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```
### 3. Install Dependencies
Install all the required Python packages from the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
This project requires an API key for the language model.

- Create a new file in the root of the project directory named `.env`.
- Open the `.env` file and add your API key in the following format:
  ```
  OPENROUTER_API_KEY="your_api_key_here"
  ```
### 5. Initialize the Database
The SQLite database file (`learning_app.db`) will be created automatically in the root directory the first time you run the application.

### 6. Run the Application
Once the setup is complete, run the following command in your terminal:
```bash
streamlit run app.py
```
The application should now be running and accessible in your web browser.

---
## 📂 Project Structure
```
├── .streamlit/
├── assets/             # CSS files
├── curriculum/         # JSON files for each subject's curriculum
├── modules/            # Backend logic (auth, db, llm, helpers)
├── pages/              # The visible pages of the app
├── .gitignore          # Files to be ignored by Git
├── app.py              # Main entry point (router)
├── README.md           # This file
└── requirements.txt