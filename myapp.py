import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Templates
prompts = {
    "Tech": {
        "analysis": """
        You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
        Please provide a professional evaluation on whether the candidate's profile aligns with the role by addressing the following points:

        1. Does the candidate's experience and skills match the job requirements?
        2. What are the strengths of the candidate in relation to the job description?
        3. What are the weaknesses or areas for improvement for the candidate in relation to the job description?

        Resume: {text}
        Job Description: {jd}
        """,
        "keywords": """
        You are a skilled ATS (Applicant Tracking System) scanner with expertise in data science and ATS functionality. Your task is to evaluate the resume against the provided job description. Please provide the following:

        1. The percentage match of the resume to the job description.
        2. A list of missing keywords that are essential for the job.
        3. Brief comments on any other noticeable shortcomings in the resume.
        4. Final thoughts on the candidate's suitability for the role.

        Resume: {text}
        Job Description: {jd}
        """,
        "improvement": """
        You are an experienced career coach with expertise in the tech industry. Your task is to review the provided resume against the job description.
        Please provide a detailed evaluation of the candidate's profile and suggest areas for improvement to increase their chances of getting the job. Include the following points:

        1. Skills or experiences that the candidate should highlight more prominently.
        2. Additional skills or certifications that would make the candidate a better fit for the job.
        3. Specific changes or additions to the resume that could make it more attractive to recruiters.

        Resume: {text}
        Job Description: {jd}
        """

        
    },
    "Business Administration": {
        "analysis": """
        You are an experienced Human Resource Manager with expertise in evaluating MBA candidates. Your task is to review the provided resume against the job description.
        Please provide a professional evaluation on whether the candidate's profile aligns with the role by addressing the following points:

        1. Does the candidate's experience and skills match the job requirements?
        2. What are the strengths of the candidate in relation to the job description?
        3. What are the weaknesses or areas for improvement for the candidate in relation to the job description?

        Resume: {text}
        Job Description: {jd}
        """,
        "keywords": """
        You are a skilled ATS (Applicant Tracking System) scanner with expertise in MBA roles. Your task is to evaluate the resume against the provided job description. Please provide the following:

        1. The percentage match of the resume to the job description.
        2. A list of missing keywords that are essential for the job.
        3. Brief comments on any other noticeable shortcomings in the resume.
        4. Final thoughts on the candidate's suitability for the role.

        Resume: {text}
        Job Description: {jd}
        """,
        "improvement": """
        You are an experienced career coach with expertise in MBA roles. Your task is to review the provided resume against the job description.
        Please provide a detailed evaluation of the candidate's profile and suggest areas for improvement to increase their chances of getting the job. Include the following points:

        1. Skills or experiences that the candidate should highlight more prominently.
        2. Additional skills or certifications that would make the candidate a better fit for the job.
        3. Specific changes or additions to the resume that could make it more attractive to recruiters.

        Resume: {text}
        Job Description: {jd}
        """
    }
}

# Streamlit app
st.title("Resume Enhancing")
st.text("Improve Your Resume")

# Job Domain Selection
job_domain = st.selectbox("Select the job domain", options=["Tech", "Business Administration"])

# Job Description and Resume Upload
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit1 = st.button("Analyze Strengths and Weaknesses")
submit2 = st.button("Evaluate Missing Keywords and Shortcomings")
submit3 = st.button("Suggest Areas for Improvement")

def handle_submission(submit, prompt_type):
    if submit and uploaded_file:
        try:
            text = input_pdf_text(uploaded_file)
            formatted_prompt = prompts[job_domain][prompt_type].format(text=text, jd=jd)
            response = get_gemini_response(formatted_prompt)
            st.subheader("Evaluation Results")
            st.write(response)
        except Exception as e:
            st.error(f"Error processing the file: {e}")
    elif submit and not uploaded_file:
        st.error("Please upload the resume")

handle_submission(submit1, "analysis")
handle_submission(submit2, "keywords")
handle_submission(submit3, "improvement")
