from itertools import zip_longest

# EMPTY = 'О'
EMPTY = " "
BODY = "■"
SUNKEN = "‡"
HIT = "†"  # '*' #"‡"
MISS = "-"
UNKNOWN = "?"
BUFFER = "·"
INP_INVITE = "\n?--> "
QUIT = ["Q", "q", "Й", "й", "quit", "QUIT"]
MOVE_DICT = {MISS: "мимо", HIT: "попал", SUNKEN: "подбит вражеский корабль длины "}


def to_lines_by_limit(string, limit=60):
    """Для форматирования: разбивает сплошной текст на строки с указанным
    лимитом знаков без переноса слов. Вероятно это была трата времени
    """
    output = ""
    while len(string) >= limit:
        string = string.strip()
        n = min(string.find("\n"), string[:limit].rfind(" "))
        if n == -1:
            n = max(string.find("\n"), string[:limit].rfind(" "))
        if n > 0:  # если пробел есть и не в начале строки
            head = string[:n].strip()
            string = string[n:]
        elif n < 0:
            raise ValueError(
                f"The limit '{limit}' is too small: the text can't be split"
            )
        else:  # если пробел в начале строки
            head = string[:limit]
            string = string[limit:]
        output += head + "\n"
    output += string.lstrip()
    return output


def print_side_by_side(str1, str2, divider="    |    "):
    """Для вывода рядом двух досок. Выводит попеременно строки из двух 
    строковых переменных с указанным разделением между ними"""
    s1 = str1.split("\n")
    s2 = str2.split("\n")

    lst = [len(elem) for elem in s1]
    nbr_spaces = max(lst)  # ищем самую длинную строку, чтобы выровнять остальные
    # clear_screen()
    for line1, line2 in zip_longest(s1, s2):
        line1, line2 = line1 or "", line2 or ""
        print(line1.ljust(nbr_spaces) + divider + line2)


def ai_to_user(mv):
    """Перевод на язык и формат пользовательских координат"""
    return f"{mv[0] + 1}{mv[1] + 1}"
