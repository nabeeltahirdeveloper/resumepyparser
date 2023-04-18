import sys, fitz

def convertToText(fname):
    doc = fitz.open(fname)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

if __name__ == "__main__":
    print(convertToText("resume.pdf"))