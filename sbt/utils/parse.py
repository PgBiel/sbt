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


class DateTime():
    """
    parses humanized datetime and returns a datetime.datetime object
    """

    def __init__(self, argument: str):
        argument = argument.lower()
        self.now = datetime.datetime.utcnow()

        if (argument.isdigit()):
            # default to minutes
            minutes = int(argument)
            if (minutes > 0):
                minutes = datetime.timedelta(minutes=minutes)
                self.timestamp = (self.now + minutes).timestamp()
        elif ("/" in argument):
            # 02/22/2020
            # 02/22/2020 11:30:30
            # 02/22/2020 11:30

            match = re.fullmatch(regex.Regex.US_DATE, argument)
            if (not match):
                match = re.fullmatch(regex.Regex.EU_DATE, argument)
                if (not match):
                    match = re.fullmatch(regex.Regex.US_DATE_TIME, argument)
                    if (not match):
                        match = re.fullmatch(regex.Regex.EU_DATE_TIME, argument)

            if (match):
                month = int(match.group("month"))
                day = int(match.group("day"))
                year = match.group("year")

                if (len(year) == 2):
                    year = str(self.now.year)[:2] + year

                year = int(year)

                if (year == 0):
                    raise commands.BadArgument()

                if (len(match.groups()) == 3):
                    try:
                        self.timestamp = datetime.datetime(year, month, day).timestamp()
                    except (ValueError) as e:
                        # day was out of range
                        raise commands.BadArgument()
                else:
                    hour = int(match.group("hour"))
                    minute = int(match.group("minute"))

                    if (match.group("second")):
                        second = int(match.group("second"))
                    else:
                        second = 0

                    if (hour not in range(0, 24)):
                        raise commands.BadArgument()

                    if (minute not in range(0, 61)):
                        raise commands.BadArgument()

                    if (second not in range(0, 61)):
                        raise commands.BadArgument()

                    self.timestamp = datetime.datetime(year, month, day, hour, minute, second).timestamp()
        elif (argument.startswith("tomorrow")):
            # tomorrow
            # tomorrow at 11
            # tomorrow at 11pm
            # tomorrow at 11am
            # tomorrow at 11:30:30
            # tomorrow at 11:30

            if (argument == "tomorrow"):
                self.timestamp = (self.now + datetime.timedelta(days=1)).timestamp()
            else:
                match = re.fullmatch(regex.Regex.TOMORROW_AT_HOUR, argument)
                if (not match):
                    match = re.fullmatch(regex.Regex.TOMORROW_AT_TIME, argument)

                if (match):
                    tomorrow = self.now + datetime.timedelta(days=1)

                    if (len(match.groups()) == 2):
                        hour = int(match.group("hour"))
                        meridies = match.group("meridies")

                        if (meridies == "pm"):
                            hour += 12

                        if (hour not in range(0, 24)):
                            raise commands.BadArgument()

                        self.timestamp = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, hour).timestamp()
                    else:
                        hour = int(match.group("hour"))
                        minute = int(match.group("minute"))

                        if (match.group("second")):
                            second = int(match.group("second"))
                        else:
                            second = 0

                        if (hour not in range(0, 24)):
                            raise commands.BadArgument()

                        if (minute not in range(0, 61)):
                            raise commands.BadArgument()

                        if (second not in range(0, 61)):
                            raise commands.BadArgument()

                        self.timestamp = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, hour, minute, second).timestamp()
        elif (argument.startswith(("today at ", "at "))):
            # today at 11
            # today at 11am
            # today at 11pm
            # today at 11:30:30
            # today at 11:30
            # at 11
            # at 11am
            # at 11pm
            # at 11:30:30
            # at 11:30
            
            match = re.fullmatch(regex.Regex.TODAY_AT_HOUR, argument)
            if (not match):
                match = re.fullmatch(regex.Regex.TODAY_AT_TIME, argument)
                if (not match):
                    match = re.fullmatch(regex.Regex.AT_HOUR, argument)
                    if (not match):
                        match = re.fullmatch(regex.Regex.AT_TIME, argument)
                        
            if (match):
                if (len(match.groups()) == 2):
                    hour = int(match.group("hour"))
                    meridies = match.group("meridies")

                    if (meridies == "pm"):
                        hour += 12

                    if (hour not in range(0, 24)):
                        raise commands.BadArgument()

                    self.timestamp = datetime.datetime(self.now.year, self.now.month, self.now.day, hour).timestamp()
                else:
                    hour = int(match.group("hour"))
                    minute = int(match.group("minute"))

                    if (match.group("second")):
                        second = int(match.group("second"))
                    else:
                        second = 0

                    if (hour not in range(0, 24)):
                        raise commands.BadArgument()

                    if (minute not in range(0, 61)):
                        raise commands.BadArgument()

                    if (second not in range(0, 61)):
                        raise commands.BadArgument()

                    self.timestamp = datetime.datetime(self.now.year, self.now.month, self.now.day, hour, minute, second).timestamp()
        elif (":" in argument):
            # 11:30:30
            # 11:30

            match = re.fullmatch(regex.Regex.TIME, argument)

            if (match):
                hour = int(match.group("hour"))
                minute = int(match.group("minute"))

                if (match.group("second")):
                    second = int(match.group("second"))
                else:
                    second = 0

                if (hour not in range(0, 24)):
                    raise commands.BadArgument()

                if (minute not in range(0, 61)):
                    raise commands.BadArgument()

                if (second not in range(0, 61)):
                    raise commands.BadArgument()

                self.timestamp = datetime.datetime(self.now.year, self.now.month, self.now.day, hour, minute, second).timestamp()
        elif (("am" in argument) or ("pm" in argument)):
            # 11am
            # 11pm
            
            match = re.fullmatch(regex.Regex.HOUR, argument)

            if (match):
                hour = int(match.group("hour"))
                meridies = match.group("meridies")

                if (meridies == "pm"):
                    hour += 12

                if (hour not in range(0, 24)):
                    raise commands.BadArgument()

                self.timestamp = datetime.datetime(self.now.year, self.now.month, self.now.day, hour).timestamp()
        else:
            # 1s
            # 1 second
            # 2 seconds
            
            match = re.fullmatch(regex.Regex.ANY_HUMANIZED_TIME, argument)
            if (match):
                new = datetime.timedelta()

                seconds = match.group("seconds")
                if (seconds):
                    seconds = int(seconds)
                    if (seconds > 0):
                        seconds = datetime.timedelta(seconds=seconds)
                        new += seconds

                minutes = match.group("minutes")
                if (minutes):
                    minutes = int(minutes)
                    if (minutes > 0):
                        minutes = datetime.timedelta(minutes=minutes)
                        new += minutes

                hours = match.group("hours")
                if (hours):
                    hours = int(hours)
                    if (hours > 0):
                        hours = datetime.timedelta(hours=hours)
                        new += hours

                days = match.group("days")
                if (days):
                    days = int(days)
                    if (days > 0):
                        days = datetime.timedelta(days=days)
                        new += days

                weeks = match.group("weeks")
                if (weeks):
                    weeks = int(weeks)
                    if (weeks > 0):
                        weeks = datetime.timedelta(weeks=weeks)
                        new += weeks

                if (new > datetime.timedelta()):
                    self.timestamp = (self.now + new).timestamp()

        if (not hasattr(self, "timestamp")):
            raise commands.BadArgument()
        
        if (self.timestamp < self.now.timestamp()):
            raise commands.BadArgument()
        
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