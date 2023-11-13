import os
import fitz  # PyMuPDF

def extract_pdf_sections(pdf_path):
    documents = []
    metadatas = []
    ids = []
    idIndex = 0

    # Get the document's name
    document_name = os.path.basename(pdf_path)
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Initialize an empty string to store the extracted text
    text = ""

    # Iterate through each page in the PDF
    for page_number in range(pdf_document.page_count):
        # Get the page
        page = pdf_document[page_number]

        # Extract paragraphs from the page
        text = page.get_text("blocks")
        
        for index, block in enumerate(text):
            documents.append(block[4])
            metadatas.append({"source": document_name, "page": page_number + 1, "paragraph":  index + 1})
            ids.append("id" + str(idIndex + 1))

    # Close the PDF file
    pdf_document.close()

    return documents, metadatas, ids

# Replace 'your_pdf_file.pdf' with the path to your PDF file
pdf_path = 'TheRoadNotTaken.pdf'
docs, mets, ids = extract_pdf_sections(pdf_path)

print(len(docs), len(mets), len(ids))
