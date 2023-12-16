import random


class Player:
    def __init__(self, name):
        self.name = name

    def place_ships(self, board):
        ship_types = [("Big", 4), ("Medium", 3), ("Medium", 3), ("Small", 2), ("Small", 2), ("Small", 2)]

        for ship_name, ship_size in ship_types:
            print(f"{self.name}, place your {ship_name} ship ({ship_size} cells) on the board.")
            start_coordinate = self.get_start_coordinate(board)
            orientation = self.get_orientation()
            ship = Ship(ship_name, ship_size)
            ship.place_ship(start_coordinate, orientation)
            board.place_ship(ship)

    def get_start_coordinate(self, board):
        while True:
            try:
                x = int(input(f"Enter the starting row (0-{board.size - 1}): "))
                y = int(input(f"Enter the starting column (0-{board.size - 1}): "))
                if 0 <= x < board.size and 0 <= y < board.size:
                    return x, y
                else:
                    print("Invalid coordinates. Try again.")
            except ValueError:
                print("Invalid input. Enter a number.")

    def get_orientation(self):
        while True:
            orientation = input("Enter 'h' for horizontal or 'v' for vertical placement: ").lower()
            if orientation in ['h', 'v']:
                return 'horizontal' if orientation == 'h' else 'vertical'
            else:
                print("Invalid input. Enter 'h' or 'v'.")

    def make_move(self, board):
        while True:
            try:
                x = int(input("Enter the row (0-9) to bomb: "))
                y = int(input("Enter the column (0-9) to bomb: "))
                return x, y
            except ValueError:
                print("Invalid input. Enter a number.")
class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.coordinates = []

    def place_ship(self, start_coordinate, orientation):
        x, y = start_coordinate
        self.coordinates = [(x + i, y) for i in range(self.size)] if orientation == 'horizontal' else [(x, y + i) for i in range(self.size)]

class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.ships = []

    def place_ship(self, ship):
        for x, y in ship.coordinates:
            self.grid[x][y] = 'S'
        self.ships.append(ship)

    def display(self, show_ships=False):
        print("  " + " ".join(str(i) for i in range(self.size)))
        for i, row in enumerate(self.grid):
            print(f"{i} {' '.join(cell if cell == 'S' and show_ships else ' ' for cell in row)}")

    def attack(self, x, y):
        for ship in self.ships:
            if (x, y) in ship.coordinates:
                ship.coordinates.remove((x, y))
                self.grid[x][y] = 'X'
                if not ship.coordinates:
                    print(f"You sunk the {ship.name}!")
                    self.ships.remove(ship)
                else:
                    print("Hit!")
                return True
        else:
            print("Miss!")
            self.grid[x][y] = 'O'
            return False

def play_battleship():
    board_size = 10
    player_board = Board(board_size)
    computer_board = Board(board_size)

    player = Player("You")
    player.place_ships(player_board)

    computer_ships = [Ship("Big", 4), Ship("Medium", 3), Ship("Medium", 3), Ship("Small", 2), Ship("Small", 2), Ship("Small", 2)]
    for ship in computer_ships:
        ship.place_ship((random.randint(0, board_size - 1), random.randint(0, board_size - 1)), random.choice(['horizontal', 'vertical']))
        computer_board.place_ship(ship)

    while player_board.ships and computer_board.ships:
        print("\nYour board:")
        player_board.display(show_ships=True)

        print("\nComputer's board:")
        computer_board.display()

        x, y = player.make_move(computer_board)
        computer_board.attack(x, y)

        if not computer_board.ships:
            print("Congratulations! You've won!")
            break

        print("\nComputer's turn:")
        x, y = random.randint(0, board_size - 1), random.randint(0, board_size - 1)
        player_board.attack(x, y)

        if not player_board.ships:
            print("Game over. You lost.")
            break

if __name__ == "__main__":
    play_battleship()
