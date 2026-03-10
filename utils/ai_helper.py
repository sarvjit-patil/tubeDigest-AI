import google.generativeai as genai
from langchain_text_splitters import RecursiveCharacterTextSplitter
import streamlit as st
import time

def get_summarization_and_sentiment(transcript, api_key):
    """
    Summarizes the transcript and performs sentiment analysis using Gemini models.
    Automatically falls back to older/alternative models if quota is exceeded.
    """
    if not api_key:
        return "Error: Gemini API Key is missing.", None

    genai.configure(api_key=api_key)
    
    try:
        available_models = [m.name.replace('models/', '') for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Priority list of models to try
        preferred_models = [
            'gemini-2.5-flash',
            'gemini-1.5-flash', 
            'gemini-1.5-flash-latest', 
            'gemini-1.5-pro', 
            'gemini-pro'
        ]
        
        # Filter to only models the key actually has access to
        models_to_try = [m for m in preferred_models if m in available_models]
        if not models_to_try and available_models:
            models_to_try = [available_models[0]] # absolute fallback
            
        if not models_to_try:
            return "Error: No text generation models available for this API key.", None

    except Exception as e:
        return f"Error initializing Gemini API: {str(e)}", None

    # Split text if it's too long
    # Gemini models have a large context window (>1M tokens), using 300k chars to minimize API calls
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300000, chunk_overlap=5000)
    chunks = text_splitter.split_text(transcript)

    # Helper function to try generating content across available models
    def generate_with_fallback(prompt):
        last_error = None
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                error_msg = str(e)
                last_error = error_msg
                # If it's a quota/rate limit error, try the next model
                if "429" in error_msg or "Quota" in error_msg or "exhausted" in error_msg.lower():
                    time.sleep(2) # Brief pause before trying fallback model
                    continue
                else:
                    # For other types of errors (e.g. safety blocks), don't fallback, just fail
                    raise Exception(f"API Error ({model_name}): {error_msg}")
        
        # If we exhausted all models because of quota
        raise Exception(f"All available models have exceeded their daily/minute quota limits. Please check your Google AI Studio billing. Last error: {last_error}")

    combined_summary = ""
    for i, chunk in enumerate(chunks):
        if i > 0:
            time.sleep(10) # Avoid hitting minute limits if we are chunking (rare)
            
        prompt = f"""
        Summarize the following YouTube video transcript into concise bullet points. 
        Focus on the main highlights and key takeaways.
        
        Transcript:
        {chunk}
        """
        try:
            text = generate_with_fallback(prompt)
            combined_summary += text + "\n"
        except Exception as e:
            return f"Error during summarization: {str(e)}", None

    # Final Summary for long videos
    if len(chunks) > 1:
        time.sleep(5)
        final_prompt = f"""
        Consolidate the following summaries into a single, high-quality, professional bulleted summary.
        
        Summaries:
        {combined_summary}
        """
        try:
            final_summary = generate_with_fallback(final_prompt)
        except Exception as e:
            return f"Error during consolidation: {str(e)}", None
    else:
        final_summary = combined_summary

    # Sentiment Analysis
    sentiment_prompt = f"""
    Based on the following video insights, provide a sentiment score between 0 and 100, 
    where 0 is very negative and 100 is very positive. Return ONLY the number.
    
    Insights:
    {final_summary}
    """
    try:
        sentiment_text = generate_with_fallback(sentiment_prompt)
        try:
            sentiment_score = float(sentiment_text.strip())
        except:
            sentiment_score = 50.0 # Default
    except Exception as e:
        sentiment_score = 50.0

    return final_summary, sentiment_score
