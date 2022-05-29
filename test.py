def to_lines_by_limit(string, limit):
    """Разбивает сплошной текст на строки с указанным
    лимитом знаков без переноса слов"""
    output = ""
    while len(string) >= limit:
        string = string.strip()
        n = min(string.find('\n'), string[:limit].rfind(' '))
        if n == -1:
            n = max(string.find('\n'), string[:limit].rfind(' '))
        if n > 0:  # если пробел есть и не в начале строки
            head = string[:n].strip()
            string = string[n:]
            # string = tail + string
        elif n < 0:
            # print(string)
            raise ValueError(f"The limit '{limit}' is too small: the text can't be split")
        else:  # если пробел в начале строки
            head = string[:limit]
            string = string[limit:]
            print("from else:", head, len(head), "n:", n)
        output += head + "\n"
    output += string.lstrip()
    return output

msg = "Вспомним детство, поиграем в ""Морской бой""?\n"
msg += "По умолчанию играем на поле 6 * 6. При желании выйти из игры (и проиграть) можно ввести 'q' " \
        "вместо хода. В каждом флоте участвуют 6 кораблей:\n"
msg += "- 1 корабль на 3 клетки\n- 2 корабля на 2 клетки\n- 4 корабля на 1 клетку\n"
msg += "Итак, приступим. Для начала надо разместить корабли на поле боя. Для размещения вручную нажмите (1), " \
        "для автоматического - (2).\nИли введите 'q' для выхода из игры (и проигрыша).\n" \
        "Ходы обозначаются двумя цифрами подряд, например 12. Первая цифра - ряд, вторая - колонка.\n"
# msg = "Вспомним детство, поиграем в ""Морской бой""?\nПо умолчанию играем на поле 6 * 6. При желании выйти из игры (и проиграть)"
# print(msg)

def foo():
    return input("enter a number")

def bar(foo):
    if int(foo()) % 2 == 0:
        print("even!")

bar(foo)