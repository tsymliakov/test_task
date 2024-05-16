# Задание 3
# имеется список списков
# a = [[1, 2, 3], [4, 5, 6]]
# сделать список словарей
# b = [{'k1' : 1, 'k2' : 2, 'k3' : 3}, {{'k1' : 4, 'k2' : 5, 'k3' : 6}]
# * написать решение в одну строчку


def get_list_of_dicts(spisok_spiskov):
    human_readable_view = list(
        map(
            lambda x, y: dict(zip(x, y)),
            [[f"k{i + 1}" for i in range(j)] for j in [len(_) for _ in spisok_spiskov]],
            spisok_spiskov
        )
    )
    one_line_view = list(map(lambda x, y: dict(zip(x, y)),[[f"k{i + 1}" for i in range(j)] for j in [len(_) for _ in spisok_spiskov]],spisok_spiskov))

    return (human_readable_view, one_line_view)


if __name__ == "__main__":
    spisok_spiskov = [[1, 2, 3], [4, 5, 6]] # :-)
    print(get_list_of_dicts(spisok_spiskov))
