import torch
from ultralytics import YOLO

def resume_training():
    # 모델 로드
    model_path = 'C:/Users/oracl/Downloads/runs/exp12/weights/last.pt'
    model = YOLO(model_path)
    
    # 데이터셋 경로
    data_path = "C:/Users/oracl/Downloads/mahjongdata/merged_data/merged_data.yaml"
    
    # 학습 재개
    model.train(
        data=data_path, 
        epochs=500,  # 전체 학습 에포크 수, 이전 에포크를 포함하여 설정
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
        name='exp12',  # 이전 프로젝트 이름과 동일하게 설정
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
        fliplr=0.5,   # 좌우 플립
        resume=model_path  # 학습 재개를 위한 체크포인트 경로
    )

if __name__ == '__main__':
    resume_training()
