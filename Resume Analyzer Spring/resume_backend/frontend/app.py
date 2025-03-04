import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import time
import requests

# Load environment variables
load_dotenv()

# Configure the generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to interact with generative AI model
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

# Function to extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

# Backend API URL
backend_url = "http://localhost:8080/api/resume/analyze"

salaries_data = {
    "Job Title": ["Data Scientist", "Software Engineer", "Product Manager", "Business Analyst", "DevOps Engineer"],
    "Average Salary (USD)": [120000, 110000, 130000, 100000, 115000]
}

salaries_df = pd.DataFrame(salaries_data)

# Prompt Templates
prompts = {
    "Tech": {
        "analysis": """
        You are an experienced Technical HR Manager. Evaluate this resume for a Tech job.
        
        - Does the experience match the job?
        - What are the strengths and weaknesses?
        
        Resume: {text}
        Job Description: {jd}
        """
    },
    "Business Administration": {
        "analysis": """
        You are an HR expert evaluating MBA candidates. Assess this resume for a Business job.
        
        - Does the experience match the job?
        - Strengths and weaknesses?
        
        Resume: {text}
        Job Description: {jd}
        """
    },
    "General Query": {
        "analysis": "Query: {query}\nContext: The resume and job description relate to {job_domain}."
    }
}

# Streamlit UI
st.title('Resume Analysis Tool')

job_domain = st.selectbox("Select the job domain", options=["Tech", "Business Administration"])
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume (PDF)")

submit_analysis = st.button("Analyze Resume") if uploaded_file and jd else None

if submit_analysis:
    with st.spinner("Uploading and Analyzing..."):
        try:
            text = input_pdf_text(uploaded_file)
            formatted_prompt = prompts[job_domain]["analysis"].format(text=text, jd=jd)

            # Send resume to backend as a file
            files = {"file": uploaded_file}
            backend_response = requests.post(backend_url, files=files)

            if backend_response.status_code == 200:
                st.subheader("Backend Response")
                st.write(backend_response.text)
            else:
                st.error(f"Backend Error: {backend_response.status_code}\n{backend_response.text}")

            # Get AI evaluation
            response = get_gemini_response(formatted_prompt)
            st.subheader("AI Evaluation")
            st.write(response)

        except Exception as e:
            st.error(f"Error processing: {e}")

# Button for suggesting improvements
if st.button("Suggest Areas for Improvement"):
    if uploaded_file and jd:
        try:
            text = input_pdf_text(uploaded_file)
            formatted_prompt = prompts[job_domain]["analysis"].format(text=text, jd=jd)
            response = get_gemini_response(formatted_prompt)
            st.subheader("Areas for Improvement")
            st.write(response)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Upload a resume and enter job description first.")

# Salary Data Visualization
if st.button("Show Info"):
    st.subheader("Mock Salaries for Tech Jobs")
    st.write(salaries_df)
    
    st.subheader("Average Salaries Bar Chart")
    plt.barh(salaries_df["Job Title"], salaries_df["Average Salary (USD)"])
    plt.xlabel('Average Salary (USD)')
    plt.title('Average Salaries for Tech Jobs')
    st.pyplot(plt)

# General Query Section
st.subheader("Ask any questions:")
query = st.text_input("Enter your question")

if st.button("Ask"):
    if query:
        try:
            formatted_prompt = prompts["General Query"]["analysis"].format(query=query, job_domain=job_domain)
            response = get_gemini_response(formatted_prompt)
            st.subheader("AI Response")
            st.write(response)
        except Exception as e:
            st.error(f"Error generating response: {e}")
    else:
        st.warning("Enter a question first.")
