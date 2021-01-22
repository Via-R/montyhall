from itertools import product
from game import Game


if __name__ == "__main__":
    games = 10 ** 6
    logs_enabled = False
    parameters_variations = product([False, True], [False, True])

    for p_choice, s_random in parameters_variations:
        wins = 0
        for ind in range(games):
            game = Game(player_change_choice=p_choice, stage_random_choice=s_random, logs_enabled=logs_enabled)
            game.launch()
            wins += game.check_win()

        print(f"Player changes his choice: {p_choice}, stage chooses goat randomly: {s_random}")
        print(f"Wins: {wins / games * 100:.2f}%\n")
