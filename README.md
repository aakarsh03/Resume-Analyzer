# Resume-Analyzer

A powerful tool to analyze resumes against job descriptions using AI. This tool helps in assessing the alignment of a candidate's profile with the job requirements, identifying strengths, and suggesting areas for improvement.

## Features

- Upload resumes in PDF format and analyze them.
- Compare resumes against job descriptions to identify strengths and weaknesses.
- Generate suggestions for improvement.
- Visualize salary data for various job titles.
- Ask AI-driven questions related to resumes and job descriptions.

## Technologies Used

- Python
- Streamlit
- Google Generative AI
- PyPDF2
- Matplotlib
- Pandas

## Setup

To configure the project, follow these steps:

1. **Create a `.env` File**
   - In the root directory of the project, create a file named `.env`.

2. **Obtain Your Gemini API Key**
   - Sign up or log in to Google Generative AI and obtain your API key.

3. **Add the API Key to the `.env` File**
   - Open the `.env` file and add the following line, replacing `YOUR_API_KEY_HERE` with your actual Gemini API key:
     ```
     GOOGLE_API_KEY=YOUR_API_KEY_HERE
     ```

4. **Save the `.env` File**
   - Make sure to save the `.env` file with the API key included.

By following these steps, you will configure the application to use your Gemini API key.


```markdown
## Usage

1. Upload your resume in PDF format.
2. Paste the job description.
3. Click on "Analyze Resume" to get insights.
4. Optionally, ask specific questions in the query section.
## Main Image

![Main Image](https://github.com/your-username/Resume-Analyzer/raw/main/assets/main.png)



