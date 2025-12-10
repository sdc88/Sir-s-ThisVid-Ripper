<p align="center">
  <h1 align="center">🎬 Sir's ThisVid Ripper</h1>
  <p align="center">
    <strong>Bulk download videos from ThisVid with ease</strong>
  </p>
  <p align="center">
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-features">Features</a> •
    <a href="#-configuration">Configuration</a> •
    <a href="#-troubleshooting">Troubleshooting</a>
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/github/license/sdc88/Sir-s-ThisVid-Ripper" alt="License">
  <img src="https://img.shields.io/badge/powered%20by-yt--dlp-red.svg" alt="Powered by yt-dlp">
</p>

---

## ✨ Features

- 📥 **Bulk downloading** — Scrape entire listing pages and download all videos
- 💾 **Progress tracking** — Stop and resume anytime, never re-download the same video
- 🔄 **Automatic retry** — Failed downloads are tracked so you can retry them later
- 🖥️ **Cross-platform** — Works on Windows, macOS, and Linux
- 🚀 **Simple setup** — Just Python and a few dependencies

---

## 🚀 Quick Start

### Prerequisites

| Requirement | How to get it |
|-------------|---------------|
| **Python 3.9+** | [python.org/downloads](https://www.python.org/downloads/) — tick "Add to PATH" on Windows! |
| **yt-dlp** | `pip install yt-dlp` |

### Installation

```bash
# Clone the repo
git clone https://github.com/sdc88/Sir-s-ThisVid-Ripper.git
cd Sir-s-ThisVid-Ripper

# Install dependencies
pip install -r requirements.txt
```

### Usage

**Windows:** Double-click `run.bat`

**Mac/Linux:** 
```bash
chmod +x run.sh
./run.sh
```

**Or manually:**
```bash
python scraper.py
```

Videos will appear in the `thisvid_downloads` folder.

---

## ⚙️ Configuration

Open `scraper.py` and edit these values at the top:

```python
START_PAGE = 37068  # Start from this page (works backwards)
END_PAGE = 37060    # Stop at this page (set to 1 for everything)

BASE_URL = "https://thisvid.com/gay-newest/{}/"  # Change category here
```

> **💡 Tip:** To find page numbers, navigate to ThisVid and look at the URL — e.g., `thisvid.com/gay-newest/500/` is page 500.

---

## 📁 Progress Files

The script creates two files to track progress:

| File | Purpose |
|------|---------|
| `download_status.csv` | All video URLs with status: `pending`, `completed`, or `failed` |
| `scraped_pages.txt` | Which listing pages have been scraped |

> ⚠️ **Don't delete these** unless you want to start from scratch!

---

## 🔧 Troubleshooting

<details>
<summary><strong>"pip is not recognized"</strong></summary>

Python wasn't added to PATH during installation. Either:
- Reinstall Python and tick "Add Python to PATH"
- Or use: `python -m pip install -r requirements.txt`
</details>

<details>
<summary><strong>"yt-dlp is not recognized"</strong></summary>

Try: `python -m pip install yt-dlp`
</details>

<details>
<summary><strong>Some videos fail to download</strong></summary>

Some videos may be private, deleted, or geo-blocked. Check `download_status.csv` to see which ones failed. To retry them, change their status from `failed` to `pending` and run the script again.
</details>

<details>
<summary><strong>I want to scrape a different category</strong></summary>

Change the `BASE_URL` variable in `scraper.py`. Keep the `{}` where the page number should go.
</details>

---

## 📜 License

[CC0 1.0 Universal](LICENSE) — Do whatever you want with this.

---

<p align="center">
  Made with ☕ by <a href="https://github.com/sdc88">Sir</a>
</p>
