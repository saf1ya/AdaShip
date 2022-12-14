from random import choice, randint
import sys
from board import Board
from config import ships, board_size
from utils import get_coordinates_tuple


class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.board = None
        self.__opponent = None

    @property
    def opponent(self):
        return self.__opponent

    @opponent.setter
    def opponent(self, opponent):
        if isinstance(opponent, (Player, Computer)):
            self.__opponent = opponent
        else:
            raise ValueError("Cannot set opponent of type %s" % type(opponent))

    def set_up_board(self, with_mine = False):
        self.board = Board()
        while True:
            placed, not_placed = self.board.get_placed_and_not_placed_ships()
            print(self, "- set up your board!")
            print("\nBoats placed on the board: ")
            if not placed:
                print("\tNo boats on the board!")
            else:
                print("\to ", "\n\to  ".join(placed))

            print("\nShip yet to be placed: ")
            if not not_placed:
                print("\tNo boats to be placed on the board!")
                break
            else:
                print("\to ", "\n\to  ".join(not_placed))

            # starting asking for the boat details to place it
            # also have option to automatically place ships legally
            print("\n\nPlease Choose options from bellow options: ")
            print("~ Press Enter to 'Auto place rest of the boat': ")
            print("~ Enter 'reset' to reset the board: ")
            print("~ | Enter the name of the boat want to place: |")
            print("~ Enter 'quit' to quit the game: ")

            boat = input().strip().title()

            if boat == "":  # this means auto_fill is chosen
                self.board.auto_place_remaining_ship()
                break
            elif boat.strip().lower() == "reset":
                print("Board is reset.")
                self.board.reset() # reset the board
                continue
            elif boat.strip().lower() == "quit":
                return "quit"

            if boat not in ships.keys():
                print("Invalid boat name!!!")
                continue
            coordinates = input("Enter the coordinates of the %s. E.g.: F3: " % boat).strip().capitalize()
            x, y = get_coordinates_tuple(coordinates)
            # in case co-ordinates are not in valid format
            while x is None or y is None:
                print("Invalid coordinates!!! Please enter in (E.g.: F3) format.")
                coordinates = input().strip().capitalize()
                x, y = get_coordinates_tuple(coordinates)

            # asking for direction of the ship
            print("Please enter the direction in which the boat is facing: ")
            print("For Vertical direction, enter 'V' or 'v'")
            print("For Horizontal direction, enter 'H' or 'h'")
            direction = input().strip().capitalize()[:1]

            # updating the board with the new entry of the boat placement
            self.board.update_board(x, y, direction, boat)

        if with_mine:
            # plant mines as the requirements of version 3
            self.board.plant_mines()

        # display the board to player before continuing
        self.show_board()
        permission = input("Do you want to continue with this board? (y/n): ")
        if permission[:1].lower() == "n":
            self.set_up_board()

    def play(self):
        print("%s's chance - " % f"Player_{self.player_id}")
        self.show_board()
        coordinates = input("Enter the coordinates to hit E.g.: F3: ").strip().upper()
        if not coordinates:
            print("Do you want to quit game?")
            selection = input("(y/n): ").strip()
            if selection[:1] == "y":
                print("Quiting the game.")
                return
        x, y = get_coordinates_tuple(coordinates)
        if x is None or y is None:
            print("Invalid coordinates, considered as complete Miss.")
            return False
        else:
            hit_status = self.opponent.board.hit(x, y)
            if hit_status in ["Hit", "Miss"]:
                print("%s%s is a '%s' on %s's boat!" % (x, y, hit_status, self.opponent))
            elif hit_status == "Blast":
                print("%s%s is a 'Blast' of Mine" % (x, y))
        print("--"* board_size[0])
        return True

    def play_salvo(self):
        print("%s's chance - " % f"Player_{self.player_id}")
        self.show_board()
        live_boats = self.board.get_live_boats()
        coordinates = input("Enter the coordinates as salvo to hit E.g.: F3 G1: ").strip().upper().split()
        if not coordinates:
            print("Do you want to quit game?")
            selection = input("(y/n): ").strip()
            if selection[:1] == "y":
                print("Quiting the game.")
                return

        for coordinate in coordinates[: len(live_boats)]:
            x, y = get_coordinates_tuple(coordinate)
            if x is None or y is None:
                print("Invalid coordinates, considered as complete Miss.")
            else:
                hit_status = self.opponent.board.hit(x, y)
                if hit_status in ["Hit", "Miss"]:
                    print("%s%s is a '%s' on %s's boat!" % (x, y, hit_status, self.opponent))
                elif hit_status == "Blast":
                    print("%s%s is a 'Blast' of Mine" % (x, y))

        print("--"* board_size[0])
        return True

    def show_board(self):
        board = (str(self)+"'s Board").center(board_size[1] * 2)+"\n"
        board += str(self.board)
        print(board)

    def __str__(self):
        return "Player_%s" % str(self.player_id)

    def __repr__(self):
        return "Player_%s" % str(self.player_id)


class Computer(Player):
    def set_up_board(self, with_mine = False):
        self.board = Board()
        print("Generating computer board...")
        self.board.auto_place_remaining_ship()
        print("Computer has generated it's board.")
        if with_mine:
            self.board.plant_mines()
        self.show_board()

    def play(self):
        print("\nComputer_%s's Chance" % str(self.player_id))
        print(self.board)
        x = choice(tuple(Board.cols.keys()))
        y = randint(0, board_size[0] - 1)
        hit_status = self.opponent.board.hit(x, y, True)
        if hit_status == "exists":
            return
        elif hit_status == "Blast":
            print("%s%s is a 'Blast' of Mine" % (x, y))

        while not hit_status:
            x = choice(tuple(Board.cols.keys()))
            y = randint(0, board_size[0] - 1)
            hit_status = self.opponent.board.hit(x, y, True)
        else:
            print("%s%s is a '%s' on %s's boat!" % (x, y, hit_status, self.opponent))
        input('Press any key to continue: \n')
        print("--"* board_size[0])

    def play_salvo(self):
        print("\nComputer_%s's Chance" % str(self.player_id))
        self.show_board()
        live_boats = self.board.get_live_boats()
        for coordinate in range(len(live_boats)):
            x = choice(tuple(Board.cols.keys()))
            y = randint(0, board_size[0] - 1)
            hit_status = self.opponent.board.hit(x, y, True)
            if hit_status == "exists":
                continue
            elif hit_status == "Blast":
                print("%s%s is a 'Blast' of Mine" % (x, y))

            while not hit_status:
                x = choice(tuple(Board.cols.keys()))
                y = randint(0, board_size[0] - 1)
                hit_status = self.opponent.board.hit(x, y, True)
            else:
                print("%s%s is a '%s' on %s's boat!" % (x, y, hit_status, self.opponent))
        input('Press any key to continue: \n')
        print("--" * board_size[0])
        return True

    def __str__(self):
        return "Computer_%s" % str(self.player_id)

    def __repr__(self):
        return "Computer_%s" % str(self.player_id)
