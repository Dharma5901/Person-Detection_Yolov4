# Person Detection – Video Analytics (YOLO + OpenCV)

This project is a **person detection system** built using **YOLO (Darknet)** and **OpenCV (DNN module)**. It connects to multiple RTSP cameras, detects people in live video streams, draws bounding boxes with labels, and saves images in a **camera‑wise and date‑wise folder structure**. The system also supports **daily rotating logs** and uses **Singapore time (Asia/Singapore)** consistently across logs and saved files.

---

## 🚀 Features

* ✅ Multi‑camera RTSP support
* ✅ Person detection using YOLO (Darknet weights + cfg)
* ✅ Camera‑wise & date‑wise image storage
* ✅ Save **with bounding box** and **without bounding box** images
* ✅ Object label loaded directly from `classes.names`
* ✅ Confidence score displayed on bounding box
* ✅ Frame‑interval based detection control
* ✅ Singapore timezone (UTC +08:00)
* ✅ Daily rotating log files (file + terminal)
* ✅ Auto camera reconnect on failure

---

## 📁 Project Structure

```
person_detection_v4/
├── main.py
├── config.json
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── logs/
│   └── detections.log
├── detected_objects/
│   ├── Front/
│   │   └── 2026-01-30/
│   │       ├── with box/
│   │       └── without box/
│   └── Back/
│       └── 2026-01-30/
│           ├── with box/
│           └── without box/
└── model_jan_28/
    ├── ipr_270126_best.weights
    ├── ipr_270126.cfg
    └── class_ids.names
```

---

## ⚙️ Requirements

### System

* Python **3.6+**
* Linux (recommended)
* RTSP enabled cameras

### Python Packages

Install dependencies using:

```bash
pip3 install -r requirements.txt
```

`requirements.txt`

```
opencv-python-headless==4.9.0.80
numpy
pytz
```

---

## 🛠 Configuration (`config.json`)

Key configuration options:

* **detected_objects** – base folder for saving images
* **log_file_path** – path for log file
* **model** – YOLO model paths and target class
* **camera** – multiple RTSP camera configurations
* **detection_frame_interval** – process every Nth frame

Example:

```json
"detected_objects": "detected_objects",
"log_file_path": "logs/detections.log",
"detection_frame_interval": 10
```

---

## ▶️ Running the Application

```bash
python3 main.py --config_file config.json
```

> Make sure the `logs/` directory is writable.

---

## 🕒 Timezone Handling

* All timestamps (logs, folder names, image names) use:

  ```
  Asia/Singapore (UTC +08:00)
  ```
* Implemented using `pytz` for Python < 3.9 compatibility.

---

## 🖼 Output Details

Each detected person generates:

* 📷 **Raw image** (without bounding box)
* 📦 **Annotated image** (with bounding box, label, confidence)

Label is read directly from `class_ids.names`.

---

## 📜 Logging

* Logs are written to **file + terminal**
* Daily rotation at midnight
* Keeps last **7 days** of logs

Example log:

```
2026-01-30 14:22:10 | INFO | person detected in Front (0.87)
```

---

## 🧩 Docker Support

Build and run using Docker:

```bash
docker build -t person-detection .
docker run --rm person-detection
```

Or using docker‑compose:

```bash
docker-compose up --build
```

---

## 🔒 Notes & Best Practices

* Avoid running as `sudo`
* Ensure RTSP URLs are reachable
* Ensure log and output folders have write permissions
* Use `opencv-python-headless` for server environments

---

## 📌 Future Enhancements

* ⏱ Time‑based detection instead of frame‑based
* 🎨 Per‑class colors
* 🧵 Multi‑threaded camera processing
* 📊 CSV / JSON detection reports
* 🧹 Auto‑cleanup old images

---

## 👨‍💻 Author

**Dharmaraj B**
Person Detection Application

---

If you need this README converted to **Tamil**, **Markdown + PDF**, or **company‑branded format**, just tell me 👍
