import os
import PyPDF2
import re

def miner():
    # Miner function let's you choose a file to extract text from it and returns an array of paragraphs.
    filenames = [filename for filename in os.listdir("src\inputs")]

    print("Which article from the list would you like to turn into audio?")
    options = [(fn, file) for fn, file in enumerate(filenames)]
    for a in options:
        print(f"{a[0]}. {a[1]}")

    objn = int(input("Select your desired file number:"))
    objfile = os.path.join("src\inputs", options[objn][1])

    if os.path.splitext(options[objn][1])[1] == ".pdf":
        file = open(objfile, "rb")
        pdfReader = PyPDF2.PdfReader(file)
        content = ""
        for i, page in enumerate(pdfReader.pages):
            pageObj = page
            content += pageObj.extract_text()
        file.close()
        paragraphs = re.split(r'\n(?=[A-Z])', content)
        for i, paragraph in enumerate(paragraphs):
            paragraphs[i] = paragraph.replace('\n', ' ')
    elif os.path.splitext(options[objn][1])[1] == ".txt":
        file = open(objfile, "r", encoding='utf-8')
        paragraphs = file.readlines()
        for i, paragraph in enumerate(paragraphs):
            paragraphs[i] = paragraph.replace('\n', ' ')
        file.close()
    else:
        print("Filetype not supported.")

    return(paragraphs, os.path.splitext(options[objn][1])[0])

if __name__ == "__main__":
    print("This module is used to import a text mining function for pdf.")