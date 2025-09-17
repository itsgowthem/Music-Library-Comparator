# Music-Library-Comparator

A Python script designed to compare two music library exports and identify missing songs. This is particularly useful for synchronizing a primary library (like an iPod) with a local computer's MP3 collection.

The script intelligently normalizes and compares song metadata from two different CSV files to produce a final list of tracks that are present in the first library but absent from the second.

## Key Features

  - **Intelligent Matching:** Compares both **Artist** and **Song Title** for accurate identification.
  - **Robust Normalization:** Cleans up text from both files—removing extra data like "(Live)", "(feat...)", and various punctuation—to ensure reliable matching.
  - **Handles Messy Exports:** Built to handle different file encodings and formatting quirks from various export tools.
  - **Easy to Use:** Simply name your files `list1.csv` and `list2.csv`, place them in the same folder as the script, and run it.

## Requirements

1.  **Python 3:** With the `pandas` library installed.
    ```bash
    pip install pandas
    ```
2.  **iTunes:** Or any similar software that can export your primary music library's metadata to a text or CSV file.
3.  **Mp3tag (Recommended):** An excellent tool for exporting metadata from local MP3 files into a clean CSV format. Other tools can be used if they produce a CSV with 'Artist' and 'Title' columns.

## Usage Guide

Follow these steps to generate your list of missing songs.

### Step 1: Export Your Primary Library (The "Master List")

This list should be the complete collection you want to check against. In this example, we use an iPod library exported via iTunes.

1.  Open iTunes and select the songs in your library or a specific playlist.
2.  Navigate to **File \> Library \> Export Playlist...**.
3.  Save the file as a **Text file (`.txt`)**. The script is configured to handle the tab-separated format from this export.
4.  Rename the exported file to **`list1.csv`**.

### Step 2: Export Your Local MP3 Library

This list contains the songs you want to compare *against* the master list.

1.  Open **Mp3tag**.
2.  Drag and drop your entire local music folder into the application.
3.  Select all the files (Ctrl+A).
4.  Right-click the selected files and choose **Export**.
5.  Select **csv** from the list and click OK. This will generate a CSV file with the necessary `Artist` and `Title` columns.
6.  Rename this file to **`list2.csv`**.

### Step 3: Run the Script

1.  Place both `list1.csv` and `list2.csv` in the **same folder** as the Python script.
2.  Open a terminal or command prompt, navigate to that folder, and run the script:
    ```bash
    python your_script_name.py
    ```

The script will execute and create **`final_list.csv`**, which contains the detailed list of songs present in `list1` but missing from `list2`.

-----

## Customization

If your CSV files use different column names for the artist and song title, you can easily update them in the **Configuration** section at the top of the Python script.

```python
# --- Column Names from LIST 1 ---
L1_SONG_TITLE_COL = 'Name'
L1_ARTIST_COL = 'Artist'

# --- Column Names from LIST 2 (Updated) ---
L2_SONG_TITLE_COL = 'Title'
L2_ARTIST_COL = 'Artist'
```
