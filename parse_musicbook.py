import os
import csv
from bs4 import BeautifulSoup
import glob

# Configuration
input_dir = "musicbook_dump"
output_file = "musicbook_songs.csv"

def parse_html_file(filepath):
    songs = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            
        # Find all rows with specific background colors or just iterate rows
        # Based on previous view, rows had bgcolor="#E7F8ED" or "#FFF0FD"
        # and cells had class="style3"
        
        # We can find the main table first. 
        # It seems the table contains rows.
        
        rows = soup.find_all("tr")
        
        for row in rows:
            # Check if it is a data row. Data rows have specific bgcolors or contain style3 cells.
            bgcolor = row.get("bgcolor", "").upper()
            if bgcolor in ["#E7F8ED", "#FFF0FD"]:
                cols = row.find_all("td")
                # We expect at least 8 columns based on the file inspection
                if len(cols) >= 8:
                    book_name = cols[0].get_text(strip=True)
                    song_name = cols[1].get_text(strip=True)
                    singer = cols[2].get_text(strip=True)
                    volume = cols[3].get_text(strip=True)
                    page = cols[4].get_text(strip=True)
                    # cols[5] is buy button
                    # cols[6] is single page count
                    remarks = cols[7].get_text(strip=True)
                    
                    songs.append([book_name, song_name, singer, volume, page, remarks])
                    
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        
    return songs

def main():
    all_songs = []
    html_files = sorted(glob.glob(os.path.join(input_dir, "page_*.html")))
    
    print(f"Found {len(html_files)} files to parse.")
    
    for i, filepath in enumerate(html_files):
        if i % 100 == 0:
            print(f"Processing {i}/{len(html_files)}: {filepath}")
        
        songs = parse_html_file(filepath)
        all_songs.extend(songs)
        
    print(f"Total songs extracted: {len(all_songs)}")
    
    # Write to CSV
    headers = ["書名", "曲名", "演唱歌手", "冊別", "頁別", "備註"]
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(all_songs)
        
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    main()
