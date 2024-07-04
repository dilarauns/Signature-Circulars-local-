from langchain_community.llms import Ollama
import fitz 
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

ollama = Ollama(model="llama3")

def extract_information(page_text):
    prompt = "Belgede görülen tarih, adres ve her imzanın sahibini ve her bir kişinin rolünü belirleyin. Cevabların hepsiini türkçe yanıtla."
    response = ollama.invoke(prompt + " " + page_text)
    return response

def process_page(page_num, page_text):
    print(f"Processing page {page_num}")
    ollama_response = extract_information(page_text)
    return ollama_response

def process_pdf(pdf_file):
    pdf_document = fitz.open(pdf_file)
    overall_response = []

  
    with ThreadPoolExecutor() as executor:
        futures = []
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            page_text = page.get_text()
            futures.append(executor.submit(process_page, page_num, page_text))
        
        for future in as_completed(futures):
            overall_response.append(future.result())

    pdf_document.close()

    return overall_response

pdf_file = "imza_sirkuleri_ornek-rotated.pdf"
overall_response = process_pdf(pdf_file)

print("Belgedeki her bir imzanın sahibi, rolü, tarih ve adres bilgisi hakkında genel bilgi:")
for page_num, response in enumerate(overall_response):
    print(f"Sayfa {page_num}: {response}")


