from dataclasses import dataclass
from typing import Dict, List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    STR_RETURN: str = ('Тип тренировки: {}; '
                       'Длительность: {:.3f} ч.; '
                       'Дистанция: {:.3f} км; '
                       'Ср. скорость: {:.3f} км/ч; '
                       'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        """Получить строку по тренировкам"""
        return self.STR_RETURN.format(self.training_type,
                                      self.duration,
                                      self.distance,
                                      self.speed,
                                      self.calories)


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HOUR: float = 60

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: float = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    COEFF_RUN_1: float = 18
    COEFF_RUN_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_RUN_1 * self.get_mean_speed() - self.COEFF_RUN_2)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_WLK_1: float = 0.035
    COEFF_WLK_2: float = 0.029

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_WLK_1 * self.weight + (self.get_mean_speed()
                ** 2 // self.height)
                * self.COEFF_WLK_2 * self.weight)
                * self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_SWM_1: float = 1.1
    COEFF_SWM_2: float = 2

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.COEFF_SWM_1)
                * self.COEFF_SWM_2 * self.weight)


dict_training: Dict[str, List[float]] = {'SWM': Swimming,
                                         'RUN': Running,
                                         'WLK': SportsWalking
                                         }


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        return dict_training[workout_type](*data)
    except KeyError as ke:
        print('Not found training in dictionary:', ke)
    except TypeError:
        print('Incorrect data from the fitness tracker')


def main(training: Training) -> None:
    """Главная функция."""
    try:
        info: InfoMessage = training.show_training_info()
        print(info.get_message())
    except AttributeError as ae:
        print(ae)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
