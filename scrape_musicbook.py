import requests

url = "https://www.musicbook.com.tw/searchSong/index.asp?offset=0"

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

# Note: The user provided Content-Length: 200 implies a body, but didn't provide the body content.
# I will first try POST with an empty body.
try:
    print("Attempting POST request...")
    response = requests.post(url, headers=headers)
    print(f"POST Status Code: {response.status_code}")
    
    with open("musicbook_response.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print(f"Saved response to musicbook_response.html (Size: {len(response.text)} bytes)")
    
except Exception as e:
    print(f"POST Request failed: {e}")

