#  FocusRAG: Local & ADHD-Friendly Multi-Source RAG System

FocusRAG is a specialized **RAG (Retrieval-Augmented Generation)** application designed for individuals with **ADHD (Attention Deficit Hyperactivity Disorder)**. It aims to eliminate **Information Overload** when dealing with massive PDF textbooks or lengthy YouTube lecture videos by breaking down complex data into bite-sized, engaging, and highly readable insights.

The entire system runs **100% locally** using **Ollama (Llama 3.2)**, ensuring absolute data privacy and zero API costs.

---

##  Key Features

*   ** ADHD-Optimized UI:** A minimalist, zero-clutter interface designed to prevent visual distraction.
*   ** Micro-Chunking:** Automatically breaks down long text paragraphs into ultra-short chunks (2-3 sentences max) to match shorter attention spans.
*   ** Bionic Reading:** Automatically formats text outputs by bolding the first half of words to improve reading speed, comprehension, and fixation.
*   ** Custom Persona Switcher (Tone Selector):** Swap AI personas on the fly depending on your current mood or study requirements (`Default`, `Gamified Study Buddy`, or `Professional`).
*   ** Precision Navigation:** Displays exact reference locations—showing **Page Numbers** for PDFs and precise **Timestamps** for YouTube videos—allowing users to cross-check without scanning the entire source.
*   ** Context Window:** Uses expandable UI containers (`st.expander`) so users can check raw source data *only* when they explicitly want to, avoiding unnecessary cognitive fatigue.

---

##  Project Architecture

To keep the system modular and maintainable for production-level scaling, the code is structurally decoupled into 4 distinct functional components:

```text
├── app.py              # Streamlit UI & Core Application State Flow
├── pdf_processor.py    # PDF text extraction and Page-Level Micro-Chunking
├── youtube_processor.py# YouTube Transcript extraction & Time-Based Chunking (No API Key Required!)
├── search_engine.py    # Keyword matching, ranking, and Bionic Reading formatting
└── prompt_manager.py   # Houses the system instructions & persona prompt configurations
