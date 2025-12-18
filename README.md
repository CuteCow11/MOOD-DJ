# 🎧 Mood DJ
> **Your face is the playlist.**

[![Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Spotify](https://img.shields.io/badge/Spotify-API-1DB954?style=flat-square&logo=spotify&logoColor=white)](https://developer.spotify.com/)
[![AI](https://img.shields.io/badge/AI-Powered-FF6F00?style=flat-square&logo=openai&logoColor=white)]()

Mood DJ lets your webcam see how you feel and uses AI to automatically curate and stream a Spotify playlist that perfectly matches your current vibe.

If you smile, the music gets upbeat. If you frown, it gets mellow. No clicks needed.

---

## 🧠 How It Works (The Vibe Flow)

This diagram shows how Mood DJ processes your video feed and turns it into music.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#1DB954', 'edgeLabelBackground':'#ffffff', 'tertiaryColor': '#f0f0f0'}}}%%
graph TD
    A[📹 Webcam Input] -->|OpenCV Captures Frame| B(👁️ Face Detection);
    B -->|FER Library Analyzes| C{🧠 AI Emotion Engine};
    
    C -- "Happy 😊" --> D[🎹 Genre: Pop/Upbeat];
    C -- "Sad 😢" --> E[🎻 Genre: Acoustic/Lo-Fi];
    C -- "Angry 😠" --> F[🎸 Genre: Rock/Metal];
    C -- "Neutral 😐" --> G[🎷 Genre: Jazz/Chill];

    D --> H[🟢 Spotify Connect];
    E --> H;
    F --> H;
    G --> H;
    
    H -->|API Call| I[🔊 Play Track on Device];
