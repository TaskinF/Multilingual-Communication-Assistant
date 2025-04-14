# 🌐 Open Source LLM Translator

This is a FastAPI and Streamlit-based application that enables users to:
- Translate text into various languages,
- Analyze the sentiment of input text (Positive / Negative / Neutral),
- Paraphrase text in different writing styles (formal, informal, simplified),
- Perform a full analysis including all the above steps.

The app uses open-source LLMs (Gemma, LLaMA, Qwen) via the Groq API for fast and intelligent language processing.

---

## 🚀 Features

✅ Translate any text into supported target languages  
✅ Sentiment analysis using selected model  
✅ Paraphrasing with style control (e.g., formal, informal)  
✅ Unified analysis endpoint for translation, sentiment, and paraphrasing  
✅ Supports multiple LLMs: `gemma`, `llama`, `qwen`  
✅ Fast and lightweight backend using FastAPI  
✅ Simple and elegant frontend built with Streamlit  

---

## 🧠 LLMs Used via [Groq API](https://console.groq.com)

- `gemma2-9b-it`  
- `llama3-8b-8192`  
- `qwen-2.5-32b`

---

## 📦 Installation

1. **Clone the repo**
    git clone https://github.com/yourusername/llm-translator-nlp-assistant.git
    cd llm-translator-nlp-assistant

2. **Create virtual environment**
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows

3. **Install dependencies**
    pip install -r requirements.txt

4. **Set up environment variables Create a .env file in the project root:**
    GROQ_API_KEY=your_groq_api_key_here

5. **Run the FastAPI backend**
    uvicorn main:app --reload --port 8000

6. **Run the Streamlit frontend**
    streamlit run app.py

## API Endpoints
- Endpoint	  Method	Description
- /translate	POST	Translates text into the target language
- /sentiment	POST	Analyzes the sentiment of the text
- /paraphrase	POST	Paraphrases the input text
- /analyze	POST	Performs translation, sentiment, and paraphrasing in one request