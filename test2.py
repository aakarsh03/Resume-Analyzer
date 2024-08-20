import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import time

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
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

salaries_data = {
    "Job Title": ["Data Scientist", "Software Engineer", "Product Manager", "Business Analyst", "DevOps Engineer"],
    "Average Salary (USD)": [120000, 110000, 130000, 100000, 115000]
}

# Create a DataFrame
salaries_df = pd.DataFrame(salaries_data)

# Prompt Templates for analysis
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
        """
    },
    "General Query":{
        "analysis": """
        The following query is related to a resume or job description analysis. Please provide a focused response based on the context of resumes and job descriptions:

        Query: {query}
        Context: The resume and job description are related to {job_domain}. 
        """
    }
}

# Streamlit app layout
st.title('Resume Analysis Tool')

# Job Domain Selection
job_domain = st.selectbox("Select the job domain", options=["Tech", "Business Administration"])

# Job Description and Resume Upload
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume (PDF)")

# Initialize submit_analysis variable
submit_analysis = False

# Submit button for analyzing the resume
if uploaded_file and jd:
    submit_analysis = st.button("Analyze Resume")

with st.spinner("Uploading and Analyzing..."):
    if submit_analysis:
        if uploaded_file and jd:
            try:
                text = input_pdf_text(uploaded_file)
                formatted_prompt = prompts[job_domain]["analysis"].format(text=text, jd=jd)

                time.sleep(2)

                response = get_gemini_response(formatted_prompt)
                st.subheader("Evaluation Results")
                st.write(response)

            except Exception as e:
                st.error(f"Error processing the file: {e}")
        else:
            st.error("Please upload the resume")

# Suggest areas for improvement button
submit_improvement = st.button("Suggest Areas for Improvement")

# Handle submission for suggesting areas for improvement
if submit_improvement:
    if uploaded_file and jd:
        try:
            text = input_pdf_text(uploaded_file)
            formatted_prompt = prompts[job_domain]["analysis"].format(text=text, jd=jd)

            time.sleep(2)

            response = get_gemini_response(formatted_prompt)
            st.subheader("Areas for Improvement")
            st.write(response)
        except Exception as e:
            st.error(f"Error processing the file: {e}")
    else:
        st.error("Please upload the resume")

if st.button("Show Info"):
    st.subheader("Mock Salaries for Tech Jobs")
    st.write(salaries_df)

    st.subheader("Average Salaries Bar Chart")
    plt.barh(salaries_df["Job Title"], salaries_df["Average Salary (USD)"])
    plt.xlabel('Average Salary (USD)')
    plt.title('Average Salaries for Tech Jobs')
    st.pyplot(plt)

# Query section for client questions
st.subheader("Ask any questions:")
query = st.text_input("Enter your question")


ask_spinner = st.empty()

if st.button("Ask"):
    if query:
        try:
            ask_spinner.text("Generating response...")
            formatted_prompt = prompts["General Query"]["analysis"].format(query=query, job_domain=job_domain)
            response = get_gemini_response(formatted_prompt)
            st.subheader("AI Response")
            st.write(response)
        except Exception as e:
            st.error(f"Error generating response: {e}")
        finally:
            ask_spinner.empty()
    else:
        st.warning("Please enter a question")

        
