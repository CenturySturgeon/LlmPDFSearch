import fitz  # PyMuPDF

def extract_pdf_sections(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Initialize an empty string to store the extracted text
    text = ""

    # Iterate through each page in the PDF
    for page_number in range(pdf_document.page_count):
        # Get the page
        page = pdf_document[page_number]
        # print(f"PAGE NUMBER {page_number + 1}\n")

        # Extract paragraphs from the page
        text = page.get_text("blocks")
        if page_number == 1:
            for block in text:
                print(block[4])
                print("\n")

    # Close the PDF file
    pdf_document.close()

    return text

# Replace 'your_pdf_file.pdf' with the path to your PDF file
pdf_path = 'TheRoadNotTaken.pdf'
extracted_text = extract_pdf_sections(pdf_path)