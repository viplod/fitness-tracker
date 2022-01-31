from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    STR_TYPE: str = 'Тип тренировки'
    STR_DURATION: str = 'Длительность'
    STR_DURATION_UNIT: str = 'ч'
    STR_DISTANCE: str = 'Дистанция'
    STR_DISTANCE_UNIT: str = 'км'
    STR_SPEED: str = 'Ср. скорость'
    STR_SPEED_UNIT: str = 'км/ч'
    STR_CALORIES: str = 'Потрачено ккал'

    def get_message(self) -> str:
        '''Получить строку по тренировкам'''

        return (f'{self.STR_TYPE}: {self.training_type}; '
                + f'{self.STR_DURATION}: {self.duration:.3f} '
                + f'{self.STR_DURATION_UNIT}.; '
                + f'{self.STR_DISTANCE}: {self.distance:.3f} '
                + f'{self.STR_DISTANCE_UNIT}; '
                + f'{self.STR_SPEED}: {self.speed:.3f} {self.STR_SPEED_UNIT}; '
                + f'{self.STR_CALORIES}: {self.calories:.3f}.')


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
        self.action = action
        self.duration = duration
        self.weight = weight

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
        self.height = height

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
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.get_mean_speed() + self.COEFF_SWM_1)
                * self.COEFF_SWM_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    return {'SWM': Swimming,
            'RUN': Running,
            'WLK': SportsWalking
            }[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
