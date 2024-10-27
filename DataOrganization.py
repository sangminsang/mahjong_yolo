import os

# 경로 설정
merged_dataset_path = r"C:/Users/oracl/Downloads/mahjongdata/merged_data"

def check_and_clean_labels(subdir):
    label_dir = os.path.join(merged_dataset_path, subdir, 'labels')
    labels = [f for f in os.listdir(label_dir) if f.endswith('.txt')]
    
    for label in labels:
        label_path = os.path.join(label_dir, label)
        with open(label_path, 'r') as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 5:  # 객체 감지(detection) 데이터 형식 (class_id x_center y_center width height)
                new_lines.append(line)
            else:
                print(f"잘못된 형식의 레이블 발견 및 제거: {label_path} - {line.strip()}")

        with open(label_path, 'w') as f:
            f.writelines(new_lines)

# 학습, 검증, 테스트 데이터셋에서 레이블 파일 확인 및 정리
check_and_clean_labels('train')
check_and_clean_labels('valid')
check_and_clean_labels('test')

print("데이터셋 정리 완료")
