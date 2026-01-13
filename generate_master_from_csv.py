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
    
    nav_select_html = '<div class="select-wrapper">\n'
    nav_select_html += '        <select class="vol-select" onchange="if(this.value) window.location.href=this.value">\n'
    nav_select_html += '            <option value="" disabled selected>選擇期數 (Select Volume)</option>\n'
    for vol in sorted_volumes:
        link = f"index_{vol}.html"
        nav_select_html += f'            <option value="{link}">第 {vol} 期</option>\n'
    nav_select_html += '        </select>\n'
    nav_select_html += '    </div>'

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
            margin-bottom: 40px;
        }}

        .vol-select {{
            padding: 12px 40px 12px 20px;
            font-size: 16px;
            border: 1px solid #d2d2d7;
            border-radius: 12px;
            background-color: white;
            cursor: pointer;
            min-width: 200px;
            appearance: none;
            -webkit-appearance: none;
            background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%230071e3%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
            background-repeat: no-repeat;
            background-position: right 15px top 50%;
            background-size: 12px auto;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            color: #1d1d1f;
            transition: all 0.2s;
        }}

        .vol-select:hover, .vol-select:focus {{
            border-color: #0071e3;
            outline: none;
            box-shadow: 0 0 0 4px rgba(0,113,227,0.1);
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
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }}

        .song-table th,
        .song-table td {{
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
        document.addEventListener('DOMContentLoaded', () => {{
            const searchInput = document.getElementById("searchInput");
            const table = document.getElementById("songTable");
            const tr = table.getElementsByTagName("tr");

            const filterSongs = () => {{
                const filter = searchInput.value.toUpperCase();

                // Start from i=1 to skip header
                for (let i = 1; i < tr.length; i++) {{
                    const tdTitle = tr[i].getElementsByTagName("td")[1];
                    const tdArtist = tr[i].getElementsByTagName("td")[2];

                    if (tdTitle || tdArtist) {{
                        const txtValueTitle = tdTitle.textContent || tdTitle.innerText;
                        const txtValueArtist = tdArtist.textContent || tdArtist.innerText;

                        if (txtValueTitle.toUpperCase().indexOf(filter) > -1 ||
                            txtValueArtist.toUpperCase().indexOf(filter) > -1) {{
                            tr[i].style.display = "";
                        }} else {{
                            tr[i].style.display = "none";
                        }}
                    }}
                }}
            }};

            // Use 'input' event instead of 'keyup' for better IME support (Chinese input)
            searchInput.addEventListener('input', filterSongs);
        }});
    </script>
</head>

<body>
    <h1>最新排行 YouTube 歌單總目錄</h1>

    <div class="nav-container">
        {nav_select_html}
    </div>

    <div class="search-container">
        <input type="text" id="searchInput" placeholder="搜尋歌名、歌手...">
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
