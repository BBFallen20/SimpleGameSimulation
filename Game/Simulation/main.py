import random
from typing import Callable

from Game.Users.UsersClasses import get_players


def check_players_hp(players: dict) -> bool:
    """Функция проверки здоровья участников"""
    for player in players.values():
        if player.get_health() == 0:
            print(f"{player} lost this fight.")
            return False
    return True


def get_heading(func: Callable) -> Callable:
    """Вывод заголовка программы"""
    creator = 'Poddubnjak Daniil'
    print(f"""{'='*30}
Game simulation.
Created by {creator}
For LightIt Academy.
{'='*30}
""")
    return func


@get_heading
def simulate_game() -> None:
    """Функция симуляции игры"""
    players = get_players()
    step = 1
    # Пока здоровье одного из участников не достигло 0 - симулировать ходы игроков случайным образом
    while check_players_hp(players):
        print(f"Step {step}.")
        random.choices([players.get('Player1', None), players.get('Player2', None)])[0].random_move()
        step += 1
    print("THE END.")


if __name__ == '__main__':
    simulate_game()
