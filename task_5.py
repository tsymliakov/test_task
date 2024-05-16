# Задание 5*
# Имеется текстовый файл с набором русских слов(имена существительные,
# им.падеж)
# Одна строка файла содержит одно слово.
# Написать программу которая выводит список слов, каждый элемент списка
# которого - это новое слово,
# которое состоит из двух сцепленных в одно, которые имеются в текстовом файле.
# Порядок вывода слов НЕ имеет значения
# Например, текстовый файл содержит слова: ласты, стык, стыковка, баласт,
# кабала, карась

# Пользователь вводмт первое слово: ласты
# Программа выводит:
# ластык
# ластыковка

# Пользователь вводмт первое слово: кабала
# Программа выводит:
# кабаласты
# кабаласт

# Пользователь вводмт первое слово: стыковка
# Программа выводит:
# стыковкабала
# стыковкарась


def get_words(path):
    words = []

    with open("task_5.txt", 'r', encoding='utf-8') as f:
        return f.read().splitlines()

def get_mutated_words(user_word, words):
    """ В реальности, конечно, лучше применить другой подход для генерации слов,
    например, подход, основанный на цепях Маркова.
    """
    mutated_words = []

    for w in words:
        mutated_words.append(user_word[:int(len(user_word) / 2)] + w[int(len(w) / 2):])

    return mutated_words

if __name__ == "__main__":
    words = get_words('./task_5.txt')
    user_word = input()
    mutated_words = get_mutated_words(user_word, words)

    print(mutated_words)
