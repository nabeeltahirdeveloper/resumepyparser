import openai
from application.webapp.nlp.main import convertFileToText
import json

import time
from pyresparser import ResumeParser
start_time = time.time()



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