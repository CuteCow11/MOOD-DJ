import json
import os
import random

DATA_FILE = "brain_data.json"


DEFAULT_DATA = {
    "banned_song_ids": [],
    "region_scores": {
        "hindi": 10,
        "english": 10,
        "punjabi": 10,
        "korean": 10
    },
    "current_region": "hindi",
    "total_songs_played": 0
}

def load_brain():
    """Loads data. Handles missing files gracefully."""
    if not os.path.exists(DATA_FILE):
        return DEFAULT_DATA.copy()
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)

            for key in DEFAULT_DATA:
                if key not in data:
                    data[key] = DEFAULT_DATA[key]
            return data
    except:
        return DEFAULT_DATA.copy()

def save_brain(data):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving brain: {e}")

def get_best_region():
    """Returns the user's favorite region."""
    data = load_brain()

    return data.get("current_region", "english")

def is_song_banned(song_id):
    """Checks if a song is banned."""
    data = load_brain()
    return song_id in data["banned_song_ids"]

def train_model(song_id, time_listened, region_tag="hindi"):
    """
    Main learning logic.
    """
    data = load_brain()
    data["total_songs_played"] += 1
    

    if region_tag not in data["region_scores"]:
        data["region_scores"][region_tag] = 10

    print(f"\n[BRAIN] Analyzing feedback for '{region_tag.upper()}'...")


    if time_listened < 15:
        print(f"   -> Skipped instantly ({time_listened:.1f}s). BANNING song.")
        if song_id not in data["banned_song_ids"]:
            data["banned_song_ids"].append(song_id)
        data["region_scores"][region_tag] -= 3
        
    elif time_listened < 30:
        print(f"   -> Skipped early ({time_listened:.1f}s). Lowering score.")
        data["region_scores"][region_tag] -= 1
        
    else:
        print(f"   -> Liked ({time_listened:.1f}s). Boosting score!")
        data["region_scores"][region_tag] += 2


    if data["region_scores"][region_tag] < 0:
        data["region_scores"][region_tag] = 0
    all_scores = list(data["region_scores"].values())
    if all(score == 0 for score in all_scores):
        print("   [BRAIN] Scores too low. Resetting all to 10.")
        for key in data["region_scores"]:
            data["region_scores"][key] = 10

    max_score = max(data["region_scores"].values())
    candidates = [r for r, s in data["region_scores"].items() if s == max_score]
    best_region = random.choice(candidates)
    
    data["current_region"] = best_region
    print(f"   -> New Score for {region_tag}: {data['region_scores'][region_tag]}")
    print(f"   -> Current Favorite: {best_region.upper()}")

    save_brain(data)
