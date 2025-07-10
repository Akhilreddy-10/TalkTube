from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from datetime import timedelta

def has_english_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en'])
        transcript.fetch()
        return True
    except (NoTranscriptFound, TranscriptsDisabled):
        return False
    except:
        return False

def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])

        formatted = []
        for entry in transcript:
            start = str(timedelta(seconds=int(entry['start'])))
            if start.startswith("0:"):
                start = start[2:]
            elif start.startswith("00:"):
                start = start[3:]
            formatted.append(f"[{start}] {entry['text']}")

        chunks, chunk = [], []
        char_count = 0
        for line in formatted:
            if char_count + len(line) > 3000:
                chunks.append("\n".join(chunk))
                chunk = []
                char_count = 0
            chunk.append(line)
            char_count += len(line)
        if chunk:
            chunks.append("\n".join(chunk))
        return chunks
    except Exception:
        return None

def format_timestamps(text):
    if "\n" in text:
        lines = text.strip().splitlines()
    else:
        lines = text.strip().split("] ")
        lines = [line + "]" if not line.endswith("]") else line for line in lines if line.strip()]
    return "\n".join(f"- {line.strip()}" for line in lines)
