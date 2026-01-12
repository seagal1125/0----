import requests
import time
import random
import os

# Configuration
start_offset = 50
end_offset = 9050
step = 50
output_dir = "musicbook_dump"
url = "https://www.musicbook.com.tw/searchSong/index.asp"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "cookie": "ASPSESSIONIDSGQQBSST=NNDPPHACGANCEGOPAIADIJDN; _gid=GA1.3.1565165737.1768178764; _gat=1; _gat_gtag_UA_78435339_1=1; _ga_PKJYN3TKL6=GS2.1.s1768178763$o1$g1$t1768179275$j26$l0$h0; _ga=GA1.1.566574784.1768178764",
    "origin": "https://www.musicbook.com.tw",
    "priority": "u=0, i",
    "referer": "https://www.musicbook.com.tw/searchSong/index.asp?offset=50",
    "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}

def scrape_page(offset):
    target_url = f"{url}?offset={offset}"
    filename = os.path.join(output_dir, f"page_{offset}.html")
    
    if os.path.exists(filename):
        print(f"Skipping offset {offset}, file already exists.")
        return

    try:
        print(f"Scraping offset {offset}...")
        response = requests.post(target_url, headers=headers)
        
        if response.status_code == 200:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Successfully saved offset {offset} ({len(response.text)} bytes)")
        else:
            print(f"Failed to scrape offset {offset}: Status Code {response.status_code}")
            
    except Exception as e:
        print(f"Error scraping offset {offset}: {e}")

def main():
    print(f"Starting batch scrape from {start_offset} to {end_offset} with step {step}")
    
    for offset in range(start_offset, end_offset + 1, step):
        scrape_page(offset)
        
        # Random delay to be polite
        sleep_time = random.uniform(1.0, 3.0)
        # print(f"Sleeping for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)
        
    print("Batch scraping completed.")

if __name__ == "__main__":
    main()
