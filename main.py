import numpy as np
import random
from dataclasses import dataclass

BOARD_SIZE = 8
TIME_LIMIT = 300


@dataclass
class Treasure:
    x: int
    y: int


class Player:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y

    def move(self, direction):
        if direction == 'north':
            if self.y > 0:
                self.y -= 1
                return True
            else:
                print("You can't go higher")
                return False
        elif direction == 'south':
            if self.y < BOARD_SIZE - 1:
                self.y += 1
                return True
            else:
                print("You can't go lower")
                return False
        elif direction == 'east':
            if self.x < BOARD_SIZE - 1:
                self.x += 1
                return True
            else:
                print("You can't go more right")
                return False
        elif direction == 'west':
            if self.x > 0:
                self.x -= 1
                return True
            else:
                print("You can't go more left")
                return False
        else:
            print("Wrong direction!!!")
            return False


def calculate_distance(player: Player, treasure: Treasure):
    return abs(player.x - treasure.x) + abs(player.y - treasure.y)


def calculate_direction(player: Player, treasure: Treasure):
    vertical = "north" if player.y > treasure.y else "south"
    horizontal = "west" if player.x > treasure.x else "east"
    return f"{vertical}-{horizontal}"


def create_board():
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    return board


def place_treasure_and_traps(num_traps):
    # treasure = (random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1))
    treasure = Treasure(random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1))
    traps = set()
    while len(traps) < num_traps:
        trap = (random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1))
        if trap != treasure:
            traps.add(trap)
    return treasure, traps


def print_board(board, player, traps):
    board.fill(0)
    board[player.y, player.x] = 1
    # for trap in traps:
    #     board[trap] = -1
    print(board)


def print_board_game_over(board, history, traps, treasure):
    print('Player = 1, Treasure = 100 , trap = 5')
    board.fill(0)
    for step in history:
        board[(step[1], step[0])] = 1
    for trap in traps:
        board[(trap[1], trap[0])] = 5

    board[(treasure.y, treasure.x)] = 100

    print(board)


def play_game():
    board = create_board()
    player = Player(0, 0)
    treasure, traps = place_treasure_and_traps(num_traps=5)
    moves = 0
    max_moves = 20
    history = [(player.x, player.y)]

    while moves < max_moves:
        print(f"Number of moves left: {max_moves - moves}")
        print_board(board, player, traps)
        distance = calculate_distance(player, treasure)
        if distance == 0:
            print("You won! You found the treasure!")
            print_board_game_over(board=board, history=history[:-1], traps=traps, treasure=treasure)
            break
        direction = calculate_direction(player, treasure)
        # Manhattan distance
        print(f"You are at a distance of {distance} steps in the direction {direction}.")

        move = input("Enter a direction (north/south/east/west): ").lower()
        if player.move(move):
            history.append((player.x, player.y))
            moves += 1

        # print(f'{traps=}')
        if (player.x, player.y) in traps:
            print("You fell into a trap! You lost!")
            print_board_game_over(board=board, history=history, traps=traps, treasure=treasure)
            break

    if moves >= max_moves:
        print("You have exceeded the number of movements allowed. You lost!")
        print_board_game_over(board=board, history=history, traps=traps, treasure=treasure)


if __name__ == '__main__':
    play_game()
