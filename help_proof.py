from copy import deepcopy
import sys
import time
#sys.setrecursionlimit(10000000)


class ALC:
    def __init__(self, k, player):
        self.board = 'ox' * k
        self.turn = player

class Linked_ALC:
    #different version of ALC just for printing tree only.
    def __init__(self, k, player):
        self.board = 'ox' * k
        self.turn = player
        self.child = set()
        #from https://stackoverflow.com/questions/20242479/printing-a-tree-data-structure-in-python
    def __str__(self, level=0):
        if self.board == '':
            return ""
        ret = "\t"*level+self.turn+ "\n"+"\t"*level+self.board+"\n\n"
        for child in self.child:
            ret += child.__str__(level+1)
        return ret

#reverse a board
def revstring(s): return s[::-1]

#find the negative of a board, x to o and o to x.
def negstring(s): 
    new_s = ''
    for c in s:
        if c == 'x':
            new_s += 'o'
        else:
            new_s += 'x'
    if new_s[0] == 'x':
        return revstring(new_s)
    return new_s

#find the count vector of current board
def count(brd): #simplfy before use, need o in front
    brd_count_list = [0,0,0,0,0,0,0,0]
    brd_list = brd.split('_')
    for subgame in brd_list:
            if subgame[0] == 'x':
                print('x game produced')
                print('x: ',subgame)
                exit()
            elif subgame == 'ox' or subgame == 'oxox' or subgame == 'ooxoxo':
                brd_count_list[3] += 1
                
            elif subgame == 'oxx':
                brd_count_list[4] += 1
            elif subgame == 'ooxoxoxo':
                brd_count_list[5] += 1
                
            elif subgame == 'oox':
                brd_count_list[2] += 1
                
            elif subgame[1] == 'x' and subgame[-1] == 'x':
                brd_count_list[6] += 1
            
            elif subgame[1] == 'x' and subgame[-1] == 'o':
                brd_count_list[0] += 1
                
            elif subgame[1] == 'o' and subgame[-2] == 'o' and subgame[-1] == 'x':
                brd_count_list[7] += 1
                
            elif subgame[1] == 'o' and subgame[-2] == 'x' and subgame[-1] == 'o':
                brd_count_list[1] += 1
                
            elif subgame[1] == 'o' and subgame[-2] == 'o' and subgame[-1] == 'o':
                brd_count_list[2] += 1
            else:
                print(f'unexpected subgame produced, board: {brd}, subgame: {subgame}')
                exit()
    return brd_count_list

def ASF(brd):
    new_brd = []
    brd_list = brd.split('_')
    #follow rules that change subgame
    for subgame in brd_list:
        if subgame == '' or 'o' not in subgame or 'x' not in subgame:
            pass
        else:
            for i in range(2):
                if subgame[i] == 'x':
                    subgame = revstring(subgame)
                    break
                elif subgame[i] == 'o' and subgame[-i-1] == 'x':
                    break
            if subgame == 'ooxx' or subgame == 'oxoxox' or subgame == '':
                pass
            elif subgame == 'oxo' or subgame == 'ooxox' or subgame == 'ooxoxoo' or subgame == 'xxoxoxx' or subgame == 'xox' or subgame == 'oxoxx':
                new_brd.append('ox')
            elif subgame == 'oxoxoxoxo':
                new_brd.append('oxx')
                new_brd.append('ox')
            elif subgame == 'ooxoxx' or subgame == 'oxoxoxoxoxox':
                new_brd.append('oxox')
                new_brd.append('ox')
            elif subgame == 'ooxoo':
                new_brd.append('oox')
            elif subgame == 'xxoxx':
                new_brd.append('oxx')
            elif subgame == 'ooxo':
                new_brd.append('oxx')
                new_brd.append('ox')
            elif subgame == 'xxox':
                new_brd.append('oox')
                new_brd.append('ox')
            else:
                new_brd.append(subgame)
    
    #to remove subgame that cancel out each other.
    brd_without_y = []
    brd_y = []    
    for subgame in new_brd:
        if subgame != 'oxx' and subgame[1] == 'x' and subgame[-1] == 'x':
                brd_y.append(subgame)
        else:
            brd_without_y.append(subgame)

    reverse_brd = []
    for game in brd_without_y:
        reverse_brd.append(negstring(game))
    final_brd = deepcopy(brd_without_y)
    for i in brd_without_y:
        if i in reverse_brd:
            final_brd.remove(i)
            reverse_brd.remove(i)
    brd_with_y_dict = {}
    for game in brd_y:
        if game in brd_with_y_dict:
            brd_with_y_dict[game] += 1
        else:
            brd_with_y_dict[game] = 1
    
    for game in brd_with_y_dict:
        if brd_with_y_dict[game] % 2 != 0:
            final_brd.append(game)
    final_str = ''

    for game in final_brd:
        final_str = add_subgame(final_str,game)
    return final_str

# add subgame to a brd, subgame are followed by ascending order by how many stone, subgame of same stone are followed
# by first x position from beginning. games with the largest first x position are putting first. i.e. ooxo is infront of oxox
def add_subgame(brd,subgame):
    if brd == '':
        return subgame
    subgame_len = len(subgame)
    game = ''
    score = 0 
    for character in subgame:
        if character == 'o':
            score += 1
        else:
            break
    j  = 0
    for i in range(len(brd)):
        if brd[i] != '_':
            game += brd[i]
        else:
            if subgame_len < len(game):
                if j == 0:
                    return f"{subgame}_{brd[j:]}"
                else:                
                    return f"{brd[0:j]}_{subgame}_{brd[j+1:]}"

            elif subgame_len ==  len(game):
                current_score = 0
                for character in game:
                    if character == 'o':
                        current_score += 1
                    else:
                        break
                if score > current_score:
                    return f"{brd[0:i]}_{subgame}_{brd[i+1:]}"
                else:
                    if j == 0:
                        return f"{subgame}_{brd[j:]}"
                    else:
                        return f"{brd[0:j]}_{subgame}_{brd[j+1:]}"
            game = ''
            j = i
        if i == len(brd) - 1:
            if subgame_len < len(game):
                if j == 0:
                    return f"{subgame}_{brd}"
                else:
                    return f"{brd[0:j]}_{subgame}_{brd[j+1:]}"
            elif subgame_len == len(game):

                current_score = 0
                for character in game:
                    if character == 'o':
                        current_score += 1
                    else:
                        break
                if score > current_score:
                    return f"{brd}_{subgame}"
                else:
                    if j == 0:
                        return f"{subgame}_{brd[j:]}"  
                    else:         
                        return f"{brd[0:j]}_{subgame}_{brd[j+1:]}"
            else:
                return f"{brd}_{subgame}"
    
#remove a subgame from the brd     
def remove_subgame(brd,subgame):
    game = ''
    j = 0
    for i in range(len(brd)):
        if brd[i] != '_':
            game += brd[i]
        else:
            if game == subgame:
                return f"{brd[0:j]}_{brd[i+1:]}"
            j = i
            game = ''
        if i == len(brd) - 1:
            if game == subgame:
                return f"{brd[0:j]}"
            else:
                print(f"{subgame} are not available to removed")
                exit()
    return brd

def right_strat(brd):
    brd_list = brd.split('_')
    if brd == "ox_oxoxoxox" or brd == "oxox_oxoxoxoxox" or brd == 'ox_oxox_oxoxoxoxoxoxoxoxox' or  brd == 'oox_oxoxo' or brd == 'ox_ooxoxoxoxo' or brd == 'oxox_ooxoxoxoxoxo' or brd == 'oxoxoxoxoxox':
        return ''
    vector = count(brd)
    #rule1
    # a8,10,a14 to o5,o7,o11
    if vector[6] != 0:
        for subgame in brd_list:
            if subgame != 'oxx' and subgame[1] == 'x' and subgame[-1] == 'x' and subgame != 'ox' and subgame != 'oxox':
                    a = subgame
                    break
        brd = remove_subgame(brd,a)
        new_subgame = 'o'+ 'xo' * int((len(a)-4)/2)
        brd = add_subgame(brd,new_subgame)
        
    #rule2
    #oo7,oo9 to oo4,oo6
    elif vector[7] != 0:
        for subgame in brd_list:
            if subgame[1] == 'o' and subgame[-2] == 'o' and subgame[-1] == 'x' and subgame != 'oox':
                break
        brd = remove_subgame(brd,subgame)
        new_subgame = 'oo' + 'xo' * int((len(subgame)-5)/2)
        brd = add_subgame(brd,new_subgame)
    
    #rule3
    elif 'oxoxo' in brd_list and 'oxox' in brd_list and 'ox' in brd_list and 'oox' in brd_list:
        brd = remove_subgame(brd,'oox')
        brd = add_subgame(brd,'ox')
    elif 'oxox' in brd_list and 'oox' in brd_list:
        brd = remove_subgame(brd,'oxox')
        brd = add_subgame(brd,'oxx')
    elif 'oox' in brd_list:
        brd = remove_subgame(brd,'oox')
        brd = add_subgame(brd,'ox')
    elif vector[2] != 0:
        ooo = ''
        for subgame in brd_list:
            if subgame[1] == 'o' and subgame[-2] == 'o' and subgame[-1] == 'o':
                if ooo == '':
                    ooo = subgame
                elif len(ooo) > len(subgame):
                    ooo = subgame
        new_subgame = 'oo' + 'xo' *int((len(ooo)-5)/2)
        brd = add_subgame(brd,new_subgame)
        brd = remove_subgame(brd,ooo)
    
    #rule4
    elif 'ooxoxoxoxo' in brd_list:
        brd = remove_subgame(brd,'ooxoxoxoxo')
        brd = add_subgame(brd,'oxoxo')
    elif 'ooxoxoxoxoxo' in brd_list:
        brd = remove_subgame(brd,'ooxoxoxoxoxo')
        brd = add_subgame(brd,'oxoxoxo')
    elif 'ooxoxoxoxoxoxo' in brd_list:
        brd = remove_subgame(brd,'ooxoxoxoxoxoxo')
        brd = add_subgame(brd,'oxoxoxoxoxo')
        brd = add_subgame(brd,'ox')
    elif 'ooxoxoxoxoxoxoxo' in brd_list:
        brd = remove_subgame(brd,'ooxoxoxoxoxoxoxo')
        brd = add_subgame(brd,'oxoxoxoxoxo')
    elif 'ooxoxoxoxoxoxoxoxo' in brd_list:
        brd = remove_subgame(brd,'ooxoxoxoxoxoxoxoxo')
        brd=  add_subgame(brd,'oxoxoxoxoxoxo')
    elif 'ooxoxoxoxoxoxoxoxoxo' in brd_list:
        brd = remove_subgame(brd,'ooxoxoxoxoxoxoxoxoxo')
        brd = add_subgame(brd,'oxoxoxoxoxoxoxoxo')
        brd = add_subgame(brd,'ox')
    elif vector[1] != 0:
        oo = ''
        for subgame in brd_list:
            if subgame[1] == 'o' and subgame[-2] == 'x' and subgame[-1] == 'o' and subgame != 'ooxoxo' and subgame != 'ooxoxoxo':
                if oo == '':
                    oo = subgame
                elif len(oo) > len(subgame):
                    oo = subgame
        new_subgame = 'o' + 'xo' * int((len(oo)-5)/2)
        brd = remove_subgame(brd,oo)
        brd = add_subgame(brd,new_subgame)
        
    #rule5
    elif brd_list.count('ooxoxo') == 2:
        
        if 'oxox' in brd_list:
        
            brd = remove_subgame(brd,'ooxoxo')
            brd = add_subgame(brd,'oxx')

        elif brd_list.count('ooxoxo') == 2 and 'ox' in brd_list:
            brd = remove_subgame(brd,'ooxoxo')
            brd = add_subgame(brd,'oxx')
        else: 
            brd = remove_subgame(brd,'ooxoxo')
            brd = add_subgame(brd,'oxx')
            brd = add_subgame(brd,'ox')
    elif 'ooxoxo' in brd_list and 'oxox' in brd_list and 'ox' in brd_list:
        brd = remove_subgame(brd,'ooxoxo')
        brd = add_subgame(brd,'oxx')
    elif 'ooxoxo' in brd_list and 'oxox' in brd_list:
        brd = remove_subgame(brd,'ooxoxo')
        brd = add_subgame(brd,'oxx')
        brd = add_subgame(brd,'ox')
    elif 'ooxoxo' in brd_list and 'ox' in brd_list:
        brd = remove_subgame(brd,'ooxoxo')
        brd = remove_subgame(brd,'ox')
        brd = add_subgame(brd,'oxx')    
    elif 'oxox' in brd_list and 'ox' in brd_list:
        brd = remove_subgame(brd,'oxox')
        brd = add_subgame(brd,'ox')
    elif 'ooxoxo' in brd_list:
        brd = remove_subgame(brd,'ooxoxo')
        brd = add_subgame(brd,'oxx')
    elif 'oxox' in brd_list:
        brd = remove_subgame(brd,'oxox')
        brd = add_subgame(brd,'oxx')
    elif 'ox' in brd_list:
        brd = remove_subgame(brd,'ox')

    #rule6
    elif vector[0] != 0:
        all_o = []
        for subgame in brd_list:
            if subgame[1] == 'x' and subgame[-1] == 'o':
                all_o.append(subgame)
        all_o = sorted(all_o, key = len, reverse = True)
        subgame = all_o[0]
        if subgame != 'oxoxoxoxoxo' and subgame != 'oxoxoxo' and subgame != 'oxoxo':
            brd = remove_subgame(brd,subgame)
            new_subgame = 'o' + 'xo' * int((len(subgame)-3)/2)
            brd = add_subgame(brd,new_subgame)
        elif 'oxoxoxoxoxo' in brd_list:
            brd = remove_subgame(brd,'oxoxoxoxoxo')
            brd = add_subgame(brd,'oxoxoxo')
            brd = add_subgame(brd,'oxx')
        elif 'oxoxoxo' in brd_list:
            brd=  remove_subgame(brd,'oxoxoxo')
            brd=  add_subgame(brd,'oxoxo')
        elif 'oxoxo' in brd_list:
            brd = remove_subgame(brd,'oxoxo')
            brd = add_subgame(brd,'oxx')

    #rule7
    elif 'ooxoxoxo' in brd_list:
        brd = remove_subgame(brd,'ooxoxoxo')
        brd = add_subgame(brd,'ooxo')
        brd = add_subgame(brd,'oxx')
    elif 'oxx' in brd_list:
        brd = remove_subgame(brd,'oxx')

    else:
        print('right_strat_error, no rules apllicable')
        print(brd)
        exit()

    return brd


def check_vector(vector,turn):
    
    a = vector[0]
    b = vector[1]
    c = vector[2]
    d = vector[3]
    e = vector[4]
    f = vector[5]
    y = vector[6]
    z = vector[7]
    
    if turn == 'x':
        if y == 0 and z == 1 and a > c:
            return True
        elif y <= 1 and z == 0 and a >= c:
            return True
        else:
            return False
            
    else:
        if y == 0 and z == 0 and a > c:
            return True
        elif a==0 and b == 0 and c ==0 and y ==0 and z==0 and e >= 1 and (d ==0 or d+e >= 3):
            return True
        elif e == 0 and f > 0:
            return True
        else:
            return False

def autoplay(game):
    if len(game.board) == 0:
        pass


    elif game.turn == 'x':
        playing_game = ALC(0,'x')
        playing_game.board = right_strat(game.board)
        playing_game.turn = 'o'
        playing_game.board = ASF(playing_game.board)
        playing_game_length = len(playing_game.board)
        if playing_game_length == 0:
            pass
        elif playing_game.board in right_checked[playing_game_length]:
            pass
        else:
            vector = count(playing_game.board)
            if check_vector(vector,playing_game.turn) == False:
                print("x move vector error",vector)
                print("parent",game.board,game.turn)
                print("child",playing_game.board,playing_game.turn)
                exit()
            elif playing_game.board == 'ox_oxoxo' or playing_game.board == 'oxox_oxoxoxo' or playing_game.board == 'ox_oxox_oxoxoxoxoxoxoxo':
                print("x move, in q",vector)
                print("parent",game.board,game.turn)
                print("child",playing_game.board,playing_game.turn)
                exit()
            elif vector[0] == 0 and vector[1] == 0 and vector[2] == 0 and vector[3] == 0 and vector[4] == 0 and vector[6] == 0 and vector[7] == 0:
                pass
            else:
                right_checked[playing_game_length].add(playing_game.board)
                autoplay(playing_game)


    else:
        board_list = game.board.split('_')
        #cheat start
        k = 0
        process = False
        if len(board_list) == 1:
            if game.board[0:2] == 'ox' and game.board[-1] == 'o':
                length = len(game.board)
                if length >= 17:
                    process = True
                    remainder = length % 4
                    for i in range(0,length,2):
                        playing_game = ALC(0,'x')
                        if i == 0:
                            oo = 'oo'+'xo' * int((length-3-i)/2)
                            playing_game.board = f"{oo}"
                            playing_game_length = len(playing_game.board)

                            if playing_game.board in left_checked[playing_game_length]:
                                pass
                            else:
                                left_checked[playing_game_length].add(playing_game.board)
                                autoplay(playing_game)

                        elif i == 6:
                            oo = 'oo'+'xo' * int((length-3-i)/2)
                            playing_game.board = f"{oo}"
                            playing_game_length = len(playing_game.board)

                            if playing_game.board in left_checked[playing_game_length]:
                                pass
                            else:
                                left_checked[playing_game_length].add(playing_game.board)
                                autoplay(playing_game)

                        elif i == 12:
                            oo = 'oo'+'xo' * int((length-3-i)/2)
                            playing_game.board = f"ox_oxox_{oo}"
                            playing_game_length = len(playing_game.board)

                            if playing_game.board in left_checked[playing_game_length]:
                                pass
                            else:
                                left_checked[playing_game_length].add(playing_game.board)
                                autoplay(playing_game)

                        elif i <= length-1 - i:
                            oo = 'oo'+'xo' * int((length-3-i)/2)
                            a = 'ox' * int(i/2)
                            playing_game.board = f"{a}_{oo}"
                            playing_game_length = len(playing_game.board)

                            if playing_game.board in left_checked[playing_game_length]:
                                pass
                            else:
                                left_checked[playing_game_length].add(playing_game.board)
                                autoplay(playing_game)

                        else:
                            if remainder == 1:
                                oo = 'oo'+'xo' * int((length-3-i)/2)
                                a = 'ox' * int(i/2)
                                playing_game.board = f"{oo}_{a}"
                                playing_game_length = len(playing_game.board)

                                if playing_game.board in left_checked[playing_game_length]:
                                    pass
                                else:
                                    left_checked[playing_game_length].add(playing_game.board)
                                    autoplay(playing_game)


                            break

        #cheat end
        if process == False:
            o_position = []
            temp_to_find_o = ''
            for i in range(len(board_list)):
                if board_list[i] == temp_to_find_o:
                    k += len(board_list[i]) + 1
                else:
                    for j in range(len(board_list[i])):
                        if board_list[i][j] == 'o':
                            o_position.append(k+j)
                    k += len(board_list[i]) + 1
                    playing_game = board_list[i]
            for position in o_position:
                if position != 0 and game.board[position-1] == 'x' :
                        playing_game = ALC(0,'x')
                        playing_game.board = f"{game.board[0:position-1]}o_{game.board[position+1:]}"
                        playing_game.turn = 'x'
                        playing_game.board = ASF(playing_game.board)
                        playing_game_length = len(playing_game.board)
                        if playing_game_length == 0:
                            print('ERROR Right play to empty')
                            exit()

                        elif playing_game.board in left_checked[playing_game_length]:
                            pass
                        else:
                            vector = count(playing_game.board)
                            if check_vector(vector,playing_game.turn) == False:
                                print('o move vector error',vector)
                                print("parent",game.board,game.turn)
                                print("child",playing_game.board,playing_game.turn)
                                exit()
                            else:
                                left_checked[playing_game_length].add(playing_game.board)
                                autoplay(playing_game)
                if position != len(game.board) - 1 and game.board[position+1] == 'x':
                        playing_game = ALC(0,'x')
                        playing_game.board = f"{game.board[0:position]}_o{game.board[position+2:]}"
                        playing_game.turn = 'x'
                        playing_game.board = ASF(playing_game.board)
                        playing_game_length = len(playing_game.board)
                        if playing_game_length == 0:
                            print('ERROR Right play to empty')
                            exit()
                        elif playing_game.board in left_checked[playing_game_length]:
                            pass
                        else:
                            vector = count(playing_game.board)
                            if check_vector(vector,playing_game.turn) == False:
                                print('o move vector error',vector)
                                print("parent",game.board,game.turn)
                                print("child",playing_game.board,playing_game.turn)
                                exit()
                            else:
                                left_checked[playing_game_length].add(playing_game.board)
                                autoplay(playing_game)
    
def autoplay_tree(game):
    
    if len(game.board) == 0:
        pass
    

    elif game.turn == 'x':
        playing_game = Linked_ALC(0,'x')
        playing_game.board = right_strat(game.board)
        playing_game.turn = 'o'
        playing_game.board = ASF(playing_game.board)
        playing_game_length = len(playing_game.board)
        inside = False
        for children in game.child:
            if playing_game.board == children.board:
                inside=  True
                break 
        if inside == False:
            game.child.add(playing_game)
        
        if playing_game_length == 0:
            pass
        elif playing_game.board in right_checked[playing_game_length]:
            pass
        else:
            vector = count(playing_game.board)
            if check_vector(vector,playing_game.turn) == False:
                print("x move vector error",vector)
                print("parent",game.board,game.turn)
                print("child",playing_game.board,playing_game.turn)
                exit()
            elif playing_game.board == 'ox_oxoxo' or playing_game.board == 'oxox_oxoxoxo' or playing_game.board == 'ox_oxox_oxoxoxoxoxoxoxo':
                print("x move, in q",vector)
                print("parent",game.board,game.turn)
                print("child",playing_game.board,playing_game.turn)
                exit()
            elif vector[0] == 0 and vector[1] == 0 and vector[2] == 0 and vector[3] == 0 and vector[4] == 0 and vector[6] == 0 and vector[7] == 0:
                pass
            else:
                
                right_checked[playing_game_length].add(playing_game.board)
                autoplay_tree(playing_game)


    else:
        board_list = game.board.split('_')
        #cheat start
        k = 0
        process = False
        if len(board_list) == 1:
            if game.board[0:2] == 'ox' and game.board[-1] == 'o':
                length = len(game.board)
                if length >= 17:
                    process = True
                    remainder = length % 4
                    for i in range(0,length,2):
                        playing_game = Linked_ALC(0,'x')
                        if i == 0:
                            oo = 'oo'+'xo' * int((length-3-i)/2)
                            playing_game.board = f"{oo}"
                            playing_game_length = len(playing_game.board)

                            if playing_game.board in left_checked[playing_game_length]:
                                pass
                            else:
                                left_checked[playing_game_length].add(playing_game.board)
                                game.child.add(playing_game)
                                
                                autoplay_tree(playing_game)

                        elif i == 6:
                            oo = 'oo'+'xo' * int((length-3-i)/2)
                            playing_game.board = f"{oo}"
                            playing_game_length = len(playing_game.board)

                            if playing_game.board in left_checked[playing_game_length]:
                                pass
                            else:
                                left_checked[playing_game_length].add(playing_game.board)
                                game.child.add(playing_game)
                                autoplay_tree(playing_game)

                        elif i == 12:
                            oo = 'oo'+'xo' * int((length-3-i)/2)
                            playing_game.board = f"ox_oxox_{oo}"
                            playing_game_length = len(playing_game.board)

                            if playing_game.board in left_checked[playing_game_length]:
                                pass
                            else:
                                left_checked[playing_game_length].add(playing_game.board)
                                game.child.add(playing_game)
                                autoplay_tree(playing_game)

                        elif i <= length-1 - i:
                            oo = 'oo'+'xo' * int((length-3-i)/2)
                            a = 'ox' * int(i/2)
                            playing_game.board = f"{a}_{oo}"
                            playing_game_length = len(playing_game.board)

                            if playing_game.board in left_checked[playing_game_length]:
                                pass
                            else:
                                left_checked[playing_game_length].add(playing_game.board)
                                game.child.add(playing_game)
                                autoplay_tree(playing_game)

                        else:
                            if remainder == 1:
                                oo = 'oo'+'xo' * int((length-3-i)/2)
                                a = 'ox' * int(i/2)
                                playing_game.board = f"{oo}_{a}"
                                playing_game_length = len(playing_game.board)

                                if playing_game.board in left_checked[playing_game_length]:
                                    pass
                                else:
                                    left_checked[playing_game_length].add(playing_game.board)
                                    game.child.add(playing_game)
                                    autoplay_tree(playing_game)


                            break

        #cheat end
        if process == False:
            
            o_position = []
            temp_to_find_o = ''
            for i in range(len(board_list)):
                if board_list[i] == temp_to_find_o:
                    k += len(board_list[i]) + 1
                else:
                    for j in range(len(board_list[i])):
                        if board_list[i][j] == 'o':
                            o_position.append(k+j)
                    k += len(board_list[i]) + 1
                    playing_game = board_list[i]
            for position in o_position:
                if position != 0 and game.board[position-1] == 'x' :
                        playing_game = Linked_ALC(0,'x')
                        playing_game.board = f"{game.board[0:position-1]}o_{game.board[position+1:]}"
                        playing_game.turn = 'x'
                        playing_game.board = ASF(playing_game.board)
                        playing_game_length = len(playing_game.board)
                        inside = False
                        for children in game.child:
                            if playing_game.board == children.board:
                                inside=  True
                                break 
                        if inside == False:
                            game.child.add(playing_game)
                        
                        if playing_game_length == 0:
                            print('ERROR Right play to empty')
                            exit()

                        elif playing_game.board in left_checked[playing_game_length]:
                            pass
                        else:
                            vector = count(playing_game.board)
                            if check_vector(vector,playing_game.turn) == False:
                                print('o move vector error',vector)
                                print("parent",game.board,game.turn)
                                print("child",playing_game.board,playing_game.turn)
                                exit()
                            else:
                                left_checked[playing_game_length].add(playing_game.board)
                                autoplay_tree(playing_game)
                if position != len(game.board) - 1 and game.board[position+1] == 'x':
                        playing_game = Linked_ALC(0,'x')
                        playing_game.board = f"{game.board[0:position]}_o{game.board[position+2:]}"
                        playing_game.turn = 'x'
                        playing_game.board = ASF(playing_game.board)
                        playing_game_length = len(playing_game.board)
                        inside = False
                        for children in game.child:
                            if playing_game.board == children.board:
                                inside=  True
                                break 
                        if inside == False:
                            game.child.add(playing_game)
                        
                        if playing_game_length == 0:
                            print('ERROR Right play to empty')
                            exit()
                        elif playing_game.board in left_checked[playing_game_length]:
                            pass
                        else:
                            vector = count(playing_game.board)
                            if check_vector(vector,playing_game.turn) == False:
                                print('o move vector error',vector)
                                print("parent",game.board,game.turn)
                                print("child",playing_game.board,playing_game.turn)
                                exit()
                            else:
                                left_checked[playing_game_length].add(playing_game.board)
                                autoplay_tree(playing_game)








#for print data
with open('data.csv','w') as f:
    f.write("length,time,left_node,right_node\n")
    left_checked = {}
    right_checked = {}
    for i in range(4,60):
        if i*2 < 26:
            for j in range(27):
                right_checked[j] =  set()
                left_checked[j] = set()
        else:
            for j in range(i*2+1):
                right_checked[j] =  set()
                left_checked[j] = set()

        right_checked[8].add("ooxoxoxo")
        right_checked[17].add("ox_oox_oxox_oxoxo")
        right_checked[26].add("ox_oxx_oxox_oxoxoxoxoxoxox")
        left_checked[9].add('oox_oxoxo')
        left_checked[11].add("ox_oxoxoxox")
        left_checked[12].add('oxoxoxoxoxox')
        left_checked[13].add('ox_ooxoxoxoxo')
        left_checked[15].add("oxox_oxoxoxoxox")
        left_checked[17].add("oxox_ooxoxoxoxoxo")
        left_checked[26].add('ox_oxox_oxoxoxoxoxoxoxoxox')
        a = ALC(i,'x')
        parent = a
        start = time.time()
        autoplay(a)
        end = time.time()
        right_amount = 0
        for length in right_checked:
            right_amount += len(right_checked[length])
        left_amount = 0
        for length in left_checked:
            left_amount += len(left_checked[length])
        print(f"{i},{end-start},{left_amount},{right_amount}")
        f.write(f"{i},{end-start},{left_amount},{right_amount}\n")
        right_checked.clear()
        left_checked.clear()



# with open('tree.txt','w') as f:
#     left_checked = {}
#     right_checked = {}
#     for i in [1,2,4,5,6,7,8]:
    
#         if i*2 < 26:
#             for j in range(27):
#                 right_checked[j] =  set()
#                 left_checked[j] = set()
#         else:
#             for j in range(i*2+1):
#                 right_checked[j] =  set()
#                 left_checked[j] = set()
#         right_checked[8].add("ooxoxoxo")
#         right_checked[17].add("ox_oox_oxox_oxoxo")
#         right_checked[26].add("ox_oxx_oxox_oxoxoxoxoxoxox")
#         left_checked[9].add('oox_oxoxo')
#         left_checked[11].add("ox_oxoxoxox")
#         left_checked[12].add('oxoxoxoxoxox')
#         left_checked[13].add('ox_ooxoxoxoxo')
#         left_checked[15].add("oxox_oxoxoxoxox")
#         left_checked[17].add("oxox_ooxoxoxoxoxo")
#         left_checked[26].add('ox_oxox_oxoxoxoxoxoxoxoxox')
#         a = Linked_ALC(i,'x')
#         parent = a
#         start = time.time()
#         autoplay_tree(a)
#         end = time.time()
#         right_amount = 0
#         for length in right_checked:
#             right_amount += len(right_checked[length])
#         left_amount = 0
#         for length in left_checked:
#             left_amount += len(left_checked[length])
#         print(f"{i},{end-start},{left_amount},{right_amount}")
#         f.write(f"{i},{end-start},{left_amount},{right_amount}\n\n")
#         f.write(str(a))
#         right_checked.clear()
#         left_checked.clear()
        




