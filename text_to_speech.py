import streamlit as st
from gtts import gTTS
import tempfile
import os

def tts_page():
    st.subheader("Text-to-Speech Conversion")
    text = st.text_area("Enter text to convert to speech", height=200, 
                       value=st.session_state.get('selected_text', ''))
    
    if text:
        language = st.selectbox("Select Language", [
            ('English', 'en'),
            ('Spanish', 'es'),
            ('French', 'fr'),
            ('German', 'de'),
            ('Hindi', 'hi'),
            ('Telugu', 'te')
        ], format_func=lambda x: x[0])
        
        if st.button("Generate Speech"):
            with st.spinner("Creating audio..."):
                try:
                    tts = gTTS(text=text, lang=language[1], slow=False)
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                        tts.save(fp.name)
                        audio_bytes = open(fp.name, 'rb').read()
                        st.audio(audio_bytes, format='audio/mp3')
                        
                        st.download_button(
                            label="Download Audio",
                            data=audio_bytes,
                            file_name="speech.mp3",
                            mime="audio/mp3"
                        )
                except Exception as e:
                    st.error(f"Error in text-to-speech: {str(e)}")
                finally:
                    if 'fp' in locals():
                        try:
                            os.unlink(fp.name)
                        except:
                            pass