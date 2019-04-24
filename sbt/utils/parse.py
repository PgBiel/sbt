"""
/utils/parse.py

    Copyright (c) 2019 ShineyDev
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

__authors__           = [("shineydev", "contact@shiney.dev")]
__maintainers__       = [("shineydev", "contact@shiney.dev")]

__version_info__      = (2, 0, 0, "alpha", 0)
__version__           = "{0}.{1}.{2}{3}{4}".format(*[str(n)[0] if (i == 3) else str(n) for (i, n) in enumerate(__version_info__)])


import datetime
import re
import struct

import discord
from discord.ext import commands

from utils import (
    regex,
)


class Color(commands.Converter):
    async def convert(self, ctx, argument: str) -> tuple:
        """
        used as a command converter by dpy
        """

        return self.parse(argument)

    @classmethod
    def parse(self, argument: str) -> tuple:
        """
        parses hexadecimal or rgb/argb values and returns a
        tuple of (int, hex, rgb, cmyk)
        """

        argument = argument.upper()
        result = None

        if (match := re.fullmatch(regex.Regex.HEXADECIMAL, argument)):
            if (argument.startswith("0X")):
                argument = argument[2:]
            elif (argument.startswith("#")):
                argument = argument[1:]

            if (len(argument) in [3, 4]):
                argument = "".join(i * 2 for i in argument)

            if (len(argument) == 8):
                argument = argument[2:]
                
            int_ = self.hexadecimal_to_int(argument)
            rgb = self.hexadecimal_to_rgb(argument)
            cmyk = self.rgb_to_cmyk(*rgb)

            result = (int_, argument, rgb, cmyk)
        elif (match := re.fullmatch(regex.Regex.RGB, argument)):
            r = int(match.group("r"))
            g = int(match.group("g"))
            b = int(match.group("b"))
            
            if (any([(i > 255) for (i) in [r, g, b]])):
                raise commands.BadArgument(argument)

            hexadecimal = self.rgb_to_hexadecimal(r, g, b)
            int_ = self.hexadecimal_to_int(hexadecimal)
            cmyk = self.rgb_to_cmyk(r, g, b)

            result = (int_, hexadecimal, (r, g, b), cmyk)
        elif (match := re.fullmatch(regex.Regex.CMYK, argument)):
            c = int(match.group("c"))
            m = int(match.group("m"))
            y = int(match.group("y"))
            k = int(match.group("k"))

            if (any([(i > 100) for (i) in [c, m, y, k]])):
                raise commands.BadArgument(argument)

            rgb = self.cmyk_to_rgb(c, m, y, k)
            hexadecimal = self.rgb_to_hexadecimal(*rgb)
            int_ = self.hexadecimal_to_int(hexadecimal)

            result = (int_, hexadecimal, rgb, (c, m, y, k))
        elif (metch := re.fullmatch(regex.Regex.DIGITS, argument)):
            int_ = match.group("digits")

            try:
                hexadecimal = self.int_to_hexadecimal(int_)
            except (ValueError) as e:
                # integer was too large
                raise commands.BadArgument(argument)

            rgb = self.hexadecimal_to_rgb(hexadecimal)
            cmyk = self.rgb_to_cmyk(*rgb)

            result = (int_, hexadecimal, rgb, cmyk)

        if (not result):
            raise commands.BadArgument(argument)

        return result

    @classmethod
    def cmyk_to_hexadecimal(self, c: int, m: int, y: int, k: int) -> str:
        r, g, b = self.cmyk_to_rgb(c, m, y, k)
        return self.rgb_to_hexadecimal(r, g, b)

    @classmethod
    def cmyk_to_rgb(self, c: int, m: int, y: int, k: int) -> tuple:
        r = int(round(255 * (1 - c / 100) * (1 - k / 100)))
        g = int(round(255 * (1 - m / 100) * (1 - k / 100)))
        b = int(round(255 * (1 - y / 100) * (1 - k / 100)))

        return (r, g, b)

    @classmethod
    def cmyk_to_int(self, c: int, m: int, y: int, k: int):
        hexadecimal = self.cmyk_to_hexadecimal(c, m, y, k)
        return self.hexadecimal_to_int(hexadecimal)

    @classmethod
    def hexadecimal_to_cmyk(self, hexadecimal: str) -> tuple:
        r, g, b = self.hexadecimal_to_rgb(hexadecimal)
        return self.rgb_to_cmyk(r, g, b)
    
    @classmethod
    def hexadecimal_to_int(self, hexadecimal: str) -> int:
        return int(hexadecimal, 16)

    @classmethod
    def hexadecimal_to_rgb(self, hexadecimal: str) -> tuple:
        return struct.unpack("BBB", bytes.fromhex(hexadecimal))

    @classmethod
    def int_to_cmyk(self, int_: int) -> tuple:
        hexadecimal = self.int_to_hexadecimal(int_)
        return self.hexadecimal_to_cmyk(hexadecimal)
    
    @classmethod
    def int_to_hexadecimal(self, int_: int) -> str:
        hexadecimal = "{0:06X}".format(100)
        
        if (len(hexadecimal) != 6):
            raise ValueError("too big")

        return hexadecimal

    @classmethod
    def int_to_rgb(self, int_: int) -> tuple:
        hexadecimal = self.int_to_hexadecimal(int_)
        return self.hexadecimal_to_rgb(hexadecimal)

    @classmethod
    def rgb_to_cmyk(self, r: int, g: int, b: int) -> tuple:
        if ((r == 0) and (g == 0) and (b == 0)):
            return (0, 0, 0, 100)

        r = r / 255
        g = g / 255
        b = b / 255

        k = 1 - max(r, g, b)

        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)

        c = int(round(c * 100))
        m = int(round(m * 100))
        y = int(round(y * 100))
        k = int(round(k * 100))

        return (c, m, y, k)

    @classmethod
    def rgb_to_hexadecimal(self, r: int, g: int, b: int) -> str:
        return "{0:02X}{1:02X}{2:02X}".format(r, g, b)

    @classmethod
    def rgb_to_int(self, r: int, g: int, b: int) -> int:
        hexadecimal = self.rgb_to_hexadecimal(r, g, b)
        return self.hexadecimal_to_int(hexadecimal)

class Date(commands.Converter):
    async def convert(self, ctx, argument: str) -> datetime.date:
        """
        used as a command converter by dpy
        """

        return self.parse(argument)
            
    @classmethod
    def parse(self, argument: str) -> datetime.date:
        """
        parses humanized datetime and returns a timezone naive
        datetime.date object or None
        """
        
        argument = argument.lower()

        self.now = datetime.datetime.utcnow()
        result = None

        if (match := re.fullmatch(regex.Regex.US_DATE, argument)):
            # 12/31/00
            # 12/31/0000
            # 12-31-00
            # 12-31-0000
            month = int(match.group("month"))
            day = int(match.group("day"))


            if (len(year := match.group("year")) == 2):
                year = str(self.now.year)[:2] + year

            year = int(year)

            try:
                result = datetime.date(year, month, day)
            except (ValueError) as e:
                # year or day is out of range
                raise commands.BadArgument(argument)
        elif (match := re.fullmatch(regex.Regex.EU_DATE, argument)):
            # 31/12/00
            # 31/12/0000
            # 31-12-00
            # 31-12-0000
            day = int(match.group("day"))
            month = int(match.group("month"))

            if (len(year := match.group("year")) == 2):
                year = str(self.now.year)[:2] + year

            year = int(year)

            try:
                result = datetime.date(year, month, day)
            except (ValueError) as e:
                # year or day is out of range
                raise commands.BadArgument(argument)
        elif (argument == "today"):
            # today
            result = datetime.date(self.now.year, self.now.month, self.now.day)
        elif (argument == "tomorrow"):
            # tomorrow
            new = self.now + datetime.timedelta(days=1)
            result = datetime.date(new.year, new.month, new.day)
        elif (match := re.fullmatch(regex.Regex.DAYS, argument)):
            # 1d
            # in 1d
            # 1 day
            # in 1 day
            # 2 days
            # in 2 days
            days = int(match.group(days))
            if (days):
                new = self.now + datetime.timedelta(days=days)
                result = datetime.date(new.year, new.month, new.day)

        if (not result):
            raise commands.BadArgument(argument)

        return result

class FutureDate(Date, commands.Converter):
    async def convert(self, ctx, argument: str) -> datetime.date:
        """
        used as a command converter by dpy
        """

        return self.parse(argument)
        
    @classmethod
    def parse(self, argument: str) -> datetime.date:
        """
        calls super().parse() but raises if the date is not in the
        future
        """

        result = super().parse(argument)

        now = datetime.date(self.now.year, self.now.month, self.now.day)
        if (result <= now):
            raise commands.BadArgument("date is not in the future")

        return result
                
class Time(commands.Converter):
    async def convert(self, ctx, argument: str) -> datetime.time:
        """
        used as a command converter by dpy
        """

        return self.parse(argument)
            
    @classmethod
    def parse(self, argument: str) -> datetime.time:
        """
        parses humanized datetime and returns a timezone naive
        datetime.time object or None
        """
        
        argument = argument.lower()

        self.now = datetime.datetime.utcnow()
        result = None
        
        if (match := re.fullmatch(regex.Regex.DIGITS, argument)):
            # 0+

            minutes = int(match.group(digits))
            if (minutes):
                new = self.now + datetime.timedelta(minutes=minutes)
                result = datetime.time(new.hour, new.minute, new.second)
        elif (match := re.fullmatch(regex.Regex.HOUR, argument)):
            # 0
            # 0am
            # 0 am
            # 0pm
            # 0 pm
            # 00
            # 00am
            # 00 am
            # 00pm
            # 00 pm
            hour = int(match.group("hour"))

            if (meridies := match.group("meridies") == "pm"):
                hour += 12

            if (hour not in range(0, 24)):
                raise commands.BadArgument("invalid hour")

            result = datetime.time(hour, 0, 0)
        elif (match := re.fullmatch(regex.Regex.TIME, argument)):
            # 00:00
            # 00:00:00

            hour = int(match.group("hour"))
            minute = int(match.group("minute"))

            if (second := match.group("second")):
                second = int(second)
            else:
                second = 0

            result = datetime.time(hour, minute, second)
        elif (match := re.fullmatch(regex.Regex.AT_HOUR, argument)):
            # at 0
            # at 0am
            # at 0 am
            # at 0pm
            # at 0 pm
            # at 00
            # at 00am
            # at 00 am
            # at 00pm
            # at 00 pm
            hour = int(match.group("hour"))

            if ((meridies := match.group("meridies")) == "pm"):
                hour += 12

            if (hour not in range(0, 24)):
                raise commands.BadArgument("invalid hour")

            result = datetime.time(hour, 0, 0)
        elif (match := re.fullmatch(regex.Regex.AT_TIME, argument)):
            # at 00:00
            # at 00:00:00

            hour = int(match.group("hour"))
            minute = int(match.group("minute"))

            if (second := match.group("second")):
                second = int(second)
            else:
                second = 0

            result = datetime.time(hour, minute, second)
        elif (match := re.fullmatch(regex.Regex.TODAY_AT_HOUR, argument)):
            # today at 0
            # today at 0am
            # today at 0 am
            # today at 0pm
            # today at 0 pm
            # today at 00
            # today at 00am
            # today at 00 am
            # today at 00pm
            # today at 00 pm
            hour = int(match.group("hour"))

            if ((meridies := match.group("meridies")) == "pm"):
                hour += 12

            if (hour not in range(0, 24)):
                raise commands.BadArgument("invalid hour")

            result = datetime.time(hour, 0, 0)
        elif (match := re.fullmatch(regex.Regex.TODAY_AT_TIME, argument)):
            # today at 00:00
            # today at 00:00:00

            hour = int(match.group("hour"))
            minute = int(match.group("minute"))

            if (second := match.group("second")):
                second = int(second)
            else:
                second = 0

            result = datetime.time(hour, minute, second)

        if (not result):
            raise commands.BadArgument(argument)

        return result

class FutureTime(Time, commands.Converter):
    async def convert(self, ctx, argument: str) -> datetime.time:
        """
        used as a command converter by dpy
        """

        return self.parse(argument)

    @classmethod
    def parse(self, argument: str) -> datetime.time:
        """
        calls super().parse() but raises if the time is not in the
        future
        """

        result = super().parse(argument)

        now = datetime.time(self.now.hour, self.now.minute, self.now.second)
        if (result <= now):
            raise commands.BadArgument("time is not in the future")

        return result

class DateTime(commands.Converter):
    async def convert(self, ctx, argument: str) -> datetime.datetime:
        """
        used as a command converter by dpy
        """

        return self.parse(argument)
            
    @classmethod
    def parse(self, argument: str) -> datetime.datetime:
        """
        parses humanized datetime and returns a timezone naive
        datetime.datetime object or None
        """
        
        argument = argument.lower()

        self.now = datetime.datetime.utcnow()
        result = None
        
        if (date := Date.parse(argument)):
            result = datetime.datetime(date.year, date.month, date.day, 0, 0, 0)
        elif (time := Time.parse(argument)):
            result = datetime.datetime(self.now.year, self.now.month, self.now.day, time.hour, time.minute, time.second)
        elif (match := re.fullmatch(regex.Regex.TOMORROW_AT_HOUR, argument)):
            # tomorrow at 0
            # tomorrow at 0am
            # tomorrow at 0 am
            # tomorrow at 0pm
            # tomorrow at 0 pm
            # tomorrow at 00
            # tomorrow at 00am
            # tomorrow at 00 am
            # tomorrow at 00pm
            # tomorrow at 00 pm
            hour = int(match.group("hour"))

            if ((meridies := match.group("meridies")) == "pm"):
                hour += 12

            if (hour not in range(0, 24)):
                raise commands.BadArgument("invalid hour")

            new = self.now + datetime.timedelta(days=1)
            result = datetime.datetime(new.year, new.month, new.day, hour, 0, 0)
        elif (match := re.fullmatch(regex.Regex.TOMORROW_AT_TIME, argument)):
            # tomorrow at 00:00
            # tomorrow at 00:00:00
            hour = int(match.group("hour"))
            minute = int(match.group("minute"))

            if (second := match.group("second")):
                second = int(second)
            else:
                second = 0
                
            new = self.now + datetime.timedelta(days=1)
            result = datetime.datetime(new.year, new.month, new.day, hour, minute, second)
        elif (match := re.fullmatch(regex.Regex.US_DATE_TIME, argument)):
            # 12/31/00 00:00
            # 12/31/00 00:00:00
            # 12/31/0000 00:00
            # 12/31/0000 00:00:00
            # 12-31-00 00:00
            # 12-31-00 00:00:00
            # 12-31-0000 00:00
            # 12-31-0000 00:00:00
            month = int(match.group("month"))
            day = int(match.group("day"))

            if (len(year := match.group("year")) == 2):
                year = str(self.now.year)[:2] + year

            year = int(year)

            hour = int(match.group("hour"))
            minute = int(match.group("minute"))

            if (second := match.group("second")):
                second = int(second)
            else:
                second = 0
                
            result = datetime.datetime(year, month, day, hour, minute, second)
        elif (match := re.fullmatch(regex.Regex.EU_DATE_TIME, argument)):
            # 31/12/00 00:00
            # 31/12/00 00:00:00
            # 31/12/0000 00:00
            # 31/12/0000 00:00:00
            # 31-12-00 00:00
            # 31-12-00 00:00:00
            # 31-12-0000 00:00
            # 31-12-0000 00:00:00
            day = int(match.group("day"))
            month = int(match.group("month"))

            if (len(year := match.group("year")) == 2):
                year = str(self.now.year)[:2] + year

            year = int(year)

            hour = int(match.group("hour"))
            minute = int(match.group("minute"))

            if (second := match.group("second")):
                second = int(second)
            else:
                second = 0
                
            result = datetime.datetime(year, month, day, hour, minute, second)
        elif (match := re.fullmatch(regex.Regex.ANY_HUMANIZED_TIME, argument)):
            new = datetime.timedelta()

            if (seconds := match.group("seconds")):
                if (seconds := int(seconds)):
                    new += datetime.timedelta(seconds=seconds)

            if (minutes := match.group("minutes")):
                if (minutes := int(minutes)):
                    new += datetime.timedelta(minutes=minutes)

            if (hours := match.group("hours")):
                if (hours := int(hours)):
                    new += datetime.timedelta(hours=hours)

            if (days := match.group("days")):
                if (days := int(days)):
                    new += datetime.timedelta(days=days)

            if (weeks := match.group("weeks")):
                if (weeks := int(weeks)):
                    new += datetime.timedelta(weeks=weeks)

            if (new > datetime.timedelta()):
                result = self.now + new

        if (not result):
            raise commands.BadArgument(argument)

        return result

class FutureDateTime(DateTime, commands.Converter):
    async def convert(self, ctx, argument: str) -> datetime.datetime:
        """
        used as a command converter by dpy
        """

        return self.parse(argument)
        
    @classmethod
    def parse(self, argument: str) -> datetime.datetime:
        """
        calls super().parse() but raises if the datetime is not in the
        future
        """

        result = super().parse(argument)

        if (result <= self.now):
            raise commands.BadArgument("datetime is not in the future")

        return result
        
class RPS():
    def __init__(self, argument: str):
        argument = argument.lower()

        if (argument in ["rock", "r", "\U0001f5ff", "\U0000270a"]):
            self.choice = "r"
        elif (argument in ["paper", "p", "\U0001f4c4", "\U0001f590"]):
            self.choice = "p"
        elif (argument in ["scissors", "s", "\U00002702", "\U0000270c"]):
            self.choice = "s"

        if (not hasattr(self, "choice")):
            raise commands.BadArgument()