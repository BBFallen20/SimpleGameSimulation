from abc import ABC, abstractmethod
import random
from Game.Users.settings import *


class PlayerAbstract(ABC):
    @abstractmethod
    def get_damage(self, damage):
        """Метод получения урона"""
        raise NotImplementedError('Method get_damage not implemented!')

    @abstractmethod
    def random_move(self):
        """Случайный выбор из существующих функций-ходов участника"""
        raise NotImplementedError('Method random_move not implemented!')

    @abstractmethod
    def get_health(self):
        """Метод вывода уровня здоровья"""
        raise NotImplementedError('Method get_health not implemented!')

    @abstractmethod
    def choose_opponent(self, opponent):
        """Метод определения оппонента"""
        raise NotImplementedError('Method choose opponent not implemented!')

    @abstractmethod
    def default_range_hit(self):
        """Метод нанесения урона в небольшом диапазоне"""
        return NotImplementedError('Method default_range_hit not implemented!')

    @abstractmethod
    def big_range_hit(self):
        """Метод нанесения урона в значительном диапазоне"""
        return NotImplementedError('Method big_range_hit not implemented!')

    @abstractmethod
    def heal(self):
        """Метод излечения"""
        return NotImplementedError('Method heal not implemented!')


class PlayerDefault(PlayerAbstract):
    """Абстрактный класс участника"""
    health = default_health
    opponent = None

    def get_damage(self, damage):
        """Метод получения урона"""
        self.health -= damage

    def get_health(self):
        """Метод вывода уровня здоровья"""
        # Предусмотрено избегание отрицательных значений здоровья(если здоровье меньше 0 - вернет 0 в любом случае)
        if self.health < 0 and off_negative:
            self.health = 0
        print(f"{self.__str__()} has {self.health}hp.")
        return self.health

    def choose_opponent(self, opponent):
        """Метод определения оппонента"""
        self.opponent = opponent

    def default_range_hit(self):
        """Метод нанесения урона в небольшом диапазоне"""
        damage = random.randint(default_range_min, default_range_max)
        self.opponent.get_damage(damage)
        print(f"{self.__str__()} damaged {self.opponent} at {damage} hp!")

    def big_range_hit(self):
        """Метод нанесения урона в значительном диапазоне"""
        damage = random.randint(big_range_min, big_range_max)
        self.opponent.get_damage(damage)
        print(f"{self.__str__()} damaged {self.opponent} at {damage}hp{'[CRITICAL HIT]'if damage > 30 else ''}!")

    def heal(self):
        """Метод излечения"""
        points = random.randint(default_range_min, default_range_max)
        self.health += points
        print(f"{self.__str__()} healed {points} hp!")

    @abstractmethod
    def random_move(self):
        """Случайный выбор из существующих функций-ходов участника"""
        pass


class PC(PlayerDefault):
    """Симуляция участника - ПК"""
    def __str__(self):
        """Корректное отображение объекта в случае вывода в консоль(преобразование в строку)"""
        return "AI"

    def random_move(self):
        """Переопределение родительского метода случайного хода для ПК.
        Если уровень здоровья станет меньше 35 - шанс лечения повышается вдвое.
        """
        if self.health < critical_health_value_for_pc:
            return random.choices([self.default_range_hit, self.big_range_hit, self.heal], weights=[1, 1, 2])[0]()
        else:
            return random.choices([self.default_range_hit, self.big_range_hit, self.heal], weights=[1, 1, 1])[0]()


class Player(PlayerDefault):
    """Симуляция участника - Игрок"""
    def __str__(self):
        return "Player"

    def random_move(self):
        """Случайный выбор из существующих функций-ходов участника"""
        return random.choices([self.default_range_hit, self.big_range_hit, self.heal], weights=[1, 1, 1])[0]()


def get_players():
    """Функция определения участников игры, возвращает словарь с двумя игроками(возможно расширение)"""
    # Создание объекта-участника - ПК
    pc = PC()
    # Создание объекта-участника - Игрока
    player = Player()
    # Опеределение оппонентов
    pc.choose_opponent(player)
    player.choose_opponent(pc)
    return {'Player1': pc, 'Player2': player}
