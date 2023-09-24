import datetime


def tmstp_to_str(unix):
    return datetime.datetime.fromtimestamp(unix).strftime("%H:%M %d.%m.%Y")


