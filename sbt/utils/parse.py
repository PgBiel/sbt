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

__authors__      = [("shineydev", "contact@shiney.dev")]
__maintainers__  = [("shineydev", "contact@shiney.dev")]

__version_info__ = (1, 0, 0, "alpha", 0)
__version__      = "{0}.{1}.{2}{3}{4}".format(*[str(n)[0] if (i == 3) else str(n) for (i, n) in enumerate(__version_info__)])

__all__ = {
    "Color",
    "Date",
    "FutureDate",
    "PastDate",
    "Time",
    "FutureTime",
    "PastTime",
    "DateTime",
    "FutureDateTime",
    "PastDateTime",
    "Flag",
    "Flags",
    "RPS",
}


import datetime
import re
import struct

import discord
from discord.ext import commands

from utils import (
    error,
    regex,
)


def boolean(string: str):
    string = string.lower()

    true = ["yes", "y", "true", "t", "enable", "on", "1"]
    false = ["no", "n", "false", "f", "disable", "off", "0"]

    if (string in true):
        return True
    elif (string in false):
        return False
    
    raise error.ParserError(self, "couldn't parse bool from '{0}'".format(string))

def iso8601(string: str):
    match = re.fullmatch(regex.Regex.ISO8601, string)
    if (not match):
        raise error.ParserError(self, "invalid ISO8601 string '{0}'".format(string))

    year = int(match.group("year"))
    month = int(match.group("month"))
    day = int(match.group("day"))
    hour = int(match.group("hour"))
    minute = int(match.group("minute"))

    return datetime.datetime(year, month, day, hour, minute, 0)


class Color(commands.Converter):
    __all__ = {
        "convert",
        "parse",
        "cmyk_to_hexadecimal",
        "cmyk_to_rgb",
        "cmyk_to_int",
        "hexadecimal_to_cmyk",
        "hexadecimal_to_int",
        "hexadecimal_to_rgb",
        "int_to_cmyk",
        "int_to_hexadecimal",
        "int_to_rgb",
        "rgb_to_cmyk",
        "rgb_to_hexadecimal",
        "rgb_to_int",
    }

    async def convert(self, ctx: commands.Context, argument: str) -> tuple:
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

        match = re.fullmatch(regex.Regex.HEXADECIMAL, argument)
        if (match):
            # 000
            # #000
            # 0x000
            # 000000
            # #000000
            # 0x000000

            if (argument.startswith("0X")):
                argument = argument[2:]
            elif (argument.startswith("#")):
                argument = argument[1:]

            if (len(argument) == 3):
                argument = "".join(i * 2 for i in argument)
                
            int_ = self.hexadecimal_to_int(argument)
            rgb = self.hexadecimal_to_rgb(argument)
            cmyk = self.rgb_to_cmyk(*rgb)

            return (int_, argument, rgb, cmyk)

        match = re.fullmatch(regex.Regex.RGB, argument)
        if (match):
            # 000,000,000
            # 000, 000, 000
            # (000,000,000)
            # (000, 000, 000)

            r = int(match.group("r"))
            g = int(match.group("g"))
            b = int(match.group("b"))

            if (r > 255):
                raise error.ParserError(self, "red out of range '{0}'".format(r))
            elif (g > 255):
                raise error.ParserError(self, "green out of range '{0}'".format(g))
            elif (b > 255):
                raise error.ParserError(self, "blue out of range '{0}'".format(b))

            hexadecimal = self.rgb_to_hexadecimal(r, g, b)
            int_ = self.hexadecimal_to_int(hexadecimal)
            cmyk = self.rgb_to_cmyk(r, g, b)

            return (int_, hexadecimal, (r, g, b), cmyk)

        match = re.fullmatch(regex.Regex.CMYK, argument)
        if (match):
            # 000,000,000,000
            # 000, 000, 000, 000
            # (000,000,000,000)
            # (000, 000, 000, 000)

            c = int(match.group("c"))
            m = int(match.group("m"))
            y = int(match.group("y"))
            k = int(match.group("k"))

            if (c > 255):
                raise error.ParserError(self, "cyan is out of range '{0}'".format(c))
            elif (m > 255):
                raise error.ParserError(self, "magenta out of range '{0}'".format(m))
            elif (y > 255):
                raise error.ParserError(self, "yellow out of range '{0}'".format(y))
            elif (k > 255):
                raise error.ParserError(self, "key out of range '{0}'".format(k))

            rgb = self.cmyk_to_rgb(c, m, y, k)
            hexadecimal = self.rgb_to_hexadecimal(*rgb)
            int_ = self.hexadecimal_to_int(hexadecimal)

            return (int_, hexadecimal, rgb, (c, m, y, k))

        match = re.fullmatch(regex.Regex.DIGITS, argument)
        if (match):
            int_ = int(match.group("digits"))

            try:
                hexadecimal = self.int_to_hexadecimal(int_)
            except (ValueError) as e:
                raise error.ParserError(self, "integer '{0}' too large to convert to hexadecimal".format(argument))

            rgb = self.hexadecimal_to_rgb(hexadecimal)
            cmyk = self.rgb_to_cmyk(*rgb)

            return (int_, hexadecimal, rgb, cmyk)

        raise error.ParserError(self, "couldn't parse color from '{0}'".format(argument))

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
        hexadecimal = "{0:06X}".format(int_)
        
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
    __all__ = {
        "convert",
        "parse",
    }

    async def convert(self, ctx: commands.Context, argument: str) -> datetime.date:
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

        match = re.fullmatch(regex.Regex.US_DATE, argument)
        if (match):
            # 12/31/00
            # 12/31/0000
            # 12-31-00
            # 12-31-0000
            # on 12/31/00
            # on 12/31/0000
            # on 12-31-00
            # on 12-31-0000
            # until 12/31/00
            # until 12/31/0000
            # until 12-31-00
            # until 12-31-0000

            month = int(match.group("month"))
            day = int(match.group("day"))

            year = match.group("year")
            if (len(year) == 2):
                year = str(self.now.year)[:2] + year

            year = int(year)

            if (not year):
                raise error.ParserError(self, "year '{0}' is out of range".format(year))

            try:
                return datetime.date(year, month, day)
            except (ValueError) as e:
                raise error.ParserError(self, "day '{0}' is out of range".format(day))

        match = re.fullmatch(regex.Regex.EU_DATE, argument)
        if (match):
            # 31/12/00
            # 31/12/0000
            # 31-12-00
            # 31-12-0000
            # on 31/12/00
            # on 31/12/0000
            # on 31-12-00
            # on 31-12-0000
            # until 31/12/00
            # until 31/12/0000
            # until 31-12-00
            # until 31-12-0000

            day = int(match.group("day"))
            month = int(match.group("month"))

            year = match.group("year")
            if (len(year) == 2):
                year = str(self.now.year)[:2] + year

            year = int(year)

            if (not year):
                raise error.ParserError(self, "year '{0}' is out of range".format(year))

            try:
                return datetime.date(year, month, day)
            except (ValueError) as e:
                raise error.ParserError(self, "day '{0}' is out of range".format(day))

        match = re.fullmatch(regex.Regex.DAYS, argument)
        if (match):
            # 1d
            # in 1d
            # for 1d
            # 1 day
            # in 1 day
            # for 1 day
            # 2 days
            # in 2 days
            # for 2 days

            days = int(match.group(days))
            if (days):
                new = self.now + datetime.timedelta(days=days)
                return datetime.date(new.year, new.month, new.day)

        raise error.ParserError(self, "couldn't parse date from '{0}'".format(argument))

class FutureDate(Date, commands.Converter):
    __all__ = {
        "convert",
        "parse",
    }

    async def convert(self, ctx: commands.Context, argument: str) -> datetime.date:
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
            raise error.ParserError(self, "date is not in the future")

        return result

class PastDate(Date, commands.Converter):
    __all__ = {
        "convert",
        "parse",
    }

    async def convert(self, ctx: commands.Context, argument: str) -> datetime.date:
        """
        used as a command converter by dpy
        """

        return self.parse(argument)
        
    @classmethod
    def parse(self, argument: str) -> datetime.date:
        """
        calls super().parse() but raises if the date is not in the
        past
        """

        result = super().parse(argument)

        now = datetime.date(self.now.year, self.now.month, self.now.day)
        if (result >= now):
            raise error.ParserError(self, "date is not in the past")

        return result
                
class Time(commands.Converter):
    __all__ = {
        "convert",
        "parse",
    }

    async def convert(self, ctx: commands.Context, argument: str) -> datetime.time:
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
        
        match = re.fullmatch(regex.Regex.DIGITS, argument)
        if (match):
            # 0+

            minutes = int(match.group("digits"))
            if (minutes):
                new = self.now + datetime.timedelta(minutes=minutes)
                return datetime.time(new.hour, new.minute, new.second)

        match = re.fullmatch(regex.Regex.HOUR, argument)
        if (match):
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
            # until 0
            # until 0am
            # until 0 am
            # until 0pm
            # until 0 pm
            # until 00
            # until 00am
            # until 00 am
            # until 00pm
            # until 00 pm

            hour = int(match.group("hour"))

            meridies = match.group("meridies")
            if (meridies == "pm"):
                hour += 12

            if (hour not in range(0, 24)):
                raise error.ParserError(self, "hour '{0}' is out of range".format(hour))

            return datetime.time(hour, 0, 0)

        match = re.fullmatch(regex.Regex.TODAY_AT_HOUR, argument)
        if (match):
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
            # until today at 0
            # until today at 0am
            # until today at 0 am
            # until today at 0pm
            # until today at 0 pm
            # until today at 00
            # until today at 00am
            # until today at 00 am
            # until today at 00pm
            # until today at 00 pm

            hour = int(match.group("hour"))

            meridies = match.group("meridies")
            if (meridies == "pm"):
                hour += 12

            if (hour not in range(0, 24)):
                raise error.ParserError(self, "hour '{0}' is out of range".format(hour))

            return datetime.time(hour, 0, 0)

        match = re.fullmatch(regex.Regex.TIME, argument)
        if (match):
            # 00:00
            # 00:00:00
            # at 00:00
            # at 00:00:00
            # until 00:00
            # until 00:00:00

            hour = int(match.group("hour"))
            minute = int(match.group("minute"))

            second = match.group("second")
            if (second):
                second = int(second)
            else:
                second = 0

            return datetime.time(hour, minute, second)

        match = re.fullmatch(regex.Regex.TODAY_AT_TIME, argument)
        if (match):
            # today at 00:00
            # today at 00:00:00
            # until today at 00:00
            # until today at 00:00:00

            hour = int(match.group("hour"))
            minute = int(match.group("minute"))

            second = match.group("second")
            if (second):
                second = int(second)
            else:
                second = 0

            return datetime.time(hour, minute, second)

        raise error.ParserError(self, "couldn't parse time from '{0}'".format(argument))

class FutureTime(Time, commands.Converter):
    __all__ = {
        "convert",
        "parse",
    }

    async def convert(self, ctx: commands.Context, argument: str) -> datetime.time:
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
            raise error.ParserError(self, "time is not in the future")

        return result

class PastTime(Time, commands.Converter):
    __all__ = {
        "convert",
        "parse",
    }

    async def convert(self, ctx: commands.Context, argument: str) -> datetime.time:
        """
        used as a command converter by dpy
        """

        return self.parse(argument)

    @classmethod
    def parse(self, argument: str) -> datetime.time:
        """
        calls super().parse() but raises if the time is not in the
        past
        """

        result = super().parse(argument)

        now = datetime.time(self.now.hour, self.now.minute, self.now.second)
        if (result >= now):
            raise error.ParserError(self, "time is not in the past")

        return result

class DateTime(commands.Converter):
    __all__ = {
        "convert",
        "parse",
    }

    async def convert(self, ctx: commands.Context, argument: str) -> datetime.datetime:
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
        
        try:
            date = Date.parse(argument)
            return datetime.datetime(date.year, date.month, date.day, 0, 0, 0)
        except (error.ParserError) as e:
            pass

        try:
            time = Time.parse(argument)
            return datetime.datetime(self.now.year, self.now.month, self.now.day, time.hour, time.minute, time.second)
        except (error.ParserError) as e:
            pass

        match = re.fullmatch(regex.Regex.TOMORROW_AT_HOUR, argument)
        if (match):
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
            # until tomorrow at 0
            # until tomorrow at 0am
            # until tomorrow at 0 am
            # until tomorrow at 0pm
            # until tomorrow at 0 pm
            # until tomorrow at 00
            # until tomorrow at 00am
            # until tomorrow at 00 am
            # until tomorrow at 00pm
            # until tomorrow at 00 pm

            hour = int(match.group("hour"))

            meridies = match.group("meridies")
            if (meridies == "pm"):
                hour += 12

            if (hour not in range(0, 24)):
                raise error.ParserError(self, "hour '{0}' is out of range".format(hour))

            tomorrow = self.now + datetime.timedelta(days=1)
            return datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, hour, 0, 0)

        match = re.fullmatch(regex.Regex.TOMORROW_AT_TIME, argument)
        if (match):
            # tomorrow at 00:00
            # tomorrow at 00:00:00
            # until tomorrow at 00:00
            # until tomorrow at 00:00:00

            hour = int(match.group("hour"))
            minute = int(match.group("minute"))

            second = match.group("second")
            if (second):
                second = int(second)
            else:
                second = 0
                
            tomorrow = self.now + datetime.timedelta(days=1)
            return datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, hour, minute, second)

        match = re.fullmatch(regex.Regex.US_DATE_TIME, argument)
        if (match):
            # 12/31/00 00:00
            # 12/31/00 at 00:00
            # 12/31/00 00:00:00
            # 12/31/00 at 00:00:00
            # 12/31/0000 00:00
            # 12/31/0000 at 00:00
            # 12/31/0000 00:00:00
            # 12/31/0000 at 00:00:00
            # 12-31-00 00:00
            # 12-31-00 at 00:00
            # 12-31-00 00:00:00
            # 12-31-00 at 00:00:00
            # 12-31-0000 00:00
            # 12-31-0000 at 00:00
            # 12-31-0000 00:00:00
            # 12-31-0000 at 00:00:00
            # on 12/31/00 00:00
            # on 12/31/00 at 00:00
            # on 12/31/00 00:00:00
            # on 12/31/00 at 00:00:00
            # on 12/31/0000 00:00
            # on 12/31/0000 at 00:00
            # on 12/31/0000 00:00:00
            # on 12/31/0000 at 00:00:00
            # on 12-31-00 00:00
            # on 12-31-00 at 00:00
            # on 12-31-00 00:00:00
            # on 12-31-00 at 00:00:00
            # on 12-31-0000 00:00
            # on 12-31-0000 at 00:00
            # on 12-31-0000 00:00:00
            # on 12-31-0000 at 00:00:00
            # until 12/31/00 00:00
            # until 12/31/00 at 00:00
            # until 12/31/00 00:00:00
            # until 12/31/00 at 00:00:00
            # until 12/31/0000 00:00
            # until 12/31/0000 at 00:00
            # until 12/31/0000 00:00:00
            # until 12/31/0000 at 00:00:00
            # until 12-31-00 00:00
            # until 12-31-00 at 00:00
            # until 12-31-00 00:00:00
            # until 12-31-00 at 00:00:00
            # until 12-31-0000 00:00
            # until 12-31-0000 at 00:00
            # until 12-31-0000 00:00:00
            # until 12-31-0000 at 00:00:00

            month = int(match.group("month"))
            day = int(match.group("day"))

            year = match.group("year")
            if (len(year) == 2):
                year = str(self.now.year)[:2] + year

            year = int(year)

            hour = int(match.group("hour"))
            minute = int(match.group("minute"))

            second = match.group("second")
            if (second):
                second = int(second)
            else:
                second = 0
                
            return datetime.datetime(year, month, day, hour, minute, second)

        match = re.fullmatch(regex.Regex.EU_DATE_TIME, argument)
        if (match):
            # 31/12/00 00:00
            # 31/12/00 at 00:00
            # 31/12/00 00:00:00
            # 31/12/00 at 00:00:00
            # 31/12/0000 00:00
            # 31/12/0000 at 00:00
            # 31/12/0000 00:00:00
            # 31/12/0000 at 00:00:00
            # 31-12-00 00:00
            # 31-12-00 at 00:00
            # 31-12-00 00:00:00
            # 31-12-00 at 00:00:00
            # 31-12-0000 00:00
            # 31-12-0000 at 00:00
            # 31-12-0000 00:00:00
            # 31-12-0000 at 00:00:00
            # on 31/12/00 00:00
            # on 31/12/00 at 00:00
            # on 31/12/00 00:00:00
            # on 31/12/00 at 00:00:00
            # on 31/12/0000 00:00
            # on 31/12/0000 at 00:00
            # on 31/12/0000 00:00:00
            # on 31/12/0000 at 00:00:00
            # on 31-12-00 00:00
            # on 31-12-00 at 00:00
            # on 31-12-00 00:00:00
            # on 31-12-00 at 00:00:00
            # on 31-12-0000 00:00
            # on 31-12-0000 at 00:00
            # on 31-12-0000 00:00:00
            # on 31-12-0000 at 00:00:00
            # until 31/12/00 00:00
            # until 31/12/00 at 00:00
            # until 31/12/00 00:00:00
            # until 31/12/00 at 00:00:00
            # until 31/12/0000 00:00
            # until 31/12/0000 at 00:00
            # until 31/12/0000 00:00:00
            # until 31/12/0000 at 00:00:00
            # until 31-12-00 00:00
            # until 31-12-00 at 00:00
            # until 31-12-00 00:00:00
            # until 31-12-00 at 00:00:00
            # until 31-12-0000 00:00
            # until 31-12-0000 at 00:00
            # until 31-12-0000 00:00:00
            # until 31-12-0000 at 00:00:00

            day = int(match.group("day"))
            month = int(match.group("month"))

            year = match.group("year")
            if (len(year) == 2):
                year = str(self.now.year)[:2] + year

            year = int(year)

            hour = int(match.group("hour"))
            minute = int(match.group("minute"))

            second = match.group("second")
            if (second):
                second = int(second)
            else:
                second = 0
                
            return datetime.datetime(year, month, day, hour, minute, second)

        match = re.fullmatch(regex.Regex.ANY_HUMANIZED_TIME, argument)
        if (match):
            new = datetime.timedelta()

            seconds = match.group("seconds")
            if (seconds):
                seconds = int(seconds)
                if (seconds):
                    new += datetime.timedelta(seconds=seconds)

            minutes = match.group("minutes")
            if (minutes):
                minutes = int(minutes)
                if (minutes):
                    new += datetime.timedelta(minutes=minutes)

            hours = match.group("hours")
            if (hours):
                hours = int(hours)
                if (hours):
                    new += datetime.timedelta(hours=hours)

            days = match.group("days")
            if (days):
                days = int(days)
                if (days):
                    new += datetime.timedelta(days=days)

            weeks = match.group("weeks")
            if (weeks):
                weeks = int(weeks)
                if (weeks):
                    new += datetime.timedelta(weeks=weeks)

            if (new > datetime.timedelta()):
                return self.now + new

        raise error.ParserError(self, "couldn't parse datetime from '{0}'".format(argument))

class FutureDateTime(DateTime, commands.Converter):
    __all__ = {
        "convert",
        "parse",
    }

    async def convert(self, ctx: commands.Context, argument: str) -> datetime.datetime:
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
            raise error.ParserError(self, "datetime is not in the future")

        return result

class PastDateTime(DateTime, commands.Converter):
    __all__ = {
        "convert",
        "parse",
    }

    async def convert(self, ctx: commands.Context, argument: str) -> datetime.datetime:
        """
        used as a command converter by dpy
        """

        return self.parse(argument)
        
    @classmethod
    def parse(self, argument: str) -> datetime.datetime:
        """
        calls super().parse() but raises if the datetime is not in the
        past
        """

        result = super().parse(argument)

        if (result >= self.now):
            raise error.ParserError(self, "datetime is not in the past")

        return result

class Flag():
    __all__ = {
        "__init__",
    }

    def __init__(self, name: str, *, required: bool = False, value: bool = False, value_type: type = None, converter: commands.Converter = None):
        self.name = name
        self.required = required
        self.value = value
        self.value_type = value_type
        self.converter = converter

class Flags(commands.Converter):
    __all__ = {
        "convert",
        "parse",
        "resolve",
    }

    async def convert(self, ctx: commands.Context, argument: str):
        """
        used as a command converter by dpy
        """

        return self.parse(argument)

    @classmethod
    def parse(cls, argument: str):
        """
        this method simply splits up the tokens and returns cls for
        the `resolve` method to resolve
        """

        cls.tokens = dict()

        for (token) in argument.split(" "):
            match = re.fullmatch(regex.Regex.FLAG_TOKEN, token)
            if (not match):
                raise error.ParserError(self, "invalid token '{0}'".format(token))

            flag = match.group("flag")
            value = match.group("value")

            if (flag in cls.tokens.keys()):
                raise error.ParserError(self, "duplicate token '{0}'".format(token))

            if (value):
                cls.tokens[flag] = value
            else:
                cls.tokens[flag] = None

        return cls

    @classmethod
    async def resolve(self, ctx: commands.Context, flags: list) -> dict:
        dict_ = dict()

        for (flag) in flags:
            if (flag.required):
                if (flag.name not in self.tokens.keys()):
                    raise error.ParserError(self, "missing required flag '{0}'".format(flag.name))

            if (flag.value):
                if (flag.name in self.tokens.keys()):
                    if (not self.tokens[flag.name]):
                        raise error.ParserError(self, "missing value for flag '{0}'".format(flag.name))
            else:
                if (flag.name in self.tokens.keys()):
                    if (self.tokens[flag.name]):
                        raise error.ParserError(self, "was given an extraneous value for flag '{0}'".format(flag.name))

            if (flag.name in self.tokens.keys()):
                value = self.tokens[flag.name]

                if (flag.value_type):
                    try:
                        value = flag.value_type(value)
                    except (Exception) as e:
                        raise error.ParserError(self, "failed to convert value '{0}' to {1}".format(value, flag.value_type))
                elif (flag.converter):
                    try:
                        value = await flag.converter().convert(ctx, value)
                    except (Exception) as e:
                        raise error.ParserError(self, "failed to convert value '{0}' to {1}".format(value, flag.converter))
                else:
                    value = True

                dict_[flag.name] = value
            else:
                dict_[flag.name] = None
                
        return dict_
        
class RPS():
    __all__ = {
        "__init__",
    }

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