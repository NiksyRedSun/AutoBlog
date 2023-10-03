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




