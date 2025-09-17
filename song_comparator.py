import pandas as pd
import re
import os

# --- Configuration ---
LIST1_FILE_PATH = 'list1.csv'
LIST2_FILE_PATH = 'list2.csv'
OUTPUT_FILE_PATH = 'final_list.csv'

# --- Column Names from LIST 1 ---
L1_SONG_TITLE_COL = 'Name'
L1_ARTIST_COL = 'Artist'

# --- Column Names from LIST 2 (Updated) ---
L2_SONG_TITLE_COL = 'Title'
L2_ARTIST_COL = 'Artist'

# --- End of Configuration ---

def normalize_text(text):
    """
    Cleans and standardizes text for a reliable comparison.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    # Remove content in parentheses or brackets (e.g., "(feat. ...)")
    text = re.sub(r'[\(\[].*?[\)\]]', '', text)
    # Keep only letters and numbers, removing all punctuation/symbols
    text = re.sub(r'[^a-z0-9\s]', '', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text.strip()

def main():
    """
    Main function to execute the script.
    """
    print("Starting song comparison with separate Artist/Title columns...")

    try:
        # --- Step 1: Read each file with its specific encoding ---
        print(f"Reading '{LIST1_FILE_PATH}' with 'utf-16' encoding...")
        df_list1 = pd.read_csv(LIST1_FILE_PATH, encoding='utf-16', sep='\t')
        print(f"Successfully loaded '{LIST1_FILE_PATH}' ({len(df_list1)} rows).")

        print(f"Reading '{LIST2_FILE_PATH}' with 'latin-1' encoding...")
        df_list2 = pd.read_csv(LIST2_FILE_PATH, encoding='latin-1', on_bad_lines='warn')
        print(f"Successfully loaded '{LIST2_FILE_PATH}' ({len(df_list2)} rows).")

        # --- Step 2: Normalize Text Fields for Both Lists ---
        # Clean up and prepare the dataframes
        df_list1.dropna(subset=[L1_SONG_TITLE_COL, L1_ARTIST_COL], inplace=True)
        df_list2.dropna(subset=[L2_SONG_TITLE_COL, L2_ARTIST_COL], inplace=True)

        print("Normalizing text from LIST1...")
        df_list1['normalized_title'] = df_list1[L1_SONG_TITLE_COL].apply(normalize_text)
        df_list1['normalized_artist'] = df_list1[L1_ARTIST_COL].apply(normalize_text)

        print("Normalizing text from LIST2...")
        df_list2['normalized_title'] = df_list2[L2_SONG_TITLE_COL].apply(normalize_text)
        df_list2['normalized_artist'] = df_list2[L2_ARTIST_COL].apply(normalize_text)

        # --- Step 3: Find Common Songs Using a High-Performance Merge ---
        print("Finding common songs by matching Artist and Title...")

        # Create a unique identifier for each song in both dataframes
        df_list1['merge_key'] = df_list1['normalized_artist'] + '||' + df_list1['normalized_title']
        df_list2['merge_key'] = df_list2['normalized_artist'] + '||' + df_list2['normalized_title']

        # Get a set of the unique song identifiers from list2 for fast checking
        songs_in_list2 = set(df_list2['merge_key'])

        # Keep only the rows from list1 where the song identifier is NOT in list2
        final_df = df_list1[~df_list1['merge_key'].isin(songs_in_list2)].copy()
        
        # Calculate how many songs were removed
        removed_count = len(df_list1) - len(final_df)


        # --- Step 4: Save the Final Result ---
        # Drop the temporary helper columns before saving
        final_df = final_df.drop(columns=['normalized_title', 'normalized_artist', 'merge_key'])
        final_df.to_csv(OUTPUT_FILE_PATH, index=False)

        print("\n--- Process Complete! ---")
        print(f"Original songs in LIST1: {len(df_list1)}")
        print(f"Songs to be removed (found in LIST2): {removed_count}")
        print(f"Final list of unique songs: {len(final_df)}")
        print(f"The final list has been saved to: '{OUTPUT_FILE_PATH}'")

    except FileNotFoundError as e:
        print(f"ERROR: File not found. Please make sure '{e.filename}' is in the same folder as the script.")
    except KeyError as e:
        print(f"\nERROR: A column was not found. Please check the column names in the Configuration section.")
        print(f"Column mentioned in error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
