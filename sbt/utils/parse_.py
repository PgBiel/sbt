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
        if (argument):
            self.argument = argument

            self.result = self.parse()
            if (not self.result):
                raise commands.BadArgument(argument)

    def parse(self, argument: str = None):
        """
        parses humanized datetime and returns a timezone naive
        datetime.date object
        """

        if (not argument):
            if (not hasattr(self, "argument")):
                raise RuntimeError("argument is undefined in all scopes")

            argument = self.argument

        if (match := re.fullmatch(regex.Regex.))

class Time():
    def __init__(self, argument: str = None):
        if (argument):
            self.argument = argument

            self.result = self.parse()
            if (not self.result):
                raise commands.BadArgument(argument)

    def parse(self, argument: str = None):
        """
        parses humanized datetime and returns a timezone naive
        datetime.time object
        """

        if (not argument):
            if (not hasattr(self, "argument")):
                raise RuntimeError("argument is undefined in all scopes")

            argument = self.argument

class DateTime():
    def __init__(self, argument: str = None):
        if (argument):
            self.argument = argument

            self.result = self.parse()
            if (not self.result):
                raise commands.BadArgument(argument)

    def parse(self, argument: str = None):
        """
        parses humanized datetime and returns a timezone naive
        datetime.datetime object
        """

        if (not argument):
            if (not hasattr(self, "argument")):
                raise RuntimeError("argument is undefined in all scopes")

            argument = self.argument
        
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