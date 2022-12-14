class Board:
    def __init__(self, row, column) -> None:
        self.row = row
        self.column = column

    def emptyBoard(self):

        board = []
        for i in range(10):
            row = []
            for j in range(10):
                row.append(' ')
            board.append(row)
        return board

    def displayBoard(self):
        board = self.emptyBoard()
        for i in range(len(board)):
            print('|'.join(board[i]))
            print('-'*20)


obj = Board(10, 10)
obj.displayBoard()

shipChoice = input("Enter ship choice:")
print("Ship choice is: " + shipChoice)
