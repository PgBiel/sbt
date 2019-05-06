"""
/modules/beta.py

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

__version_info__ = (2, 0, 0, "alpha", 0)
__version__      = "{0}.{1}.{2}{3}{4}".format(*[str(n)[0] if (i == 3) else str(n) for (i, n) in enumerate(__version_info__)])

__level__        = 6

__all__ = {
    "Beta",
    "setup",
}


import discord
from discord.ext import commands

from utils import (
    checks,
    error,
    format,
    parse,
)


class Beta(commands.Cog, name="beta"):
    __all__ = {
        "__init__",
        "_parse",
        "_parse_boolean",
        "_parse_color",
        "_parse_date",
        "_parse_futuredate",
        "_parse_pastdate",
        "_parse_time",
        "_parse_futuretime",
        "_parse_pasttime",
        "_parse_datetime",
        "_parse_futuredatetime",
        "_parse_pastdatetime",
        "_parse_flags",
        "_parse_mention",
        "_parse_snowflake",
        "_parse_url",
        "_parse_version",
    }

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.__authors__ = __authors__
        self.__maintainers__ = __maintainers__
        self.__version_info__ = __version_info__
        self.__version__ = __version__
        self.__level__ = __level__

        super().__init__()

    @checks.is_beta()
    @checks.is_debugging()
    @commands.group(name="parse", invoke_without_command=True)
    async def _parse(self, ctx: commands.Context):
        """
        parser debugging
        """

        await ctx.bot.send_help(ctx)

    @checks.is_beta()
    @checks.is_debugging()
    @_parse.command(name="boolean")
    async def _parse_boolean(self, ctx: commands.Context, *, boolean: str):
        """
        boolean parser
        """

        try:
            boolean = parse.boolean(boolean)
        except (error.ParserError) as e:
            await ctx.message.add_reaction("\U0000274e")
            await ctx.send(format.inline(e.original))
        else:
            await ctx.message.add_reaction("\U00002705")
            await ctx.send(format.inline(boolean))

    @checks.is_beta()
    @checks.is_debugging()
    @_parse.command(name="color")
    async def _parse_color(self, ctx: commands.Context, *, color: str):
        """
        color parser
        """

        try:
            color = parse.Color.parse(color)
        except (error.ParserError) as e:
            await ctx.message.add_reaction("\U0000274e")
            await ctx.send(format.inline(e.original))
        else:
            await ctx.message.add_reaction("\U00002705")
            await ctx.send(format.inline(color))

    @checks.is_beta()
    @checks.is_debugging()
    @_parse.command(name="date")
    async def _parse_date(self, ctx: commands.Context, *, date: str):
        """
        date parser
        """

        try:
            date = parse.Date.parse(date)
        except (error.ParserError) as e:
            await ctx.message.add_reaction("\U0000274e")
            await ctx.send(format.inline(e.original))
        else:
            await ctx.message.add_reaction("\U00002705")
            await ctx.send(format.inline(format.humanize_datetime(date)))

    @checks.is_beta()
    @checks.is_debugging()
    @_parse.command(name="futuredate")
    async def _parse_futuredate(self, ctx: commands.Context, *, date: str):
        """
        futuredate parser
        """

        try:
            date = parse.FutureDate.parse(date)
        except (error.ParserError) as e:
            await ctx.message.add_reaction("\U0000274e")
            await ctx.send(format.inline(e.original))
        else:
            await ctx.message.add_reaction("\U00002705")
            await ctx.send(format.inline(format.humanize_datetime(date)))

    @checks.is_beta()
    @checks.is_debugging()
    @_parse.command(name="pastdate")
    async def _parse_pastdate(self, ctx: commands.Context, *, date: str):
        """
        pastdate parser
        """

        try:
            date = parse.PastDate.parse(date)
        except (error.ParserError) as e:
            await ctx.message.add_reaction("\U0000274e")
            await ctx.send(format.inline(e.original))
        else:
            await ctx.message.add_reaction("\U00002705")
            await ctx.send(format.inline(format.humanize_datetime(date)))

    @checks.is_beta()
    @checks.is_debugging()
    @_parse.command(name="time")
    async def _parse_time(self, ctx: commands.Context, *, time: str):
        """
        time parser
        """

        try:
            time = parse.Time.parse(time)
        except (error.ParserError) as e:
            await ctx.message.add_reaction("\U0000274e")
            await ctx.send(format.inline(e.original))
        else:
            await ctx.message.add_reaction("\U00002705")
            await ctx.send(format.inline(format.humanize_datetime(time)))

    @checks.is_beta()
    @checks.is_debugging()
    @_parse.command(name="futuretime")
    async def _parse_futuretime(self, ctx: commands.Context, *, time: str):
        """
        futuretime parser
        """

        try:
            time = parse.FutureTime.parse(time)
        except (error.ParserError) as e:
            await ctx.message.add_reaction("\U0000274e")
            await ctx.send(format.inline(e.original))
        else:
            await ctx.message.add_reaction("\U00002705")
            await ctx.send(format.inline(format.humanize_datetime(time)))

    @checks.is_beta()
    @checks.is_debugging()
    @_parse.command(name="pasttime")
    async def _parse_pasttime(self, ctx: commands.Context, *, time: str):
        """
        pasttime parser
        """

        try:
            time = parse.PastTime.parse(time)
        except (error.ParserError) as e:
            await ctx.message.add_reaction("\U0000274e")
            await ctx.send(format.inline(e.original))
        else:
            await ctx.message.add_reaction("\U00002705")
            await ctx.send(format.inline(format.humanize_datetime(time)))

    @checks.is_beta()
    @checks.is_debugging()
    @_parse.command(name="datetime")
    async def _parse_datetime(self, ctx: commands.Context, *, datetime: str):
        """
        datetime parser
        """

        try:
            datetime = parse.DateTime.parse(datetime)
        except (error.ParserError) as e:
            await ctx.message.add_reaction("\U0000274e")
            await ctx.send(format.inline(e.original))
        else:
            await ctx.message.add_reaction("\U00002705")
            await ctx.send(format.inline(format.humanize_datetime(datetime)))

    @checks.is_beta()
    @checks.is_debugging()
    @_parse.command(name="futuredatetime")
    async def _parse_futuredatetime(self, ctx: commands.Context, *, datetime: str):
        """
        futuredatetime parser
        """

        try:
            datetime = parse.FutureDateTime.parse(datetime)
        except (error.ParserError) as e:
            await ctx.message.add_reaction("\U0000274e")
            await ctx.send(format.inline(e.original))
        else:
            await ctx.message.add_reaction("\U00002705")
            await ctx.send(format.inline(format.humanize_datetime(datetime)))

    @checks.is_beta()
    @checks.is_debugging()
    @_parse.command(name="pastdatetime")
    async def _parse_pastdatetime(self, ctx: commands.Context, *, datetime: str):
        """
        pastdatetime parser
        """

        try:
            datetime = parse.PastDateTime.parse(datetime)
        except (error.ParserError) as e:
            await ctx.message.add_reaction("\U0000274e")
            await ctx.send(format.inline(e.original))
        else:
            await ctx.message.add_reaction("\U00002705")
            await ctx.send(format.inline(format.humanize_datetime(datetime)))

    @checks.is_beta()
    @checks.is_debugging()
    @_parse.command(name="flags")
    async def _parse_flags(self, ctx: commands.Context, *, flags: str):
        """
        flags parser
        """

        try:
            flags = parse.Flags.parse(flags)
        except (error.ParserError) as e:
            await ctx.message.add_reaction("\U0000274e")
            await ctx.send(format.inline(e.original))
        else:
            await ctx.message.add_reaction("\U00002705")
            await ctx.send(format.inline(flags))

    @checks.is_beta()
    @checks.is_debugging()
    @_parse.command(name="mention")
    async def _parse_mention(self, ctx: commands.Context, mention: str):
        """
        mention parser
        """

        try:
            mention = parse.mention(mention)
        except (error.ParserError) as e:
            await ctx.message.add_reaction("\U0000274e")
            await ctx.send(format.inline(e.original))
        else:
            await ctx.message.add_reaction("\U00002705")
            await ctx.send(format.inline(mention))

    @checks.is_beta()
    @checks.is_debugging()
    @_parse.command(name="snowflake")
    async def _parse_snowflake(self, ctx: commands.Context, snowflake: str):
        """
        snowflake parser
        """

        try:
            snowflake = parse.snowflake(snowflake)
        except (error.ParserError) as e:
            await ctx.message.add_reaction("\U0000274e")
            await ctx.send(format.inline(e.original))
        else:
            await ctx.message.add_reaction("\U00002705")
            await ctx.send(format.inline(snowflake))

    @checks.is_beta()
    @checks.is_debugging()
    @_parse.command(name="url")
    async def _parse_url(self, ctx: commands.Context, *, url: str):
        """
        url parser
        """

        try:
            url = parse.url(url)
        except (error.ParserError) as e:
            await ctx.message.add_reaction("\U0000274e")
            await ctx.send(format.inline(e.original))
        else:
            await ctx.message.add_reaction("\U00002705")
            await ctx.send(format.inline(url))

    @checks.is_beta()
    @checks.is_debugging()
    @_parse.command(name="version")
    async def _parse_version(self, ctx: commands.Context, version: str):
        """
        version parser
        """

        try:
            version = parse.version(version)
        except (error.ParserError) as e:
            await ctx.message.add_reaction("\U0000274e")
            await ctx.send(format.inline(e.original))
        else:
            await ctx.message.add_reaction("\U00002705")
            await ctx.send(format.inline(version))


def setup(bot: commands.Bot):
    extension = Beta(bot)
    bot.add_cog(extension)