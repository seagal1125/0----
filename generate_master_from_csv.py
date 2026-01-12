import csv
import os

def main():
    csv_file = "musicbook_songs.csv"
    output_file = "index_yt.html"
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found.")
        return

    # Read CSV
    all_songs = []
    available_volumes = set()
    
    print("Reading CSV...")
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        
        for row in reader:
            if not row or len(row) < 4:
                continue
            
            try:
                title = row[1].strip()
                artist = row[2].strip()
                vol_str = row[3].strip()
                note = row[5].strip() if len(row) > 5 else ""
                
                if not vol_str.isdigit():
                    continue
                
                vol = int(vol_str)
                available_volumes.add(vol)
                
                all_songs.append({
                    'vol': vol,
                    'title': title,
                    'artist': artist,
                    'note': note
                })
            except ValueError:
                continue

    # Sort songs: Volume DESC
    all_songs.sort(key=lambda x: x['vol'], reverse=True)
    
    # Sort volumes DESC
    sorted_volumes = sorted(list(available_volumes), reverse=True)
    
    print(f"Total songs: {len(all_songs)}")
    print(f"Total volumes: {len(sorted_volumes)}")

    # Generate HTML
    
    nav_buttons_html = ""
    for vol in sorted_volumes:
        # Check if file 'exists' conceptually - we link to it regardless, 
        # assuming the batch process will create it.
        # Format: index_161.html
        link = f"index_{vol}.html"
        nav_buttons_html += f'<a href="{link}" class="nav-button">第 {vol} 期</a>\n'

    song_list_html = ""
    for song in all_songs:
        search_query = f"{song['artist']} {song['title']}"
        search_url = f"https://www.youtube.com/results?search_query={search_query}"
        
        song_list_html += f"""
            <tr>
                <td><span class="vol-tag">{song['vol']}</span></td>
                <td><a href="{search_url}" target="_blank" class="song-link">{song['title']}</a></td>
                <td>{song['artist']}</td>
                <td>{song['note']}</td>
            </tr>
        """

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
    <script>
        function filterSongs() {{
            var input, filter, table, tr, tdTitle, tdArtist, i, txtValueTitle, txtValueArtist;
            input = document.getElementById("searchInput");
            filter = input.value.toUpperCase();
            table = document.getElementById("songTable");
            tr = table.getElementsByTagName("tr");
            
            for (i = 1; i < tr.length; i++) {{
                tdTitle = tr[i].getElementsByTagName("td")[1];
                tdArtist = tr[i].getElementsByTagName("td")[2];
                if (tdTitle || tdArtist) {{
                    txtValueTitle = tdTitle.textContent || tdTitle.innerText;
                    txtValueArtist = tdArtist.textContent || tdArtist.innerText;
                    if (txtValueTitle.toUpperCase().indexOf(filter) > -1 || txtValueArtist.toUpperCase().indexOf(filter) > -1) {{
                        tr[i].style.display = "";
                    }} else {{
                        tr[i].style.display = "none";
                    }}
                }}
            }}
        }}
    </script>
</head>
<body>
    <h1>最新排行 YouTube 歌單總目錄</h1>
    
    <div class="nav-container">
        {nav_buttons_html}
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
            {song_list_html}
        </tbody>
    </table>
</body>
</html>
    """
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Successfully created {output_file}")

if __name__ == "__main__":
    main()
