import streamlit as st
from groq import Groq
from langchain_text_splitters import RecursiveCharacterTextSplitter
import time
import re

def get_summarization_and_sentiment(transcript, api_key):
    """
    Summarizes the transcript and performs sentiment analysis using Groq models.
    """
    if not api_key:
        return "Error: Groq API Key is missing.", None

    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        return f"Error initializing Groq API: {str(e)}", None

    model_name = "llama-3.1-8b-instant"
    
    # Groq Free Tier limits you to 6,000 Tokens Per Minute (TPM).
    # 18,000 characters is roughly 4,500 tokens. 
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=18000, chunk_overlap=1000)
    chunks = text_splitter.split_text(transcript)

    def generate_content(prompt):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant that provides accurate summaries and analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Groq API Error: {str(e)}")

    combined_summary = ""
    
    if len(chunks) > 1:
        st.warning(f"⚠️ Long video detected! Groq's Free Tier limits us to 6,000 tokens per minute. We have to process this in {len(chunks)} chunks and wait 60 seconds between each to avoid crashing.")

    for i, chunk in enumerate(chunks):
        if i > 0:
            with st.spinner(f"Waiting 60 seconds to bypass Groq free tier limits (Chunk {i+1}/{len(chunks)})..."):
                time.sleep(61) # Wait out the 1-minute TPM limit
            
        prompt = f"""
        Summarize the following YouTube video transcript into concise bullet points. 
        Focus on the main highlights and key takeaways.
        
        Transcript:
        {chunk}
        """
        try:
            text = generate_content(prompt)
            combined_summary += text + "\n"
        except Exception as e:
            # If we STILL hit the rate limit, fallback to returning what we have so far
            if 'rate_limit_exceeded' in str(e).lower() and combined_summary:
                st.error("Hit strict Groq rate limit. Returning partial summary of the video.")
                break
            return f"Error during summarization: {str(e)}", None

    # Final Summary for long videos
    if len(chunks) > 1 and combined_summary:
        with st.spinner("Waiting 60 seconds before final consolidation..."):
            time.sleep(61)
        final_prompt = f"""
        Consolidate the following summaries into a single, high-quality, professional bulleted summary.
        
        Summaries:
        {combined_summary}
        """
        try:
            final_summary = generate_content(final_prompt)
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
        time.sleep(1)
        sentiment_text = generate_content(sentiment_prompt)
        # Extract just the number in case the model is chatty
        match = re.search(r'\d+', sentiment_text)
        if match:
            sentiment_score = float(match.group())
        else:
            sentiment_score = 50.0
            
        # cap score bounds
        sentiment_score = max(0.0, min(100.0, sentiment_score))
    except Exception as e:
        sentiment_score = 50.0

    return final_summary, sentiment_score
