from dotenv import load_dotenv
import streamlit as st
import base64
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def gemini_response(it, p_cont, pmpt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([it, p_cont[0], pmpt])
    return response.text

def it_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=r"Release-24.02.0-0\poppler-24.02.0\Library\bin")          # Convert the PDF to image
        first_page = images[0]

        img_byte_arr = io.BytesIO()                                # Convert to bytes
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App

st.set_page_config(page_title="ATS")
st.header("Application Tracking System")
it = st.text_area("Enter the Job Description: ", key="input")
if not it:
    st.error("No job description entered")
uploaded_file = st.file_uploader("Upload your resume here", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully :)")

s1 = st.button("Tell Me About my Resume")
s2 = st.button("Percentage match")
s3 = st.button("How to improve my resume")

ip1 = """
You are an experienced Technical expert and HR in the field of computer science. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

ip2 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of Computer Science Engineering and Technology field and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First, the output should come as a percentage and keywords missing should be in the next line and in the next line the final thoughts.
"""

ip3= """
You are a expert in computer science field with 30 years of experience. After evaluating the resume of the candidate depending upon the job description tell the candidate how they can improve their 
resume depending upon the missing skills and how to work on the missing skills. Highlight some key points that will helps the candidate to improve the resume.
"""

if s1:
    if uploaded_file is not None:
        pdf_content = it_setup(uploaded_file)
        response = gemini_response(it, pdf_content, ip1)
        st.subheader("Here's the response")
        st.write(response)
    else:
        st.write("No Resume Found !!!! Please upload your resume")

elif s2:
    if uploaded_file is not None:
        pdf_content = it_setup(uploaded_file)
        response = gemini_response(it, pdf_content, ip2)
        st.subheader("Here's the response")
        st.write(response)
    else:
        st.write("No Resume Found !!!! Please upload your resume")

elif s3:
    if uploaded_file is not None:
        pdf_content = it_setup(uploaded_file)
        response = gemini_response(it, pdf_content, ip3)
        st.subheader("Here's the response")
        st.write(response)
    else:
        st.write("No Resume Found !!!! Please upload your resume")

