from fastapi import FastAPI, Request
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
from dotenv import load_dotenv
import os
from langchain.prompts import ChatPromptTemplate

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Model Selection
def get_model(model_name: str):
    supported_models = {
        "gemma": "gemma2-9b-it",
        "llama": "llama3-8b-8192",
        "qwen": "qwen-2.5-32b"
    }
    if model_name not in supported_models:
        raise ValueError("Unsupported model. Choose from: gemma, llama, qwen")
    return ChatGroq(model=supported_models[model_name], groq_api_key=groq_api_key)

# Prompt template
system_template = (
    "You are a professional translation engine designed to convert text between languages with maximum accuracy. "
    "STRICTLY follow these rules:\n"
    "1. Translate the following text into {language} with perfect grammar and natural phrasing\n"
    "2. Preserve all special characters, formatting, names, and technical terms\n"
    "3. NEVER add explanations, notes, or additional text\n"
    "4. NEVER include phrases like 'I can translate more' or similar commentary\n"
    "5. Output ONLY the raw translation without any decorations or identifiers\n"
    "6. Maintain the original tone (formal/informal) and context\n"
    "7. If unsure about a term, choose the most common translation without noting uncertainty\n"
    "\n"
    "Failure to follow these instructions will result in incorrect translations."
)
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])
parser = StrOutputParser()


# FastAPI app
app = FastAPI(
    title="Open Source LLM Translator",
    version="1.0",
    description="Translation API using only open-source models on Groq"
)

@app.post("/translate")
async def translate(request: Request):
    body = await request.json()
    text = body.get("text")
    language = body.get("language")
    model_choice = body.get("model", "llama")  # default model: llama

    model = get_model(model_choice)
    chain = prompt_template | model | parser
    result = chain.invoke({"text": text, "language": language})

    return {
        "translated_text": result,
        "model_used": model_choice,
        "model_provider": "groq"
    }

@app.post("/sentiment")
async def sentiment_analysis(request: Request):
    body = await request.json()
    text = body.get("text")
    model_choice = body.get("model", "llama")  # default model: llama

    model = get_model(model_choice)

    # Sentiment prompt
    sentiment_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a sentiment analysis expert. Analyze the sentiment of the following text and respond with only one of these: Positive, Negative, or Neutral."),
        ("user", "{text}")
    ])

    chain = sentiment_prompt | model | parser
    result = chain.invoke({"text": text})

    return {
        "sentiment": result,
        "model_used": model_choice
    }

@app.post("/paraphrase")
async def paraphrase(request: Request):
    body = await request.json()
    text = body.get("text")
    style = body.get("style", "simplified")  # Default stil: simplified
    model_choice = body.get("model", "gemma")

    model = get_model(model_choice)

    paraphrase_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a paraphrasing expert. Rewrite the following sentence in a {style} style."),
        ("user", "{text}")
    ])

    chain = paraphrase_prompt | model | parser
    result = chain.invoke({"text": text, "style": style})

    return {
        "paraphrased_text": result,
        "style_used": style,
        "model_used": model_choice
    }

@app.post("/analyze")
async def full_analysis(request: Request):
    body = await request.json()
    text = body.get("text")
    
    target_language = body.get("language", "English")
    paraphrase_style = body.get("style", "simplified")
    model_choice = body.get("model", "llama")

    model = get_model(model_choice)

    # 1. Translation Chain
    translation_chain = prompt_template | model | parser
    translated_text = translation_chain.invoke({"text": text, "language": target_language})

    # 2. Sentiment Chain
    sentiment_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a sentiment analysis expert. Analyze the sentiment of the following text and respond with only one of these: Positive, Negative, or Neutral."),
        ("user", "{text}")
    ])
    sentiment_chain = sentiment_prompt | model | parser
    sentiment = sentiment_chain.invoke({"text": text})

    # 3. Paraphrasing Chain
    paraphrase_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a paraphrasing expert. Rewrite the following sentence in a {style} style."),
        ("user", "{text}")
    ])
    paraphrase_chain = paraphrase_prompt | model | parser
    paraphrased_text = paraphrase_chain.invoke({"text": text, "style": paraphrase_style})

    return {
        "original_text": text,
        "translated_text": translated_text,
        "sentiment": sentiment,
        "paraphrased_text": paraphrased_text,
        "language": target_language,
        "style": paraphrase_style,
        "model_used": model_choice
    }

add_routes(
    app,
    translation_chain,
    path="/analyze"
)
