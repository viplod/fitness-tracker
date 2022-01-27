class InfoMessage:
    """Информационное сообщение о тренировке."""
    
    def __init__(self,
                training_type)



class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * LEN_STEP / M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        pass


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calories_1 = 18
        coeff_calories_2 = 18
        return (coeff_calories_1 * get_mean_speed() - 20) * self.weight / M_IN_KM * self.duration 


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                height: float,
                ) -> None:
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calories_1 = 0.035
        coeff_calories_2 = 2
        coeff_calories_3 = 0.029
        return (coeff_calories_1 * self.height + (get_mean_speed() ** coeff_calories_2 // self.height) *
                coeff_calories_3 * self.weight) * self.duration

class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.length_pool * self.count_pool / M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calories_1 = 1.1
        coeff_calories_2 = 2
        return (get_mean_speed() + coeff_calories_1) * coeff_calories_2 * self.height


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    pass


def main(training: Training) -> None:
    """Главная функция."""
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

