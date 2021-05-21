
#맵 프리셋 객체
#모든 맵은 다음과 같은 값을 가져야함

# map_struct = 맵 구조 (리스트)
# player_loc = 초기 플레이어의 위치
# score = 초기 박스의 갯수
class Map_preset:

    map_struct = []
    player_loc = []
    score = 0
    def __init__(self,map_struct,player_loc,score):
        self.map_struct = map_struct
        self.player_loc = player_loc
        self.score = score

#임시 테스트 맵1
Test_map_1 = Map_preset(
              [["w","w","w","w","w","w"],
              ["w","&"," ","o","_","w"],
              ["w"," "," "," "," ","w"],
              ["w","w"," ","o"," ","w"],
              ["w","w"," "," ","_","w"],
              ["w","w","w","w","w","w"]],[1,1],2)


#맵 보여주는 함수
def show_map(map):
    for row in map:
        for entry in row:
            #벽 보양 바꾸어서 보여줌
            if entry == "w":
                entry = "■"
            print(entry,end=" ")
        print("")



#캐릭터 움직이는 함수
def character_move(play_loc,dir,map,score):
    #주요 변수
    #play_loc 현재 플레이어의 위치
    #score 남은 박스의 갯수
    #입력받은 방향 값
    #함수 작성시 편의를 위해 x,y로 나누어줌
    player_x = play_loc[0]
    player_y = play_loc[1]

    
    #왼쪽 이동
    if dir == "l":
        
        #이동할려는 곳에 벽이 있는지 확인
        if map[player_y][player_x - 1] == "w":
                
            #이동 불가 메시지 띄어줌
            cantmove()
        
        #이미 박스가 들어간 자리가 있는지 확인
        elif map[player_y][player_x - 1] == "X":
            # 이동 불가 메시지 
            cantmove()
        
        #이동할려는 곳에 상자가 있는지 확인
        elif map[player_y][player_x - 1] == "o":
            #편의를 위해 박스의 좌표를 가져옴
            box_x = player_x - 1
            box_y = player_y
            
            #박스가 움직이는 곳에 벽이 있는지 확인
            if map[box_y][box_x - 1] == "w":
                #이동불가
                cantmove()

            #박스가 움직이는 곳에 골인 지점이 있다면
            elif map[box_y][box_x - 1] == "_":
                #남은 박스의 갯수 줄여줌 & 만약 남은 박스가 없다면 게임 종료
                score = setscore(score,-1)
                #해당 공간을 완료된 구역으로 변경
                map[box_y][box_x - 1] = "X"
                #박스가 있던 위치는 다시 빈공간으로
                map[box_y][box_x] = " "
                #플레이어를 이동시킴
                map[player_y][player_x - 1] = "&"
                #플레이어가 있던 위치는 다시 빈공간으로
                map[player_y][player_x] = " "
                #위치 갱신
                play_loc = [player_x - 1, player_y]
            
            #박스가 움직이는 곳이 빈공간 이면
            elif map[box_y][box_x - 1] == " ":
                #박스 이동 및 원래 위치 빈공간으로
                map[box_y][box_x - 1] = "o"
                map[box_y][box_x] = " "
                #플레이어 이동 및 원래 위치 빈공간으로
                map[player_y][player_x - 1] = "&"
                map[player_y][player_x] = " "
                #플레이어 위치 갱신
                play_loc = [player_x - 1, player_y]

            #인식 불가능한 문자 예외 처리
            else:
                print("error>character_move>인식할 수 없는 공간입니다.")
                
        #이동하는 곳이 빈공간인지 확인 & 플레이어 위치가 이상이 있는지 까지 체크함
        elif map[player_y][player_x - 1] == " " and map[player_y][player_x] == "&":
            map[player_y][player_x - 1] = "&"
            map[player_y][player_x] = " "
            play_loc = [player_x - 1, player_y]
        #이동할려는 곳이 빈공간인지 확인 & 플레이어가 만약 목표지점 위에 있었는지 확인
        elif map[player_y][player_x - 1] == " " and map[player_y][player_x] == "±":
            map[player_y][player_x - 1] = "&"
            #목표지점으로 다시 표시
            map[player_y][player_x] = "_"
            play_loc = [player_x - 1, player_y]
            
        #이동할려는 곳이 목표지점이면 플레이어 모양 변경
        elif map[player_y][player_x - 1] == "_":
            map[player_y][player_x - 1] = "±"
            map[player_y][player_x] = " "
            play_loc = [player_x - 1, player_y]

        #오류 방지를 위한 예외처리
        else:
            print("error>character_move>인식할 수 없는 공간입니다.")

    #오른쪽 방향
    #아래 코드는 방향 제외하곤 모두 동일
    elif dir == "r":

        if map[player_y][player_x + 1] == "w":
            cantmove()

        elif map[player_y][player_x + 1] == "X":
            cantmove()

        elif map[player_y][player_x + 1] == "o":

            box_x = player_x + 1
            box_y = player_y

            if map[box_y][box_x + 1] == "w":
                cantmove()


            elif map[box_y][box_x + 1] == "_":
                score = setscore(score,-1)
                map[box_y][box_x + 1] = "X"
                map[box_y][box_x] = " "
                map[player_y][player_x + 1] = "&"
                map[player_y][player_x] = " "
                play_loc = [player_x + 1, player_y]

            elif map[box_y][box_x + 1] == " ":
                map[box_y][box_x + 1] = "o"
                map[box_y][box_x] = " "
                map[player_y][player_x + 1] = "&"
                map[player_y][player_x] = " "
                play_loc = [player_x + 1, player_y]

            else:
                print("error>character_move>인식할 수 없는 공간입니다.")

        elif map[player_y][player_x + 1] == " " and map[player_y][player_x] == "&":
            map[player_y][player_x + 1] = "&"
            map[player_y][player_x] = " "
            play_loc = [player_x + 1, player_y]

        elif map[player_y][player_x + 1] == " " and map[player_y][player_x] == "±":
            map[player_y][player_x + 1] = "&"
            map[player_y][player_x] = "_"
            play_loc = [player_x + 1, player_y]

        elif map[player_y][player_x + 1] == "_":
            map[player_y][player_x + 1] = "±"
            map[player_y][player_x] = " "
            play_loc = [player_x + 1, player_y]

        else:
            print("error>character_move>인식할 수 없는 공간입니다.")

    #위쪽 방향
    elif dir == "u":

        if map[player_y-1][player_x] == "w":
            cantmove()

        elif map[player_y-1][player_x] == "X":
            cantmove()

        elif map[player_y-1][player_x] == "o":

            box_x = player_x
            box_y = player_y - 1

            if map[box_x][box_y-1] == "w":
                cantmove()


            elif map[box_y-1][box_x] == "_":
                score = setscore(score,-1)
                map[box_y-1][box_x] = "X"
                map[box_y][box_x] = " "
                map[player_y-1][player_x] = "&"
                map[player_y][player_x] = " "
                play_loc = [player_x, player_y - 1]


            elif map[box_y-1][box_x] == " ":
                map[box_y-1][box_x] = "o"
                map[box_y][box_x] = " "
                map[player_y-1][player_x] = "&"
                map[player_y][player_x] = " "
                play_loc = [player_x, player_y - 1]


            else:
                print("error>character_move>인식할 수 없는 공간입니다.")

        elif map[player_y - 1][player_x] == " " and map[player_y][player_x] == "&":
            map[player_y - 1][player_x] = "&"
            map[player_y][player_x] = " "
            play_loc = [player_x, player_y - 1]

        elif map[player_y - 1][player_x] == " " and map[player_y][player_x] == "±":
            map[player_y - 1][player_x] = "&"
            map[player_y][player_x] = "_"
            play_loc = [player_x, player_y - 1]

        elif map[player_y - 1][player_x] == "_":
            map[player_y - 1][player_x] = "±"
            map[player_y][player_x] = " "
            play_loc = [player_x, player_y - 1]

        else:
            print("error>character_move>인식할 수 없는 공간입니다.")

    #아래쪽 방향
    elif dir == "d":

        if map[player_y + 1][player_x] == "w":
            cantmove()

        elif map[player_y + 1][player_x] == "X":
            cantmove()

        elif map[player_y + 1][player_x] == "o":

            box_x = player_x
            box_y = player_y + 1

            if map[box_y + 1][box_x] == "w":
                cantmove()


            elif map[box_y + 1][box_x] == "_":
                score = setscore(score, -1)
                map[box_y + 1][box_x] = "X"
                map[box_y][box_x] = " "
                map[player_y + 1][player_x] = "&"
                map[player_y][player_x] = " "
                play_loc = [player_x,player_y+1]


            elif map[box_y + 1][box_x] == " ":
                map[box_y + 1][box_x] = "o"
                map[box_y][box_x] = " "
                map[player_y + 1][player_x] = "&"
                map[player_y][player_x] = " "
                play_loc = [player_x,player_y+1]


            else:
                print("error>character_move>인식할 수 없는 공간입니다.")


        elif map[player_y + 1][player_x] == " " and map[player_y][player_x] == "&":
            map[player_y + 1][player_x] = "&"
            map[player_y][player_x] = " "
            play_loc = [player_x, player_y + 1]

        elif map[player_y + 1][player_x] == " " and map[player_y][player_x] == "±":
            map[player_y + 1][player_x] = "&"
            map[player_y][player_x] = "_"
            play_loc = [player_x, player_y + 1]

        elif map[player_y+1][player_x] == "_":
            map[player_y+1][player_x] = "±"
            map[player_y][player_x] = " "
            play_loc = [player_x, player_y+1]

        else:
            print("error>character_move>인식할 수 없는 공간입니다.")

    #l,u,d,r이외의 값이 입력됬을 때 예외처리
    else:
        print("!error > character_move > dir에 잘못된 방향이 입력됨")

    #갱신된 값들을 다시 반환
    return play_loc,map,score

#이동불가 메시지 출력
def cantmove():
    print(">> 움직일 수 없는 곳입니다!")

#해당 값만큼 남은 상자의 갯수 증가시킴
def setscore(score,amount):
    score += amount
    #종료 메시지
    if score == 0:
        print("축하합니다! 클리어하셨습니다!")
    #오류 방지를 위한 예외처리
    elif score < 0:
        print("error>setscore>점수가 0보다 낮습니다!")

    return score
#소코반의 메인 함수 이 함수를 호출하여 소코반 시작
def main_sokoban():
    #맵의 기본 정보 불러옴
    #map_struct = 맵 구조 (리스트)
    #player_loc = 초기 플레이어의 위치
    #score = 초기 박스의 갯수
    map = Test_map_1.map_struct
    player_loc = Test_map_1.player_loc
    score = Test_map_1.score

    #남은 박스의 갯수가 0일때 종료
    while(score > 0):
        #방향 입력받는 변수
        push_key = ""
        #맵 보여줌
        show_map(map)
        #남은 박스 갯수 표시
        print("Left boxes >> ",score)
        #현재 위치 표시
        print("Your location >> ", [player_loc[0]+1,player_loc[1]+1])
        print("< < 이동할 방향을 입력하세요 > >")
        print(" ←(l)  ↑(u)  ↓(d)  →(r) ")
        push_key = input(">> ")
        #입력받은 값 확인
        if push_key in ["l","u","d","r"]:
            player_loc,map,score = character_move(player_loc,push_key,map,score)
        #예외처리
        else:
            print("키를 잘못 입력하셨습니다.")

    show_map(map)

#소코반 시작
main_sokoban()