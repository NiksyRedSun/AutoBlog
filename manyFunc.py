import datetime, random


def tmstp_to_str(unix):
    return datetime.datetime.fromtimestamp(unix).strftime("%H:%M %d.%m.%Y")


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




