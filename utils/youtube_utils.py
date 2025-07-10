from youtubesearchpython import VideosSearch
from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    parsed = urlparse(url)
    if parsed.hostname == "youtu.be":
        return parsed.path[1:]
    if parsed.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed.query).get("v", [None])[0]
    return None

def search_videos_with_transcript(query, has_english_transcript):
    videosSearch = VideosSearch(query, limit=10)
    results = videosSearch.result().get("result", [])
    video_list, video_data = [], {}

    for item in results:
        title = item["title"]
        url = item["link"]
        channel = item["channel"]["name"]
        video_id = get_video_id(url)
        if not video_id or not has_english_transcript(video_id):
            continue
        label = f"{title} - {channel}"
        video_list.append(label)
        video_data[label] = {
            "title": title,
            "url": url,
            "channel": channel,
            "video_id": video_id
        }

    return video_list, video_data
