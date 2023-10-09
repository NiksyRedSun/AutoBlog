import random


def badlang(lenght):
    marks = '@#$%&?№*'
    res = ""
    for i in range(lenght):
        res += random.choice(marks)
    return res



def badlang_correct(text):
    mat = ["хуй", "пизда", "сука", "блять", "блядь"]
    for word in mat:
        text = text.replace(word, badlang(len(word)))
    return text


def in_web_presentation(self):

    def make_short_string(string: str, long: int):
        result = ' '
        word_list = string.split()
        count = 0
        for i in word_list:
            if count + len(i) > long:
                result += '\n '
                count = 0
            result += i + " "
            count += len(i)
        return result

    pres_name = "+" + self.name.center(22, "-") + "+"
    pres_level = "+" + ("Уровень: " + str(self.level)).center(22, "-") + "+"
    text = [
        f"{pres_name}",
        make_short_string(self.story, 26),
        f"",
        f" Здоровье: ".ljust(20) + f"{self.hp}/{self.max_hp}",
        f" Атака: ".ljust(20) + f"{self.attack}",
        f" Защита: ".ljust(20) + f"{self.defense}",
        f" Ловкость: ".ljust(20) + f"{self.initiative}",
        f" Золото: ".ljust(20) + f"{self.money}",
        f" Опыт: ".ljust(20) + f"{self.exp}/{self.next_level_exp}",
        f"",
        f"{pres_level}"
    ]
    return text



