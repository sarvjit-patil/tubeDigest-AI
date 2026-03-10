import importlib

modules = [
    "streamlit",
    "plotly",
    "google.generativeai",
    "langchain_text_splitters",
    "youtube_transcript_api"
]

missing = []
for mod in modules:
    try:
        importlib.import_module(mod)
        print(f"✅ {mod} is installed")
    except ImportError:
        print(f"❌ {mod} is missing")
        missing.append(mod)

if missing:
    print(f"\nMissing modules: {', '.join(missing)}")
else:
    print("\nAll dependencies are satisfied!")
