import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Initialize an empty string to store the extracted text
    text = ""

    # Iterate through each page in the PDF
    for page_number in range(pdf_document.page_count):
        # Get the page
        page = pdf_document[page_number]

        # Extract text from the page
        text += page.get_text()

    # Close the PDF file
    pdf_document.close()

    return text

# Replace 'your_pdf_file.pdf' with the path to your PDF file
pdf_path = 'ChromaDB.pdf'
extracted_text = extract_text_from_pdf(pdf_path)

# Print or use the extracted text as needed
print(extracted_text)
