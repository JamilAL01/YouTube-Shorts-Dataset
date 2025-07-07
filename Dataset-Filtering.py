import json
import requests

def load_dataset(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def is_valid_short(url):
    """Check if a Shorts URL remains a Shorts video or redirects to a regular video."""
    try:
        response = requests.get(url, allow_redirects=True)
        final_url = response.url
        return "/shorts/" in final_url  # True if still a Shorts video
    except requests.RequestException:
        return False

def filter_shorts(data):
    filtered_data = []
    for video in data:
        duration = video.get("duration", 0)
        published_year = int(video.get("published_at", "2000")[:4])
        short_url = video.get("short_url", "")

        if 0 < duration <= 180 and 2020 <= published_year <= 2025 and is_valid_short(short_url):
            filtered_data.append(video)
    
    return filtered_data

def save_filtered_data(filtered_data, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(filtered_data, file, indent=4)

def main():
    input_file = "path/to/dataset/file.json"  
    output_file = "path/to/output/file.json"
    
    print("Loading dataset...")
    data = load_dataset(input_file)
    
    print("Filtering Shorts...")
    filtered_data = filter_shorts(data)
    
    print(f"Saving {len(filtered_data)} valid Shorts...")
    save_filtered_data(filtered_data, output_file)
    
    print("Filtering complete! Saved to", output_file)

if __name__ == "__main__":
    main()