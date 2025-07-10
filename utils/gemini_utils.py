from google.generativeai import GenerativeModel, configure

model = None

def configure_gemini(api_key):
    global model
    configure(api_key=api_key)
    model = GenerativeModel("gemini-1.5-pro-latest")

def generate_timestamps(transcript_chunks):
    transcript_to_use = "\n\n".join(transcript_chunks[:6])
    prompt = f"""
You are a helpful assistant. Given a transcript of a YouTube video with actual timestamps, identify 8–12 key sections and assign short descriptive titles to them.

Return your answer in this format:
[00:00] Title of Section 1
[01:30] Title of Section 2
...

Here is the transcript:
{transcript_to_use}
"""
    return model.generate_content(prompt).text

def answer_question(transcript_chunks, user_question):
    context = "\n\n".join(transcript_chunks[:6])
    prompt = f"""
You are a helpful assistant. Given this transcript of a YouTube video, answer the user's question clearly and accurately.

Transcript:
{context}

Question: {user_question}
Answer:
"""
    return model.generate_content(prompt).text
