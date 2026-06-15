from seleniumbase import SB
from bs4 import BeautifulSoup
import os
import time
import random

# CONFIG

BASE_URL = (
    "https://putusan3.mahkamahagung.go.id/"
    "direktori/index/kategori/perdata-khusus"
)

# PAGE RANGE

START_PAGE = 4
END_PAGE = 5

# DOWNLOAD FOLDER

DOWNLOAD_FOLDER = os.path.abspath(
    "downloaded_files"
)

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# RETRY CONFIG

MAX_RETRY = 3

# START BROWSER

with SB(
    uc=True,
    headless=False
) as sb:

    # SET DOWNLOAD FOLDER CHROME

    sb.driver.execute_cdp_cmd(
        "Page.setDownloadBehavior",
        {
            "behavior": "allow",
            "downloadPath": DOWNLOAD_FOLDER
        }
    )

    print("=" * 60)
    print("MEMULAI SCRAPER MA...")
    print("=" * 60)

    # LOOP SEMUA PAGE

    for page_number in range(START_PAGE, END_PAGE + 1):

        print("\n")
        print("=" * 60)
        print(f"MEMBUKA PAGE {page_number}")
        print("=" * 60)

        # URL PAGE

        if page_number == 1:

            page_url = f"{BASE_URL}.html"

        else:

            page_url = (
                f"{BASE_URL}/page/{page_number}.html"
            )

        print(page_url)

        # OPEN PAGE    

        success_open_page = False

        for retry in range(MAX_RETRY):

            try:

                print(
                    f"COBA OPEN PAGE "
                    f"({retry+1}/{MAX_RETRY})"
                )

                sb.open(page_url)

                sb.sleep(5)

                success_open_page = True

                break

            except Exception as e:

                print("ERROR OPEN PAGE:")
                print(e)

                sb.sleep(5)

        # =================================================
        # JIKA GAGAL OPEN PAGE
        # =================================================

        if not success_open_page:

            print("=" * 60)
            print("GAGAL MEMBUKA PAGE!")
            print("=" * 60)

            continue

        # =================================================
        # AMBIL HTML PAGE
        # =================================================

        html = sb.get_page_source()

        soup = BeautifulSoup(html, "lxml")

        # =================================================
        # AMBIL SEMUA LINK PUTUSAN
        # =================================================

        putusan_links = []

        for link in soup.find_all("a", href=True):

            href = link["href"]

            if "/direktori/putusan/" in href:

                # =========================================
                # FIX URL RELATIVE
                # =========================================

                if not href.startswith("http"):

                    href = (
                        "https://putusan3.mahkamahagung.go.id"
                        + href
                    )

                # =========================================
                # HINDARI DUPLIKAT
                # =========================================

                if href not in putusan_links:

                    putusan_links.append(href)

        print("=" * 60)
        print(f"TOTAL PUTUSAN PAGE {page_number}:")
        print(len(putusan_links))
        print("=" * 60)

        # =================================================
        # LOOP PUTUSAN
        # =================================================

        for index, putusan_url in enumerate(putusan_links):

            print("\n")
            print("=" * 60)
            print(
                f"PAGE {page_number} "
                f"| PUTUSAN {index + 1}"
            )
            print("=" * 60)

            print(putusan_url)

            # =============================================
            # OPEN HALAMAN PUTUSAN
            # =============================================

            success_open_putusan = False

            for retry in range(MAX_RETRY):

                try:

                    print(
                        f"COBA OPEN PUTUSAN "
                        f"({retry+1}/{MAX_RETRY})"
                    )

                    sb.open(putusan_url)

                    sb.sleep(3)

                    success_open_putusan = True

                    break

                except Exception as e:

                    print("ERROR OPEN PUTUSAN:")
                    print(e)

                    sb.sleep(5)

            # =============================================
            # JIKA GAGAL OPEN PUTUSAN
            # =============================================

            if not success_open_putusan:

                print("=" * 60)
                print("SKIP PUTUSAN!")
                print("=" * 60)

                continue

            # =============================================
            # AMBIL SEMUA LINK
            # =============================================

            all_links = sb.find_elements("a")

            pdf_url = None
            pdf_name = None

            # =============================================
            # CARI LINK PDF
            # =============================================

            for link in all_links:

                try:

                    href = link.get_attribute("href")
                    text = link.text.strip()

                    if (
                        href
                        and "/pdf/" in href
                    ):

                        pdf_url = href
                        pdf_name = text

                        break

                except:
                    pass

            # =============================================
            # PDF TIDAK DITEMUKAN
            # =============================================

            if not pdf_url:

                print("=" * 60)
                print("PDF TIDAK DITEMUKAN!")
                print("=" * 60)

                continue

            print("=" * 60)
            print("PDF DITEMUKAN!")
            print("=" * 60)

            print("NAMA PDF:")
            print(pdf_name)

            print("\nPDF URL:")
            print(pdf_url)

            # =============================================
            # FILE NAME AMAN
            # =============================================

            safe_name = (
                pdf_name
                .replace("/", "_")
                .replace("\\", "_")
                .replace(":", "_")
                .replace("*", "_")
                .replace("?", "_")
                .replace('"', "_")
                .replace("<", "_")
                .replace(">", "_")
                .replace("|", "_")
            )

            file_path = os.path.join(
                DOWNLOAD_FOLDER,
                safe_name
            )

            # =============================================
            # SKIP FILE JIKA SUDAH ADA
            # =============================================

            if os.path.exists(file_path):

                print("=" * 60)
                print("FILE SUDAH ADA, SKIP...")
                print("=" * 60)

                continue

            # =============================================
            # DOWNLOAD PDF VIA BROWSER
            # =============================================

            success_download = False

            for retry in range(MAX_RETRY):

                try:

                    print(
                        f"COBA DOWNLOAD "
                        f"({retry+1}/{MAX_RETRY})"
                    )

                    # BUKA PDF LANGSUNG

                    sb.open(pdf_url)

                    # TUNGGU DOWNLOAD

                    time.sleep(15)

                    print("=" * 60)
                    print("DOWNLOAD BERHASIL!")
                    print("=" * 60)

                    success_download = True

                    break

                except Exception as e:

                    print("ERROR DOWNLOAD:")
                    print(e)

                    time.sleep(5)
            
            # JIKA GAGAL TOTAL

            if not success_download:

                print("=" * 60)
                print("DOWNLOAD GAGAL TOTAL")
                print("=" * 60)

            # RANDOM DELAY

            delay = random.randint(3, 7)

            print(f"DELAY {delay} DETIK...")

            time.sleep(delay)

    # SELESAI

    print("\n")
    print("=" * 60)
    print("SEMUA DOWNLOAD SELESAI!")
    print("=" * 60)

    print("HASIL DOWNLOAD:")
    print(DOWNLOAD_FOLDER)

    input("Tekan Enter untuk keluar...")