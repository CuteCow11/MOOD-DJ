import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import brain  

def setup_spotify():
    SPOTIPY_CLIENT_ID = "YOUR SPOTIPY_CLIENT_ID"         
    SPOTIPY_CLIENT_SECRET = "YOUR SPOTIPY_CLIENT_SECRET"
    SPOTIPY_REDIRECT_URI = "YOUR SPOTIPY_REDIRECT_URI"

    scope = "user-library-read playlist-modify-public user-top-read user-read-playback-state user-modify-playback-state"
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=scope,
        open_browser=True,
        cache_path="token.txt"
    ))
    return sp

def get_user_seeds(sp):
    return []

def detect_emotion(detector, frame):
    try:
        analysis = detector.detect_emotions(frame)
        if analysis:
            return detector.top_emotion(frame)
    except:
        pass
    return None, None

def get_spotify_recommendations(sp, emotion):

    try:
        preferred_region = brain.get_best_region()
    except Exception as e:
        print(f"Brain Error: {e}. Defaulting to Hindi.")
        preferred_region = "hindi"

    print(f"   [AI] Targeting Region: {preferred_region.upper()}")

    search_query = ""
    if emotion == 'happy':
        search_query = random.choice([f"happy {preferred_region} pop", f"upbeat {preferred_region}"])
    elif emotion == 'sad':
        search_query = random.choice([f"sad {preferred_region} songs", f"{preferred_region} acoustic"])
    elif emotion == 'angry':
        search_query = random.choice([f"angry {preferred_region} rock", f"high energy {preferred_region}"])
    elif emotion == 'neutral':
        search_query = random.choice([f"chill {preferred_region} lofi", f"soft {preferred_region}"])
    elif emotion == 'surprise':
        search_query = f"trending {preferred_region} viral"
    elif emotion == 'fear':
        search_query = "cinematic suspense"
    elif emotion == 'disgust':
        search_query = "heavy metal"


    try:
        print(f"   -> Searching: '{search_query}'...")
        random_offset = random.randint(0, 50)
        
        results = sp.search(q=search_query, limit=20, offset=random_offset, type='track')
        raw_items = results['tracks']['items']
        

        valid_items = []
        for item in raw_items:
            if not brain.is_song_banned(item['id']):
                valid_items.append(item)
            else:
                print(f"   [AI] Filtered Banned Song: {item['name']}")

        if valid_items:
            random.shuffle(valid_items)
            return valid_items, preferred_region
        else:

            fallback = sp.search(q=f"top {preferred_region}", limit=10)
            return fallback['tracks']['items'], preferred_region

    except Exception as e:
        print(f"   -> Search failed: {e}")
        return [], "english"

def play_track_object(track, sp):
    try:
        devices = sp.devices()
        active_device = next((d for d in devices['devices'] if d['is_active']), None)
        if not active_device and devices['devices']:
            active_device = devices['devices'][0]
        
        if active_device:
            sp.start_playback(device_id=active_device['id'], uris=[track['uri']])
        else:
            print("No active Spotify device found.")
    except Exception as e:
        print(f"Could not play: {e}")
