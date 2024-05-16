# Задание 2
# в наличии список множеств, внутри множества целые числа
# посчитать
# 1. общее количество чисел
# 2. общую сумму чисел
# 3. посчитать среднее чисел
# 4. собрать все числа из множеств в один кортеж
# написать решение в одну строку


def get_result(m):

    # Решение в одну строку:
    one_line_view = (sum(map(lambda sub_m: len(sub_m),[_ for _ in m])), sum(map(lambda sub_m: sum(sub_m),[_ for _ in m])), sum(map(lambda sub_m: sum(sub_m),[_ for _ in m])) / sum(map(lambda sub_m: len(sub_m),[_ for _ in m])), tuple(sum([list(_) for _ in m], [])))

    # Форматированный вариант решения
    human_readable_view = (sum(
        map(
            lambda sub_m: len(sub_m),
            [_ for _ in m]
        )
    ), sum(
        map(
            lambda sub_m: sum(sub_m),
            [_ for _ in m]
        )
    ), sum(
        map(
            lambda sub_m: sum(sub_m),
            [_ for _ in m]
        )
    ) / sum(
        map(
            lambda sub_m: len(sub_m),
            [_ for _ in m]
        )
    ), tuple(
        sum([list(_) for _ in m], [])
    )
    )

    return (one_line_view, human_readable_view)

if __name__ == "__main__":
    m = [
        {11, 3, 5},
        {2, 17, 87, 32},
        {4, 44},
        {24, 11, 9, 7, 8},
    ]

    print(get_result(m))