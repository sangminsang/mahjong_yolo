import cv2
import numpy as np
from ultralytics import YOLO
import json
import tkinter as tk
from tkinter import filedialog

def load_model():
    model = YOLO("E:/학습한 가중치/1차/best.pt")
    return model

def detect_mahjong_tiles_in_image(model, image_path):
    image = cv2.imread(image_path)
    detected_tiles = []

    # 모델로 이미지에서 마작 패 감지
    results = model(image)
    frame_tiles = []
    
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

        # 감지한 범위 표시
        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(image, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    detected_tiles.append(frame_tiles)

    # 이미지 보여주기
    cv2.imshow('Mahjong Detection', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    save_detected_tiles(detected_tiles)

def save_detected_tiles(detected_tiles, filename="detected_tiles.json"):
    with open(filename, 'w') as f:
        json.dump(detected_tiles, f, indent=4)

def select_image():
    root = tk.Tk()
    root.withdraw()

    image_path = filedialog.askopenfilename(
        initialdir="c", 
        title="Select Image File",
        filetypes=(("Image files", "*.jpg;*.png"), ("All files", "*.*"))
    )
    return image_path

if __name__ == '__main__':
    model = load_model()
    image_path = select_image()

    if image_path:
        detect_mahjong_tiles_in_image(model, image_path)
    else:
        print("No file selected.")
