from ultralytics import YOLO
import os
import torch

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

def start_training():
    model = YOLO("yolov10m.pt")
    data_path = "C:/Users/oracl/Downloads/mahjongdata/merged_data/merged_data.yaml"
    model.train(
        data=data_path, 
        epochs=500, 
        imgsz=640, 
        batch=16,  
        workers=2, 
        lr0=1e-4, 
        save_period=10, 
        cos_lr=True, 
        augment=True, 
        patience=10, 
        lrf=0.01, 
        project='runs', 
        name='exp1',
        verbose=True, 
        device='cuda' if torch.cuda.is_available() else 'cpu',
        hsv_h=0.015, 
        hsv_s=0.7, 
        hsv_v=0.4, 
        degrees=30.0,  # 회전 각도 조정
        translate=0.1, 
        scale=0.5, 
        shear=0.0, 
        perspective=0.0, 
        flipud=0.5,  # 상하 플립
        fliplr=0.5   # 좌우 플립
    )

if __name__ == '__main__':
    start_training()
