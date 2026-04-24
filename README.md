# TubeDigest AI ✨

TubeDigest AI is a powerful, elegant YouTube video summarization and sentiment analysis tool. Built with Streamlit and powered by Groq API (Llama 3.1), it allows users to paste any YouTube video URL and instantly receive a comprehensive summary of the content along with an analysis of the audience's mood.

## 🚀 Features

- **Instant Summaries:** Get concise and meaningful summaries of long YouTube videos in seconds.
- **Sentiment Analytics:** Analyzes the transcript to determine the overall mood of the video (Positive, Neutral/Mixed, or Negative/Concerned).
- **Interactive Visualizations:** Includes a visually appealing gauge chart to represent the sentiment score using Plotly.
- **Modern UI/UX:** A clean, dark-themed responsive interface with custom CSS styling.
- **Secure API Key Handling:** Users can securely input their own Gemini API key via the sidebar.

## 🛠️ Tech Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/)
- **AI / LLM:** [Google Gemini 2.5 Flash](https://aistudio.google.com/) via `google-generativeai`
- **Data Visualization:** [Plotly](https://plotly.com/python/) 
- **Video Processing:** `yt-dlp` for transcript and metadata extraction
- **Language:** Python

## ⚙️ Prerequisites

- Python 3.8+
- A Google Gemini API Key

## 📥 Installation

1. **Clone the repository (or download the source code):**
   ```bash
   git clone https://github.com/sarvjit-patil/tubeDigest-AI.git
   cd tubeDigest-AI
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

1. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```
   *Alternatively, you can double-click on `run_app.bat` if you are on Windows.*

2. **Open your browser** and navigate to `http://localhost:8501`.

3. **Enter your Gemini API Key** in the left sidebar. You can get one from [Google AI Studio](https://aistudio.google.com/).

4. **Paste a YouTube video URL** into the main input field.

5. **Click "Summarize Now"** and enjoy the AI-generated insights!

## 👨‍💻 Developer

Created by **Sarvajit Patil**
- [GitHub](https://github.com/sarvjit-patil)
- [LinkedIn](https://www.linkedin.com/in/sarvjit-patil-74980923b)
