class Board:
    board = []
    ships = {
      'Carrier': 5,
      'Battleship': 4,
      'Destroyer': 3,
      'Submarine': 3,
      'Patrol Boat': 2
    }
    def __init__(self, row, column) -> None:
        self.row = row
        self.column = column

    def emptyBoard(self):
        for i in range(10):
            row = []
            for j in range(10):
                row.append(' ')
            Board.board.append(row)
        return Board.board

    def displayBoard(self, board):
        
        for i in range(len(board)):
            print('|'.join(board[i]))
            print('-'*20)
            
    def shipIndex(self, coordinateShip):
    
        column, row = list(coordinateShip)
        row_index = int(row) - 1
        col_index = coordinates[column]
        return row_index, col_index

    def updateBoard(self):
        ships_list = list(Board.ships.keys())
        i = 0
        while i<len(ships_list):
            ship = ships_list[i]
            directionShip = input("Vertical or Horizontal: [V/H]: ")
            coordinateShip = input("Enter {} coardinates: ".format(ship))
            if not self.shipValidation(ship, coordinateShip, directionShip):
                print('Coordinates in use, please re enter valide coordinates')
                continue
            row, column = self.shipIndex(coordinateShip)    
            if directionShip.upper() == 'V':
                for i in range(row, row+Board.ships[ship]):
                    Board.board[i][column] = ship[0]
            elif directionShip.upper() == 'H':
                for i in range(column, column+Board.ships[ship]):
                    Board.board[row][i] = ship[0]
            i+=1
        return Board.board

    def shipValidation(self, ship, coordinate, direction):
        row, column = self.shipIndex(coordinate)
        if direction.upper() == 'V':
                for i in range(row, row + Board.ships[ship]):
                    if Board.board[i][column] != ' ':
                        return False
        elif direction.upper() == 'H':
            for i in range(column, column+Board.ships[ship]):
                if Board.board[row][i] != ' ':
                    return False
        return True
        
                      

obj = Board(10, 10)
board = obj.emptyBoard()
obj.displayBoard(board) 


                   
mainMenu = '''1. One Player v Computer 
2. Two Player 
3. Computer v Computer 
0. Quit'''
print(mainMenu)
menuChoice = input("Enter game choice: ")
print(menuChoice)

menuBoardSetup = '''1. Select and Place a Ship
2. Select and Auto-Place a Ship 
3. Auto-Place All Available Ships
4. Auto-place All Ships
5. Reset Board'''

print(menuBoardSetup)
setupChoice = input("Select board setup to conitinue: ")
print(setupChoice)

coordinates = {
  'A': 0,
  'B': 1,
  'C': 2,
  'D': 3,
  'E': 4,
  'F': 5,
  'G': 6,
  'H': 7,
  'I': 8,
  'J': 9,
}

board = obj.updateBoard()
obj.displayBoard(board)