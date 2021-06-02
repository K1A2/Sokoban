# [CSE1017] 프로그래밍기초 기말고사
#
# 이름 : 
# 학번 : 
#
################################################################
# 1. [5+5점] 게임 맵을 표현하고 그리기
################################################################
#
# [ ] 완성 | [ ] 부분 완성 | [v] 미완성
def trans_cell(cell):
    map = []
    for i in cell:
        if i == 'w':
            map.append('W')
        elif i == 'b':
            map.append('o')
        elif i == 'B':
            map.append('O')
        elif i == ' ':
            map.append(' ')
        elif i == 't':
            map.append('_')
        elif i == 'P':
            map.append('&')
        elif i == 'p':
            map.append('@')
    return map

# [ ] 완성 | [ ] 부분 완성 | [v] 미완성
def draw_map(map):
    for m in map:
        codes = trans_cell(m)
        print(''.join(codes))


################################################################
# 2. 창고지기 캐릭터 이동하기
################################################################
# [10] 창고지기 캐릭터의 이동 위치를 입력받는 함수 move_direction
# [ ] 완성 | [ ] 부분 완성 | [v] 미완성
def move_direction():
    move = input()
    while move not in ['a', 's', 'w', 'd']:
        move = input()
    return move

# [10] 창고지기 캐릭터의 현재 위치를 알려주는 함수 find_player
# [ ] 완성 | [ ] 부분 완성 | [v] 미완성
def find_player(map):
    for  i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] in ['p', 'P']:
                return i, j

# [10] 창고지기 캐릭터의 움직임을 맵에 반영하는 함수 mapping
# [ ] 완성 | [ ] 부분 완성 | [v] 미완성
def mapping(map, move):
    i, j = find_player(map)
    moving = (0, 0)
    if move == 'a':
        moving = (0, -1)
    elif move == 's':
        moving = (1, 0)
    elif move == 'w':
        moving = (-1, 0)
    else:
        moving = (0, 1)
    move_pos = (i + moving[0], j + moving[1])
    if 0 <= move_pos[0] < len(map) and 0 <= move_pos[1] < len(map[0]):
        now_pos = map[i][j]
        next_pos = map[move_pos[0]][move_pos[1]]
        if next_pos == 'w':
            print('해당 방향은 벽 떄문에 갈 수 없습니다.')
        elif next_pos == ' ':
            map[move_pos[0]][move_pos[1]] = 'P'
            if now_pos == 'P':
                map[i][j] = ' '
            else:
                map[i][j] = 't'
        elif next_pos == 't':
            map[move_pos[0]][move_pos[1]] = 'p'
            if now_pos == 'P':
                map[i][j] = ' '
            else:
                map[i][j] = 't'
        elif next_pos in ['b', 'B']:
    else:
        print('해당 방향으로 갈 수 없습니다.')

################################################################
# 3. 메인 함수 작성
################################################################
# [10] 게임 종료 여부를 확인하는 보조함수 is_game_finished
# [ ] 완성 | [ ] 부분 완성 | [v] 미완성
def is_game_finished(map):
    return False

# [10] 게임을 수행하는 메인 함수 sokoban
# [ ] 완성 | [ ] 부분 완성 | [v] 미완성
def sokoban(map):
    print("welcome to sokoban")
    draw_map(map)
    # while not is_game_finished(map):



################################################################
# 4. 게임 확장
################################################################
# [10] 한번에 여러 이동을 입력받도록 move_direction을 확장한 move_directions
# [ ] 완성 | [ ] 부분 완성 | [v] 미완성
def move_directions():
    return None

# [10] 창고지기 캐릭터의 여러 움직임을 맵에 반영하는 함수 mapping2
# [ ] 완성 | [ ] 부분 완성 | [v] 미완성
def mapping2(map, moves):
    i, j = find_player(map)
    pass

# [10] 추가된 종료조건 함수 (움직일 수 없는 블록 탐지)
# [ ] 완성 | [ ] 부분 완성 | [v] 미완성
def no_more_move(map):
    return None

# 확장 함수를 사용한 메인함수 sokoban2
# [ ] 완성 | [ ] 부분 완성 | [v] 미완성
def sokoban2(map):
    print("welcome to sokoban")
    draw_map(map)
    while not is_game_finished(map):
        #
        pass
        #
        if no_more_move(map):
            # print message for no_more_move
            break
    # print message for end of game

################################################################
#
# 아래 준비된 게임 맵으로 테스트 해 보세요.
#

def test_sample():
    sokoban(sample)

def test1():
    sokoban(test_map1)

def test2():
    sokoban(test_map2)

sample = [
    ["w","w","w","w","w","w"],
    ["w","P","B"," ","t","w"],
    ["w","w","w","w","w","w"],
]

test_map1 = [
    [" "," ","w","w","w"," "," "," "],
    [" "," ","w","t","w"," "," "," "],
    [" "," ","w"," ","w","w","w","w"],
    ["w","w","w","B"," ","B","t","w"],
    ["w","t"," ","B","P","w","w","w"],
    ["w","w","w","w","B","w"," "," "],
    [" "," "," ","w","t","w"," "," "],
    [" "," "," ","w","w","w"," "," "],
]

test_map2 = [
    ["w","w","w","w","w"," "," "," "," "],
    ["w"," "," "," ","w"," "," "," "," "],
    ["w"," ","B"," ","w"," ","w","w","w"],
    ["w"," ","B"," ","w"," ","w","t","w"],
    ["w","w","w"," ","w","w","w","t","w"],
    [" ","w","w"," ","P"," "," ","t","w"],
    [" ","w"," ","B"," ","w"," "," ","w"],
    [" ","w"," "," "," ","w","w","w","w"],
    [" ","w","w","w","w","w"," "," "," "],
]

test2()

