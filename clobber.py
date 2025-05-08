ASF1 = ['o','oo','ooo','ooxx','oxoxox']
ASF3 = ['oxo','ooxox','ooxoxoo','xxoxoxx']
ASF4 = ['oxoxoxoxo']
ASF5 = ['ooxoxx','oxoxoxoxoxox']
ASF6 = ['ooxoo']
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)
def convert_str_to_game(string):
    if has_numbers(string):
        if 'x' not in string:
            #A
            if 'a' in string:
                num = int(string[1:])/2
                return 'ox'* int(num)
            
            #O
            elif string.count('o') == 1:
                num = (int(string[1:])-1)/2
                return 'o' + 'xo' * int(num)
            elif string.count('o') == 2:
                num = int(string[2:])
                if num % 2 == 0:
                    return 'o' + 'ox' * int((num-2)/2) + 'o'
                else:
                    return 'o' + 'ox' * int((num-1)/2)
            elif string.count('o') == 4:
                num = int(string[2:-2])
                return 'o' + 'ox' * int((num-3)/2) + 'oo'
        else:
            if 'o' in string:
                num = (int(string[2:]))
                return 'oo' + 'ox' * int((num-4)/2) + 'xx'
            elif string.count('x') == 1:
                num = (int(string[1:])-1)/2
                return 'x' + 'ox' * int(num)
            elif string.count('x') == 2:
                num = int(string[2:])
                if num % 2 == 0:
                    return 'x' + 'xo' * int((num-2)/2) + 'x'
                else:
                    return 'x' + 'xo' * int((num-1)/2)
            elif string.count('o') == 4:
                num = int(string[2:-2])
                return 'x' + 'xo' * int((num-3)/2) + 'xx'
            
    else:
        return string
        
        
def find_negative(part):
    negative_stone = ''
    for stone in part:
        if stone == 'x':
            negative_stone += 'o'
        else:
            negative_stone += 'x'
    return negative_stone
def find_sym(part):
    return part[::-1]
class GameState:
    def __init__(self, turn, board):
        self.turn = turn
        self.board = board
        self.vec = []
    def perform_asf(self):
        temp_board = []
        for i in range(len(self.board)):
            if self.board[i] in ASF1 or find_negative(self.board[i]) in ASF1 or self.board[i][::-1] in ASF1 or find_negative(self.board[i][::-1]) in ASF1:
                pass
            elif self.board[i] in ASF3 or find_negative(self.board[i]) in ASF3 or self.board[i][::-1] in ASF3 or find_negative(self.board[i][::-1]) in ASF3:
                temp_board.append('ox')
            elif self.board[i] in ASF4 or self.board[i][::-1] in ASF4:
                temp_board.append('xxo')
                temp_board.append('ox')
            elif find_negative(self.board[i]) in ASF4 or find_negative(self.board[i][::-1]) in ASF4:
                temp_board.append('oox')
                temp_board.append('ox')
            elif self.board[i] in ASF5 or find_negative(self.board[i]) in ASF5 or self.board[i][::-1] in ASF5 or find_negative(self.board[i][::-1]) in ASF5:
                temp_board.append('oxox')
                temp_board.append('ox')
            elif self.board[i] in ASF6 or self.board[i][::-1] in ASF6:
                temp_board.append('oox')
            elif find_negative(self.board[i]) in ASF6 or find_negative(self.board[i][::-1]) in ASF6:
                temp_board.append('xxo')  
            elif self.board[i] == 'ooxo' or self.board[i][::-1] == 'ooxo':
                temp_board.append('xxo')
                temp_board.append('ox')
            elif self.board[i] == 'xxox' or self.board[i][::-1] == 'xxox':
                temp_board.append('oox')
                temp_board.append('xo')
            else:
                temp_board.append(self.board[i])
            
        self.board = temp_board
    def perform_asf2(self):
        for i in range(len(self.board)):
            for j in range(i+1,len(self.board)):
                if self.board[i] == find_negative(self.board[j]) or self.board[i][::-1] == find_negative(self.board[j]):
                    self.board[i] = ''
                    self.board[j] = ''
        self.board = [item for item in self.board if item != '']
    def cal_vec(self):
        a = 0
        b = 0
        c = 0
        d = 0
        e = 0
        f = 0
        y = 0
        z = 0
        for part in self.board:
            if part == 'xxo' or part == 'oxx':
                e += 1
            elif part == 'ooxoxoxo' or part == 'oxoxoxoo':
                f += 1
            elif part in ('ox','oxox','ooxox','xo','xoxo','xoxoo'):
                d += 1
            elif part[0:2] == "oo":
                if len(part) %2 == 0:
                    b +=1
                else:
                    if part[-2:] == 'oo':
                        c += 1
                    else:
                        z += 1
            else:
                if len(part) %2 == 0:
                    y +=1
                else:
                    a += 1
        self.vec = (a,b,c,d,e,f,y,z)
        return self.vec

    def set_distinguish(self):
        S0 = False
        S1 = False
        S2 = False
        a,b,c,d,e,f,y,z = self.vec
        if (a >= c and y <= 1 and z == 0 and a+b+c+d+e+f+y+z >= 1) or (a >= (c+1) and y == 0 and z == 1):
            S0 = True
        if y == 0 and z ==0 and a >= (c+1): #TODO: add special case
            S1 = True
        if a == 0 and b == 0 and c == 0 and y == 0 and z == 0 and (e+f) >= 1 and (d == 0 or d+e >= 3):
            S3 = True
        print(f'In S0:{S0}')
        print(f'In S1:{S1}')
        print(f'In S2:{S2}')


def main():
    game_part = input("Put down game state: ")
    game_part2 = input("Put down game2 state: ")
    input_list = game_part.split()
    input_list2 = game_part2.split()
    final_input_list_1 = []
    for part in input_list:
        final_input_list_1.append(convert_str_to_game(part))
        
    final_input_list_2 = []
    for part in input_list2:
        final_input_list_2.append(convert_str_to_game(part))
    game = GameState('x',final_input_list_1)
    game2 = GameState('x',final_input_list_2)
    print(game.board)
    before = game.cal_vec()
    
    game.set_distinguish()
    game.perform_asf()
    print(game.board)
    after11 = game.cal_vec()
    game.set_distinguish()
    game.perform_asf2()
    print(game.board)
    after12 = game.cal_vec()
    game.set_distinguish()



    print(game2.board)
    before2 = game2.cal_vec()
    game2.set_distinguish()
    game2.perform_asf()
    print(game2.board)
    after21 = game2.cal_vec()
    game2.set_distinguish()
    game2.perform_asf2()
    print(game2.board)
    after22 = game2.cal_vec()
    game2.set_distinguish()
    print(after12)
    print(after22)
    cal_list = []
    for i in range(len(after12)):
        cal_list.append(after22[i]-after12[i])
    print(cal_list)

main()


        
        


    
            

            

