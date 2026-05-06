import sys
import random

from trivia.game_old import GameOld
from trivia.igame import IGame

def read_yes_no() -> bool:
    while True:
        yn = input(">> Was the answer correct? [y/n] ").strip().upper()
        if yn in ['Y', 'N']:
            return yn == 'Y'
        print("y or n please", file=sys.stderr)

def read_roll() -> int:
    while True:
        roll_str = input(">> Throw a die and input roll, or [ENTER] to generate a random roll: ").strip()
        if not roll_str:
            roll = random.randint(1, 6)
            print(f">> Random roll: {roll}")
            return roll
        if not roll_str.isdigit():
            print(f"Not a number: '{roll_str}'", file=sys.stderr)
            continue
        roll = int(roll_str)
        if roll < 1 or roll > 6:
            print("Invalid roll", file=sys.stderr)
            continue
        return roll

def main():
    print("*** Welcome to Trivia Game ***\n")
    try:
        player_count = int(input("Enter number of players: 1-4\n"))
    except ValueError:
        raise ValueError("No player 1..4")
        
    if player_count < 1 or player_count > 4:
        raise ValueError("No player 1..4")

    print(f"Reading names for {player_count} players:")

    a_game: IGame = GameOld()

    for i in range(1, player_count + 1):
        player_name = input(f"Player {i} name: ")
        a_game.add(player_name)

    print("\n\n--Starting game--")

    not_a_winner = False
    while True:
        roll = read_roll()
        a_game.roll(roll)

        correct = read_yes_no()
        if correct:
            not_a_winner = a_game.handle_correct_answer()
        else:
            not_a_winner = a_game.wrong_answer()

        if not not_a_winner:
            break
            
    print(">> Game won!")

if __name__ == '__main__':
    main()
