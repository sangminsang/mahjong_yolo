#입력받은 마작 패 14개를 또이쯔 머리 하나와 커쯔나 슌쯔 몸통 3개로 나누는 알고리즘

from collections import Counter

def find_mahjong_sets(tiles):
    tiles.sort()  # 패 정렬
    tile_count = Counter(tiles)  # 패 카운트

    # 머리 찾기
    heads = []
    for tile, count in tile_count.items():
        if count >= 2:
            heads.append((tile, 2))  # (타일 값, 개수)
    
    # 자패와 숫패 구분
    def is_honor(tile):
        return tile.endswith('z')
    
    def tile_to_value(tile):
        return int(tile[:-1])
    
    def tile_to_type(tile):
        return tile[-1]

    # 모든 머리 조합에 대해 시도
    for head_tile, head_count in heads:
        remaining_tiles = tiles[:]
        remaining_tiles.remove(head_tile)
        remaining_tiles.remove(head_tile)
        
        bodies = []
        while len(remaining_tiles) >= 3:
            found_body = False
            for tile in set(remaining_tiles):
                # 숫패인 경우: 슌쯔와 커쯔 둘 다 가능
                if not is_honor(tile):
                    tile_val = tile_to_value(tile)
                    tile_type = tile_to_type(tile)
                    
                    # 커쯔 찾기
                    if remaining_tiles.count(tile) >= 3:
                        bodies.append([tile] * 3)
                        for _ in range(3):
                            remaining_tiles.remove(tile)
                        found_body = True
                        break
                    
                    # 슌쯔 찾기
                    next_tile_1 = f"{tile_val + 1}{tile_type}"
                    next_tile_2 = f"{tile_val + 2}{tile_type}"
                    if next_tile_1 in remaining_tiles and next_tile_2 in remaining_tiles:
                        bodies.append([tile, next_tile_1, next_tile_2])
                        remaining_tiles.remove(tile)
                        remaining_tiles.remove(next_tile_1)
                        remaining_tiles.remove(next_tile_2)
                        found_body = True
                        break
                
                # 자패인 경우: 커쯔만 가능
                else:
                    if remaining_tiles.count(tile) >= 3:
                        bodies.append([tile] * 3)
                        for _ in range(3):
                            remaining_tiles.remove(tile)
                        found_body = True
                        break
            
            if not found_body:
                break
        
        if len(bodies) == 4:
            return [[head_tile, head_tile], *bodies]
    
    return None

# 사용 예시
tiles = ['4p', '2p', '3p', '3s', '4s', '5s', '1m', '2m', '3m', '5z', '5z', '5z', '1z', '1z']
result = find_mahjong_sets(tiles)

if result:
    print("구성된 배열:", result)
else:
    print("가능한 조합이 없습니다.")
