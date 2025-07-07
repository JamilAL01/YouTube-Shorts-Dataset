# YouTube Shorts Dataset

This repository contains metadata for over 100,000 YouTube Shorts videos, collected for research and analysis of short-form video content.

## License

This metadata is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).

You are free to share and adapt the dataset, **with attribution**, for non-commercial purposes. No video content is included.


## Dataset Contents

- `shorts_metadata.json`: JSON file containing metadata for each video, including:
  - `short_url`: URL to the YouTube Shorts video
  - `channel_name`: Name of the channel
  - `title`: Video title
  - `description`: Video description
  - `published_at`: ISO timestamp of publishing
  - `channel_id`: Channel unique ID
  - `category_id` and `category_name`: YouTube video category
  - `tags`: Comma-separated list of tags
  - `view_count`, `like_count`, `comment_count`: Engagement statistics
  - `duration`: Length of the video in seconds

## Note
Video files are not included due to copyright and size restrictions. Only metadata is shared.

## Purpose

The goal of this dataset is to support academic and industry research into:
- Short-form video trends
- Content categorization and tagging
- Viewer engagement patterns
- Encoding and compression analysis

## Usage

The dataset can be loaded in Python using:

```python
import json

with open("shorts_metadata.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(data[0])  # Preview first video's metadata

