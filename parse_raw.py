import re
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='Parse raw text to Markdown for YouTube Playlist')
    parser.add_argument('input_file', help='Input raw text file path')
    parser.add_argument('--output', '-o', help='Output Markdown file path')
    parser.add_argument('--volume', '-v', required=True, help='Volume number (e.g. 160)')
    
    args = parser.parse_args()
    
    input_file = args.input_file
    volume = args.volume
    output_file = args.output
    
    if not output_file:
         output_file = f"YouTube_Playlist_{volume}.md"

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# 最新排行{volume} YouTube歌單\n\n")
        f.write("> [!TIP]\n")
        f.write("> **[點擊此處播放全部 / 另存為播放清單](https://www.youtube.com/watch_videos?video_ids=...)**\n")
        f.write("> 1. 點擊上方連結進入播放頁面。\n")
        f.write("> 2. 若右側清單無儲存按鈕，請點擊 **左側影片標題下方的「儲存」** 按鈕。\n")
        f.write("> 3. 選擇 **「+ 新增播放清單」**。\n")
        f.write(f"> 4. 名稱輸入：`最新排行{volume}`，隱私設定：**公開**。\n")
        f.write("> 5. 建立後即可分享。\n\n")
        f.write("| 曲名 | 歌手 | YouTube 搜尋 | 備註 |\n")
        f.write("|---|---|---|---|\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split()
            
            # Expected parts:
            # 0: 最新排行(簡譜)：最新單曲
            # 1: Song
            # 2: Artist (sometimes Artist/Arist2)
            # 3: Volume (e.g. 159, 160)
            # 4: Page
            # ...
            
            if len(parts) >= 3:
                song = parts[1]
                artist = parts[2]
                
                search_url = f"https://www.youtube.com/results?search_query={artist}%20{song}"
                
                note = ""
                # Logic to extract note: everything after page details until "無實體書"
                # Standard format seems to have volume at index 3.
                # If parts[3] matches the volume, usually parts[5] is count (2/3/4)
                # Note usually starts from index 6 if exists.
                # "無實體書" is usually last.
                
                # Let's be safe and look for the volume number as anchor
                vol_index = -1
                for i, p in enumerate(parts):
                    if p == volume:
                        vol_index = i
                        break
                
                if vol_index != -1 and vol_index + 2 < len(parts):
                    # parts[vol_index] = 159
                    # parts[vol_index+1] = Page (002)
                    # parts[vol_index+2] = Count? (3) or Cart?
                    
                    # Notes start after vol_index+2 ?
                    # Example: 159 011 2 影集《華麗計程車行 》插曲 無實體書
                    # vol=159 (idx 3), 011 (idx 4), 2 (idx 5), Note starts idx 6
                    
                    start_note_idx = vol_index + 3
                    
                    if start_note_idx < len(parts):
                        potential_note_parts = parts[start_note_idx:]
                        # Remove "無實體書" if it is the last one
                        if potential_note_parts and potential_note_parts[-1] == "無實體書":
                            potential_note_parts = potential_note_parts[:-1]
                        
                        note = " ".join(potential_note_parts)

                f.write(f"| {song} | {artist} | [搜尋]({search_url}) | {note} |\n")

    print(f"Successfully created {output_file}")

if __name__ == "__main__":
    main()
