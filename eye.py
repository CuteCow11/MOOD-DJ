
import cv2
from fer.fer import FER

detector = FER(mtcnn=False) 

def detect_emotion(frame):
    """
    Takes a video frame and returns the dominant emotion using FER.
    """
    try:
        result = detector.detect_emotions(frame)
        if result:
            top_face = result[0]
            emotions = top_face['emotions']
            dominant_emotion = max(emotions, key=emotions.get)
            return dominant_emotion
            
        return None

    except Exception as e:
        print(f"⚠️ Vision Error: {e}")
        return None

def draw_results(frame, emotion):
    """
    Helper to draw the emotion text on the video frame.
    """
    if emotion:
        cv2.putText(frame, f"Emotion: {emotion.upper()}", (30, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return frame