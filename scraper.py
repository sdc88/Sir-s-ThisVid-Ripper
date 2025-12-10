#!/usr/bin/env python3
"""
Sir's ThisVid Scraper
=====================
Bulk download videos from ThisVid listing pages.

Usage:
    1. Set START_PAGE and END_PAGE below
    2. Run: python scraper.py
    3. Videos download to thisvid_downloads/

The script tracks progress in CSV files, so you can stop and resume anytime.
"""

import os
import csv
import requests
from bs4 import BeautifulSoup
import subprocess
import time

# =============================================================================
# CONFIGURATION - CHANGE THESE VALUES
# =============================================================================

START_PAGE = 37068  # Script starts from this page and works backwards
END_PAGE = 37060    # Script stops at this page (set to 1 for everything)

# Change this URL pattern to scrape different sections
# The {} is where the page number goes
BASE_URL = "https://thisvid.com/gay-newest/{}/"

# Folder where videos will be saved
DOWNLOAD_FOLDER = "thisvid_downloads"

# =============================================================================
# DON'T EDIT BELOW THIS LINE (unless you know what you're doing)
# =============================================================================

LINKS_FILE = "download_status.csv"
PAGES_FILE = "scraped_pages.txt"


def load_scraped_pages():
    """Load the set of page numbers we've already scraped."""
    if not os.path.exists(PAGES_FILE):
        return set()
    try:
        with open(PAGES_FILE, 'r') as f:
            return {int(line.strip()) for line in f}
    except (IOError, ValueError) as e:
        print(f"Warning: Could not read {PAGES_FILE}. Starting fresh. Error: {e}")
        return set()


def load_video_statuses():
    """Load the dictionary of video URLs and their download status."""
    if not os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['video_url', 'status'])
        return {}

    video_status_map = {}
    try:
        with open(LINKS_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                if row:
                    video_status_map[row[0]] = row[1]
    except (IOError, StopIteration) as e:
        print(f"Warning: Could not read {LINKS_FILE}. Starting with an empty list. Error: {e}")
        return {}
    return video_status_map


def update_status_in_csv(video_url, status):
    """Update the status of a single video in the CSV file."""
    rows = []
    with open(LINKS_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    url_found = False
    for i, row in enumerate(rows):
        if row and row[0] == video_url:
            rows[i][1] = status
            url_found = True
            break

    with open(LINKS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def scrape_new_pages(start_page, end_page, scraped_pages_set, video_status_map):
    """Scrape listing pages for video links."""
    print("--- STEP 1: SCRAPING NEW PAGES ---")
    print(f"Checking pages from {start_page} down to {end_page}.")

    new_links_added = 0
    for page_num in range(start_page, end_page - 1, -1):
        if page_num in scraped_pages_set:
            print(f"Page {page_num}: Already scraped. Skipping.")
            continue

        page_url = BASE_URL.format(page_num)
        print(f"Page {page_num}: Scraping...")

        try:
            response = requests.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            page_video_links = [
                a['href'] for a in soup.find_all('a', class_='tumbpu')
                if a.has_attr('href')
            ]

            if not page_video_links:
                print(f" -> No links found on page {page_num}.")
            print(len(page_video_links), "links found on page", page_num)

            with open(LINKS_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for link in page_video_links:
                    if link not in video_status_map:
                        video_status_map[link] = 'pending'
                        writer.writerow([link, 'pending'])
                        new_links_added += 1

            with open(PAGES_FILE, 'a') as f:
                f.write(f"{page_num}\n")
            scraped_pages_set.add(page_num)
            print(f" -> Success. Added {len(page_video_links)} links (if new).")

        except requests.exceptions.RequestException as e:
            print(f" -> FAILED to scrape page {page_num}: {e}")

        time.sleep(1)  # Be nice to the server

    print(f"\nScraping finished. Added a total of {new_links_added} new video links to the list.")


def download_pending_videos(video_status_map):
    """Download all videos that have 'pending' status."""
    print("\n--- STEP 2: DOWNLOADING PENDING VIDEOS ---")
    urls_to_download = [url for url, status in video_status_map.items() if status == 'pending']

    if not urls_to_download:
        print("No pending videos to download. All tasks are complete.")
        return

    print(f"Found {len(urls_to_download)} videos to download.")
    for i, video_url in enumerate(urls_to_download, 1):
        print(f"\nDownloading video {i}/{len(urls_to_download)}: {video_url}")
        try:
            command = [
                'yt-dlp',
                '--format', 'best',
                '-o', os.path.join(DOWNLOAD_FOLDER, '%(title)s - [%(id)s].%(ext)s'),
                video_url
            ]
            subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')
            update_status_in_csv(video_url, 'completed')
            print(f" -> SUCCESS.")
        except subprocess.CalledProcessError as e:
            update_status_in_csv(video_url, 'failed')
            print(f" -> FAILED. See error below:\n{e.stderr.strip()}")
        except Exception as e:
            update_status_in_csv(video_url, 'failed')
            print(f" -> FAILED with an unexpected error: {e}")


def main():
    """Main entry point."""
    print("=" * 50)
    print("Sir's ThisVid Scraper")
    print("=" * 50)

    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    scraped_pages = load_scraped_pages()
    video_statuses = load_video_statuses()

    scrape_new_pages(START_PAGE, END_PAGE, scraped_pages, video_statuses)
    download_pending_videos(video_statuses)

    print("\nScript finished.")


if __name__ == "__main__":
    main()
