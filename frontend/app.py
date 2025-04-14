import streamlit as st
import requests

st.set_page_config(page_title="LLM Translator", page_icon="🌐")
st.title("🌐 Smart LLM Translation Assistant")

st.markdown("This app analyzes your natural language input and performs translation, sentiment analysis, or paraphrasing.")

text = st.text_area("✏️ Please enter the text to analyze:", height=150, placeholder="E.g., This is a terrible product, I would never buy it.")

language = st.selectbox("🌍 Target Language", ["Turkish", "English", "Germany", "French"])
style = st.selectbox("✍️ Paraphrasing Style", ["simplified", "informal", "formal"])
model = st.selectbox("🤖 Model Selection", ["llama", "qwen", "gemma"])

submit = st.button("🚀 Submit")

if submit and text:
    with st.spinner("Analyzing the text..."):
        response = requests.post("http://127.0.0.1:8000/analyze", json={
            "text": text,
            "language": language,
            "style": style,
            "model": model
        })
        if response.status_code == 200:
            result = response.json()
            st.success("✅ Analysis completed!")

            st.markdown(f"### 🔄 Translated Text:\n{result['translated_text']}")
            st.markdown(f"### 😊 Sentiment Analysis: `{result['sentiment']}`")
            st.markdown(f"### ✍️ Paraphrased Text ({result['style']}):\n{result['paraphrased_text']}")
        else:
            st.error("🚫 API request failed.")
