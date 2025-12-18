import cv2
from fer.fer import FER
import time
import os

try:
    import music 
except ImportError:
    print("WARNING: 'music.py' not found.")
    exit()

def run_app():
    print("--- MOOD DJ IS READY ---")
    
    # SETUP
    try:
        sp_client = music.setup_spotify()
        user = sp_client.current_user()
        print(f"Logged in as: {user['display_name']}")
    except:
        print("Login failed. Delete token.txt and try again.")
        return

    detector = FER(mtcnn=True) 
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: No webcam.")
        return

    print("Press 's' to SKIP/TRAIN. Press 'q' to QUIT.")

    while True:
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.flip(frame, 1)

        # Detect
        try:
            emotion, score = music.detect_emotion(detector, frame) if hasattr(music, 'detect_emotion') else detector.top_emotion(frame)
        except:
            emotion = None

        if emotion:
            text = f"Mood: {emotion} ({score*100:.0f}%)"
            color = (0, 255, 0)
        else:
            text = "Scanning..."
            color = (0, 0, 255)

        cv2.putText(frame, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.imshow('Mood DJ', frame)

        # PLAY LOGIC
        if emotion:
            print(f"\n[LOCKED] User is {emotion}.")
            
            # Freeze Screen
            cv2.putText(frame, "FETCHING SONG...", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            cv2.imshow('Mood DJ', frame)
            cv2.waitKey(1) 

            # Get Song
            tracks, region_tag = music.get_spotify_recommendations(sp_client, emotion)
            
            if tracks:
                track = tracks[0]
                music.play_track_object(track, sp_client)
                
                print(f"--> Playing: {track['name']} ({region_tag})")
                
                start_time = time.time()
                
                # Update UI
                cv2.putText(frame, f"Playing: {track['name']}", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(frame, f"Region: {region_tag}", (20, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
                cv2.putText(frame, "Press 's' to SKIP", (20, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                cv2.imshow('Mood DJ', frame)

                print("--> LISTENING... (Press 's' to Skip)")
                
                # Wait Loop
                while True:
                    key = cv2.waitKey(0) & 0xFF
                    
                    if key == ord('s'):
                        end_time = time.time()
                        duration = end_time - start_time
                        
                        # TRAIN AI
                        music.brain.train_model(track['id'], duration, region_tag)
                        
                        print("Rescanning...")
                        break 
                    elif key == ord('q'):
                        cap.release()
                        cv2.destroyAllWindows()
                        return 
            else:
                print("No tracks found.")
                time.sleep(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_app()