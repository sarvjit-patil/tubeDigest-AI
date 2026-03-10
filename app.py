import streamlit as st
import plotly.graph_objects as go
from utils.youtube_helper import extract_video_id, get_video_transcript, get_video_thumbnail_url
from utils.ai_helper import get_summarization_and_sentiment
from styles.custom_css import apply_custom_css, card_container

# Set Page Config
st.set_page_config(
    page_title="TubeDigest AI | YouTube Summarizer",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Styling
apply_custom_css()

# Sidebar
with st.sidebar:
    st.markdown("<h2 style='color:#00D2FF;'>🚀 Navigation</h2>", unsafe_allow_html=True)
    st.info("Experience the future of video content consumption with AI-powered insights.")
    
    with st.expander("ℹ️ How it Works"):
        st.markdown("""
        1. **Paste URL**: Enter any YouTube video link.
        2. **Extract**: We fetch the transcript and metadata.
        3. **Analyze**: Gemini 1.5 Flash processes the text.
        4. **Insights**: Get a summary and audience mood analysis instantly!
        """)
        
    st.markdown("---")
    st.markdown("<h3 style='color:#00D2FF;'>👨‍💻 Developer</h3>", unsafe_allow_html=True)
    st.markdown("""
    Created by **Sarvajit Patil**
    - [GitHub](https://github.com/sarvjit-patil)
    - [LinkedIn](https://www.linkedin.com/in/sarvjit-patil-74980923b)
    """)
    
    # API Key Input
    api_key = st.text_input("Enter Gemini API Key", type="password", help="Get yours at https://aistudio.google.com/")

# Header Section
st.markdown("<div class='main-title'>TubeDigest AI ✨</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Elevate your YouTube experience with professional AI-driven summaries and sentiment analytics.</div>", unsafe_allow_html=True)

# Input Area
with st.container():
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        video_url = st.text_input("", placeholder="Enter YouTube URL (e.g., https://www.youtube.com/watch?v=...)")
    with col_btn:
        st.markdown("<div style='margin-top:25px;'></div>", unsafe_allow_html=True)
        summarize_button = st.button("Summarize Now")

if summarize_button:
    if not video_url:
        st.error("Please provide a valid YouTube URL.")
    elif not api_key:
        st.warning("Please enter your Gemini API Key in the sidebar.")
    else:
        video_id = extract_video_id(video_url)
        if not video_id:
            st.error("Could not extract Video ID. Please check the URL.")
        else:
            with st.spinner("✨ Analyzing video content... Hang tight!"):
                transcript = get_video_transcript(video_id)
                
                if transcript.startswith("Error:"):
                    st.error(f"Failed to fetch transcript: {transcript}")
                else:
                    summary, sentiment_score = get_summarization_and_sentiment(transcript, api_key)
                    
                    if summary.startswith("Error"):
                        st.error(summary)
                    else:
                        # Success Layout
                        st.markdown("---")
                        left_col, right_col = st.columns([3, 2], gap="large")
                        
                        with left_col:
                            st.markdown(f"### 📹 Video Insights")
                            st.image(get_video_thumbnail_url(video_id), use_container_width=True)
                            card_container("Key Highlights", summary)
                            
                        with right_col:
                            st.markdown(f"### 📊 Sentiment Analytics")
                            
                            # Create Gauge Chart
                            fig = go.Figure(go.Indicator(
                                mode = "gauge+number",
                                value = sentiment_score,
                                domain = {'x': [0, 1], 'y': [0, 1]},
                                title = {'text': "Audience Mood (Sentiment Score)", 'font': {'size': 20, 'color': "#00D2FF"}},
                                gauge = {
                                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                                    'bar': {'color': "#00D2FF"},
                                    'bgcolor': "rgba(0,0,0,0)",
                                    'borderwidth': 2,
                                    'bordercolor': "#3A3F47",
                                    'steps': [
                                        {'range': [0, 40], 'color': 'rgba(255, 0, 0, 0.3)'},
                                        {'range': [40, 70], 'color': 'rgba(255, 255, 0, 0.3)'},
                                        {'range': [70, 100], 'color': 'rgba(0, 255, 0, 0.3)'}
                                    ],
                                    'threshold': {
                                        'line': {'color': "white", 'width': 4},
                                        'thickness': 0.75,
                                        'value': sentiment_score
                                    }
                                }
                            ))
                            
                            fig.update_layout(
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font={'color': "white", 'family': "Inter"},
                                height=400,
                                margin=dict(l=20, r=20, t=50, b=20)
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                            
                            mood_description = "The audience overall is feeling **Positive**! 🌟" if sentiment_score > 70 else \
                                             "The sentiment is **Neutral/Mixed**. ⚖️" if sentiment_score > 40 else \
                                             "The mood seems quite **Negative/Concerned**. 😟"
                            
                            card_container("Mood Summary", mood_description)

# Footer
st.markdown("---")
st.markdown("<div style='text-align:center; color:#666;'>Powered by Google Gemini 1.5 Flash • Built with Streamlit</div>", unsafe_allow_html=True)
