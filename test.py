import cv2
import numpy as np
from ultralytics import YOLO
import json
import tkinter as tk
from tkinter import filedialog

def load_model():
    model = YOLO("E:/학습한 가중치/2차/exp1/weights/epoch100.pt")
    return model

def detect_mahjong_tiles(model, video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    detected_tiles = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_tiles = []
        results = model(frame)

        for det in results[0].boxes:
            x1, y1, x2, y2 = det.xyxy[0]
            conf = det.conf[0]
            cls = int(det.cls[0])
            label = model.names[cls]
            frame_tiles.append({
                "x1": int(x1),
                "y1": int(y1),
                "x2": int(x2),
                "y2": int(y2),
                "confidence": float(conf),
                "class": label
            })

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        detected_tiles.append(frame_tiles)

        cv2.imshow('Mahjong Detection', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('j'):
            current_pos = cap.get(cv2.CAP_PROP_POS_FRAMES)
            new_pos = max(0, current_pos - (5 * fps))
            cap.set(cv2.CAP_PROP_POS_FRAMES, new_pos)
        elif key == ord('l'):
            current_pos = cap.get(cv2.CAP_PROP_POS_FRAMES)
            new_pos = min(frame_count - 1, current_pos + (5 * fps))
            cap.set(cv2.CAP_PROP_POS_FRAMES, new_pos)

    cap.release()
    cv2.destroyAllWindows()
    save_detected_tiles(detected_tiles)

def save_detected_tiles(detected_tiles, filename="detected_tiles.json"):
    with open(filename, 'w') as f:
        json.dump(detected_tiles, f, indent=4)

def select_video():
    root = tk.Tk()
    root.withdraw()

    video_path = filedialog.askopenfilename(
        initialdir="c", 
        title="Select Video File",
        filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*"))
    )
    return video_path

if __name__ == '__main__':
    model = load_model()
    video_path = select_video()

    if video_path:
        detect_mahjong_tiles(model, video_path)
    else:
        print("No file selected.")