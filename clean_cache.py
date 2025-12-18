import os

print("Searching for Spotify cache files...")

# Common names for the cache file
files_to_remove = [".spotipy_cache", ".cache", ".spotify_cache"]

found = False
for filename in os.listdir('.'):
    # Check if the file starts with .cache or matches our list
    if filename.startswith(".cache") or filename in files_to_remove:
        try:
            os.remove(filename)
            print(f"✅ DELETED: {filename}")
            found = True
        except Exception as e:
            print(f"❌ Could not delete {filename}: {e}")

if found:
    print("\nSUCCESS! Now run main.py again.")
    print("Your browser will open -> Click 'Agree' -> Copy the URL -> Paste it back here.")
else:
    print("\nNo cache files found. You might be good to go, or the file is hidden.")