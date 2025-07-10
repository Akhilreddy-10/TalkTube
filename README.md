# 🎥 TalkTube — Ask Questions About Any YouTube Video

TalkTube is a powerful Streamlit app that lets you:
- 🔍 Search YouTube videos
- 📄 Extract and analyze transcripts
- 🧠 Get key timestamps automatically using Gemini Pro
- 🤖 Ask natural language questions about the video content

---


## 🚀 Features

- 🔎 **YouTube Search** with transcript filter  
- 🧾 **Transcript Extraction** (English only)  
- ⏱️ **Key Timestamp Generation** using Google Gemini  
- 💬 **Question Answering** on video content  
- 💡 **Interactive & Simple UI** with Streamlit

---

## 📁 Project Structure

```
talktube/
├── app.py                 # Main Streamlit app
├── .env                   # Contains your Gemini API key
├── requirements.txt       # All Python dependencies
├── utils/                 # Modular helper functions
│   ├── __init__.py
│   ├── youtube_utils.py
│   ├── transcript_utils.py
│   └── gemini_utils.py
└── assets/                # Optional images/gifs
```

---

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/talktube.git
cd talktube
```

### 2. Set up a Python environment (recommended)

Using Conda:

```bash
conda create -n talktube python=3.10
conda activate talktube
```

Or using venv:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Gemini API key

Create a `.env` file in the root folder and add:

```
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

> You can get your API key from [Google AI Studio](https://makersuite.google.com/).

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Then open your browser at: [http://localhost:8501](http://localhost:8501)

---

