import os
import shutil

# 수정된 매핑 테이블
label_mapping = {
    '0': '1man', '1': '1pin', '2': '1sou',
    '3': '2man', '4': '2pin', '5': '2sou',
    '6': '3man', '7': '3pin', '8': '3sou',
    '9': '4man', '10': '4pin', '11': '4sou',
    '12': '5man', '13': '5pin', '14': '5sou',
    '15': '6man', '16': '6pin', '17': '6sou',
    '18': '7man', '19': '7pin', '20': '7sou',
    '21': '8man', '22': '8pin', '23': '8sou',
    '24': '9man', '25': '9pin', '26': '9sou',
    '27': 'chun', '28': 'east', '29': 'haku', '30': 'hatsu', '31': 'north', '32': 'south', '33': 'west',
    '34': 'back', '35': 'r5man', '36': 'r5pin', '37': 'r5sou'
}

# 뒤쪽 데이터셋의 매핑 테이블
reverse_label_mapping = {
    '1man': 0, '1pin': 1, '1sou': 2,
    '2man': 3, '2pin': 4, '2sou': 5,
    '3man': 6, '3pin': 7, '3sou': 8,
    '4man': 9, '4pin': 10, '4sou': 11,
    '5man': 12, '5pin': 13, '5sou': 14,
    '6man': 15, '6pin': 16, '6sou': 17,
    '7man': 18, '7pin': 19, '7sou': 20,
    '8man': 21, '8pin': 22, '8sou': 23,
    '9man': 24, '9pin': 25, '9sou': 26,
    'chun': 27, 'east': 28, 'haku': 29, 'hatsu': 30, 'north': 31, 'south': 32, 'west': 33,
    'back': 34, 'r5man': 35, 'r5pin': 36, 'r5sou': 37
}

# 경로 설정
first_dataset_path = r"C:/Users/oracl/Downloads/mahjongdata/YOLO_Mahjong.v7i.yolov9"
second_dataset_path = r"C:/Users/oracl/Downloads/mahjongdata/Riichi Mahjong.v8i.yolov9"
merged_dataset_path = r"C:/Users/oracl/Downloads/mahjongdata/merged_data"

# 결과를 저장할 파일 경로 설정
result_file_path = r"C:/Users/oracl/Downloads/data_merge_results.txt"

# 폴더 구조 설정
os.makedirs(os.path.join(merged_dataset_path, 'train', 'images'), exist_ok=True)
os.makedirs(os.path.join(merged_dataset_path, 'train', 'labels'), exist_ok=True)
os.makedirs(os.path.join(merged_dataset_path, 'valid', 'images'), exist_ok=True)
os.makedirs(os.path.join(merged_dataset_path, 'valid', 'labels'), exist_ok=True)
os.makedirs(os.path.join(merged_dataset_path, 'test', 'images'), exist_ok=True)
os.makedirs(os.path.join(merged_dataset_path, 'test', 'labels'), exist_ok=True)

def convert_label(old_label):
    global label_mapping
    global reverse_label_mapping
    old_label_str = str(old_label)
    if old_label_str in label_mapping:
        new_label = label_mapping[old_label_str]
        if new_label in reverse_label_mapping:
            converted_label = reverse_label_mapping[new_label]
            with open(result_file_path, 'a') as f:
                f.write(f"변환 성공: {old_label_str} -> {new_label} -> {converted_label}/n")
            return converted_label
    with open(result_file_path, 'a') as f:
        f.write(f"레이블 변환 실패: {old_label_str}/n")
    return None

def process_file(file_path, new_file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 5:
            with open(result_file_path, 'a') as f:
                f.write(f"잘못된 레이블 형식: {line.strip()}/n")
            continue
        
        old_label = parts[0]
        new_label = convert_label(old_label)
        if new_label is not None:
            new_line = f"{new_label} {' '.join(parts[1:])}/n"
            new_lines.append(new_line)
        else:
            with open(result_file_path, 'a') as f:
                f.write(f"레이블 변환 실패: {old_label}/n")

    with open(new_file_path, 'w') as f:
        f.writelines(new_lines)
    
    if not new_lines:
        with open(result_file_path, 'a') as f:
            f.write(f"빈 레이블 파일 생성: {new_file_path}/n")
    else:
        with open(result_file_path, 'a') as f:
            f.write(f"레이블 파일 생성 성공: {new_file_path}/n")

def copy_and_convert_labels(source_path, dest_path, image_subdir, label_subdir):
    for subdir, _, files in os.walk(os.path.join(source_path, label_subdir)):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(subdir, file)
                new_file_path = file_path.replace(source_path, dest_path)
                new_file_path = new_file_path.replace(label_subdir, label_subdir)
                os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                process_file(file_path, new_file_path)

    for subdir, _, files in os.walk(os.path.join(source_path, image_subdir)):
        for file in files:
            if file.endswith(('.jpg', '.png')):
                file_path = os.path.join(subdir, file)
                new_file_path = file_path.replace(source_path, dest_path)
                os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                shutil.copy2(file_path, new_file_path)

# 결과 파일 초기화
with open(result_file_path, 'w') as f:
    f.write("데이터 통합 결과:/n")

# 레이블 파일 및 이미지 파일 변환 및 복사
copy_and_convert_labels(first_dataset_path, merged_dataset_path, 'train/images', 'train/labels')
copy_and_convert_labels(first_dataset_path, merged_dataset_path, 'valid/images', 'valid/labels')
copy_and_convert_labels(first_dataset_path, merged_dataset_path, 'test/images', 'test/labels')

copy_and_convert_labels(second_dataset_path, merged_dataset_path, 'train/images', 'train/labels')
copy_and_convert_labels(second_dataset_path, merged_dataset_path, 'valid/images', 'valid/labels')
copy_and_convert_labels(second_dataset_path, merged_dataset_path, 'test/images', 'test/labels')

with open(result_file_path, 'a') as f:
    f.write("데이터 통합 완료/n")

print("데이터 통합 완료")
