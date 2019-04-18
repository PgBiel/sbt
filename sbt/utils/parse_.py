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

import discord
from discord.ext import commands

from utils import (
    regex,
)


class Date():
    def __init__(self, argument: str = None):
        """
        only command typehints should invoke here with arguments
        since it will raise if it doesn't find anything.
        """

        if (argument):
            self.result = self.parse(argument)
            if (not self.result):
                raise commands.BadArgument(argument)
            
    @classmethod
    def parse(self, argument: str = None):
        """
        parses humanized datetime and returns a timezone naive
        datetime.date object or None
        """

        self.now = datetime.datetime.utcnow()
        result = None

        if (match := re.fullmatch(regex.Regex.US_DATE, argument)):
            # 12/31/00
            # 12/31/0000
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
        elif (match := re.fullmatch(regex.Regex.DAYS)):
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

        return result

class FutureDate(Date):
    def __init__(self, argument: str = None):
        """
        only command typehints should invoke here with arguments
        since it will raise if it doesn't find anything.
        """

        super().__init__(argument)
        
    @classmethod
    def parse(self, argument: str = None):
        """
        calls super().parse() but raises if the date is not in the
        future
        """

        result = super().parse(argument)

        if (not result):
            raise commands.BadArgument(argument)

        now = datetime.date(self.now.year, self.now.month, self.now.day)
        if (result <= now):
            raise commands.BadArgument("date is not in the future")

        return result
                
class Time():
    def __init__(self, argument: str = None):
        """
        only command typehints should invoke here with arguments
        since it will raise if it doesn't find anything.
        """

        if (argument):
            self.result = self.parse(argument)
            if (not self.result):
                raise commands.BadArgument(argument)
            
    @classmethod
    def parse(self, argument: str = None):
        """
        parses humanized datetime and returns a timezone naive
        datetime.time object or None
        """

        self.now = datetime.datetime.utcnow()
        result = None

        if (match := re.fullmatch(regex.Regex.HOUR, argument)):
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
        elif (match := re.fullmatch(regex.Regex.DIGITS, argument)):
            # 0+

            minutes = int(match.group(digits))
            if (minutes):
                new = self.now + datetime.timedelta(minutes=minutes)
                result = datetime.time(new.hour, new.minute, new.second)

        return result

class FutureTime(Time):
    def __init__(self, argument: str = None):
        """
        only command typehints should invoke here with arguments
        since it will raise if it doesn't find anything.
        """

        super().__init__(argument)

    @classmethod
    def parse(self, argument: str = None):
        """
        calls super().parse() but raises if the time is not in the
        future
        """

        result = super().parse(argument)

        if (not result):
            raise commands.BadArgument(argument)

        now = datetime.time(self.now.hour, self.now.minute, self.now.second)
        if (result <= now):
            raise commands.BadArgument("time is not in the future")

        return result

class DateTime():
    def __init__(self, argument: str = None):
        """
        only command typehints should invoke here with arguments
        since it will raise if it doesn't find anything.
        """

        if (argument):
            self.result = self.parse(argument)
            if (not self.result):
                raise commands.BadArgument(argument)
            
    @classmethod
    def parse(self, argument: str = None):
        """
        parses humanized datetime and returns a timezone naive
        datetime.datetime object or None
        """

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

        return result

class FutureDateTime(DateTime):
    def __init__(self, argument: str = None):
        """
        only command typehints should invoke here with arguments
        since it will raise if it doesn't find anything.
        """

        super().__init__(argument)
        
    @classmethod
    def parse(self, argument: str = None):
        """
        calls super().parse() but raises if the datetime is not in the
        future
        """

        result = super().parse(argument)

        if (not result):
            raise commands.BadArgument(argument)

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