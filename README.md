# 📝 AI Question Paper Generator

## 📌 Project Overview

The **AI Question Paper Generator** is a Python-based web application that uses Google Gemini AI to generate structured question papers based on an uploaded syllabus PDF.

The application allows users to configure examination details, total marks, question distribution, and difficulty levels. It also generates questions with Course Outcome (CO) mapping and Bloom’s Taxonomy levels, helping make the question paper creation process more organized and efficient.

## ✨ Features

- **Subject and Exam Details:** Enter the subject name and examination name.
- **Syllabus PDF Upload:** Upload a PDF syllabus for question generation.
- **AI-Powered Generation:** Uses Google Gemini AI to generate questions based on the provided syllabus.
- **Customizable Marks:** Configure the total marks and the number of 2-mark, 5-mark, and 10-mark questions.
- **Difficulty Distribution:** Set the percentage of Easy, Medium, and Hard questions.
- **Course Outcome Mapping:** Associate questions with relevant Course Outcomes (COs).
- **Bloom’s Taxonomy:** Include a Bloom’s Taxonomy level for each question.
- **Validation Checks:** Check the question count and detect CO, Bloom’s Taxonomy, and difficulty labels.
- **Download Options:** Download the generated question paper as a TXT or DOCX file.
- **Interactive Interface:** Simple, user-friendly web interface powered by Streamlit.

## 🛠️ Technologies Used

- **Python** – Core programming language
- **Streamlit** – Web application interface
- **Google Gemini API** – AI-powered question generation
- **pypdf** – Extracting text from syllabus PDFs
- **python-docx** – Creating downloadable Word documents
- **Regular Expressions (`re`)** – Detecting question numbers for validation
- **io** – Managing document data in memory

## ⚙️ How It Works

1. Enter the subject and exam details.
2. Set the total marks for the question paper.
3. Configure the Easy, Medium, and Hard difficulty percentages so they total 100%.
4. Choose the number of 2-mark, 5-mark, and 10-mark questions.
5. Enter the Course Outcomes.
6. Upload a readable, text-based syllabus PDF.
7. Click **Generate Question Paper**.
8. The application sends the syllabus and configuration to Gemini AI.
9. Review the generated questions and validation results.
10. Download the question paper in TXT or DOCX format.

## 📋 Requirements

- Python 3.10 or a compatible Python version
- Google Gemini API key
- Internet connection for Gemini API access
- Required Python libraries

## 🚀 Installation and Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

Replace `YOUR-USERNAME` and `YOUR-REPOSITORY` with your GitHub username and repository name.

### Step 2: Open the project folder

```bash
cd YOUR-REPOSITORY
```

### Step 3: Install the dependencies

```bash
pip install streamlit pypdf google-genai python-docx
```

### Step 4: Configure the Gemini API key

Create a folder named `.streamlit` in your project directory.

Inside that folder, create a file named `secrets.toml` and add:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

Replace the placeholder with your own API key.

**Security note:** Never upload your actual API key or `secrets.toml` file to a public GitHub repository. Keep your credentials private.

### Step 5: Run the application

If your Python file is named `App.py`, run:

```bash
streamlit run App.py
```

The application will open in your browser.

## 📁 Project Structure

```text
AI-Question-Paper-Generator/
│
├── App.py
├── README.md
├── requirements.txt
└── .streamlit/
    └── secrets.toml
```

**Important:** Add `.streamlit/secrets.toml` to `.gitignore` before committing your project.

Example `.gitignore`:

```gitignore
.streamlit/secrets.toml
__pycache__/
.venv/
venv/
```

## 📦 Dependencies

You can create a `requirements.txt` file containing:

```text
streamlit
pypdf
google-genai
python-docx
```

Install all dependencies with:

```bash
pip install -r requirements.txt
```

## 🎯 Use Cases

- Creating practice question papers for students
- Preparing draft examination papers from a syllabus
- Supporting teachers in question paper preparation
- Organizing questions by marks and difficulty
- Mapping questions to Course Outcomes and Bloom’s Taxonomy

## 🔮 Future Enhancements

- Export question papers directly to PDF
- Add multiple-choice questions (MCQs)
- Support additional syllabus file formats
- Improve automatic validation of generated questions
- Add unit-wise question distribution
- Provide answer keys and explanations
- Improve document formatting and examination templates

## ⚠️ Limitations

- The quality of generated questions depends on the readability and completeness of the uploaded syllabus.
- Scanned PDFs without extractable text may not work.
- A valid Gemini API key and internet access are required.
- AI-generated questions and their CO mappings should be reviewed by a teacher before official use.
- The current validation checks detect certain labels and question counts; they do not guarantee the academic correctness of the paper or independently verify every generated mark and difficulty assignment.

