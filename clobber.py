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
            if 'a' in string:
                num = int(string[1:])/2
                return 'ox'* num
            elif string.count('o') == 1:
                num = (int(string[1:])-1)/2
                return 'o' + 'ox' * num
            elif string.count('o') == 2:
                
                if num % 2 == 0:
                    return 'o' + 'ox' * ((num-2)/2) + 'o'
                else:
                    return 'o' + 'ox' * ((num-1)/2)
            elif string.count('o') == 4:
                
                return 'o' + 'ox' * ((num-3)/2) + 'oo'
        else:
            if 'o' in string:
                num = (int(string[2:]))
                return 'oo' + 'ox' * ((num-4)/2) + 'xx'
            elif string.count('x') == 1:
                num = (int(string[1:])-1)/2
                return 'x' + 'xo' * num
            elif string.count('x') == 2:
                
                if num % 2 == 0:
                    return 'x' + 'xo' * ((num-2)/2) + 'x'
                else:
                    return 'x' + 'xo' * ((num-1)/2)
            elif string.count('o') == 4:
                return 'x' + 'xo' * ((num-3)/2) + 'xx'
            
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
    def perform_asf(self):
        temp_board = []
        for i in range(len(self.board)):
            if self.board[i] in ASF3 or find_negative(self.board[i]) in ASF3:
                temp_board.append('ox')
            elif self.board[i] in ASF4:
                temp_board.append('xxo')
                temp_board.append('ox')
            elif find_negative(self.board[i]) in ASF4:
                temp_board.append('oox')
                temp_board.append('ox')
            elif self.board[i] in ASF5 or find_negative(self.board[i]) in ASF5:
                temp_board.append('oxox')
                temp_board.append('ox')
            elif self.board[i] in ASF6:
                temp_board.append('oox')
            elif find_negative(self.board[i]) in ASF6:
                temp_board.append('xxo')  
            elif self.board[i] == 'ooxo':
                temp_board.append('xxo')
                temp_board.append('ox')
            elif self.board[i] == 'xxox':
                temp_board.append('oox')
                temp_board.append('xo')
            
        self.board = temp_board
    def perform_asf2(self):
        negative_list = []
        for i in range(len(self.board)):
            negative_list.append(find_negative(self.board[i]))
            for j in range(len(negative_list)):
                if self.board[i] == negative_list[j]:
                    self.board[i] == ''
                    self.board[j] == ''
        temp_board = []
        for i in range(len(self.board)):
            if self.board[i] != '':
                temp_board.append(self.board[i])
        self.board = temp_board
def main():
    game_part = input("Put down game state: ")
    input_list = game_part.split()
    game = GameState('x',input_list)
    game.perform_asf()
    print(game.board)
main()


        
        


    
            

            

