import os
from PyPDF2 import PdfReader
import pathlib
from dotenv import load_dotenv
import openai


def get_pdf_text(path: str) -> str:
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def analyze_resume(resume: str) -> str:
    with open("prompt.txt") as f:
        prompt = f.read()

    messages = [
        {
            "role": "system",
            "content": "你現在是一個專業的 ai 工程師，你需要幫忙篩選履歷",
        },
        {
            "role": "user",
            "content": prompt.replace("{{prompt}}", resume)
        },
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content


if __name__ == '__main__':
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    for pdf in pathlib.Path("pdfs").glob("*.pdf"):
        print(f"ready to analyze: {pdf.name}")
        text = get_pdf_text(str(pdf))
        analysis = analyze_resume(text)
        print("got analysis")
        name = f"outputs/{pdf.name.split('.')[0]}.txt"
        with open(name, "w") as f:
            f.write(analysis)
        print(f"saved to {name}")
        print("-" * 50)
