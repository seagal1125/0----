import os
import re

def parse_md_file(file_path):
    """
    Parses a Markdown playlist file and returns a list of songs.
    Returns: list of dicts {vol, song, artist, link, note}
    """
    songs = []
    
    # Extract Volume from filename
    # Expected: YouTube_Playlist_161.md
    basename = os.path.basename(file_path)
    match = re.search(r'YouTube_Playlist_(\d+)\.md', basename)
    if match:
        vol = match.group(1)
    else:
        vol = "Unknown"
        
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if not line.startswith("|") or "曲名" in line or "|---" in line:
            continue
            
        # Format: | {song} | {artist} | [搜尋]({search_url}) | {note} |
        parts = [p.strip() for p in line.split('|')]
        
        # parts[0] is empty
        # parts[1] = Song
        # parts[2] = Artist
        # parts[3] = Link (Markdown format)
        # parts[4] = Note
        
        if len(parts) >= 4:
            song = parts[1]
            artist = parts[2]
            link_md = parts[3]
            note = parts[4] if len(parts) > 4 else ""
            
            # Extract URL from markdown link [搜尋](url)
            link_match = re.search(r'\((http.*?)\)', link_md)
            link = link_match.group(1) if link_match else ""
            
            songs.append({
                "vol": vol,
                "song": song,
                "artist": artist,
                "link": link,
                "note": note
            })
            
    return songs

def main():
    base_dir = "/Users/david/Library/Mobile Documents/com~apple~CloudDocs/0最新排行"
    files = [f for f in os.listdir(base_dir) if f.startswith("YouTube_Playlist_") and f.endswith(".md")]
    
    # Sort files by volume keys (descending)
    def vol_sort(f):
        m = re.search(r'(\d+)', f)
        return int(m.group(1)) if m else 0
        
    files.sort(key=vol_sort, reverse=True)
    
    all_songs = []
    
    for f in files:
        path = os.path.join(base_dir, f)
        all_songs.extend(parse_md_file(path))
        
    # Generate HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>最新排行 YouTube 歌單總目錄</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f7;
            color: #1d1d1f;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 30px;
            color: #1d1d1f;
        }}
        .nav-container {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 40px;
        }}
        .nav-button {{
            background-color: #0071e3;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 20px;
            font-weight: 500;
            transition: all 0.2s;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .nav-button:hover {{
            background-color: #0077ed;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        .search-container {{
            margin-bottom: 20px;
            text-align: center;
        }}
        #searchInput {{
            padding: 12px;
            width: 80%;
            max-width: 400px;
            border: 1px solid #d2d2d7;
            border-radius: 10px;
            font-size: 16px;
        }}
        .song-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        .song-table th, .song-table td {{
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #e5e5e5;
        }}
        .song-table th {{
            background-color: #fbfbfd;
            font-weight: 600;
            color: #86868b;
        }}
        .song-table tr:last-child td {{
            border-bottom: none;
        }}
        .song-table tr:hover {{
            background-color: #f5f5f7;
        }}
        .vol-tag {{
            background-color: #e8e8ed;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.9em;
            color: #1d1d1f;
            display: inline-block;
        }}
        a.song-link {{
            color: #0066cc;
            text-decoration: none;
        }}
        a.song-link:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>最新排行 YouTube 歌單總目錄</h1>
    
    <div class="nav-container">
    """
    
    # Add Navigation Buttons
    distinct_vols = sorted(list(set(s['vol'] for s in all_songs)), reverse=True, key=lambda x: int(x))
    
    for vol in distinct_vols:
        html_content += f'<a href="index_{vol}.html" class="nav-button">第 {vol} 期</a>\n'
        
    html_content += """
    </div>

    <div class="search-container">
        <input type="text" id="searchInput" onkeyup="filterSongs()" placeholder="搜尋歌名、歌手...">
    </div>

    <table class="song-table" id="songTable">
        <thead>
            <tr>
                <th width="10%">期數</th>
                <th width="30%">歌名</th>
                <th width="25%">歌手</th>
                <th width="35%">備註</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for song in all_songs:
        # Build a search link or use existing? 
        # Actually, the user wants to identify which vol it is in. 
        # The link in markdown goes to YouTube search. 
        # Ideally, we link to the song in the specific playlist HTML? 
        # But the playlist HTML doesn't have anchors for each song easily unless we add IDs.
        # For now, let's link to the YouTube search as per markdown, or better:
        # Link to the generated `index_VOL.html`?
        # But specific song playing is nice.
        # The markdown has "search_url". 
        
        # We can link to the YouTube search for now, as that's what we have parsed.
        
        html_content += f"""
            <tr>
                <td><span class="vol-tag">{song['vol']}</span></td>
                <td><a href="{song['link']}" target="_blank" class="song-link">{song['song']}</a></td>
                <td>{song['artist']}</td>
                <td>{song['note']}</td>
            </tr>
        """
        
    html_content += """
        </tbody>
    </table>

    <script>
    function filterSongs() {
        var input, filter, table, tr, td, i, txtValue;
        input = document.getElementById("searchInput");
        filter = input.value.toUpperCase();
        table = document.getElementById("songTable");
        tr = table.getElementsByTagName("tr");

        for (i = 1; i < tr.length; i++) {
            // Check Song (idx 1), Artist (idx 2), Note (idx 3)
            var found = false;
            for(var j=1; j<=3; j++) {
                td = tr[i].getElementsByTagName("td")[j];
                if (td) {
                    txtValue = td.textContent || td.innerText;
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {
                        found = true;
                        break;
                    }
                }
            }
            if (found) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
    </script>
</body>
</html>
    """
    
    output_path = os.path.join(base_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"Successfully created master index at: {output_path}")

if __name__ == "__main__":
    main()
