import re
import subprocess
import urllib.parse

def get_video_id(query):
    try:
        # Use yt-dlp to search and get the ID of the first result
        cmd = ['yt-dlp', f'ytsearch1:{query}', '--get-id', '--default-search', 'ytsearch']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        video_id = result.stdout.strip()
        return video_id
    except subprocess.CalledProcessError as e:
        print(f"Error finding {query}: {e}")
        return None

import argparse

def main():
    parser = argparse.ArgumentParser(description='Generate YouTube Playlist HTML from Markdown')
    parser.add_argument('input_file', nargs='?', default='YouTube_Playlist_Latest.md', help='Input Markdown file')
    parser.add_argument('--output', '-o', default='index.html', help='Output HTML file')
    parser.add_argument('--title', '-t', default='最新排行 YouTube 歌單', help='Page Title')
    
    args = parser.parse_args()
    
    md_file = args.input_file
    output_file = args.output
    page_title = args.title
    
    songs_data = []
    
    print(f"Reading from: {md_file}")
    
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{md_file}' not found.")
        return

    # Skip header lines (approx first 4 lines based on file view)
    # Expected format: | 曲名 | 歌手 | ...
    
    print("Fetching Video IDs... This may take a moment.")
    
    for line in lines:
        if not line.startswith('|'):
            continue
        parts = [p.strip() for p in line.split('|')]
        # parts[0] is empty string because line starts with |
        # parts[1] is Song
        # parts[2] is Artist
        if len(parts) < 3:
            continue
            
        song = parts[1]
        artist = parts[2]
        
        # Skip header row if it matches "曲名" and "歌手"
        if song == '曲名' and artist == '歌手':
            continue
        if song.startswith('---'): # Separator line
             continue

        if song and artist:
            query = f"{artist} {song}"
            print(f"Searching for: {query}")
            vid = get_video_id(query)
            if vid:
                songs_data.append({
                    'song': song,
                    'artist': artist,
                    'id': vid
                })
                print(f"Found: {vid}")
            else:
                print("Not found.")

    if songs_data:
        # Join IDs with comma
        video_ids = [s['id'] for s in songs_data]
        ids_str = ",".join(video_ids)
        playlist_url = f"https://www.youtube.com/watch_videos?video_ids={ids_str}"
        print("\nSUCCESS! Here is your playlist link:")
        print(playlist_url)

        # Generate Song List HTML
        song_list_html = ""
        for s in songs_data:
            song_list_html += f"""
            <div class="song-item">
                <a href="https://www.youtube.com/watch?v={s['id']}" target="_blank" class="song-link">
                    <span class="song-title">{s['song']}</span>
                    <span class="song-artist">{s['artist']}</span>
                </a>
            </div>
            """

        # Generate HTML
        html_content = f"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f7;
            color: #1d1d1f;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .button-container {{
            text-align: center;
            margin-bottom: 40px;
        }}
        .save-button {{
            display: inline-block;
            background-color: #ff0000;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            font-size: 18px;
            border-radius: 25px;
            font-weight: bold;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .save-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        }}
        .song-list {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        .song-item {{
            border-bottom: 1px solid #eee;
        }}
        .song-item:last-child {{
            border-bottom: none;
        }}
        .song-link {{
            display: flex;
            justify-content: space-between;
            padding: 15px 10px;
            text-decoration: none;
            color: inherit;
            border-radius: 8px;
            transition: background-color 0.2s;
        }}
        .song-link:hover {{
            background-color: #f5f5f7;
        }}
        .song-title {{
            font-weight: 600;
            color: #1d1d1f;
        }}
        .song-artist {{
            color: #86868b;
        }}
    </style>
</head>
<body>
    <h1>{page_title}</h1>
    
    <div class="button-container">
        <a href="{playlist_url}" target="_blank" class="save-button">
            ▶ 播放全部 / 儲存播放清單
        </a>
    </div>

    <div class="song-list">
        <h3>歌曲列表 ({len(songs_data)} 首)</h3>
        {song_list_html}
    </div>
</body>
</html>
        """
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"\nSuccessfully created '{output_file}'. Open this file to play/save the playlist.")
        
    else:
        print("No video IDs found.")

if __name__ == "__main__":
    main()
