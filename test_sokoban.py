import pygame
import sys
import copy
import threading

pygame.init()
#맵 프리셋 객체
#모든 맵은 다음과 같은 값을 가져야함
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 480
SCREEN_MARGIN = 64
SCREEN_TOP_PART = 160
ONE_BLOCK_SIZE = 32


# map_struct = 맵 구조 (리스트)
# player_loc = 초기 플레이어의 위치
# score = 초기 박스의 갯수
class Map_preset:
    map_struct = []
    player_loc = []
    score = 0
    def __init__(self,map_struct):
        self.map_struct = map_struct
        for i in range(len(map_struct)):
            for j in range(len(map_struct[0])):
                code = map_struct[i][j]
                if code in ['o', 'X']:
                    self.score += 1
                elif code == '&':
                    self.player_loc = [j, i]

class MainMenuButton:
    def __init__(self, x, y, display, text, size, action=None, is_pressed=False):
        self.display = display
        btn_font = pygame.font.Font("fonts/Fipps-Regular.ttf", size)
        btn = btn_font.render(text, True, (255, 255, 255))
        self.width, self.height = btn.get_width(), btn.get_height()
        x = (SCREEN_WIDTH - self.width) / 2

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        self.is_pressed = is_pressed

        if x + self.width > mouse[0] > x and y + self.height > mouse[1] > y:
            btn_font = pygame.font.Font("fonts/Fipps-Regular.ttf", size + 5)
            btn = btn_font.render(text, True, (255, 255, 255))
            display.blit(btn, (x, y))
            if click[0] and action != None and not self.is_pressed:
                self.is_pressed = True
                # action(display)
            elif not click[0] and self.is_pressed:
                self.is_pressed = False
        else:
            self.is_pressed = False
            btn_font = pygame.font.Font("fonts/Fipps-Regular.ttf", size)
            btn = btn_font.render(text, True, (255, 255, 255))
            display.blit(btn, (x, y))

    def get_pressed(self):
        return self.is_pressed

#임시 테스트 맵1
# map_p = [["w","w","w","w","w","w"],
#               ["w","&"," "," ","_","w"],
#               ["w"," "," ","o"," ","w"],
#               ["w","w"," ","o"," ","w"],
#               ["w","w"," "," ","_","w"],
#               ["w","w","w","w","w","w"]]
# map_p = [["w","w","w","w","w","w",'w','w','w','w'],
#          ["w","&"," ","o","_"," "," "," "," ","w"],
#          ["w"," "," "," ","w","w","w"," ","_","w"],
#          ["w","w"," ","w","w","w"," "," "," ","w"],
#          ["w","w"," ","o"," "," "," "," "," ","w"],
#          ["w","w","w","w","w","w"," "," ","w","w"]]
map_p = [['w','w','w','w','w','w','w','w'],
         ['w','w',' ','&',' ','w','_','w'],
         ['w',' ',' ','w','o',' ',' ','w'],
         ['w',' ','o',' ',' ',' ',' ','w'],
         ['w',' ','w','w',' ','o',' ','w'],
         ['w',' ',' ','w',' ',' ',' ','w'],
         ['w','_','w','_',' ',' ',' ','w'],
         ['w','w','w','w','w','w','w','w']]

#이미지 불러옴
image_character = pygame.image.load('sprite/character.png')
image_character_and_mark = pygame.image.load('sprite/character and mark.png')
image_box = pygame.image.load('sprite/box.png')
image_box_amd_mark = pygame.image.load('sprite/box and mark.png')
image_block = pygame.image.load('sprite/block.png')
image_mark = pygame.image.load('sprite/mark.png')
image_None = pygame.image.load('sprite/None.png')

#폰트 불러옴
fipps = pygame.font.Font("fonts/Fipps-Regular.ttf", 30)


#맵 보여주는 함수
def show_map(map,screen, x, y):
    x_back = x
    y_back = y
    for row in map:
        for entry in row:
            #벽 보양 바꾸어서 보여줌
            if entry == "w":
                screen.blit(image_block,(x,y))
            elif entry == "o":
                screen.blit(image_box,(x,y))
            elif entry == "_":
                screen.blit(image_mark,(x,y))
            elif entry == "X":
                screen.blit(image_box_amd_mark,(x,y))
            elif entry == "&":
                screen.blit(image_character,(x,y))
            elif entry == "@":
                screen.blit(image_character_and_mark,(x,y))
            elif entry == " ":
                screen.blit(image_None, (x, y))
            x += ONE_BLOCK_SIZE
            # print(entry,end=" ")
        # print("")
        y += ONE_BLOCK_SIZE
        x = x_back



#캐릭터 움직이는 함수
def character_move(play_loc,dir,map,score):
    #주요 변수
    #play_loc 현재 플레이어의 위치
    #score 남은 박스의 갯수
    #입력받은 방향 값
    #함수 작성시 편의를 위해 x,y로 나누어줌
    player_x = play_loc[0]
    player_y = play_loc[1]



    if score == - 9999:
        pass

    else:
        if dir in ["l","u","d","r"]:
            #왼쪽 이동
            be_x = player_x
            be_y = player_y
            if dir == "l":
                af_x = player_x - 1
                af_y = player_y

                be_box_x = af_x
                be_box_y = af_y

                af_box_x = af_x - 1
                af_box_y = af_y

            elif dir == "r":
                af_x = player_x + 1
                af_y = player_y

                be_box_x = af_x
                be_box_y = af_y

                af_box_x = af_x + 1
                af_box_y = af_y

            elif dir == "d":
                af_x = player_x
                af_y = player_y+1

                be_box_x = af_x
                be_box_y = af_y

                af_box_x = af_x
                af_box_y = af_y+1

            elif dir == "u":

                af_x = player_x
                af_y = player_y-1

                be_box_x = af_x
                be_box_y = af_y

                af_box_x = af_x
                af_box_y = af_y-1

            box_loc = [af_box_x, af_box_y]

            #이동할려는 곳에 벽이 있는지 확인
            if map[af_y][af_x] == "w":
                #이동 불가 메시지 띄어줌
                cantmove()

            #이미 박스가 들어간 자리가 있는지 확인
            elif map[af_y][af_x] == "X":
            # 이동 불가 메시지
                cantmove()

                #이동할려는 곳에 상자가 있는지 확인
            elif map[af_y][af_x] == "o":
                    #박스가 움직이는 곳에 벽이 있는지 확인
                if map[af_box_y][af_box_x] == "w":
                        #이동불가
                    cantmove()

                    #박스가 움직이는 곳에 골인 지점이 있다면
                elif map[af_box_y][af_box_x] == "_":
                        #남은 박스의 갯수 줄여줌 & 만약 남은 박스가 없다면 게임 종료
                    score -= 1
                        #해당 공간을 완료된 구역으로 변경
                    map,_ = change_mark(map, be_box_x, be_box_y, af_box_x, af_box_y, " ", "X")
                        #플레이어를 이동시킴
                    map, play_loc = change_mark(map,be_x,be_y,af_x,af_y," ","&")

                    #박스가 움직이는 곳이 빈공간 이면
                elif map[af_box_y][af_box_x] == " ":
                        #박스 이동 및 원래 위치 빈공간으로
                    map, _ = change_mark(map, be_box_x, be_box_y, af_box_x, af_box_y, " ", "o")
                        #플레이어 이동 및 원래 위치 빈공간으로
                    if map[be_y][be_x] == "@":
                        map, play_loc = change_mark(map, be_x, be_y, af_x, af_y, "_", "&")
                    elif map[be_y][be_x] == "&":
                        map, play_loc = change_mark(map, be_x, be_y, af_x, af_y, " ", "&")
                        #박스를 더 이상 움직일 수 없는지 확인
                    possible = check_game_over(box_loc, map, [])
                    if not possible:
                        score = -9999

                    #인식 불가능한 문자 예외 처리
                else:
                    print("error>character_move>인식할 수 없는 공간입니다.")

                #이동하는 곳이 빈공간인지 확인 & 플레이어 위치가 이상이 있는지 까지 체크함
            elif map[af_y][af_x] == " " and map[player_y][player_x] == "&":
                map, play_loc = change_mark(map, be_x, be_y, af_x, af_y, " ", "&")
                #이동할려는 곳이 빈공간인지 확인 & 플레이어가 만약 목표지점 위에 있었는지 확인
            elif map[af_y][af_x] == " " and map[player_y][player_x] == "@":
                map, play_loc = change_mark(map, be_x, be_y, af_x, af_y, "_", "&")

                #이동할려는 곳이 목표지점이면 플레이어 모양 변경
            elif map[af_y][af_x] == "_":
                map, play_loc = change_mark(map, be_x, be_y, af_x, af_y, " ", "@")

                #오류 방지를 위한 예외처리
            else:
                print("error>character_move>인식할 수 없는 공간입니다.")

        #l,u,d,r이외의 값이 입력됬을 때 예외처리
        else:
            print("!error > character_move > dir에 잘못된 방향이 입력됨"+str(dir)+" gg")

    #갱신된 값들을 다시 반환
    return play_loc,map,score

#이동불가 메시지 출력
def cantmove():
    print(">> 움직일 수 없는 곳입니다!")

# def check_game_over(box_loc,map,score):
#     count = 0
#     if (map[box_loc[1]+1][box_loc[0]] in ["w","o","X"]):
#         count += 1
#     if (map[box_loc[1]-1][box_loc[0]] in ["w","o","X"]):
#         count += 1
#     if (map[box_loc[1]][box_loc[0]+1] in ["w","o","X"]):
#         count += 1
#     if (map[box_loc[1]][box_loc[0]-1] in ["w","o","X"]):
#         count += 1
#
#     if count >= 2:
#         score = -9999
#     return score

def check_game_over(box_loc,map, checked_box_loc):
    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]
    check_site = []
    check_site_bool = [] # 한칸 아래, 한칸 위, 왼쪽, 오른쪽 순으로 이동 가능 여부 저장
    checked_box_loc.append(box_loc)
    for i in range(4):
        check_site.append([box_loc[0] + dx[i], box_loc[1] + dy[i]])
    while check_site != []:
        check_pos = check_site.pop(0)
        x, y = check_pos[0], check_pos[1]
        if 0 <= x < len(map[0]) and 0 <= y < len(map):
            code = map[y][x]
            if code == 'w':
                check_site_bool.append(False)
            elif code in ['o', 'X']:
                if check_pos not in checked_box_loc:
                    check_site_bool.append(check_game_over([x, y], map, checked_box_loc))
                else:
                    check_site_bool.append(False)
            else:
                check_site_bool.append(True)
        else:
            check_site_bool.append(False)

    prev_possibllity = check_site_bool[3]
    for i in range(4):
        possibllity = check_site_bool[i]
        if not (prev_possibllity or possibllity):
            return False
        prev_possibllity = possibllity
    return True

def change_mark(map,be_x,be_y,af_x,af_y,be_mark,af_mark):
    map[af_y][af_x] = af_mark
    map[be_y][be_x] = be_mark
    return map,[af_x,af_y]

#소코반의 메인 함수 이 함수를 호출하여 소코반 시작
def main_sokoban_1p():
    #맵의 기본 정보 불러옴
    #map_struct = 맵 구조 (리스트)
    #player_loc = 초기 플레이어의 위치
    #score = 초기 박스의 갯수
    Test_map_1 = Map_preset(copy.deepcopy(map_p))
    map = Test_map_1.map_struct
    player_loc = Test_map_1.player_loc
    score = Test_map_1.score

    SCREEN_WIDTH_1P = SCREEN_MARGIN * 2 + len(map[0]) * ONE_BLOCK_SIZE
    SCREEN_HEIGHT_1P = SCREEN_TOP_PART * 2 + len(map) * ONE_BLOCK_SIZE

    screen = pygame.display.set_mode((SCREEN_WIDTH_1P, SCREEN_HEIGHT_1P))
    pygame.display.set_caption("소코반_1p")
    screen.fill((0,0,0))
    fps = pygame.time.Clock()
    #키 눌렀는지 확인하는 변수
    check = False
    is_game = True
    go_to_main = False
    is_finish = False
    check_key = ""

    title_font = pygame.font.Font("fonts/Fipps-Regular.ttf", 30)
    other_font = pygame.font.Font("fonts/PressStart2P-vaV7.ttf", 10)

    pygame.display.update()

    #남은 박스의 갯수가 0일때 종료
    while is_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game = False
        #방향 입력받는 변수
        push_key = ""
        #맵 보여줌
        screen.fill((0, 0, 0))
        show_map(map,screen, SCREEN_MARGIN, SCREEN_TOP_PART)

        text_loc = "Your location >> " + str(player_loc[0] + 1) + "," + str(player_loc[1] + 1)
        text_box = "left Box(es) >> " + str(score)
        loc = other_font.render(text_loc, True, (255, 255, 255))
        box = other_font.render(text_box, True, (255, 255, 255))
        title = title_font.render("Sokoban 1P", True, (255, 255, 255))
        screen.blit(loc, ((SCREEN_WIDTH_1P - loc.get_width()) / 2, 80))
        screen.blit(title,((SCREEN_WIDTH_1P - title.get_width()) / 2, 10))
        screen.blit(box, ((SCREEN_WIDTH_1P - box.get_width()) / 2, 100))

        if score == 0:
            is_finish = True
            font = pygame.font.Font("fonts/PressStart2P-vaV7.ttf", 30)
            text = font.render("You Win!", True, (255, 255, 255))
            screen.blit(text, ((SCREEN_WIDTH_1P - text.get_width()) / 2, SCREEN_HEIGHT_1P - SCREEN_TOP_PART + 50))

            font_main = pygame.font.Font("fonts/PressStart2P-vaV7.ttf", 15)
            text_main = font_main.render('press tab key', True, (255, 255, 255))
            screen.blit(text_main, ((SCREEN_WIDTH_1P - text_main.get_width()) / 2, SCREEN_HEIGHT_1P - SCREEN_TOP_PART + 80))
            pygame.display.update()

        if score == -9999:
            is_finish = True
            font = pygame.font.Font("fonts/PressStart2P-vaV7.ttf", 30)
            text = font.render("You Lose!", True, (255, 255, 255))
            screen.blit(text, ((SCREEN_WIDTH_1P - text.get_width()) / 2, SCREEN_HEIGHT_1P - SCREEN_TOP_PART + 50))

            font_main = pygame.font.Font("fonts/PressStart2P-vaV7.ttf", 15)
            text_main = font_main.render('press tab key', True, (255, 255, 255))
            screen.blit(text_main, ((SCREEN_WIDTH_1P - text_main.get_width()) / 2, SCREEN_HEIGHT_1P - SCREEN_TOP_PART + 80))
            pygame.display.update()
        pygame.display.update()


        # 방향키 인식
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if event.type == pygame.KEYDOWN and check == False:
            if event.key == pygame.K_LEFT:
                push_key = "l"
                check_key = "l"
            elif event.key == pygame.K_RIGHT:
                push_key = "r"
                check_key = "r"
            elif event.key == pygame.K_UP:
                push_key = "u"
                check_key = "u"
            elif event.key == pygame.K_DOWN:
                push_key = "d"
                check_key = "d"
            elif event.key == pygame.K_TAB:

                is_game = False
                go_to_main = True

            check = True
            player_loc, map, score = character_move(player_loc, push_key, map, score)

        if event.type == pygame.KEYUP and check == True:

            if event.key == pygame.K_LEFT:
                check_release = "l"

            elif event.key == pygame.K_RIGHT:

                check_release = "r"

            elif event.key == pygame.K_UP:

                check_release = "u"

            elif event.key ==pygame.K_DOWN:

                check_release = "d"

            if (check_release == check_key):

                check = False

        key_event = pygame.key.get_pressed()
        if key_event[pygame.K_TAB]:
            is_game = False
            go_to_main = True

        fps.tick(30)
        show_map(map,screen, SCREEN_MARGIN, 160)

    if go_to_main:
        show_start_page()

MAP_MIDDLE_GAP = 64

def main_sokoban_2p():
    Test_map_1 = Map_preset(copy.deepcopy(map_p))
    Test_map_2 = Map_preset(copy.deepcopy(map_p))

    map_1p = Test_map_1.map_struct
    player_loc_1p = Test_map_1.player_loc
    score_1p = Test_map_1.score

    map_2p = Test_map_2.map_struct
    player_loc_2p = Test_map_2.player_loc
    score_2p = Test_map_2.score

    SCREEN_WIDTH_2P = SCREEN_MARGIN * 2 + len(map_1p[0]) * ONE_BLOCK_SIZE * 2 + MAP_MIDDLE_GAP
    SCREEN_HEIGHT_2P = SCREEN_TOP_PART * 2 + len(map_1p) * ONE_BLOCK_SIZE

    screen = pygame.display.set_mode((SCREEN_WIDTH_2P, SCREEN_HEIGHT_2P))
    pygame.display.set_caption("소코반 2p")
    screen.fill((0, 0, 0))
    fps = pygame.time.Clock()

    title_font = pygame.font.Font("fonts/Fipps-Regular.ttf", 30)
    other_font = pygame.font.Font("fonts/PressStart2P-vaV7.ttf", 10)

    check_1p = False
    check_2p = False
    is_game = True
    is_finish = False
    go_to_main = False

    check_1p_preseed = False
    check_2p_preseed = False
    check_1p_preseed_key = ""
    check_2p_preseed_key = ""
    check_1p_release_key = ""
    check_2p_release_key = ""
    push_key_1p = ""
    push_key_2p = ""
    
    while is_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game = False
        screen.fill((0, 0, 0))

        title = title_font.render("Sokoban 2P", True, (255, 255, 255))
        screen.blit(title,((SCREEN_WIDTH_2P - title.get_width()) / 2, 10))

        show_map(map_1p, screen, SCREEN_MARGIN, 160)
        show_map(map_2p, screen, SCREEN_MARGIN + len(map_2p[0]) * ONE_BLOCK_SIZE + MAP_MIDDLE_GAP, 160)

        text_loc_1p = "1p location >> " + str(player_loc_1p[0] + 1) + "," + str(player_loc_1p[1] + 1)
        text_box_1p = "1p left Box(es) >> " + str(score_1p)
        loc_1p = other_font.render(text_loc_1p, True, (255, 255, 255))
        box_1p = other_font.render(text_box_1p, True, (255, 255, 255))
        screen.blit(loc_1p, (((SCREEN_MARGIN + len(map_2p[0]) * ONE_BLOCK_SIZE + MAP_MIDDLE_GAP) - loc_1p.get_width()) / 2, 80))
        screen.blit(box_1p, (((SCREEN_MARGIN + len(map_2p[0]) * ONE_BLOCK_SIZE + MAP_MIDDLE_GAP) - box_1p.get_width()) / 2, 100))

        text_loc_2p = "2p location >> " + str(player_loc_2p[0] + 1) + "," + str(player_loc_2p[1] + 1)
        text_box_2p = "2p left Box(es) >> " + str(score_2p)
        loc_2p = other_font.render(text_loc_2p, True, (255, 255, 255))
        box_2p = other_font.render(text_box_2p, True, (255, 255, 255))
        screen.blit(loc_2p, (((SCREEN_MARGIN + len(map_2p[0]) * ONE_BLOCK_SIZE + MAP_MIDDLE_GAP) - loc_2p.get_width()) / 2 + SCREEN_MARGIN + len(map_2p[0]) * ONE_BLOCK_SIZE, 80))
        screen.blit(box_2p, (((SCREEN_MARGIN + len(map_2p[0]) * ONE_BLOCK_SIZE + MAP_MIDDLE_GAP) - box_2p.get_width()) / 2 + SCREEN_MARGIN + len(map_2p[0]) * ONE_BLOCK_SIZE, 100))

        def print_finish(winner):
            font = pygame.font.Font("fonts/PressStart2P-vaV7.ttf", 30)
            text = font.render(winner, True, (255, 255, 255))
            screen.blit(text, ((SCREEN_WIDTH_2P - text.get_width()) / 2, SCREEN_HEIGHT_2P - SCREEN_TOP_PART + 50))

            font_main = pygame.font.Font("fonts/PressStart2P-vaV7.ttf", 15)
            text_main = font_main.render('press tab key', True, (255, 255, 255))
            screen.blit(text_main, ((SCREEN_WIDTH_2P - text_main.get_width()) / 2, SCREEN_HEIGHT_2P - SCREEN_TOP_PART + 80))
            return True

        if score_1p == 0 and score_2p == 0:
            is_finish = print_finish('Draw!')
        elif score_1p == 0 and score_2p != 0:
            is_finish = print_finish('1P Win!')
        elif score_1p != 0 and score_2p == 0:
            is_finish = print_finish('2P Win!')

        if score_1p == -9999 and score_2p == -9999:
            is_finish = print_finish('Draw!')
        elif score_1p == -9999 and score_2p != -9999:
            is_finish = print_finish('2P Win!')
        elif score_1p != -9999 and score_2p == -9999:
            is_finish = print_finish('1P Win!')
            
        #TODO 키 입력 개선
        event = pygame.event.wait()
        if not is_finish:
            if event.type == pygame.KEYDOWN and check_1p_preseed == False:
                push_key_1p = ""
                check_1p = 0
                if event.key == pygame.K_a:
                    push_key_1p = "l"
                    check_1p_preseed_key = "l"
                    check_1p = 1
                elif event.key == pygame.K_d:
                    push_key_1p = "r"
                    check_1p_preseed_key = "r"
                    check_1p = 1
                elif event.key == pygame.K_w:
                    push_key_1p = "u"
                    check_1p_preseed_key = "u"
                    check_1p = 1
                elif event.key == pygame.K_s:
                    push_key_1p = "d"
                    check_1p_preseed_key = "d"
                    check_1p = 1
                if check_1p == 1:
                    check_1p_preseed = True
                    player_loc_1p, map_1p, score_1p = character_move(player_loc_1p, push_key_1p, map_1p, score_1p)

            if event.type == pygame.KEYDOWN and check_2p_preseed == False:
                push_key_2p = ""
                check_2p = 0
                if event.key == pygame.K_LEFT:
                    push_key_2p = "l"
                    check_2p_preseed_key = "l"
                    check_2p = 1
                elif event.key == pygame.K_RIGHT:
                    push_key_2p = "r"
                    check_2p_preseed_key = "r"
                    check_2p = 1
                elif event.key == pygame.K_UP:
                    push_key_2p = "u"
                    check_2p_preseed_key = "u"
                    check_2p = 1
                elif event.key == pygame.K_DOWN:
                    push_key_2p = "d"
                    check_2p_preseed_key = "d"
                    check_2p = 1
                if check_2p == 1:
                    check_2p_preseed = True
                    player_loc_2p, map_2p, score_2p = character_move(player_loc_2p, push_key_2p, map_2p, score_2p)

            if event.type == pygame.KEYUP and check_1p_preseed == True:

                if event.key == pygame.K_a:
                    check_1p_release = "l"

                elif event.key == pygame.K_d:

                    check_1p_release = "r"

                elif event.key == pygame.K_w:

                    check_1p_release = "u"

                elif event.key == pygame.K_s:

                    check_1p_release = "d"

                if (check_1p_release == check_1p_preseed_key):
                    check_1p_preseed = False

            if event.type == pygame.KEYUP and check_2p_preseed == True:

                if event.key == pygame.K_LEFT:
                    check_2p_release = "l"

                elif event.key == pygame.K_RIGHT:

                    check_2p_release = "r"

                elif event.key == pygame.K_UP:

                    check_2p_release = "u"

                elif event.key == pygame.K_DOWN:

                    check_2p_release = "d"

                if (check_2p_release == check_2p_preseed_key):
                    check_2p_preseed = False

            key_event = pygame.key.get_pressed()
            if key_event[pygame.K_TAB]:
                is_game = False
                go_to_main = True
        #-----------------------------------------------------

                # if not check_1p:
        #             is_1p_pressed = False
        #             if key_event[pygame.K_a]:
        #                 push_key_1p = "l"
        #                 check_key_2p = "l"
        #                 is_1p_pressed = True
        #             elif key_event[pygame.K_d]:
        #                 push_key_1p = "r"
        #                 check_key_2p = "r"
        #                 is_1p_pressed = True
        #             elif key_event[pygame.K_w]:
        #                 push_key_1p = "u"
        #                 check_key_2p = "u"
        #                 is_1p_pressed = True
        #             elif key_event[pygame.K_s]:
        #                 push_key_1p = "d"
        #                 check_key_2p = "d"
        #                 is_1p_pressed = True
        #
        #             if is_1p_pressed:
        #                 check_1p = True
        #                 player_loc_1p, map_1p, score_1p = character_move(player_loc_1p, push_key_1p, map_1p, score_1p)
        #
        #         if not check_2p:
        #             is_2p_pressed = False
        #             if key_event[pygame.K_LEFT]:
        #                 push_key_2p = "l"
        #                 check_key_1p = "l"
        #                 is_2p_pressed = True
        #             elif key_event[pygame.K_RIGHT]:
        #                 push_key_2p = "r"
        #                 check_key_1p = "r"
        #                 is_2p_pressed = True
        #             elif key_event[pygame.K_UP]:
        #                 push_key_2p = "u"
        #                 check_key_1p = "u"
        #                 is_2p_pressed = True
        #             elif key_event[pygame.K_DOWN]:
        #                 push_key_2p = "d"
        #                 check_key_1p = "d"
        #                 is_2p_pressed = True
        #
        #             if is_2p_pressed:
        #                 check_2p = True
        #                 player_loc_2p, map_2p, score_2p = character_move(player_loc_2p, push_key_2p, map_2p, score_2p)
        #
        #     if key_event[pygame.K_TAB]:
        #         is_game = False
        #         go_to_main = True
        #
        # event = pygame.event.wait()
        # if event.type == pygame.KEYUP:
        #     key_event = pygame.key.get_pressed()
        #     if not (key_event[pygame.K_LEFT] or key_event[pygame.K_RIGHT] or key_event[pygame.K_UP] or key_event[pygame.K_DOWN]):
        #         check_1p = False
        #     if not (key_event[pygame.K_a] or key_event[pygame.K_d] or key_event[pygame.K_w] or key_event[pygame.K_s]):
        #         check_2p = False
        # if event == pygame.K_TAB:
        #     is_game = False
        #     go_to_main = True

        show_map(map_1p, screen, SCREEN_MARGIN, 160)
        show_map(map_2p, screen, SCREEN_MARGIN + len(map_2p[0]) * ONE_BLOCK_SIZE + MAP_MIDDLE_GAP, 160)

        pygame.display.update()
        fps.tick(60)

    if go_to_main:
        show_start_page()

def start_1p_game():
    print("1p game start")
    main_sokoban_1p()

def start_2p_game():
    print('2p game start')
    main_sokoban_2p()

def show_start_page():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("소코반")
    fps = pygame.time.Clock()

    is_start_pressed_1p = False
    is_start_pressed_2p = False
    is_game = True
    while is_game:
        event = pygame.event.poll()  # 이벤트 처리
        if event.type == pygame.QUIT:
            is_game = False

        screen.fill((0, 0, 0))
        title_font = pygame.font.Font("fonts/Fipps-Regular.ttf", 30)
        title = title_font.render("Sokoban", True, (255, 255, 255))
        screen.blit(title, ((SCREEN_WIDTH - title.get_width()) / 2, 10))

        btn_1p = MainMenuButton(60, 200, screen, "1p", 18, start_1p_game, is_start_pressed_1p)
        btn_2p = MainMenuButton(60, 240, screen, "2p", 18, start_2p_game, is_start_pressed_2p)
        is_start_pressed_1p = btn_1p.get_pressed()
        is_start_pressed_2p = btn_2p.get_pressed()

        if is_start_pressed_1p or is_start_pressed_2p:
            is_game = False

        pygame.display.update()
        fps.tick(60)

    if is_start_pressed_1p:
        start_1p_game()
    elif is_start_pressed_2p:
        start_2p_game()

#소코반 시작
show_start_page()