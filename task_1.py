# Задание 1
# имеется текстовый файл f.csv, по формату похожий на .csv с разделителем |
"""
lastname|name|patronymic|date_of_birth|id
Фамилия1|Имя1|Отчество1 |21.11.1998 |312040348-3048
Фамилия2|Имя2|Отчество2 |11.01.1972 |457865234-3431
...
"""
# 1. Реализовать сбор уникальных записей
# 2. Случается, что под одинаковым id присутствуют разные данные - собрать
# такие записи

import csv


def read_csv(file_path):
    records = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        for row in reader:
            for i in range(len(row)):
                row[i] = row[i].strip()
            records.append(row)
    return records[1:]

def get_unique_records(records):
    unique_records = set()

    for record in records:
        hashable_form = tuple(record)
        unique_records.add(hashable_form)
    return unique_records

def get_fake_simmilar_records(records):
    """Функция возвращает такие записи, которые имеют дубликаты по полю id, но
    несут в себе отличающиеся другие данные.

    Args:
        records (list[list[str]]): Список списков данных из CSV- файла

    Returns:
        list[list[str]]: Строки, имеющие дублирующие их ID и имеющие различие в
        других данных
    """
    id_column_index = 4 # Не самый удачный момент

    ids = {}

    for record in records:
        if not ids.get(record[id_column_index]):

            # Ради экономии вычислительных ресурсов, в жертву расходу памяти,
            # Дублируем id в словаре
            ids[record[id_column_index]] = [record]

        if record in ids[record[id_column_index]]:
            continue

        ids[record[id_column_index]].append(record)

    fake_the_same_indexes = []

    for id in ids.keys():
        if len(ids[id]) > 1:
            fake_the_same_indexes.extend(ids[id])

    return fake_the_same_indexes

def main():
    input_file = 'task_1.csv'

    records = read_csv(input_file)

    # Задание 1
    unique_records = get_unique_records(records)

    # Задание 2
    fake_simmilar_records = get_fake_simmilar_records(records)

if __name__ == "__main__":
    main()
