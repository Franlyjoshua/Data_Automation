import requests
from bs4 import BeautifulSoup

# ==========================================
# URL TARGET
# ==========================================

url = "https://putusan3.mahkamahagung.go.id/direktori/index/kategori/perdata-khusus.html"

# ==========================================
# HEADER BROWSER ASLI
# ==========================================

headers = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/136.0 Safari/537.36"
    ),

    "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",

    "Referer": "https://putusan3.mahkamahagung.go.id/",

    "Accept": (
        "text/html,"
        "application/xhtml+xml,"
        "application/xml;q=0.9,"
        "image/avif,image/webp,*/*;q=0.8"
    )
}

# ==========================================
# REQUEST WEBSITE
# ==========================================

response = requests.get(
    url,
    headers=headers,
    timeout=60
)

# ==========================================
# STATUS
# ==========================================

print("=" * 50)
print("STATUS CODE:", response.status_code)
print("=" * 50)

# ==========================================
# PARSE HTML
# ==========================================

soup = BeautifulSoup(response.text, "lxml")

# ==========================================
# TITLE WEBSITE
# ==========================================

print("JUDUL WEBSITE:")

if soup.title:
    print(soup.title.text)
else:
    print("Tidak ada title")

print("=" * 50)

# ==========================================
# CARI LINK PUTUSAN
# ==========================================

putusan_links = []

for link in soup.find_all("a", href=True):

    href = link["href"]

    if "/direktori/putusan/" in href:

        full_link = "https://putusan3.mahkamahagung.go.id" + href

        putusan_links.append(full_link)

# ==========================================
# HASIL
# ==========================================

print(f"JUMLAH LINK PUTUSAN: {len(putusan_links)}")

print("=" * 50)

# ==========================================
# TAMPILKAN 10 LINK PERTAMA
# ==========================================

for link in putusan_links[:10]:

    print(link)
    print("-" * 50)