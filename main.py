import os
from PyPDF2 import PdfReader
import pathlib
from dotenv import load_dotenv
import openai


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


def process_pdf(pdf_name: str, pdf_path: str, prompt: str):
    print(f"ready to analyze: {pdf_name}")
    text = get_pdf_text(pdf_path)
    analysis = analyze_resume_with_prompt(text, prompt)
    print("got analysis")
    output_name = f"outputs/{pdf_name.split('.')[0]}.txt"
    save_analysis_to_file(output_name, analysis)
    print(f"saved to {output_name}")
    print("-" * 50)


def main():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = get_prompt()

    for pdf in pathlib.Path("pdfs").glob("*.pdf"):
        process_pdf(pdf.name, str(pdf), prompt)


if __name__ == '__main__':
    main()
