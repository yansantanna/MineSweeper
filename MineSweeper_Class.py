
import random
import os
class MineSweeper():
    
    def __init__(self):
        
        self.presentacion = self.presentacion()
        self.n = int(input('Write the number of rows and columns( ej: 9): '))
        self.mines = int(input('Write the number of mines (ej: 5): '))
        self.mine_values = [[' ' for y in range(self.n)] for x in range(self.n)]
        self.hidden_board = self.create_hidden_board()
        self.hidden_board, self.hidden_mines = self.insert_mines()
        self.hidden_board = self.insert_clues()
        self.board = self.create_board()
        self.check_mines = []
        self.flag_mines = 0
        self.jugando = True
    
    def create_board(self): #crea un tablero visible

        st = "   "
        for i in range(self.n):
            if i >=10:
                st = st + "    " + str(i + 1)
            else:
                st = st + "     " + str(i + 1)
        print(st)   


        for r in range(self.n):
            st = "     "
            if r == 0:
                for col in range(self.n):
                    st = st + "______" 
                print(st)

            st = "     "
            for col in range(self.n):
                st = st + "|     "
            print(st + "|")

            if r+1 >= 10: 
                st = " " + str(r + 1) + "  "
            else:
                st = "  " + str(r + 1) + "  "

            for col in range(self.n):
                if self.mine_values[r][col] == 999:
                    st = st + "| " + str(self.mine_values[r][col]) + " "
                else:
                    st = st + "|  " + str(self.mine_values[r][col]) + "  "
            print(st + "|") 
            st = "     "
            for col in range(self.n):
                st = st + "|_____"
            print(st + '|')    

    def create_hidden_board(self): #crea un tablero invisible

        board= []
        for i in range(self.n):
            board.append([])
            for j in range(self.n):
                board[i].append(0)     
        return board



    def insert_mines(self): #inserta minas de forma randomica de acuerdo con el numero indicado por el jugador
        hidden_mines = []
        number = 0
        while number < self.mines:
            y = random.randint(0, self.n-1)
            x = random.randint(0, self.n-1)
            if self.hidden_board[y][x] !=999:
                self.hidden_board[y][x] = 999
                number += 1
                hidden_mines.append((y,x))
        return self.hidden_board, hidden_mines

    def insert_clues(self): #inserta pistas de acuerdo con la posición de las minas

        for y in range(self.n):
            for x in range(self.n):
                if self.hidden_board[y][x] == 999:
                    for i in [-1,0,1]:
                        for j in [-1,0,1]:
                            if 0 <= y+i <=self.n-1 and 0 <= x+j <=self.n -1:
                                if self.hidden_board[y+i][x+j] !=999:
                                    self.hidden_board[y+i][x+j] += 1
        return self.hidden_board


    def expand(self, y, x): #expande el tablero hasta donde haya una pista
  

        zeros = [(y,x)]
        while len(zeros) > 0:
            y, x = zeros.pop()
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if 0 <= y+i <= self.n-1 and 0 <= x+j <= self.n-1:
                        if self.mine_values[y+i][x+j] == ' ' and self.hidden_board[y+i][x+j] == 0:
                            self.mine_values[y+i][x+j] = 0
                            if(y+i,x+j) not in zeros:
                                zeros.append((y+i,x+j))
                        else:
                            self.mine_values[y+i][x+j] = self.hidden_board[y+i][x+j]
        return self.mine_values


    def menu(self):

        print("Instructions:")
        print("1. Enter row and column number to select a cell, Example \"2 3\"")
        print("2. To mark a mine, enter F or to unmark enter B after row and column numbers, Example \"2 3 F\"")
        position = input().split()


        return  position

    def complet_board(self): #verifica si el tablero está completo 

        for y in range(self.n):
            for x in range(self.n):
                if self.mine_values[y][x] == " " or (self.mine_values[y][x] == '⚑' and self.hidden_board[y][x] != 999) or                 self.mine_values[y][x] == '✖':
                    return False
        return True

    def game_over(self):
        for y in range(self.n):
            for x in range(self.n):
                if self.hidden_board[y][x] == 999:
                    self.hidden_board[y][x] = '✖'
                    self.mine_values[y][x] = self.hidden_board[y][x]
        return self.mine_values


    def presentacion(self):


        print('********************************')
        print('*                              *')
        print('*          MINESWEEPER         *')
        print('*                              *')
        print('********************************')
        print()
        input(" 'Enter' to start...")
    
    def start_game(self):
        while self.jugando:
            mov = self.menu()
            y = int(mov[0])-1
            x = int(mov[1])-1
            try:
                f = mov[2]
            except:
                f = None
            if f == 'F':
                if self.mine_values[y][x] ==" ":
                    self.mine_values[y][x] = '⚑'


                    if (y,x) not in self.check_mines:
                        self.check_mines.append((y,x))
                    if self.hidden_board[y][x] == 999:
                        self.flag_mines+=1

            elif f == 'B':
                if self.mine_values[y][x] =='⚑':
                    self.mine_values[y][x] = ' '
                    self.flag_mines-=1
                    if (y,x) in self.check_mines:
                        self.check_mines.remove((y,x))

            elif f == None:
                if self.hidden_board[y][x] == 999:
                    self.mine_values[y][x] = '✖'
                    self.game_over()
                    os.system("clear")
                    self.create_board()
                    print('\n\n')
                    print('✖✖✖  GAME OVER  ✖✖✖ \n')
                    self.jugando = False
                    
                elif self.hidden_board[y][x] !=0:
                    self.mine_values[y][x] = self.hidden_board[y][x]
                    real = self.mine_values[y][x]
                elif self.hidden_board[y][x] == 0:
                    self.mine_values[y][x] = 0
                    self.mine_values = self.expand( y, x)


            if self.complet_board() == True:
                os.system("clear")
                self.create_board()
                print('\n\n')
                print('Congratulations, you won the Game!! \n')
                self.jugando = False
            else:
                pass
            if self.jugando ==True:
            

                os.system("clear")
                print('********************************************************')
                print('   *                                                *')
                print('   *                   MINESWEEPER                  *')
                print('   *                                                *')
                print('********************************************************')
                print()



                self.create_board()
            else:
                pass




start = MineSweeper()
start.start_game() 

