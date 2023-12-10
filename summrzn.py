# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# import nltk
# import torch




# def summarize_text(file_path):
#     # Try different encodings if utf-8 doesn't work (e.g., 'latin-1', 'utf-16', etc.)
#     encodings_to_try = ['utf-8', 'latin-1']

#     for encoding in encodings_to_try:
#         try:
#             with open(file_path, 'rb') as file:
#                 FileContent = file.read().decode(encoding)
#             break  # Break the loop if decoding is successful
#         except UnicodeDecodeError:
#             continue  # Try the next encoding

#     checkpoint = "sshleifer/distilbart-cnn-12-6"

#     tokenizer = AutoTokenizer.from_pretrained(checkpoint)
#     model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

#     sentences = nltk.tokenize.sent_tokenize(FileContent)

#     # initialize
#     max_sequence_length = 1024
#     stride = 512
#     summarization_result = []

#     for i in range(0, len(sentences), stride):
#         chunk = " ".join(sentences[i:i+stride])
#         inputs = tokenizer(chunk, return_tensors="pt", max_length=max_sequence_length, truncation=True)

#         # Adjust parameters based on your needs
#         output = model.generate(**inputs, max_length=150, min_length=50, length_penalty=2.0, num_beams=4)
#         summarization_result.append(tokenizer.decode(*output, skip_special_tokens=True))

#     return ' '.join(summarization_result)

# if __name__ == "__main__":
#     # You can add a test or example here if needed
#     pass






# import nbformat
# from nbconvert import PythonExporter
# from IPython.display import display, HTML
# import os

# def run_ipynb(ipynb_path):
#     with open(ipynb_path, 'r', encoding='utf-8') as f:
#         nb_content = nbformat.read(f, as_version=4)
    
#     exporter = PythonExporter()
#     python_script, _ = exporter.from_notebook_node(nb_content)
    
#     # Execute the Python script in a temporary namespace
#     namespace = {}
#     try:
#         exec(python_script, namespace)
#     except Exception as e:
#         print(f"Error executing the notebook: {e}")
#         return
    
#     # Display the notebook output if available
#     if 'display' in namespace:
#         display(HTML(namespace['display']))

# if __name__ == "__main__":
#     # Specify the path to your .ipynb file
#     notebook_path = "notebook.ipynb"
    
#     if os.path.exists(notebook_path):
#         run_ipynb(notebook_path)
#     else:
#         print("Notebook file not found.")




# import google.colab
# import requests

# def run_colab_notebook(notebook_url):
#     # Mount Google Drive to save and load notebooks
#     google.colab.drive.mount('/content/drive')

#     # Fetch the notebook content
#     response = requests.get(notebook_url)
#     notebook_content = response.text

#     # Save the notebook locally
#     notebook_path = '/content/drive/MyDrive/colab_notebook.ipynb'
#     with open(notebook_path, 'w') as f:
#         f.write(notebook_content)

#     # Open the notebook in Colab
#     google.colab.drive.flush_and_unmount()
#     google.colab.shell.ShellAccess.notebook_open(notebook_path)

# # Example usage
# colab_notebook_url = "https://colab.research.google.com/drive/1eroAGdYwqlT1dAFr_SBSxWKb69gBGDAJ#scrollTo=zdwjrh8mGN7p"
# run_colab_notebook(colab_notebook_url)



# summerizer.py
from fpdf import FPDF

def convert_text_to_pdf(text_file_path, pdf_file_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    with open(text_file_path, 'r', encoding='utf-8') as text_file:
        text_content = text_file.read()
        pdf.multi_cell(0, 10, text_content)

    pdf.output(pdf_file_path)

    return pdf_file_path
