import json
import os
import subprocess

# Load JSON file
json_file = "path/to/dataset/file.json"
with open(json_file, "r", encoding="utf-8") as f:
    videos = json.load(f)

# Extract video IDs
video_ids = [video["short_url"].split("/")[-1] for video in videos]

# Define batch size
BATCH_SIZE = 100

# Track already downloaded videos
downloaded_videos_file = "path/to/downloaded/videos" # To ensure that each video is downloaded once!
if os.path.exists(downloaded_videos_file):
    with open(downloaded_videos_file, "r", encoding="utf-8") as f:
        downloaded_videos = json.load(f)
else:
    downloaded_videos = []

# Select new videos
remaining_videos = [vid for vid in video_ids if vid not in downloaded_videos]
batch = remaining_videos[:BATCH_SIZE]

# Create output folder
output_folder = "path/to/output/folder"
os.makedirs(output_folder, exist_ok=True)

# Track unavailable videos
unavailable_videos = []

# Define format itags for video resolutions
video_itags = {  #To ensure that all videos are downloaded at all available resolutions, we use the available video itags for all videos
    "144p": "394",
    "240p": "395",
    "360p": "396",
    "480p": "397",
    "720p": "398",
    "1080p": "399",
    "1440p": "400",
    "2160p": "401",
    "4320p": "402"
}
audio_itag = "251"

# Process each video
for video_id in batch:
    url = f"https://www.youtube.com/short/{video_id}"
    print(f"\nProcessing video: {url}")

    try:
        # List available formats
        format_cmd = ["yt-dlp", "-F", url] #use yt-dlp to check first all video format --> Resolutions "itag values".
        format_result = subprocess.run(format_cmd, capture_output=True, text=True)
        if "This video is unavailable" in format_result.stderr or "ERROR" in format_result.stderr.upper():
            print(f"Video unavailable: {video_id}")
            unavailable_videos.append(video_id)
            continue

        available_formats = format_result.stdout

        # Try downloading each resolution if available
        for res, vtag in video_itags.items():
            if vtag in available_formats and audio_itag in available_formats:
                output_path = f"{output_folder}/{video_id}-{res}.mp4"
                cmd = [
                    "yt-dlp",
                    "-f", f"{vtag}+{audio_itag}",
                    "--merge-output-format", "mp4",
                    "--output", output_path,
                    url
                ]
                print(f"→ Downloading {res} ({vtag}+{audio_itag})...")
                subprocess.run(cmd, capture_output=True, text=True)
            else:
                print(f"✗ {res} not available")

        downloaded_videos.append(video_id)

    except Exception as e:
        print(f"Error processing {video_id}: {e}")
        unavailable_videos.append(video_id)

# Save updated list of downloaded videos
with open(downloaded_videos_file, "w", encoding="utf-8") as f:
    json.dump(downloaded_videos, f, indent=4)

# Save unavailable videos
unavailable_videos_file = "path/to/unavailable/videos/file" #Sometimes some videos are putted private or removed, so enusre to print those video's IDs to remove it then from the dataset file
if os.path.exists(unavailable_videos_file):
    with open(unavailable_videos_file, "r", encoding="utf-8") as f:
        previous_unavailable = json.load(f)
else:
    previous_unavailable = []

all_unavailable_videos = list(set(previous_unavailable + unavailable_videos))
with open(unavailable_videos_file, "w", encoding="utf-8") as f:
    json.dump(all_unavailable_videos, f, indent=4)

# Summary
print(f"Batch complete: {len(batch)} video(s) processed.")
print(f"{len(unavailable_videos)} video(s) were unavailable.")
