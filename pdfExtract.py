import os
import chromadb
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
            ids.append("Page: " + str(page_number + 1) + ", Parragraph: " +  str(index + 1))

    # Close the PDF file
    pdf_document.close()

    return documents, metadatas, ids

def split_pdf_by_chunks(pdf_path, chunk_size=500):
    pdf_document = fitz.open(pdf_path)
    chunks_list = []

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        chunks_list.extend(chunks)

    pdf_document.close()
    return chunks_list


# Replace 'your_pdf_file.pdf' with the path to your PDF file
pdf_path = 'UN_Climate_Change.pdf'
docs, mets, ids = extract_pdf_sections(pdf_path)

print(len(docs), len(mets), len(ids))

chunks = split_pdf_by_chunks('UN_Climate_Change.pdf',1200)
print(chunks[0])

#Create a chroma collection and add the pdf data
isPersistent = True

if not isPersistent :
    # Get the chroma client and set it to use duckdb+parquet (a normal db like sqlite3 and the parquet file format [which is column oriented])
    client = chromadb.Client()
else:
    # Get a chromadb persistent (data remains after the end of the execution) client
    client = chromadb.PersistentClient(path="./db")

# Create a collection (think of it like it's an sql table)
collection = client.get_or_create_collection(name="UN_Climate_Change")

# Add the data to the collection
collection.add(
    documents = docs,
    metadatas = mets,
    ids = ids
)

results = collection.query(
    query_texts=["what is climate change?"],
    n_results=5
)

print("\n")
print(results)