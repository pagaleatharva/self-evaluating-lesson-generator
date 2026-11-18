# 📚 Self-Evaluating AI Lesson Generator

An AI-powered lesson generation system that creates beginner-friendly educational content, evaluates its quality using six strict criteria, and automatically improves rejected lessons through a LangGraph workflow.

## 🚀 Project Overview

The Self-Evaluating AI Lesson Generator uses Generative AI to create educational lessons for beginners.

Unlike a basic AI content generator, this project includes a separate evaluation process. Every generated lesson is checked for accuracy, clarity, examples, technical terminology, topic coverage, and teaching flow.

If a lesson fails the evaluation, the evaluator provides feedback to the generator. The system then regenerates the lesson using that feedback, with a maximum of two retries.

The project also uses SQLite to store previous lesson results and rejection feedback, helping future runs learn from past evaluations.

## ✨ Key Features

- **AI Lesson Generation:** Creates structured, beginner-friendly lessons.
- **Automated Quality Evaluation:** Evaluates lessons using six predefined criteria.
- **Feedback-Based Regeneration:** Improves rejected lessons using evaluator feedback.
- **Retry Mechanism:** Allows a maximum of two regeneration attempts.
- **Rejection History:** Stores and displays failed evaluation attempts.
- **Persistent Memory:** Saves lesson history and evaluation feedback using SQLite.
- **Streamlit Interface:** Provides an interactive interface for generating and reviewing lessons.

## 🧠 Evaluation Criteria

Each generated lesson is evaluated using six strict PASS/FAIL checks:

| Criteria | Description |
|---|---|
| Accuracy | Checks whether the information is factually correct. |
| Beginner Language | Ensures explanations are easy to understand. |
| Examples | Checks for at least two useful examples. |
| Jargon Explanation | Ensures difficult technical terms are explained. |
| Key Coverage | Checks topic meaning, importance, and working. |
| Teaching Flow | Evaluates the logical structure of the lesson. |

A lesson is approved only when all six criteria pass.

## 🏗️ Project Architecture

```text
self-evaluating-lesson-generator/
│
├── agents/
│   ├── __init__.py
│   ├── generator.py
│   └── evaluator.py
│
├── evaluation/
│   ├── __init__.py
│   └── rubric.py
│
├── memory/
│   ├── __init__.py
│   └── database.py
│
├── workflow/
│   ├── __init__.py
│   └── graph.py
│
├── images/
│
├── app.py
├── main.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

**Note:** The `.env` file and SQLite database are kept locally and should not be uploaded to GitHub.

## ⚙️ Technologies Used

- Python
- LangChain
- LangGraph
- Groq API
- Pydantic
- Streamlit
- SQLite
- python-dotenv

## 🔄 How It Works

1. The user enters a learning topic.
2. The Generator Agent creates a beginner-friendly lesson.
3. The Evaluator Agent checks the lesson against six criteria.
4. If all criteria pass, the lesson is approved.
5. If any criterion fails, the evaluator generates improvement feedback.
6. The Generator Agent uses the feedback to regenerate the lesson.
7. The process repeats until the lesson passes or the maximum retry limit is reached.
8. The system saves the result, evaluation and rejection history in SQLite.

## 📸 Application Screenshots

## 📸 Application Screenshots

### 1. Main Application Interface

![Main Application Interface](images/Screenshot%202026-11-18%20at%209.50.04%E2%80%AFPM.png)

[View Screenshot 1](https://github.com/pagaleatharva/self-evaluating-lesson-generator/blob/main/images/Screenshot%202026-11-18%20at%209.50.04%E2%80%AFPM.png)

### 2. Lesson Generation

![Lesson Generation](images/Screenshot%202026-11-18%20at%209.50.12%E2%80%AFPM.png)

[View Screenshot 2](https://github.com/pagaleatharva/self-evaluating-lesson-generator/blob/main/images/Screenshot%202026-11-18%20at%209.50.12%E2%80%AFPM.png)

### 3. Evaluation Results

![Evaluation Results](images/Screenshot%202026-11-18%20at%209.50.20%E2%80%AFPM.png)

[View Screenshot 3](https://github.com/pagaleatharva/self-evaluating-lesson-generator/blob/main/images/Screenshot%202026-11-18%20at%209.50.20%E2%80%AFPM.png)

*Replace the image filenames above with your actual screenshot filenames if they are different.*

## 💻 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/self-evaluating-lesson-generator.git
```

### 2. Navigate to the Project

```bash
cd self-evaluating-lesson-generator
```

### 3. Create a Virtual Environment

```bash
uv venv
```

### 4. Activate the Virtual Environment

For macOS/Linux:

```bash
source .venv/bin/activate
```

### 5. Install Dependencies

```bash
uv pip install -r requirements.txt
```

### 6. Configure the API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from [Groq Console](https://console.groq.com/keys).

Never upload your actual API key to GitHub.

### 7. Run the Streamlit Application

```bash
streamlit run app.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

## 🧪 Example

**Input Topic:** Introduction to RAG

**Expected Process:**

- Generate a beginner-friendly RAG lesson.
- Evaluate the lesson using six quality criteria.
- Identify failed checks, if any.
- Regenerate the lesson using evaluator feedback.
- Display the final evaluation and rejection history.
- Save the run in SQLite memory.

## 🧠 Memory and Self-Improvement

The project uses SQLite to maintain persistent lesson history.

It stores:
- Learning topics
- Generated lessons
- Evaluation results
- Rejection logs
- Workflow status
- Number of regeneration attempts

Previous rejection feedback for the same topic is retrieved and included in future generation prompts.

This provides prompt-level improvement based on previous runs. It does not retrain the underlying language model.

## 🔮 Future Improvements

- Support for multiple learning topics and subject areas.
- More detailed evaluation rubrics.
- Advanced lesson personalization.
- Improved memory retrieval.

## 👨‍💻 Author

**Atharva Pagale**

B.E. Computer Engineering Graduate | GenAI & Data Enthusiast

- GitHub: https://github.com/pagaleatharva
- LinkedIn: https://www.linkedin.com/in/atharva-pagale-224786296/

---

⭐ If you find this project interesting, consider giving the repository a star.
