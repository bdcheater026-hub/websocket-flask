import asyncio
import websockets
import requests
from bs4 import BeautifulSoup
import json

headers = {"User-Agent": "Mozilla/5.0"}

links = [
    "https://www.cnnindonesia.com/otomotif/20260402191659-603-1343841/panduan-singkat-beralih-ke-mobil-listrik-bagi-pemula",
    "https://www.cnnindonesia.com/ekonomi/20230303123945-85-920000/harga-bbm-dunia-naik-akibat-perang-rusia-ukraina",
]

# =====================
# SCRAPING FUNCTION
# =====================
def scrape_data():
    data_list = []

    for link in links:
        try:
            res = requests.get(link, headers=headers, timeout=5)

            soup = BeautifulSoup(res.text, "html.parser")

            title_tag = soup.find("h1")
            title = title_tag.get_text(strip=True) if title_tag else "Tidak ada judul"

            content_div = soup.find("div", class_="detail-text")

            if content_div:
                paragraphs = content_div.find_all("p")
                content = " ".join([p.get_text(strip=True) for p in paragraphs])
            else:
                content = "Isi tidak ditemukan"

            data_list.append({
                "title": title,
                "content": content[:150],
                "link": link
            })

        except Exception as e:
            print("Error:", e)

    return data_list


# =====================
# WEBSOCKET HANDLER
# =====================
async def handler(websocket):
    print("Client terhubung")

    try:
        while True:
            data = scrape_data()
            await websocket.send(json.dumps(data, ensure_ascii=False))
            print("Data dikirim")
            await asyncio.sleep(5)

    except:
        print("❌ Client terputus")


# =====================
# MAIN
# =====================
async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Server jalan di ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())
