# Jerrin Shirks

# native imports
import math
import json



def formatYoutubeDebugInfo(text, fps) -> str:
    try:
        value = float(json.loads(text)['cmt']) + 1 / (fps * 10)
        value = float("%.3f" % value)
        value = math.floor(value * fps) / fps
        value = "%.3f" % value
        return value, True
    except:
        return text, False




def formatToTime(value: float = 0, fps: int = 30):
    if isinstance(value, str):
        value = float(value)
    isNegative = value < 0
    value = abs(value)
    # rounds num to the nearest frame (if useFPS is on)

    value += 0.001
    value = value - (value % 1) % (1 / fps)
    # create all the components
    milli = ".{:0>3d}".format(int(round(value % 1, 3) * 1000))
    seconds = int(value % 60)
    minutes = int((value / 60) % 60)
    hours = int((value / 3600) % 24)
    days = int((value / 86400) % 7)
    weeks = int((value / 604800))
    # new formatting technique
    formattedTime = ""
    if weeks != 0:
        formattedTime += f"{weeks}w "
    if days != 0:
        formattedTime += f"{days}d "
    if hours != 0:
        formattedTime += str(hours) + ":"
        formattedTime += "{:0>2d}".format(minutes) + ":"
    else:
        formattedTime += str(minutes) + ":"
    # add seconds
    formattedTime += "{:0>2d}".format(seconds)
    if milli != ".000":
        formattedTime += milli
    # re-add the "-" if the num was originally neg.
    if isNegative:
        formattedTime = "–" + formattedTime
    return formattedTime



