import cv2
import json
import os
import time
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import pytz

# ---------- load config ----------
with open("config.json", "r") as f:
    config = json.load(f)

site_name = config["site_name"]
show_video = config.get("show_video", False)

model_cfg = config["model"]
detection_cfg = config["detection_settings"]
display_cfg = config["display_settings"]
runtime_cfg = config["runtime"]
cameras_cfg = config["camera"]

base_detected_dir = config["detected_objects"]
detection_frame_interval = config["detection_frame_interval"]

# ---------- Singapore timezone ----------
SG_TZ = pytz.timezone("Asia/Singapore")

# ---------- logging (daily rotation + terminal) ----------
log_file = config["log_file_path"]

log_dir = os.path.dirname(log_file)
if log_dir:
    os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

file_handler = TimedRotatingFileHandler(
    log_file, when="midnight", interval=1, backupCount=7
)
file_handler.suffix = "%Y-%m-%d"
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

logging.info("========== Application Started ==========")
logging.info(f"Site Name : {site_name}")

# ---------- load YOLO ----------
logging.info("Loading YOLO model...")

with open(model_cfg["classes_path"], "r") as f:
    classes = [c.strip() for c in f.readlines()]

target_class_id = classes.index(model_cfg["target_class"])

net = cv2.dnn.readNetFromDarknet(
    model_cfg["config_path"],
    model_cfg["weight_path"],
)

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

logging.info("YOLO model loaded successfully")


# ---------- camera helper ----------
def open_camera(name, cfg):
    logging.info(f"Connecting to camera: {name}")
    cap = cv2.VideoCapture(cfg["url"])

    if not cap.isOpened():
        logging.error(f"Failed to open camera: {name}")
        return None

    cap.set(cv2.CAP_PROP_FPS, cfg["fps"])
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cfg["width"])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cfg["height"])

    logging.info(f"Camera {name} connected")
    return cap


# ---------- initialize cameras ----------
cameras = {}

for cam_name, cam_cfg in cameras_cfg.items():
    cam_base_dir = os.path.join(base_detected_dir, cam_name)
    os.makedirs(cam_base_dir, exist_ok=True)

    cap = open_camera(cam_name, cam_cfg)

    cameras[cam_name] = {
        "cap": cap,
        "cfg": cam_cfg,
        "base_dir": cam_base_dir,
    }

    logging.info(f"Camera initialized: {cam_name}")

# ---------- main loop ----------
try:
    while True:
        for cam_name, cam in cameras.items():
            cap = cam["cap"]

            if cap is None or not cap.isOpened():
                logging.warning(f"Reconnecting camera: {cam_name}")
                time.sleep(2)
                cam["cap"] = open_camera(cam_name, cam["cfg"])
                continue

            ret, frame = cap.read()
            if not ret:
                logging.warning(f"Frame read failed: {cam_name}")
                cap.release()
                cam["cap"] = open_camera(cam_name, cam["cfg"])
                continue

            # ---- frame interval control ----
            if int(cap.get(cv2.CAP_PROP_POS_FRAMES)) % detection_frame_interval != 0:
                continue

            height, width = frame.shape[:2]

            blob = cv2.dnn.blobFromImage(
                frame,
                1 / 255.0,
                (model_cfg["model_size"], model_cfg["model_size"]),
                swapRB=True,
                crop=False,
            )

            net.setInput(blob)
            detections = net.forward(output_layers)

            boxes, confidences, class_ids = [], [], []

            for output in detections:
                for det in output:
                    scores = det[5:]
                    class_id = int(scores.argmax())
                    confidence = scores[class_id]

                    if class_id != target_class_id:
                        continue
                    if confidence < detection_cfg["confidence_threshold"]:
                        continue

                    cx, cy, bw, bh = det[:4]
                    x = int((cx - bw / 2) * width)
                    y = int((cy - bh / 2) * height)
                    bw = int(bw * width)
                    bh = int(bh * height)

                    boxes.append([x, y, bw, bh])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

            indexes = cv2.dnn.NMSBoxes(
                boxes,
                confidences,
                detection_cfg["confidence_threshold"],
                detection_cfg["nms_threshold"],
            )

            if len(indexes) == 0:
                continue

            # ---------- Singapore time ----------
            now_sg = datetime.now(SG_TZ)
            today = now_sg.strftime("%Y-%m-%d")
            timestamp = now_sg.strftime("%Y%m%d_%H%M%S")

            date_dir = os.path.join(cam["base_dir"], today)
            with_box_dir = os.path.join(date_dir, "with box")
            without_box_dir = os.path.join(date_dir, "without box")

            os.makedirs(with_box_dir, exist_ok=True)
            os.makedirs(without_box_dir, exist_ok=True)

            if runtime_cfg["save_without_bbox"]:
                raw_path = os.path.join(without_box_dir, f"{timestamp}.jpg")
                cv2.imwrite(raw_path, frame)

            boxed_frame = frame.copy()

            for i in indexes.flatten():
                x, y, bw, bh = boxes[i]
                label = classes[class_ids[i]]
                confidence = confidences[i]

                cv2.rectangle(
                    boxed_frame,
                    (x, y),
                    (x + bw, y + bh),
                    tuple(display_cfg["box_color"]),
                    display_cfg["box_thickness"],
                )

                cv2.putText(
                    boxed_frame,
                    f"{label} {confidence:.2f}",
                    (x, max(y - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    display_cfg["text_size"],
                    tuple(display_cfg["text_color"]),
                    2,
                )

            if runtime_cfg["save_with_bbox"]:
                boxed_path = os.path.join(with_box_dir, f"{timestamp}.jpg")
                cv2.imwrite(boxed_path, boxed_frame)

            if show_video:
                cv2.imshow(cam_name, boxed_frame)

        if show_video and cv2.waitKey(1) & 0xFF == ord("q"):
            logging.info("Exit requested by user")
            break

except KeyboardInterrupt:
    logging.warning("Keyboard interrupt received")

finally:
    for cam in cameras.values():
        if cam["cap"]:
            cam["cap"].release()
    cv2.destroyAllWindows()
    logging.info("========== Application Stopped ==========")
