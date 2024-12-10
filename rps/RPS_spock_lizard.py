import random
import rps.probabilidades_rps as DTMC
from enum import IntEnum
from statistics import mode


class GameAction(IntEnum):
    Rock = 0
    Paper = 1
    Scissors = 2
    # Spock = 3
    # Lizard = 4

    @classmethod
    def minus(cls, *actions_excluded):
        return [ action for action in GameAction if action not in actions_excluded ]


class GameResult(IntEnum):
    Victory = 0
    Defeat = 1
    Tie = 2


class Game:

    def __init__(self):
        self.game_history = []
        self.user_actions_history = []

        self.victories = {
            GameAction.Rock: GameAction.minus(GameAction.Scissors, # GameAction.Lizard
                                              ),
            GameAction.Paper: GameAction.minus(# GameAction.Spock, 
                GameAction.Rock),
            GameAction.Scissors: GameAction.minus(GameAction.Paper, # GameAction.Lizard
                                                  ),
            # GameAction.Spock: GameAction.minus(GameAction.Scissors, GameAction.Rock),
            # GameAction.Lizard: GameAction.minus(GameAction.Spock, GameAction.Paper)
        }

    def user_actions_history_append(self, action):
        self.user_actions_history.append(action)

    def game_history_append(self, game_result):
        self.game_history.append(game_result)

    def assess_game(self, user_action, computer_action):
        game_result = None

        if user_action == computer_action:
            print(f"User and computer picked {user_action.name}. Draw game!")
            game_result = GameResult.Tie

        elif computer_action in self.victories[user_action]:
            print(f"{computer_action.name} wins {user_action.name}. You lost!")
            game_result = GameResult.Defeat

        else:
            print(f"{user_action.name} wins {computer_action.name}. You win!")
            game_result = GameResult.Victory

        return game_result


    def get_computer_action(self):

        # No previous user actions => max initial probability action
        if not self.user_actions_history or not self.game_history:
            computer_action = GameAction(DTMC.max_initial_probability_index())
        # Alternative AI functionality
        # Markov chain (Discrete Time Markov Chain)
        else:
            computer_action = GameAction(DTMC.max_probab_postaction_index(self.user_actions_history[-1].value))

        print(f"Computer picked {computer_action.name}.")

        return computer_action


    def get_user_action(self):
        # Scalable to more options (beyond rock, paper and scissors...)
        game_choices = [f"{game_action.name}[{game_action.value}]" for game_action in GameAction]
        game_choices_str = ", ".join(game_choices)
        user_selection = int(input(f"\nPick a choice ({game_choices_str}): "))
        user_action = GameAction(user_selection)

        return user_action


    def play_another_round(self):
        another_round = input("\nAnother round? (y/n): ")
        return another_round.lower() == 'y'


    def user_actions_history_dumps(self):
        file = open('user_actions_history.txt', 'a', encoding="utf-8")
        print([action.name for action in self.user_actions_history])
        file.write(repr([action.value for action in self.user_actions_history]) + '\n')
        file.close()


    def user_actions_history_load(self):
        file = open('user_actions_history.txt', 'r', encoding="utf-8")
        for line in file:
            print(eval(line))
        file.close()


    def play(self):
        while True:
            computer_action = self.get_computer_action()
            try:
                user_action = self.get_user_action()
                self.user_actions_history_append(user_action)
            except ValueError:
                range_str = f"[0, {len(GameAction) - 1}]"
                print(f"Invalid selection. Pick a choice in range {range_str}!")
                continue

            game_result = self.assess_game(user_action, computer_action)
            self.game_history_append(game_result)

            if not self.play_another_round():
                break

        self.user_actions_history_dumps()
        self.user_actions_history_load()


if __name__ == "__main__":

    game = Game()
    game.play()
    