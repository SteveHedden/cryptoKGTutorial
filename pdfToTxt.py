import PyPDF2
import os

directory = <directory>
rawWhitePapers = directory + "/rawWhitePapers"
txtWhitePapers = directory + "/txtWhitePapers"
for filename in os.listdir(rawWhitePapers):
    print(filename)
    if filename == ".DS_Store":
        pass
    else:
        pdffileobj = open(directory + "/rawWhitePapers" + "/" + filename, 'rb')
        # create reader variable that will read the pdffileobj
        pdfreader = PyPDF2.PdfFileReader(pdffileobj)
        # This will store the number of pages of this pdf file
        x = pdfreader.numPages
        for page in range(x):
            pageobj = pdfreader.getPage(page)
            text = pageobj.extractText()
            file1 = open(txtWhitePapers + "/" + filename + ".txt", "a")
            file1.writelines(text)
            file1.close()
