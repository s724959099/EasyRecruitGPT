import io
import os
from PyPDF2 import PdfReader
import pathlib
from dotenv import load_dotenv
import openai
import streamlit as st


def get_pdf_text(path: str) -> str:
    reader = PdfReader(path)
    return "".join(page.extract_text() for page in reader.pages)


def get_prompt() -> str:
    with open("prompt.txt") as f:
        return f.read()


def analyze_resume_with_prompt(resume: str, prompt: str) -> str:
    messages = [
        {"role": "system", "content": "你現在是一個專業的 ai 工程師，你需要幫忙篩選履歷"},
        {"role": "user", "content": prompt.replace("{{prompt}}", resume)}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content


def save_analysis_to_file(name: str, analysis: str):
    with open(name, "w") as f:
        f.write(analysis)


def process_pdf(pdf_name: str, bytes_data: io.BytesIO, prompt: str) -> str:
    print(f"ready to analyze: {pdf_name}")
    text = get_pdf_text(bytes_data)
    analysis = analyze_resume_with_prompt(text, prompt)
    return analysis


def main():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = get_prompt()

    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        processed_data = process_pdf(uploaded_file.name, io.BytesIO(bytes_data), prompt)
        st.markdown(processed_data)


if __name__ == '__main__':
    main()
