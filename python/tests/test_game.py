import sys
import io
import random
import unittest

from trivia.game import Game
from trivia.game_old import GameOld
from trivia.igame import IGame

class GameTest(unittest.TestCase):
    def test_caracterization(self):
        # runs 10,000 "random" games to see the output of old and new code matches
        for seed in range(1, 10000):
            self._test_seed(seed, False)

    def _test_seed(self, seed: int, print_expected: bool):
        expected_output = self.extract_output(seed, GameOld())
        if print_expected:
            print(expected_output)
        actual_output = self.extract_output(seed, Game())
        self.assertEqual(expected_output, actual_output, 
                         f"Change detected for seed {seed}. To breakpoint through it, run this seed alone.")

    def test_one_seed(self):
        # Ignored by default in Java, we can just skip or run it
        # self._test_seed(1, True)
        pass

    def extract_output(self, seed: int, a_game: IGame) -> str:
        # We need a predictable random sequence based on the seed
        rand = random.Random(seed)
        
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        try:
            sys.stdout = new_stdout

            a_game.add("Chet")
            a_game.add("Pat")
            a_game.add("Sue")

            not_a_winner = False
            while True:
                # Java: rand.nextInt(5) + 1 -> 1 to 5 inclusive
                a_game.roll(rand.randint(1, 5))

                # Java: rand.nextInt(9) == 7 -> 0 to 8 inclusive
                if rand.randint(0, 8) == 7:
                    not_a_winner = a_game.wrong_answer()
                else:
                    not_a_winner = a_game.handle_correct_answer()

                if not not_a_winner:
                    break
        finally:
            sys.stdout = old_stdout

        return new_stdout.getvalue()

if __name__ == '__main__':
    unittest.main()
