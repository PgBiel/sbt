"""
/utils/format.py

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
import typing

import discord


def bold(text: str) -> str:
    return "**{0}**".format(text)

def camelify(text: str) -> str:
    result = list()

    for (word) in text.split("_"):
        result.append(word.title())

    return "".join(result)

def code(text: str, language: str = "") -> str:
    return "```{0}\n{1}\n```".format(language, text)

def dedent(text: str, *, max: int = None, force: bool = False) -> str:
    lines = text.split("\n")

    if (force):
        result = ""
        for (line) in lines:
            if (line):
                result += line.lstrip()

            result += "\n"
    else:
        levels = list()
        for (line) in lines:
            if (line):
                levels.append(len(line) - len(line.lstrip(" ")))

        if (levels):
            if (max):
                unnecessary_indent = min(levels + [max])
            else:
                unnecessary_indent = min(levels)
        else:
            unnecessary_indent = 0

        result = ""
        for (line) in lines:
            if (line):
                result += line[unnecessary_indent:]

            result += "\n"

    return result

def embed(title: str = None, description: str = None,
          *,
          color: int = None,
          thumbnail: str = None,
          author: str = None, author_url: str = None, author_icon_url: str = None,
          fields: list = list(),
          image: str = None,
          footer: str = None, footer_icon_url: str = None,
          to_dict: bool = False) -> discord.Embed:

    e = discord.Embed()

    if (title):
        e.title = title

    if (description):
        e.description = description

    if (color is None):
        color = discord.Color.blurple()

    if (thumbnail):
        e.set_thumbnail(url=thumbnail)

    e.color = color

    if (author):
        if (author_url and author_icon_url):
            e.set_author(name=author, url=author_url, icon_url=author_icon_url)
        elif (author_url):
            e.set_author(name=author, url=author_url)
        elif (author_icon_url):
            e.set_author(name=author, icon_url=author_icon_url)
        else:
            e.set_author(name=author)

    for (field) in fields:
        if (len(field) == 2):
            e.add_field(name=field[0], value=field[1])
        elif (len(field) == 3):
            e.add_field(name=field[0], value=field[1], inline=field[2])

    if (image):
        e.set_image(url=image)

    if (footer):
        if (not footer_icon_url):
            e.set_footer(text=footer)
        else:
            e.set_footer(text=footer, icon_url=footer_icon_url)

    if (to_dict):
        return e.to_dict()
    return e

def escape(text: str,
           *,
           backslash: bool = False,
           mentions: bool = True,
           emoji: bool = False,
           urls: bool = False, invites: bool = False,
           asterisk: bool = True, backticks: bool = True, tilde: bool = True, underscores: bool = True) -> str:

    if (backslash):
        text = text.replace("\\", "\\\\")

    if (mentions):
        text = text.replace("@", "@\u200b")

    if (emoji):
        text = re.sub("<(a)?:([a-zA-Z0-9_]+):([0-9]+)>", "<\u200b\\1:\\2:\\3>", text)

    if (urls):
        text = text.replace("https://", "https:/\u200b/")

    if (invites):
        text = text.replace("discord.gg/", "discord.gg/\u200b")

    if (asterisk):
        text = text.replace("*", "\\*")

    if (backticks):
        text = text.replace("`", "\\`")

    if (tilde):
        text = text.replace("~", "\\~")

    if (underscores):
        text = text.replace("_", "\\_")

    return text

def get_lines(text: str, start: int, end: int = None) -> str:
    lines = text.split("\n")
    start -= 1

    if (end == -1):
        return text
    elif (not end):
        if (start in range(len(lines))):
            return lines[start]
        else:
            return text

    end = min([end, len(lines)])

    result = ""
    for (i) in range(start, end):
        result += lines[i]
        result += "\n"

    return result

def humanize_bytes(bytes: int) -> str:
    symbols = ["kB", "mB", "gB", "tB", "pB", "eB", "zB", "yB"]

    prefixes = dict()
    for (i, symbol) in enumerate(symbols):
        prefixes[symbol] = 1 << (i + 1) * 10

    for (symbol) in reversed(symbols):
        if (bytes >= prefixes[symbol]):
            value = bytes / prefixes[symbol]

            if (str(value).endswith(".0")):
                return "{0:.0f}{1}".format(value, symbol)
            return "{0:.2f}{1}".format(value, symbol)

    if (str(bytes).endswith(".0")):
        return "{0:.0f}B".format(bytes)
    return "{0:.2f}B".format(bytes)

def humanize_percentage(percent: float):
    if (str(percent).endswith(".0")):
        return "{0:.0f}%".format(percent)
    return "{0:.2f}%".format(percent)

def humanize_seconds(seconds: float, *, long: bool = True) -> str:
    seconds, microseconds = divmod(seconds, 1)  # exact
    minutes, seconds = divmod(seconds, 60)      # exact
    hours, minutes = divmod(minutes, 60)        # exact
    days, hours = divmod(hours, 24)             # exact
    weeks, days = divmod(days, 7)               # exact
    months, weeks = divmod(weeks, 4)            # approximate
    years, months = divmod(months, 12)          # approximate

    result = list()
    approximate = False

    if (microseconds):
        if (long):
            end = " microsecond"
            if (microseconds != 1):
                end += "s"
        else:
            end = "μs"

        microseconds = str(microseconds).split(".")[-1][:6]
        microseconds = "{0}{1}".format(microseconds, end)
        result.append(microseconds)

    if (seconds):
        if (long):
            end = " second"
            if (seconds != 1):
                end += "s"
        else:
            end = "s"
            
        seconds = str(seconds).split(".")[0]
        seconds = "{0}{1}".format(seconds, end)
        result.append(seconds)

    if (minutes):
        if (long):
            end = " minute"
            if (minutes != 1):
                end += "s"
        else:
            end = "m"
            
        minutes = str(minutes).split(".")[0]
        minutes = "{0}{1}".format(minutes, end)
        result.append(minutes)

    if (hours):
        if (long):
            end = " hour"
            if (hours != 1):
                end += "s"
        else:
            end = "h"
            
        hours = str(hours).split(".")[0]
        hours = "{0}{1}".format(hours, end)
        result.append(hours)

    if (days):
        if (long):
            end = " day"
            if (days != 1):
                end += "s"
        else:
            end = "d"
            
        days = str(days).split(".")[0]
        days = "{0}{1}".format(days, end)
        result.append(days)

    if (weeks):
        if (long):
            end = " week"
            if (weeks != 1):
                end += "s"
        else:
            end = "w"
            
        weeks = str(weeks).split(".")[0]
        weeks = "{0}{1}".format(weeks, end)
        result.append(weeks)

    if (months):
        approximate = True

        if (long):
            end = " month"
            if (months != 1):
                end += "s"
        else:
            end = "mo"
            
        months = str(months).split(".")[0]
        months = "{0}{1}".format(months, end)
        result.append(months)

    if (years):
        approximate = True

        if (long):
            end = " year"
            if (years != 1):
                end += "s"
        else:
            end = "y"
            
        years = str(years).split(".")[0]
        years = "{0}{1}".format(years, end)
        result.append(years)

    result = result[::-1]

    if (len(result) >= 2):
        if (long):
            result.append("and")
        else:
            result.append("&")

        result[-1], result[-2] = result[-2], result[-1]

        if (long):
            for (i) in range(0, len(result) - 3):
                result[i] += ","

    if (long and approximate):
        result = ["approximately"] + result

    return " ".join(result)

def humanize_datetime(time: typing.Union[datetime.datetime, datetime.date] = datetime.datetime.utcnow):
    if (callable(time)):
        time = time()

    day = time.strftime("%d")
    if (day in ["01", "21", "31"]):
        suffix = "st"
    elif (day in ["02", "22"]):
        suffix = "nd"
    elif (day in ["03", "23"]):
        suffix = "rd"
    else:
        suffix = "th"

    if (day.startswith("0")):
        day = day[1:]

    if (isinstance(time, datetime.datetime)):
        return time.strftime("%A {0}{1} %B, %Y %H:%M:%S (UTC)".format(day, suffix))
    else:
        return time.strftime("%A {0}{1} %B, %Y".format(day, suffix))

def indent(text: str, *, amount: int) -> str:
    lines = text.split("\n")

    result = ""
    for (line) in lines:
        if (line):
            result += " " * amount
            result += line

        result += "\n"

    return result

def inline(text: str) -> str:
    return "`{0}`".format(text)

def italic(text: str) -> str:
    return "*{0}*".format(text)

def jump_url(message: discord.Message) -> str:
    if (message.guild):
        return "https://discordapp.com/channels/{0.guild.id}/{0.channel.id}/{0.id}/".format(message)
    return "https://discordapp.com/channels/@me/{0.channel.id}/{0.id}/".format(message)

def pagify(text: str, *, delims: list = ["\n"], shorten_by: int = 0, page_length: int = 2000) -> str:
    in_text = text
    page_length -= shorten_by

    while (len(in_text) > page_length):
        closest_delim = max([in_text.rfind(d, 0, page_length) for d in delims])
        closest_delim = closest_delim if closest_delim != -1 else page_length

        yield in_text[:closest_delim]
        in_text = in_text[closest_delim:]

    yield in_text

def snakify(text: str) -> str:
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", text)).lower()

def strikethrough(text: str) -> str:
    return "~~{0}~~".format(text)

def underline(text: str) -> str:
    return "__{0}__".format(text)

def unescape(text: str,
             *,
             backslash: bool = False,
             mentions: bool = True,
             emoji: bool = False,
             urls: bool = False, invites: bool = False,
             asterisk: bool = True, backticks: bool = True, tilde: bool = True, underscores: bool = True) -> str:

    if (backslash):
        text = text.replace("\\\\", "\\")

    if (mentions):
        text = text.replace("@\u200b", "@")

    if (emoji):
        text = re.sub("<\u200b(a)?:([a-zA-Z0-9_]+):([0-9]+)>", "<\\1:\\2:\\3>", text)

    if (urls):
        text = text.replace("https:/\u200b/", "https://")

    if (invites):
        text = text.replace("discord.gg/\u200b", "discord.gg/")

    if (asterisk):
        text = text.replace("\\*", "*")

    if (backticks):
        text = text.replace("\\`", "`")

    if (tilde):
        text = text.replace("\\~", "~")

    if (underscores):
        text = text.replace("\\_", "_")

    return text

def wrap_url(text: str):
    return "<{0}>".format(text)