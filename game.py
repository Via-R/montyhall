import random


class Game:
    def __init__(self, change_choice: bool):
        self.change_choice: bool = change_choice
        self.doors = [False] * 3

    def _hide_prize(self) -> None:
        self.doors[random.randint(0, 2)] = True
