from google.generativeai import GenerativeModel, configure
import numpy as np
import faiss

model = None

def configure_gemini(api_key):
    global model
    configure(api_key=api_key)
    model = GenerativeModel("gemini-1.5-pro-latest")

def get_embedding(text):
    try:
        response = model.embed_content(
            content=text,
            task_type="RETRIEVAL_DOCUMENT",
            title="YouTube Transcript"
        )
        return np.array(response["embedding"], dtype=np.float32)
    except Exception as e:
        print("Embedding error:", e)
        return np.zeros(768, dtype=np.float32)


def build_faiss_index(chunks):
    dim = 768
    index = faiss.IndexFlatL2(dim)
    embeddings = []
    for chunk in chunks:
        emb = get_embedding(chunk)
        embeddings.append(emb)
    index.add(np.array(embeddings))
    return index, chunks, embeddings


def retrieve_top_chunks(query, index, chunks, k=4):
    query_emb = get_embedding(query).reshape(1, -1)
    distances, indices = index.search(query_emb, k)
    return [chunks[i] for i in indices[0]]

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


def answer_question(transcript_chunks, user_question, index=None, chunks=None):
    if index is not None and chunks is not None:
        top_chunks = retrieve_top_chunks(user_question, index, chunks)
        context = "\n\n".join(top_chunks)
    else:
        context = "\n\n".join(transcript_chunks[:6])  # fallback if no index

    prompt = f"""
You are a helpful assistant. Given this transcript of a YouTube video, answer the user's question clearly and accurately.

Transcript:
{context}

Question: {user_question}
Answer:
"""
    return model.generate_content(prompt).text
