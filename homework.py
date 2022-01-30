class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = '{0:.3f}'.format(duration)
        self.distance = '{0:.3f}'.format(distance)
        self.speed = '{0:.3f}'.format(speed)
        self.calories = '{0:.3f}'.format(calories)

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                + f'Длительность: {self.duration} ч.; '
                + f'Дистанция: {self.distance} км; '
                + f'Ср. скорость: {self.speed} км/ч; '
                + f'Потрачено ккал: {self.calories}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

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
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

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

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        """(18 * средняя_скорость – 20) * вес_спортсмена
        / M_IN_KM * время_тренировки_в_минутах"""
        coeff_calories_1 = 18
        coeff_calories_2 = 20
        coeff_calories_3 = 60
        return ((coeff_calories_1 * self.get_mean_speed() - coeff_calories_2)
                * self.weight / self.M_IN_KM
                * self.duration * coeff_calories_3)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

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
        """(0.035 * вес + (скорость ** 2 // рост) * 0.029 * вес)
            * время_тренировки_в_минутах"""
        coeff_calories_1 = 0.035
        coeff_calories_2 = 2
        coeff_calories_3 = 0.029
        coeff_calories_4 = 60
        return ((coeff_calories_1 * self.weight + (self.get_mean_speed()
                ** coeff_calories_2 // self.height)
                * coeff_calories_3 * self.weight)
                * self.duration * coeff_calories_4)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

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
        """(скорость + 1.1) * 2 * вес"""
        coeff_calories_1 = 1.1
        coeff_calories_2 = 2
        return ((self.get_mean_speed() + coeff_calories_1)
                * coeff_calories_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        return Swimming(*data)
    elif workout_type == 'RUN':
        return Running(*data)
    elif workout_type == 'WLK':
        return SportsWalking(*data)
    return None


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
