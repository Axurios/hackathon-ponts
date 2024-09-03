from io import StringIO
import os
import fitz
import openai
from dotenv import load_dotenv
from nltk.tokenize import sent_tokenize
# from flask_dotenv import DotEnv
from openai import OpenAI

load_dotenv(dotenv_path=".env")


def open_file(filepath):
    with open(filepath, "r", encoding="utf-8") as infile:
        return infile.read()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# print(os.getenv("OPENAI_API_KEY"))
# print(client.api_key)


def read_pdf(filename):
    context = ""

    # Open the PDF file
    with fitz.open(filename) as pdf_file:
        # Get the number of pages in the PDF file
        num_pages = pdf_file.page_count

        # Loop through each page in the PDF file
        for page_num in range(num_pages):
            # Get the current page
            page = pdf_file[page_num]

            # Get the text from the current page
            page_text = page.get_text().replace("\n", "")

            # Append the text to context
            context += page_text
    return context


def split_text(text, chunk_size=5000):
    chunks = []
    current_chunk = StringIO()
    current_size = 0
    sentences = sent_tokenize(text)
    for sentence in sentences:
        sentence_size = len(sentence)
        if sentence_size > chunk_size:
            while sentence_size > chunk_size:
                chunk = sentence[:chunk_size]
                chunks.append(chunk)
                sentence = sentence[chunk_size:]
                sentence_size -= chunk_size
                current_chunk = StringIO()
                current_size = 0
        if current_size + sentence_size < chunk_size:
            current_chunk.write(sentence)
            current_size += sentence_size
        else:
            chunks.append(current_chunk.getvalue())
            current_chunk = StringIO()
            current_chunk.write(sentence)
            current_size = sentence_size
    if current_chunk:
        chunks.append(current_chunk.getvalue())
    return chunks


filename = os.path.join(os.path.dirname(__file__), "filename.pdf")
document = read_pdf(filename)
chunks = split_text(document)


def initialize_memory():
    return [{"role": "system",
             "content": "You are a helpful assistant that helps understand the contents provided."}]


def add_new_message(memory, new):
    memory.append({"role": "user", "content": new})
    return memory


def gpt3_completion(user_message):
    response_gpt = client.chat.completions.create(
        model="gpt-4o-mini", messages=user_message
    )
    return response_gpt.choices[0].message.content


# return only the response, used to verify gpt3_completion
def ask_question_pdf(user_message, histo, texte=document):
    histo.append({"role": "system",
                  "content": f"you have this as your ground truth :{texte}"})
    add_new_message(memory=histo, new=user_message)
    return gpt3_completion(histo)
