import streamlit as st 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import pipeline
import torch
import base64
from audio import main as audio_main # Importing the main function from audio.py

# txtfile = summarize_text(os.path.join(r"downloads", f"{sanitized_title}.wav"))




# model and tokenizer loading
checkpoint = "LaMini-Flan-T5-248M"
tokenizer = T5Tokenizer.from_pretrained(checkpoint)
base_model = T5ForConditionalGeneration.from_pretrained(checkpoint, device_map='auto', torch_dtype=torch.float32)

# file loader and preprocessing
def file_preprocessing(file):
    loader = PyPDFLoader(file)
    pages = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    
    final_texts = ""

    for text in pages:
        # Send at most 250 words to the summarization model
        chunk_size = 250
        num_chunks = len(text.page_content.split()) // chunk_size + 1

        for i in range(num_chunks):
            start_idx = i * chunk_size
            end_idx = (i + 1) * chunk_size
            segment = text.page_content.split()[start_idx:end_idx]

            # Apply summarization on the segment
            pipe_sum = pipeline(
                'summarization',
                model=base_model,
                tokenizer=tokenizer,
                max_length=250,
                min_length=25)

            result_segment = pipe_sum(' '.join(segment))
            summary_segment = result_segment[0]['summary_text']

            # Concatenate the summaries
            final_texts += summary_segment
    
    return final_texts

# LLM pipeline
def llm_pipeline(filepath):
    input_text = file_preprocessing(filepath)
    return input_text

@st.cache_data
# function to display the PDF of a given file 
def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

# streamlit code 
st.set_page_config(layout="wide")

def main():
    st.title("Document Summarization App using Language Model")

    uploaded_file = st.file_uploader("Upload your PDF file", type=['pdf'])

    if uploaded_file is not None:
        if st.button("Summarize"):
            col1, col2 = st.columns(2)
            filepath = "data/"+uploaded_file.name
            with open(filepath, "wb") as temp_file:
                temp_file.write(uploaded_file.read())
            with col1:
                st.info("Uploaded File")
                pdf_view = displayPDF(filepath)

            with col2:
                summary = llm_pipeline(filepath)
                st.info("Summarization Complete")
                st.success(summary)

if __name__ == "__main__":
    main()