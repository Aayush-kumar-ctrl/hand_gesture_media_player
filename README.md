
#  Hand Gesture Media Player Controller

Control your media player using **hand gestures** through your webcam.
This project uses **OpenCV**, **MediaPipe**, and system automation libraries to detect gestures and perform media actions like play/pause, track change, and volume control.

---

## Features

✅ Play / Pause media using **Open Palm**
✅ Next Track using **Swipe Right**
✅ Previous Track using **Swipe Left**
✅ Volume Up using **Thumbs Up**
✅ Volume Down using **Thumbs Down**
✅ Real-time hand tracking using MediaPipe
✅ Works with most media players (Spotify, VLC, YouTube, etc.)

---

##  How It Works

1. Webcam captures live video feed.
2. MediaPipe detects hand landmarks.
3. Gesture recognition logic identifies gestures.
4. Actions module sends system media commands.

---

## Project Structure

```
├── main.py                  # Main application loop
├── gesture_recognition.py   # Hand detection + gesture logic
├── actions.py               # Media control actions (play, volume, etc.)
```

---

## Requirements

* Python 3.8+
* Webcam
* Windows (Best support for system volume via Pycaw)

---

## Run Project

```bash
python main.py
```

Press **Q** to exit.

---

## Gesture Controls

| Gesture     | Action         |
| ----------- | -------------- |
| Open Palm   | Play / Pause   |
| Swipe Right | Next Track     |
| Swipe Left  | Previous Track |
| Thumbs Up   | Volume Up      |
| Thumbs Down | Volume Down    |

---

## Modules Explanation

### main.py

* Captures webcam feed
* Detects gestures
* Triggers media actions

### gesture_recognition.py

* Hand landmark detection
* Finger state detection
* Swipe detection using movement buffer

### actions.py

* Sends media control commands
* Handles system volume (Windows Pycaw support)
* Fallback using keyboard / pyautogui

---

## Notes

* For best results:

  * Use good lighting
  * Keep hand clearly visible
* Volume control works best on **Windows with Pycaw installed**
* Some media apps may require focus window

---

## Future Improvements

* Multi-hand gesture support
* Gesture customization
* GUI interface
* Cross-platform volume control

---

## 👨‍💻 Author
AAYUSH KUMAR 
---
