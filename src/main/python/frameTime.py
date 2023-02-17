# Jerrin Shirks

# native imports
import json
from json import JSONDecodeError


class FrameTime:
    def __init__(self, time: int = 0, fps: int = 30):
        self.time: int = time
        self.fps: int = fps
        self.backup_milliseconds: int = time
        self.milliseconds: int = time

        self.timeStart: int = float("inf")
        self.timeEnd: int = 0


    def setStartAndEnd(self, timeStart: int, timeEnd: int):
        self.timeStart = timeStart
        self.timeEnd = timeEnd


    def updateFPS(self, fps: int = 30):
        if fps != self.fps:
            self.fps = fps
            self.renew()


    def renew(self) -> None:
        self.milliseconds = self.backup_milliseconds
        self._round_milliseconds()


    def _round_milliseconds(self):
        self.upper = self.milliseconds - self.milliseconds % 1000

        milli = self.milliseconds / 1000 + 0.001
        milli = milli - (milli % 1) % (1 / self.fps)
        milli = int(round(milli % 1, 3) * 1000)
        # milli -= (milli % (1000 / self.fps))
        self.milliseconds = self.upper + milli


    def roundValueMilliseconds(self, value):
        self.upper = value - value % 1000

        milli = value / 1000 + 0.001
        milli = milli - (milli % 1) % (1 / self.fps)
        milli = int(round(milli % 1, 3) * 1000)
        # milli -= (milli % (1000 / self.fps))
        value = self.upper + milli
        return value



    def setSeconds(self, seconds: int or float = 0) -> None:
        assert type(seconds) in [int, float]
        self.backup_milliseconds = int(seconds * 1000)
        self.renew()


    def setMilliseconds(self, milliseconds: int = 0.0) -> None:
        assert isinstance(milliseconds, int)
        self.backup_milliseconds = milliseconds
        self.renew()


    def setYoutubeDebugTime(self, dict_str: str) -> bool:
        try:
            seconds = float(json.loads(dict_str)['cmt'])
            self.setSeconds(seconds)
            return True
        except json.JSONDecodeError:
            return False


    @staticmethod
    def isValidTime(time_str: str,
                    allow_decimal: bool = True,
                    allow_negative: bool = True) -> bool:
        time_str = time_str.replace("–", "-")
        allowed_chars = " 0123456789:"
        if allow_negative:
            allowed_chars += "-"
            if "-" in time_str:
                if not time_str.startswith("-"):
                    return False
        if allow_decimal:
            allowed_chars += "."


        valid_1 = all(x in allowed_chars for x in time_str)
        valid_2 = time_str.count(".") < 2
        valid_3 = time_str.count("-") < 2
        return all([valid_1, valid_2, valid_3])


    @staticmethod
    def convertToSeconds(time_str: str, debug: bool = False) -> int:
        time_str = time_str.replace("–", "-")
        time_str = time_str.replace(" ", ":")

        is_negative = "-" in time_str

        if "." not in time_str:
            time_str += ".0"

        time_str = time_str.replace(".", ":")

        time_values = []
        times_split = time_str.split(":")
        for index, i in enumerate(times_split):
            if i in ["", "0"]:
                time_values.append(0)
            else:
                if index != len(times_split) - 1:
                    time_values.append(int(i))
                else:
                    time_values.append(int(i.ljust(3, "0")))

        time_values = [-i if is_negative else i for i in time_values]
        time_values = list(reversed(time_values))

        total_milli = 0

        times_to_milli = [1, 1000, 60000, 3600000, 86400000]  # milli|sec|min|hour|day

        for index, value in enumerate(time_values):

            total_milli += value * times_to_milli[index]
        # :sunglasses: we did it fam!!! :heart-emoji:
        return total_milli


    def setFromTimeString(self, time_str: str, debug: bool = False) -> None:
        milliseconds = self.convertToSeconds(time_str, debug)
        self.setMilliseconds(milliseconds)


    def getSign(self) -> bool:
        return self.milliseconds < 0



    def getTotalMilliseconds(self) -> int:
        milli = self.milliseconds
        return abs(milli)


    def getMillisecondsInt(self) -> int:
        milli = self.getTotalMilliseconds() % 1000
        return milli


    def getMillisecondsFloat(self) -> float:
        milli = self.getMillisecondsInt() / 1000
        return milli


    def getMilliseconds3Str(self) -> str:
        milli = self.getTotalMilliseconds() % 1000
        milli = str(milli).rjust(3, "0")
        return milli


    def getMilliseconds2Str(self) -> str:
        milli = self.getMilliseconds3Str()
        return milli[:2]


    def getMilliseconds1Str(self) -> str:
        milli = self.getMilliseconds3Str()
        return milli[:1]


    def getTotalSeconds(self) -> int:
        seconds = int(self.getTotalMilliseconds() / 1000)
        return seconds


    def getSecondsInt(self) -> int:
        seconds = self.getTotalSeconds() % 60
        return seconds


    def getSecondsStr(self) -> str:
        return str(self.getSecondsInt())


    def getPaddedSecondsStr(self) -> str:
        seconds = self.getSecondsStr()
        return seconds.rjust(2, "0")


    def getTotalMinutes(self) -> int:
        minutes = int(self.getTotalSeconds() / 60)
        return minutes


    def getMinutesInt(self) -> int:
        minutes = self.getTotalMinutes() % 60
        return minutes

    def getMinutesStr(self) -> str:
        return str(self.getMinutesInt())


    def getPaddedMinutesStr(self) -> str:
        minutes = self.getMinutesStr()
        return minutes.rjust(2, "0")


    def getTotalHours(self) -> int:
        hours = int(self.getTotalMinutes() / 60)
        return hours


    def getHoursInt(self) -> int:
        return self.getTotalHours()



    def getHoursStr(self) -> str:
        return str(self.getHoursInt())


    def getPaddedHoursStr(self) -> str:
        """no functionality"""
        pass


    def getTimeSections(self) -> tuple:
        hours: str = self.getHoursInt()
        minutes: str = self.getMinutesInt()
        seconds: str = self.getSecondsInt()
        milli: str = self.getMillisecondsInt()
        return hours, minutes, seconds, milli


    @staticmethod
    def isYTDebug(text):
        try:
            int(float(json.loads(text)['cmt']) * 1000)
            return True
        except:
            return False



    def YTDebugInfo(self, text) -> [str, bool]:
        value = int(float(json.loads(text)['cmt']) * 1000)
        self.setMilliseconds(value)



    def getTotalTime(self, rounded=True) -> str:
        time_str: str = ""
        hours, minutes, seconds, milli = self.getTimeSections()
        if self.getSign():
            time_str += "–"
        if hours:
            time_str += self.getHoursStr() + ":"
            time_str += self.getPaddedMinutesStr() + ":"
        else:
            time_str += self.getMinutesStr() + ":"
        time_str += self.getPaddedSecondsStr()
        if rounded:
            time_str += "." + self.getMilliseconds3Str()
        else:
            time_str += "." + str(abs(self.backup_milliseconds) % 1000).rjust(3, "0")
        return time_str


    def createModMessage(self,
                         message_str: str):
        self.updateFPS(self.fps)

        items = {
            "H": self.getHoursStr(),
            "M": self.getMinutesStr(),
            "S": self.getSecondsStr(),

            "MS": self.getMilliseconds3Str(),
            "2MS": self.getMilliseconds2Str(),
            "1MS": self.getMilliseconds1Str(),

            "PM": self.getPaddedMinutesStr(),
            "PS": self.getPaddedSecondsStr(),

            "TS": FrameTime(self.timeStart).getTotalTime(),
            "TE": FrameTime(self.timeEnd).getTotalTime(),

            "TT": self.getTotalTime(),

            "FPS": self.fps,
        }

        for key in items:
            value = items[key]
            if value is None:
                continue

            message_str = message_str.replace("{" + f"{key}" + "}", f"{value}")

        return message_str
