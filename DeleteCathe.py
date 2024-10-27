import os

# 통합된 데이터셋 경로 설정
merged_dataset_path = r"C:/Users/oracl/Downloads/mahjongdata/merged_data"

# 캐시 파일 경로 설정
train_cache = os.path.join(merged_dataset_path, 'train', 'labels.cache')
valid_cache = os.path.join(merged_dataset_path, 'valid', 'labels.cache')

# 캐시 파일 삭제
if os.path.exists(train_cache):
    os.remove(train_cache)
    print(f"{train_cache} 삭제 완료")
else:
    print(f"{train_cache} 파일을 찾을 수 없습니다.")

if os.path.exists(valid_cache):
    os.remove(valid_cache)
    print(f"{valid_cache} 삭제 완료")
else:
    print(f"{valid_cache} 파일을 찾을 수 없습니다.")
