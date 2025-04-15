import streamlit as st
from deep_translator import GoogleTranslator
from googletrans import LANGUAGES

def translate_page():
    st.subheader("Text Translation")
    text = st.text_area("Enter text to translate", value=st.session_state.get('selected_text', ''))
    
    if text:
        # Language selection with full names
        language = st.selectbox("Select Language", list(LANGUAGES.values()))
        
        # Get language code
        lang_code = [code for code, name in LANGUAGES.items() if name == language][0]
        
        if st.button("Translate"):
            with st.spinner("Translating..."):
                try:
                    translation = GoogleTranslator(
                        source='auto', 
                        target=lang_code
                    ).translate(text)
                    
                    st.session_state.selected_text = translation
                    st.text_area("Translated Text", translation, height=200)
                except Exception as e:
                    st.error(f"Translation error: {str(e)}")