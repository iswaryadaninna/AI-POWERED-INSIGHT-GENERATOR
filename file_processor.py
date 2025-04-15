import streamlit as st
import pdfplumber
from docx import Document
from nltk.tokenize import word_tokenize
from text_summarizer import extract_quality_keywords, improved_summarize
import pyperclip

def file_upload_page():
    st.subheader("File Upload and Analysis")
    uploaded_file = st.file_uploader("Choose a file (PDF or DOCX)", type=["pdf", "docx"])
    
    if uploaded_file is not None:
        try:
            text = ""
            if uploaded_file.type == "application/pdf":
                with pdfplumber.open(uploaded_file) as pdf:
                    text = " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = Document(uploaded_file)
                text = " ".join([para.text for para in doc.paragraphs if para.text])
            
            if text.strip():
                st.session_state.selected_text = text
                st.text_area("Extracted Text", text, height=200)
                
                # Immediate keyword display without button
                keywords = extract_quality_keywords(text)
                st.markdown("**Keywords**")
                st.write(", ".join(keywords))
                
                # Summary section with customization
                word_count = st.number_input(
                    "Number of words for summary",
                    min_value=10,
                    max_value=2000,
                    value=100,
                    step=10
                )
                
                if st.button("Generate Summary"):
                    summary, word_count = improved_summarize(text, word_count)
                    st.write("Summary:", summary)
                
                # Copy functionality
                if st.button("Copy Text"):
                    pyperclip.copy(text)
                    st.success("Copied to clipboard!")
            else:
                st.warning("The file appears to be empty or couldn't be processed.")
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")