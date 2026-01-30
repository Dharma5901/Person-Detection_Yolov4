# Person Detection – Video Analytics

This project is a **real‑time multi‑camera person detection system** built using **OpenCV + YOLO**. It connects to one or more RTSP cameras, detects people, draws bounding boxes with labels and confidence, and saves results in a **clean, date‑wise and camera‑wise folder structure**. The system is designed to be **production‑ready**, with robust logging, reconnection handling, and Docker support.

---

## 🚀 Key Features

* ✅ **Multi‑camera support** (RTSP streams)
* ✅ **YOLO‑based person detection**
* ✅ **Bounding box + label + confidence overlay**
* ✅ **Singapore Time (Asia/Singapore)** for timestamps
* ✅ **Date‑wise & camera‑wise image storage**
* ✅ **With box / Without box image saving**
* ✅ **Frame‑interval based detection control**
* ✅ **Daily rotating log files** (terminal + file)
* ✅ **Auto camera reconnection** on failure
* ✅ **Docker & Docker‑Compose support**

---

## 📂 Project Structure

```
person_detection_v4/
├── main.py
├── config.json
├── requirements.txt
├── Makefile
├── Dockerfile
├── install.Dockerfile
├── docker-compose.yml
├── logs/
│   └── detections.log
└── detected_objects/
    ├── Front/
    │   └── 2026-01-30/
    │       ├── with box/
    │       └── without box/
    └── Back/
        └── 2026-01-30/
            ├── with box/
            └── without box/
```
---

## 🧠 Detection Logic

* Frames are continuously read from each camera
* Detection runs every **N frames** (`detection_frame_interval`)
* YOLO detects objects
* Only the configured `target_class` (default: `person`) is processed
* Bounding boxes are filtered using **confidence threshold + NMS**

---

## 🖼️ Output Format

For every detection:

* **Without box** → original frame saved
* **With box** → bounding box + label + confidence drawn

Label is automatically read from `classes.names`.

Example overlay:

```
person 0.87
```

---

## 📝 Logging

* Logs are written to **terminal + file**
* **Daily rotating logs** using `TimedRotatingFileHandler`
* Old logs automatically cleaned (configurable via `backupCount`)

Example log:

```
2026-01-30 14:32:10 | INFO | person detected in Front (0.92)
```

---

## ▶️ How to Run (Local)

### 1. Install dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Run application

```bash
python3 main.py --config_file config.json
```

Press `q` to exit if `show_video` is enabled.

---

## 🐳 Docker Support

### Build image

```bash
docker build -t person-detection .
```

### Run with docker‑compose

```bash
docker-compose up -d
```

---

## 🛠 Requirements

* Python 3.7+
* OpenCV
* NumPy
* pytz
* RTSP‑enabled IP cameras

See `requirements.txt` for exact versions.

---

## 🔒 Production Notes

* Avoid running as `sudo`
* Ensure `logs/` and `detected_objects/` are writable
* Use strong RTSP credentials
* Prefer `opencv-python-headless` for servers

---

## 🚧 Future Enhancements

* ⏱ Time‑based detection instead of frame‑based
* 🎨 Different colors per class
* 📊 Detection metrics export (CSV / JSON)
* 🧵 Multi‑threaded camera processing
* 🧹 Auto‑cleanup old images
* ☁️ Cloud upload support

---

## 👨‍💻 Author

Built and maintained as a **real‑world CCTV video analytics system**.

---

✅ **This README reflects the full current project accurately.**
