import openai
# from application.webapp.nlp.main import convertFileToText
import json

from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser, PDFSyntaxError
import io
from pdfminer.converter import PDFPageAggregator, TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import (
    LAParams,
    LTChar,
    LTFigure,
    LTTextBox,
    LTTextLine,
    LTTextLineHorizontal,
)
import time
from pyresparser import ResumeParser
start_time = time.time()


def extract_text_from_pdf(pdf_path):
    """
    Helper function to extract the plain text from .pdf files
    :param pdf_path: path to PDF file to be extracted (remote or local)
    :return: iterator of string of extracted text
    """
    # https://www.blog.pythonlibrary.org/2018/05/03/exporting-data-from-pdfs-with-python/
    if not isinstance(pdf_path, io.BytesIO):
        # extract text from local pdf file
        with open(pdf_path, "rb") as fh:
            try:
                for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                    resource_manager = PDFResourceManager()
                    fake_file_handle = io.StringIO()
                    converter = TextConverter(
                        resource_manager, fake_file_handle, laparams=LAParams()
                    )
                    page_interpreter = PDFPageInterpreter(resource_manager, converter)
                    page_interpreter.process_page(page)

                    text = fake_file_handle.getvalue()
                    yield text

                    # close open handles
                    converter.close()
                    fake_file_handle.close()
            except PDFSyntaxError:
                return
    else:
        # extract text from remote pdf file
        try:
            for page in PDFPage.get_pages(
                pdf_path, caching=True, check_extractable=True
            ):
                resource_manager = PDFResourceManager()
                fake_file_handle = io.StringIO()
                converter = TextConverter(
                    resource_manager, fake_file_handle, laparams=LAParams()
                )
                page_interpreter = PDFPageInterpreter(resource_manager, converter)
                page_interpreter.process_page(page)

                text = fake_file_handle.getvalue()
                yield text

                # close open handles
                converter.close()
                fake_file_handle.close()
        except PDFSyntaxError:
            return




def convertFileToText(fileName):
    ext = fileName.split(".")[-1]
    # print("file:", fileName)
    if ext == "pdf":
        # print("working as pdf")
        text = ""
        for page in extract_text_from_pdf(fileName):
            text += " " + page
        return text
    elif ext == "docx":
        text = getTextFromDocx(fileName)
        return text
    elif ext == "doc":
        text = getTextFromDocx(fileName)
        return text
    else:
        None



def chat(text):
    global messages
    messages.append({"role": "user", "content": text})
    return openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages,
      max_tokens= 2000
    )


extractedText = convertFileToText("OmkarResume.pdf")
finalText = f"""
         create a json parsing from below text \n {extractedText}
         """
messages = []

answer = chat(finalText)

# save json file

with open('OmkarResume-gpt.json', 'w') as outfile:
    json.dump(json.loads(answer['choices'][0]['message']['content']), outfile)


end_time = time.time()

execution_time = end_time - start_time

data = ResumeParser('OmkarResume.pdf', skills_file='skills.csv').get_extracted_data()

with open('OmkarResume-parser.json', 'w') as outfile:
    json.dump(data, outfile)

print("Execution time:", execution_time)


# if __name__ == "__main__":
#     messages = []
#     while True:s
#         text = input("You: ")
#         finalText = f"""
#         create a cover letter according to these parameters {text}
#         max1000 limit"""
#         # if text == "exit":
#         #     break
#         response = chat(finalText)
#         print("AI: ", response['choices'][0]['message']['content'])