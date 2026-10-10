
import streamlit as st
from pypdf import PdfReader
from google import genai
from docx import Document
import io
import re

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Question Paper Generator",
    page_icon="📝",
    layout="wide"
)

st.title("📝 AI Question Paper Generator")
st.caption("Generate structured question papers using AI")

# -----------------------------
# API KEY
# -----------------------------
api_key = st.secrets["GEMINI_API_KEY"]


# -----------------------------
# INPUTS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    subject = st.text_input(
        "Subject",
        placeholder="Example: Data Structures"
    )

    exam = st.text_input(
        "Exam",
        placeholder="Example: Mid Examination"
    )

    total_marks = st.number_input(
        "Total Marks",
        min_value=10,
        max_value=200,
        value=60
    )

with col2:
    easy = st.slider("Easy %", 0, 100, 30)
    medium = st.slider("Medium %", 0, 100, 50)
    hard = st.slider("Hard %", 0, 100, 20)

    st.write(
        f"Difficulty Total: **{easy + medium + hard}%**"
    )

# -----------------------------
# QUESTION CONFIGURATION
# -----------------------------
st.subheader("Question Configuration")

c1, c2, c3 = st.columns(3)

with c1:
    two_mark = st.number_input(
        "2-Mark Questions",
        0, 20, 10
    )

with c2:
    five_mark = st.number_input(
        "5-Mark Questions",
        0, 20, 6
    )

with c3:
    ten_mark = st.number_input(
        "10-Mark Questions",
        0, 10, 2
    )

# -----------------------------
# CO MAPPING
# -----------------------------
st.subheader("Course Outcomes")

co_text = st.text_area(
    "Enter Course Outcomes",
    value="""CO1: Understand fundamental concepts.
CO2: Apply concepts to solve problems.
CO3: Analyze algorithms and techniques."""
)

# -----------------------------
# SYLLABUS UPLOAD
# -----------------------------
st.subheader("Upload Syllabus")

uploaded_file = st.file_uploader(
    "Upload syllabus PDF",
    type=["pdf"]
)

syllabus_text = ""

if uploaded_file is not None:

    try:
        pdf = PdfReader(uploaded_file)

        for page in pdf.pages:
            extracted_text = page.extract_text()

            if extracted_text:
                syllabus_text += extracted_text + "\n"

        if syllabus_text.strip():

            st.success("Syllabus loaded successfully!")

            with st.expander("View extracted syllabus"):
                st.text(syllabus_text[:5000])

        else:
            st.warning(
                "No readable text found. Please upload a text-based PDF."
            )

    except Exception as e:
        st.error(f"Error reading PDF: {e}")

# -----------------------------
# GENERATE QUESTION PAPER
# -----------------------------
if st.button(
    "🚀 Generate Question Paper",
    use_container_width=True
):

    

    if not subject:
        st.error("Please enter the subject.")
        st.stop()

    if not syllabus_text.strip():
        st.error("Please upload a readable syllabus PDF.")
        st.stop()

    if easy + medium + hard != 100:
        st.error("Difficulty percentages must total 100%.")
        st.stop()

    expected_marks = (
        two_mark * 2 +
        five_mark * 5 +
        ten_mark * 10
    )

    if total_marks != expected_marks:
        st.error(
            f"Question configuration gives {expected_marks} marks, "
            f"but total marks is {total_marks}. Please correct it."
        )
        st.stop()

    # -----------------------------
    # GEMINI AI
    # -----------------------------
    try:

        client = genai.Client(api_key=api_key)

        prompt = f"""
You are an expert university question paper setter.

Generate a professional question paper.

SUBJECT:
{subject}

EXAM:
{exam}

TOTAL MARKS:
{total_marks}

SYLLABUS:
{syllabus_text}

COURSE OUTCOMES:
{co_text}

QUESTION DISTRIBUTION:

2-mark questions: {two_mark}
5-mark questions: {five_mark}
10-mark questions: {ten_mark}

DIFFICULTY DISTRIBUTION:

Easy: {easy}%
Medium: {medium}%
Hard: {hard}%

REQUIREMENTS:

1. Questions must be strictly based on the supplied syllabus.
2. Do not invent topics outside the syllabus.
3. Cover different units/topics.
4. Avoid duplicate questions.
5. Assign a Course Outcome (CO) to every question.
6. Assign a Bloom's Taxonomy level.
7. Assign difficulty: Easy, Medium or Hard.
8. Clearly mention marks.
9. Maintain the requested number of questions.
10. Make the paper suitable for B.Tech students.

FORMAT:

QUESTION PAPER

Subject: {subject}
Exam: {exam}
Maximum Marks: {total_marks}

SECTION A – 2 MARKS

Q1. Question
CO:
Bloom:
Difficulty:
Marks:

SECTION B – 5 MARKS

SECTION C – 10 MARKS

At the end provide:

VALIDATION SUMMARY
Total Questions:
Total Marks:
Difficulty Distribution:
CO Distribution:
Topics Covered:
"""

        with st.spinner("Generating question paper..."):

            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )

            result = response.text

        if not result:
            st.error("Gemini returned an empty response.")
            st.stop()

        # -----------------------------
        # DISPLAY
        # -----------------------------
        st.success("Question paper generated!")

        st.markdown("---")
        st.markdown(result)

        # -----------------------------
        # VALIDATION
        # -----------------------------
        st.subheader("🔍 Validation")

        question_count = len(
            re.findall(r"Q\d+\.", result)
        )

        st.write(
            f"Detected Questions: **{question_count}**"
        )

        expected_questions = (
            two_mark +
            five_mark +
            ten_mark
        )

        if question_count == expected_questions:
            st.success("✓ Question count is correct")
        else:
            st.warning(
                f"Expected {expected_questions} questions, "
                f"but detected {question_count}."
            )

        if "CO:" in result:
            st.success("✓ CO mapping detected")
        else:
            st.warning("CO mapping not detected")

        if "Bloom:" in result:
            st.success("✓ Bloom's taxonomy detected")
        else:
            st.warning("Bloom's taxonomy not detected")

        if "Difficulty:" in result:
            st.success("✓ Difficulty mapping detected")
        else:
            st.warning("Difficulty mapping not detected")

        # -----------------------------
        # TXT DOWNLOAD
        # -----------------------------
        st.download_button(
            "📥 Download Question Paper",
            result,
            file_name="AI_Question_Paper.txt",
            mime="text/plain"
        )

        # -----------------------------
        # DOCX DOWNLOAD
        # -----------------------------
        doc = Document()

        doc.add_heading(
            "AI Generated Question Paper",
            0
        )

        for line in result.split("\n"):
            if line.strip():
                doc.add_paragraph(line)

        buffer = io.BytesIO()

        doc.save(buffer)

        st.download_button(
            "📄 Download DOCX",
            buffer.getvalue(),
            file_name="AI_Question_Paper.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    except Exception as e:
        st.error(f"An error occurred: {e}")