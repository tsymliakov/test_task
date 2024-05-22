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


MIN_SIMMILAR_CHARS = 2

def get_words(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().splitlines()

def get_mutated_words(user_word: str, words: str) -> list[str]:
    continuing_words : list[str] = []

    for w in words:
        if w == user_word:
            continue

        if MIN_SIMMILAR_CHARS == 0:
            continuing_words.append(user_word + w)
            continue

        user_word_char_idx = 0

        while user_word_char_idx < len(user_word):
            simmillar_chars = 0
            w_char_idx = 0

            while user_word_char_idx < len(user_word) and w_char_idx < len(w):
                if user_word[user_word_char_idx] != w[w_char_idx]:
                    break

                simmillar_chars += 1
                user_word_char_idx += 1
                w_char_idx += 1

                if user_word_char_idx == len(user_word):
                    if simmillar_chars >= MIN_SIMMILAR_CHARS:
                        continuing_words.append(user_word + w[simmillar_chars:])
                        break
                    break

            user_word_char_idx += 1

    return continuing_words

if __name__ == "__main__":
    words = get_words('./task_5.txt')
    user_word = input()
    mutated_words = get_mutated_words(user_word, words)

    print(mutated_words)
