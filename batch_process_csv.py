import csv
import os
import subprocess
import time

def run_command(command):
    print(f"Executing: {command}")
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return False

def generate_markdown(vol, songs):
    filename = f"YouTube_Playlist_{vol}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# 最新排行{vol} YouTube歌單\n\n")
        f.write(f"> [!TIP]\n")
        f.write(f"> **[點擊此處播放全部 / 另存為播放清單](https://www.youtube.com/watch_videos?video_ids=...)**\n")
        f.write(f"> 1. 點擊上方連結進入播放頁面。\n")
        f.write(f"> 2. 若右側清單無儲存按鈕，請點擊 **左側影片標題下方的「儲存」** 按鈕。\n")
        f.write(f"> 3. 選擇 **「+ 新增播放清單」**。\n")
        f.write(f"> 4. 名稱輸入：`最新排行{vol}`，隱私設定：**公開**。\n")
        f.write(f"> 5. 建立後即可分享。\n\n")
        f.write("| 曲名 | 歌手 | YouTube 搜尋 | 備註 |\n")
        f.write("|---|---|---|---|\n")
        
        for song in songs:
            title = song['title']
            artist = song['artist']
            note = song['note']
            search_query = f"{artist} {title}"
            search_url = f"https://www.youtube.com/results?search_query={search_query}"
            
            f.write(f"| {title} | {artist} | [搜尋]({search_url}) | {note} |\n")
            
    return filename

def main():
    csv_file = "musicbook_songs.csv"
    start_vol = 146
    end_vol = 1
    
    # Read CSV and group by volume
    songs_by_vol = {}
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found.")
        return

    print("Reading CSV...")
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None) # Skip header
        
        for row in reader:
            if not row or len(row) < 4:
                continue
            
            # CSV Columns: 書名,曲名,演唱歌手,冊別,頁別,備註
            # idx: 0, 1, 2, 3, 4, 5
            
            try:
                title = row[1].strip()
                artist = row[2].strip()
                vol_str = row[3].strip()
                note = row[5].strip() if len(row) > 5 else ""
                
                if not vol_str.isdigit():
                    continue
                    
                vol = int(vol_str)
                
                if vol not in songs_by_vol:
                    songs_by_vol[vol] = []
                
                songs_by_vol[vol].append({
                    'title': title,
                    'artist': artist,
                    'note': note
                })
            except ValueError:
                continue
    
    print(f"Loaded songs for {len(songs_by_vol)} volumes.")

    # Process volumes
    volumes_to_process = range(start_vol, end_vol - 1, -1)
    
    for vol in volumes_to_process:
        print(f"\n{'='*30}")
        print(f"Processing Volume {vol}")
        print(f"{'='*30}")
        
        # Check if output exists
        output_html = f"index_{vol}.html"
        if os.path.exists(output_html):
            print(f"Skipping Volume {vol}: {output_html} already exists.")
            continue
            
        if vol not in songs_by_vol:
            print(f"No songs found for Volume {vol} in CSV. Skipping.")
            continue
            
        songs = songs_by_vol[vol]
        print(f"Found {len(songs)} songs for Volume {vol}.")
        
        # 1. Generate Markdown
        md_file = generate_markdown(vol, songs)
        print(f"Generated {md_file}")
        
        # 2. Run fetch_ids.py
        title = f"最新排行{vol}"
        cmd_fetch = f"python3 fetch_ids.py {md_file} --output {output_html} --title \"{title}\""
        
        if run_command(cmd_fetch):
            print(f"Successfully generated {output_html}")
        else:
            print(f"Failed to generate {output_html}")
            # Optional: break or continue? Continue to try others.

if __name__ == "__main__":
    main()
