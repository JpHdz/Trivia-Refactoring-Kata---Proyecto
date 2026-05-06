from typing import List
from .igame import IGame

class Player:
    def __init__(self, name: str):
        self.name = name
        self.position = 1
        self.coins = 0
        self.in_penalty_box = False

class QuestionDeck:
    def __init__(self):
        self.questions_by_category = {
            "Pop": [],
            "Science": [],
            "Sports": [],
            "Rock": []
        }
        for i in range(50):
            self.questions_by_category["Pop"].append(f"Pop Question {i}")
            self.questions_by_category["Science"].append(f"Science Question {i}")
            self.questions_by_category["Sports"].append(f"Sports Question {i}")
            self.questions_by_category["Rock"].append(f"Rock Question {i}")

    def next_question(self, category: str) -> str:
        return self.questions_by_category[category].pop(0)

class Game(IGame):
    BOARD_SIZE = 12
    WINNING_COINS = 6

    def __init__(self):
        self.players = []
        self.deck = QuestionDeck()
        self.current_player = 0
        self.is_getting_out_of_penalty_box = False

    def has_enough_players(self) -> bool:
        return self.how_many_players() >= 2

    def add(self, player_name: str) -> bool:
        self.players.append(Player(player_name))

        print(f"{player_name} was added")
        print(f"They are player number {len(self.players)}")
        return True

    def how_many_players(self) -> int:
        return len(self.players)

    def roll(self, roll: int) -> None:
        player = self.players[self.current_player]
        print(f"{player.name} is the current player")
        print(f"They have rolled a {roll}")

        if player.in_penalty_box:
            if roll % 2 != 0:
                self.is_getting_out_of_penalty_box = True
                print(f"{player.name} is getting out of the penalty box")
                self._move_player_and_ask_question(player, roll)
            else:
                print(f"{player.name} is not getting out of the penalty box")
                self.is_getting_out_of_penalty_box = False
        else:
            self._move_player_and_ask_question(player, roll)

    def _move_player_and_ask_question(self, player: Player, roll: int) -> None:
        player.position = player.position + roll
        if player.position > self.BOARD_SIZE:
            player.position = player.position - self.BOARD_SIZE

        print(f"{player.name}'s new location is {player.position}")
        print(f"The category is {self.current_category(player)}")
        self.ask_question()

    def ask_question(self) -> None:
        player = self.players[self.current_player]
        category = self.current_category(player)
        print(self.deck.next_question(category))

    def current_category(self, player: Player) -> str:
        if player.position - 1 == 0: return "Pop"
        if player.position - 1 == 4: return "Pop"
        if player.position - 1 == 8: return "Pop"
        if player.position - 1 == 1: return "Science"
        if player.position - 1 == 5: return "Science"
        if player.position - 1 == 9: return "Science"
        if player.position - 1 == 2: return "Sports"
        if player.position - 1 == 6: return "Sports"
        if player.position - 1 == 10: return "Sports"
        return "Rock"

    def handle_correct_answer(self) -> bool:
        player = self.players[self.current_player]
        if player.in_penalty_box:
            if self.is_getting_out_of_penalty_box:
                print("Answer was correct!!!!")
                player.coins += 1
                print(f"{player.name} now has {player.coins} Gold Coins.")

                winner = self.did_player_win(player)
                self._next_player()

                return winner
            else:
                self._next_player()
                return True
        else:
            print("Answer was corrent!!!!")
            player.coins += 1
            print(f"{player.name} now has {player.coins} Gold Coins.")

            winner = self.did_player_win(player)
            self._next_player()

            return winner

    def wrong_answer(self) -> bool:
        player = self.players[self.current_player]
        print("Question was incorrectly answered")
        print(f"{player.name} was sent to the penalty box")
        player.in_penalty_box = True

        self._next_player()
        return True

    def _next_player(self) -> None:
        self.current_player += 1
        if self.current_player == len(self.players):
            self.current_player = 0

    def did_player_win(self, player: Player) -> bool:
        return not (player.coins == self.WINNING_COINS)
