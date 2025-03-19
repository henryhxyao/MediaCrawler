import streamlit as st
import json
import os
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Media Crawler Data Viewer", layout="wide")
st.title("Media Crawler Data Viewer")

# Define paths for the data files
data_dir = Path("../data/xhs/json")
contents_file = data_dir / "search_contents_2025-03-19.json"
comments_file = data_dir / "search_comments_2025-03-19.json"

# Load data from JSON files
@st.cache_data
def load_data():
    try:
        with open(contents_file, 'r', encoding='utf-8') as f:
            contents_list = json.load(f)
        
        with open(comments_file, 'r', encoding='utf-8') as f:
            comments_list = json.load(f)
        
        return contents_list, comments_list
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return [], []

contents_list, comments_list = load_data()

if not contents_list or not comments_list:
    st.warning("No data found or error loading data.")
    st.stop()

# Process data - aggregate comments for each content
def aggregate_comments(contents, comments):
    # Create a dictionary to map note_ids to their comments
    comment_map = {}
    for comment in comments:
        note_id = comment.get("note_id")
        content = comment.get("content")
        if note_id:
            if note_id not in comment_map:
                comment_map[note_id] = []
            comment_map[note_id].append(content)
    
    # Add aggregated comments to contents
    for content in contents:
        note_id = content.get("note_id")
        if note_id:
            content["comments_aggregate"] = comment_map.get(note_id, [])
    
    return contents

# Process and display the data
processed_contents = aggregate_comments(contents_list, comments_list)

# Convert data to DataFrame for table display
table_data = []
for content in processed_contents:
    # Join comments into a single string with line breaks for display in table
    comments = content.get("comments_aggregate", [])
    comments_text = "\n".join([f"{j+1}. {comment}" for j, comment in enumerate(comments)]) if comments else "No comments"
    
    row = {
        "Note ID": content.get("note_id", "N/A"),
        "Title": content.get("title", "N/A"),
        "Description": content.get("desc", "N/A"),
        "Likes": content.get("liked_count", "N/A"),
        "Comments": comments_text
    }
    table_data.append(row)

# Create DataFrame
df = pd.DataFrame(table_data)

# Display as table
st.header("Contents with Comments")
st.dataframe(df, use_container_width=True)

# Add option to see detailed view of a selected row
if len(df) > 0:
    st.header("Detailed View")
    selected_note_id = st.selectbox("Select Note ID to view details:", df["Note ID"].tolist())
    
    if selected_note_id:
        selected_content = next((c for c in processed_contents if c.get("note_id") == selected_note_id), None)
        if selected_content:
            st.write(f"**Title:** {selected_content.get('title', 'N/A')}")
            st.write(f"**Description:** {selected_content.get('desc', 'N/A')}")
            st.write(f"**Likes:** {selected_content.get('liked_count', 'N/A')}")
            
            st.write("**Comments:**")
            comments = selected_content.get("comments_aggregate", [])
            if comments:
                for j, comment in enumerate(comments):
                    st.write(f"{j+1}. {comment}")
            else:
                st.write("No comments found.")
