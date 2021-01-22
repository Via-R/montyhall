import unittest
from game import Stage, Player


class TestStage(unittest.TestCase):
    def test_input_situation(self):
        s = Stage()
        for door in s.doors:
            self.assertIsInstance(door, bool)

        self.assertEqual(sum(s.doors), 0)

        s.hide_prize()

        self.assertEqual(sum(s.doors), 1)

    def test_find_goat(self):
        s = Stage()
        s.hide_prize()

        self.assertEqual(s.doors[s.find_goat()], False)

    def test_check_win(self):
        s = Stage()
        s.hide_prize()
        wins = 0
        for door_ind in range(len(s.doors)):
            wins += s.check_win(door_ind)

        self.assertEqual(wins, 1)


class TestPlayer(unittest.TestCase):
    def test_choice(self):
        p = Player(change_choice=False)
        interval = p.choice_interval
        for _ in range(412):
            c = p.make_choice()
            self.assertIn(c, interval)

    def test_exclude_door(self):
        p = Player(change_choice=False)
        interval = p.choice_interval.copy()
        p.exclude_door(p.make_choice())
        self.assertNotEqual(len(p.choice_interval), len(interval))
        for ind in p.choice_interval:
            self.assertIn(ind, interval)


if __name__ == "__main__":
    unittest.main()
