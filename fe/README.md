# Media Crawler Data Viewer

This Streamlit application displays content data from Xiaohongshu (XHS) along with their aggregated comments.

## Requirements

- Python 3.7+
- Streamlit
- Pandas

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the App

From the `fe` directory, run:

```bash
streamlit run app.py
```

## Data

The application reads data from:
- `../data/xhs/json/search_contents_2025-03-19.json` - Content items
- `../data/xhs/json/search_comments_2025-03-19.json` - Comments

Each content item displays:
- Note ID
- Title
- Description
- Like count
- Aggregated comments
