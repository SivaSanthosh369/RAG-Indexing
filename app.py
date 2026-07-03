# app.py
import streamlit as st
import ollama

from pdf_processor import extract_and_chunk_pdf
from youtube_processor import extract_and_chunk_youtube #
from search_engine import get_relevant_chunks, format_bionic_text
from prompt_manager import get_adhd_system_instruction

st.set_page_config(page_title="FocusRAG Local", page_icon="⚡", layout="centered")

st.title("⚡ FocusRAG (Multi-Source)")
st.caption("PDF or YouTube!")

data_source = st.radio("Source:", ["PDF Document", "YouTube Video Link"])

chunks_ready = False

if data_source == "PDF Document":
    uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")
    if uploaded_file:
        if 'pdf_chunks' not in st.session_state:
            with st.spinner("Processing PDF in the background..."):
                st.session_state.active_chunks = extract_and_chunk_pdf(uploaded_file)
        chunks_ready = True
else:
    youtube_url = st.text_input("Enter YouTube Video Link:")
    if youtube_url:
        if 'yt_url_cached' not in st.session_state or st.session_state.yt_url_cached != youtube_url:
            with st.spinner("Fetching YouTube video transcript..."):
                res = extract_and_chunk_youtube(youtube_url)
                if res:
                    st.session_state.active_chunks = res
                    st.session_state.yt_url_cached = youtube_url
                    st.success("Video data is ready!")
                else:
                    st.error("Sorry, couldn't fetch subtitles for this video (please use videos with English/Malayalam subtitles).")
        if 'active_chunks' in st.session_state:
            chunks_ready = True

if chunks_ready and 'active_chunks' in st.session_state:
    ai_tone = st.selectbox("AI Tone:", ["Default", "Gamified", "Professional"])
    query = st.text_input("What do you want to know?")

    if query:
        relevant_items = get_relevant_chunks(query, st.session_state.active_chunks)
        
        if not relevant_items:
            st.warning("there is no relevant information found in the provided context. Please try a different query.")
        else:
            context_str = "\n".join([item["text"] for item in relevant_items])
            pages_found = sorted(list(set([item["page"] for item in relevant_items])))
            pages_str = ", ".join([f"{p}" for p in pages_found])
            
            system_instruction = get_adhd_system_instruction(mode=ai_tone.lower())
            user_prompt = f"Context:\n{context_str}\n\nQuestion: {query}"
            
            with st.spinner("Llama 3.2 Thinking..."):
                try:
                    response = ollama.chat(model='llama3.2:1b', messages=[
                        {'role': 'system', 'content': system_instruction},
                        {'role': 'user', 'content': user_prompt}
                    ])
                    
                    st.markdown("---")
                    st.subheader("⚡ answer:")
                    
                    raw_text = response['message']['content']
                    bionic_output = format_bionic_text(raw_text)
                    st.markdown(bionic_output)
                    
                    # Display the pages where the relevant information was found
                    st.markdown(f"📖 **Expected Pages:** `{pages_str}`")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.expander("real data?"):
                        for item in relevant_items:
                            st.write(f"**[{item['page']}]** {item['text']}")
                            st.markdown("---")
                    
                except Exception as e:
                    st.error(f"error occurred: {e}")