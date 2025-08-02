# 🎚️ Hand Gesture Volume Control with OpenCV and MediaPipe

This project allows you to control your **system volume** using just your **hand gestures** via a webcam. Built using **Python**, **OpenCV**, and **MediaPipe**, the application detects the distance between your **thumb and index finger** and maps it to volume levels. Ideal for touchless volume control on macOS.


---

## 🛠️ Features
- Real-time hand tracking using webcam input.
- Measures distance between thumb and index finger.
- Converts hand distance to system volume percentage.
- Works on **macOS** using `osascript` to control volume.
- Clean modular structure with reusable `HandTrackingModule`.

---

## 🚀 How It Works
1. **Detect hand** using MediaPipe's hand landmark model.
2. **Track thumb tip (id 4)** and **index finger tip (id 8)**.
3. **Calculate distance** between the two fingers.
4. **Interpolate distance** to match system volume scale (0–100%).
5. **Set volume** in real-time using macOS system command.

---

## 📦 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
