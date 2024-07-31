import os
from langchain_openai import OpenAI
import PyPDF2

class LLM_RECOMMENDER:
    def __init__(self, api_key):
        self.api_key = api_key
        self.files_content = {}
        self.llm = OpenAI(api_key=api_key)

    def read_pdf(self, file_path):
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text

    def read_all_pdfs_in_directory(self, directory_path):
        files_content = {}
        for filename in os.listdir(directory_path):
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(directory_path, filename)
                files_content[filename] = self.read_pdf(file_path)
        self.files_content = files_content
        return files_content

    def analyze_pdf(self, file_name):
        if file_name not in self.files_content:
            raise ValueError(f"PDF file {file_name} not found in the provided directory.")
        file_content = self.files_content[file_name]
        response = self.llm.invoke(file_content, max_tokens=150)
        return response

    def analyze_all_pdfs(self):
        general_recommendations = {}
        for file_name, file_content in self.files_content.items():
            response = self.llm.invoke(file_content, max_tokens=150)
            general_recommendations[file_name] = response
        return general_recommendations