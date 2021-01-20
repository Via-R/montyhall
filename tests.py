import unittest
from game import Game


class TestGameSetup(unittest.TestCase):
    def test_input_situation(self):
        g = Game(change_choice=False)
        for door in g.doors:
            self.assertIsInstance(door, bool)

        for door in g.doors:
            self.assertEqual(sum(g.doors), 0)

        g._hide_prize()

        for door in g.doors:
            self.assertEqual(sum(g.doors), 1)


if __name__ == "__main__":
    unittest.main()
