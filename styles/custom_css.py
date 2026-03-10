import streamlit as st

def apply_custom_css():
    """
    Applies custom CSS to create a professional, dark-mode high-end UI.
    """
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Container Styling */
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }

    /* Header Styling */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        background: -webkit-linear-gradient(45deg, #00D2FF 30%, #3A7BD5 90%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .sub-title {
        text-align: center;
        font-size: 1.2rem;
        color: #B0B0B0;
        margin-bottom: 2rem;
    }

    /* Input & Button Styling */
    .stTextInput > div > div > input {
        border-radius: 12px;
        background-color: #1E2227;
        color: #F0F0F0;
        border: 1px solid #3A3F47;
        padding: 12px;
    }

    .stButton > button {
        border-radius: 12px;
        background: linear-gradient(45deg, #0072FF, #00D2FF);
        color: white;
        font-weight: 600;
        border: none;
        padding: 12px 24px;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 210, 255, 0.4);
        background: linear-gradient(45deg, #00D2FF, #0072FF);
    }

    /* Card Styling */
    .feature-card {
        background-color: #1E2227;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid #3A3F47;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #161B22;
    }

    /* Custom Accent Color */
    .electric-blue {
        color: #00D2FF;
    }
    
    /* Metrics / Status */
    .stMetric {
        background-color: #1E2227;
        padding: 10px;
        border-radius: 8px;
    }
    
    </style>
    """, unsafe_allow_html=True)

import textwrap
import re

def card_container(title, content):
    """
    Helper function to render a styled card, converting simple markdown to HTML.
    """
    lines = content.split('\n')
    html_lines = []
    in_list = False
    
    for line in lines:
        line = line.strip()
        if line.startswith('- ') or line.startswith('* '):
            if not in_list:
                html_lines.append('<ul style="margin-top: 5px; padding-left: 20px;">')
                in_list = True
            text = line[2:].strip()
            # Parse bold text
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            html_lines.append(f'<li style="margin-bottom: 8px;">{text}</li>')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            
            if line:
                # Parse bold text
                line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
                html_lines.append(f'<p style="margin-bottom: 8px;">{line}</p>')
            else:
                html_lines.append('<br>')
                
    if in_list:
        html_lines.append('</ul>')
        
    formatted_content = "\n".join(html_lines)
    
    html_content = f"""
<div class="feature-card">
    <h3 style="margin-top:0; margin-bottom:15px; color:#00D2FF;">{title}</h3>
    <div style="color:#B0B0B0; line-height:1.6; font-size: 1rem;">
        {formatted_content}
    </div>
</div>
"""
    st.markdown(html_content, unsafe_allow_html=True)
