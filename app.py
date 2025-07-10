import streamlit as st
from dotenv import load_dotenv
import os

from utils.youtube_utils import get_video_id, search_videos_with_transcript
from utils.transcript_utils import has_english_transcript, fetch_transcript, format_timestamps
from utils.gemini_utils import configure_gemini, generate_timestamps, answer_question

# === Load API Key ===
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("🚨 Gemini API key not found. Please add it to a .env file.")
    st.stop()

configure_gemini(GEMINI_API_KEY)

# === Streamlit App ===
st.set_page_config(page_title="TalkTube", layout="wide")
st.title("🎥 TalkTube")

query = st.text_input("🔍 Search YouTube videos:")

if query and query.strip():
    if "last_query" not in st.session_state or st.session_state.last_query != query:
        st.session_state.last_query = query
        st.session_state.video_list, st.session_state.video_data = search_videos_with_transcript(query, has_english_transcript)

# === Show Video List ===
if st.session_state.get("video_list"):
    selected = st.radio("📺 Choose a video to watch:", st.session_state.video_list)
    if "selected_video_label" not in st.session_state or st.session_state.selected_video_label != selected:
        st.session_state.selected_video_label = selected
        st.session_state.video = st.session_state.video_data[selected]
        st.session_state.transcript_chunks = fetch_transcript(st.session_state.video["video_id"])
        st.session_state.timestamps = None

# === Show Video and Interaction ===
if "video" in st.session_state and st.session_state.get("transcript_chunks"):
    video = st.session_state.video
    st.video(video["url"])

    if st.session_state.timestamps is None:
        with st.spinner("🧠 Analyzing full video for key moments..."):
            st.session_state.timestamps = generate_timestamps(st.session_state.transcript_chunks)

    st.subheader("⏱ Key Timestamps")
    st.markdown(format_timestamps(st.session_state.timestamps))

    st.subheader("🤖 Ask a question about this video")
    user_q = st.text_input("Ask your question...")

    if user_q:
        with st.spinner("💬 Thinking..."):
            answer = answer_question(st.session_state.transcript_chunks, user_q)
            st.markdown(f"**Answer:** {answer}")
