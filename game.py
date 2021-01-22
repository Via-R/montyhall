import random
import logging
logging.basicConfig()
logger = logging.getLogger()

class StageError(Exception):
    pass


class PlayerError(Exception):
    pass


class Stage:
    def __init__(self, randomize_goat_choice: bool = False):
        self.doors = [False] * 3
        self.randomize_goat_choice = randomize_goat_choice
        logger.debug("Stage initiated ")

    def hide_prize(self) -> None:
        if sum(self.doors) == 1:
            raise StageError("The prize was already hidden")

        self.doors[random.randint(0, 2)] = True

        logger.debug("A prize was hidden")
        logger.debug(f"Stage setup: {self.doors}")

    def find_goat(self, chosen_door) -> int:
        inactive_doors = self.doors.copy()
        inactive_doors[chosen_door] = True
        first_goat_ind = inactive_doors.index(False)
        logger.debug(f"Stage found first goat behind the door #{first_goat_ind + 1}")

        if not self.randomize_goat_choice:
            return first_goat_ind

        try:
            second_goat_ind = inactive_doors.index(False, first_goat_ind + 1)
        except ValueError:
            logger.debug("There was only one goat behind closed doors")
            return first_goat_ind

        logger.debug(f"Stage second goat behind the door #{second_goat_ind+1}")
        goat_ind = [first_goat_ind, second_goat_ind][random.randint(0, 1)]
        logger.debug(f"Randomly decided to show the goat behind the door #{goat_ind+1}")

        return goat_ind

    def check_win(self, door: int):
        return self.doors[door]


class Player:
    allowed_distributions = {"linear"}

    def __init__(self, change_choice: bool, choice_distribution: str = "linear"):
        if choice_distribution not in self.allowed_distributions:
            raise PlayerError("This distribution is not allowed")

        self.intuition = random.choice
        self.change_choice: bool = change_choice
        self.choice_interval = [0, 1, 2]

    def make_choice(self, previous_choice: int = None):
        if previous_choice is not None:
            if not self.change_choice:
                return previous_choice

            self.choice_interval.remove(previous_choice)

            return self.choice_interval[0]

        return self.intuition(self.choice_interval)

    def exclude_door(self, ind):
        logger.debug(f"Player will now choose between all doors, excluding #{ind+1}")
        self.choice_interval.remove(ind)


class Game:
    def __init__(self, player_change_choice: bool, stage_random_choice: bool, logs_enabled: bool):
        self.stage = Stage(stage_random_choice)
        self.player = Player(player_change_choice)
        self.win = False

        if logs_enabled:
            logger.setLevel(logging.DEBUG)

    def launch(self):
        logger.debug("Hiding prize...")
        self.stage.hide_prize()
        logger.debug("Player makes choice...")
        chosen_door = self.player.make_choice()
        logger.debug(f"Player chose the door #{chosen_door+1}")
        goat_door = self.stage.find_goat(chosen_door)
        self.player.exclude_door(goat_door)
        logger.debug("Player is asked to change his choice...")
        final_door = self.player.make_choice(chosen_door)
        logger.debug(f"Player chose the door #{final_door + 1}")
        self.win = self.stage.check_win(final_door)
        logger.debug(f"Player won: {self.win}\n")

    def check_win(self):
        return self.win
