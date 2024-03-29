"""
/modules/information.py

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

__authors__     = [("shineydev", "contact@shiney.dev")]
__maintainers__ = [("shineydev", "contact@shiney.dev")]

__level__ = 3


import copy
import datetime
import dis
import glob
import inspect
import psutil
import random
import re
import struct
import typing
import unicodedata

import discord
from discord.ext import commands, tasks

from utils import (
    channels,
    context,
    dataio,
    enumerators,
    error,
    checks,
    format,
    fuzzywuzzy,
    paginate,
    parse,
    regex,
    search,
    settings,
)


class Information(commands.Cog, name="information"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.__authors__ = __authors__
        self.__maintainers__ = __maintainers__
        self.__level__ = __level__

    @checks.is_guild()
    @commands.command(name="avatar", aliases=["icon"])
    async def _avatar(self, ctx: commands.Context, *, member: discord.Member = None):
        """
        show a member's avatar

        defaults to your own
        """

        if (not member):
            member = ctx.author

        e = discord.Embed(color=member.color)
        e.set_author(name=member, url=member.avatar_url)
        e.set_image(url=member.avatar_url)
        await ctx.send(embed=e)

    @commands.cooldown(1, 60, commands.cooldowns.BucketType.user)
    @commands.command(name="code", aliases=["lines"])
    async def _code(self, ctx: commands.Context):
        """
        files, lines, characters
        """

        files_ = [
            *glob.glob("*.py"),
            *glob.glob("utils\\*.py"),
            *glob.glob("modules\\*.py"),
        ]

        files = 0
        lines = 0
        characters = 0

        for (file) in files_:
            files += 1
            for (line) in open(file):
                lines += 1
                characters += len(line)

        color = ctx.me.color if ctx.guild else discord.Color.blurple()
        e = discord.Embed(color=color)
        e.set_author(name="Code")
        e.add_field(name="Files", value=str(files))
        e.add_field(name="Lines", value=str(lines))
        e.add_field(name="Characters", value=str(characters))
        e.set_footer(
            text = "{0} | {1}".format(
                ctx.author,
                format.humanize_datetime()
            ),
            icon_url=ctx.author.avatar_url
        )

        await ctx.send(embed=e)

    @commands.command(name="color", aliases=["colour"])
    async def _color(self, ctx: commands.Context, *, code: typing.Optional[parse.Color]):
        """
        parse and display a color

        defaults to a random color

        examples:
            `>color`           :: random
            `>color 0xFF0000`  :: red
            `>color 255, 0, 0` :: red

        see source for regex patterns
        """

        if (not code):
            code = "".join([random.choice("0123456789ABCDEF") for (_) in range(6)])
            code = parse.Color.parse(code)

        int_, hex, rgb, cmyk = code

        rgb = "({0}, {1}, {2})".format(*rgb)
        cmyk = "({0}, {1}, {2}, {3})".format(*cmyk)

        e = discord.Embed(title="Color", color=int_)
        e.add_field(name="Hexadecimal", value="0x{0}".format(hex))
        e.add_field(name="Red, Green, Blue", value=rgb)
        e.add_field(name="Cyan, Magenta, Yellow, Key", value=cmyk)
        e.set_footer(
            text = "{0} | {1}".format(
                ctx.author,
                format.humanize_datetime()
            ),
            icon_url=ctx.author.avatar_url
        )

        await ctx.send(embed=e)

    @commands.command(name="contributors", aliases=["affiliates"])
    async def _contributors(self, ctx: commands.Context):
        """
        display sbt's contributors
        """

        pass
        
    @commands.command(name="dis")
    async def _dis(self, ctx: commands.Context, *, command: str):
        """
        display the disassembled source of a command

        example:
            `>dis owner` :: show the disassembled source of `owner`
        """

        command = ctx.bot.get_command(command)
        if (not command):
            await ctx.bot.send_help(ctx)
            return

        if (not await command.can_run(ctx)):
            await ctx.bot.send_help(ctx)
            return

        message = dis.Bytecode(command.callback).dis()
        if (not message):
            await ctx.bot.send_help(ctx)
            return

        message = message.replace("```", "``")
        
        for (page) in format.pagify(message, shorten_by=8):
            if (page):
                await ctx.send("```\n{0}```".format(page))

    @commands.command(name="discriminator", aliases=["discrim"])
    async def _discriminator(self, ctx: commands.Context, discriminator: typing.Optional[str]):
        """
        display all users with a discriminator

        defaults to your own

        examples:
            `>discriminator`      :: display all users with your discriminator
            `>discriminator 0001` :: display all users with the `0001` discriminator
        """

        if (not discriminator):
            discriminator = ctx.author.discriminator

        if ((not len(discriminator) == 4) or (not discriminator.isdigit())):
            await ctx.bot.send_help(ctx)
            return

        members = list()
        for (guild) in ctx.bot.guilds:
            for (member) in guild.members:
                if (member.discriminator == discriminator):
                    members.append(member)

        if (not members):
            await ctx.send("no results")
            return

        message = ""
        for (member) in members:
            message += "{0}\n".format(member)

        color = ctx.me.color if ctx.guild else discord.Color.blurple()
        e = discord.Embed(color=color)
        e.add_field(name="Members", value=message)
        e.set_footer(
            text="{0} | {1}".format(
                ctx.author,
                format.humanize_datetime()
            ),
            icon_url=ctx.author.avatar_url
        )

        await ctx.send(embed=e)

    @commands.command(name="flags")
    async def _flags(self, ctx: commands.Context, member: typing.Optional[discord.Member]):
        """
        display a user's flags

        defaults to your own

        examples:
            `>flags`
            `>flags 310418322384748544`
        """

        author = ctx.author

        if (member):
            ctx = copy.copy(ctx)
            ctx.author = member

        flags = list()

        if (checks.is_owner_check(ctx)):
            flags.append("owner")

        if (checks.is_supervisor_check(ctx)):
            flags.append("supervisor")

        if (checks.is_support_check(ctx)):
            flags.append("support team")

        if (checks.is_alpha_check(ctx)):
            flags.append("alpha tester")

        if (checks.is_beta_check(ctx)):
            flags.append("beta tester")

        if (checks.is_dj_check(ctx)):
            flags.append("dj")

        if (ctx.author.id in ctx.bot._settings.whitelist):
            flags.append("whitelisted")

        if (ctx.author.id in ctx.bot._settings.blacklist):
            flags.append("blacklisted")

        if (not flags):
            await ctx.send("no results")
            return

        message = ", ".join(flags)

        color = ctx.me.color if ctx.guild else discord.Color.blurple()
        e = discord.Embed(color=color)
        e.add_field(name="Flags for {0}".format(ctx.author), value=message)
        e.set_footer(
            text = "{0} | {1}".format(
                author.name,
                format.humanize_datetime()
            ),
            icon_url=author.avatar_url
        )

        await ctx.send(embed=e)

    @commands.command(name="invite")
    async def _invite(self, ctx: commands.Context):
        """
        display sbt's invite links
        """

        sbt_guild = "not yet"
        sbt_oauth = ctx.bot._settings.oauth

        color = ctx.me.color if ctx.guild else discord.Color.blurple()
        e = discord.Embed(color=color)
        e.add_field(name="SBT Support Guild", value=sbt_guild)
        e.add_field(name="SBT OAuth Invite", value=sbt_oauth)
        e.set_footer(
            text = "{0} | {1}".format(
                ctx.author,
                format.humanize_datetime()
            ),
            icon_url=ctx.author.avatar_url
        )

        await ctx.send(embed=e)

    @commands.command(name="latency", aliases=["ping"])
    async def _latency(self, ctx: commands.Context):
        """
        display sbt's api and websocket latency
        """

        ws_latency = ctx.bot.latency

        with context.Timer() as t:
            await ctx.trigger_typing()

        api_latency = t.time

        if (ctx.invoked_with == "ping"):
            ws_latency = format.humanize_seconds(ws_latency, long=False)
            api_latency = format.humanize_seconds(api_latency, long=False)
        else:
            ws_latency = format.humanize_seconds(ws_latency)
            api_latency = format.humanize_seconds(api_latency)

        color = ctx.me.color if ctx.guild else discord.Color.blurple()
        e = discord.Embed(color=color)
        e.add_field(name="WS Latency", value=ws_latency)
        e.add_field(name="API Latency", value=api_latency)
        await ctx.send(embed=e)

    @checks.is_guild()
    @commands.command(name="messages", aliases=["messagecount"])
    async def _messages(self, ctx: commands.Context, member: typing.Optional[discord.Member]):
        """
        display how many messages a user has sent in the past 24 hours

        defaults to your own
        """

        if (not member):
            member = ctx.author

        async with ctx.typing():
            messages = 0
            yesterday = datetime.datetime.utcnow() - datetime.timedelta(days=1)
            async for (message) in ctx.channel.history(limit=1000, after=yesterday):
                if (message.author == member):
                    messages += 1

        s = "" if (messages == 1) else "s"
        await ctx.send("{0} sent {1} message{2} to this channel in the past 24 hours".format(member, messages, s))

    @commands.command(name="now", aliases=["time"])
    async def _now(self, ctx: commands.Context):
        """
        display the current time in utc
        """

        time = format.humanize_datetime()
        await ctx.send(time)

    @checks.is_guild()
    @commands.command(name="permissions", aliases=["perms"])
    async def _permissions(self, ctx: commands.Context, object: typing.Optional[typing.Union[discord.TextChannel, discord.VoiceChannel, discord.Role, discord.Member, int]], member_or_role: typing.Optional[typing.Union[discord.Role, discord.Member]]):
        """
        display permissions for an object

        defaults to you

        can be a channel, a role, a member, or a permissions integer

        member_or_role is ignored unless the object is a channel, in which case we find the channel permissions for that member or role
        """
        
        if (not object):
            object = ctx.author

        if (isinstance(object, (discord.TextChannel, discord.VoiceChannel))):
            if (not member_or_role):
                permissions = object.overwrites_for(ctx.guild.default_role)
                message = "{0} ({1}) overwrites for @everyone ({2})\n\n".format(
                    object.name, object.id, ctx.guild.id)
            else:
                permissions = object.overwrites_for(member_or_role)
                message = "{0} ({1}) overwrites for {2} ({3})\n\n".format(
                    object.name, object.id, member_or_role.name, member_or_role.id)

        elif (isinstance(object, discord.Role)):
            permissions = object.permissions
            message = "{0} ({1})\n\n".format(object.name, object.id)
        elif (isinstance(object, discord.Member)):
            permissions = object.guild_permissions
            message = "{0} ({1})\n\n".format(object.name, object.id)
        else:
            permissions = discord.Permissions(object)
            message = "{0}\n\n".format(object)

        for (permission, value) in sorted(permissions):
            if (value):
                message += "+ {0}\n".format(permission)
            elif (value == None):
                message += "  {0}\n".format(permission)
            else:
                message += "- {0}\n".format(permission)

        await ctx.send(format.code(message, "diff"))
        
    @commands.command(name="since")
    async def _since(self, ctx: commands.Context, date: parse.PastDate):
        """
        display distance between today and a date

        examples:
            `>since 01/01/19`
        """

        now = datetime.datetime.utcnow()
        today = datetime.date(now.year, now.month, now.day)
        days = -(date - today).days

        message = "{0} since {1}".format(
            format.humanize_seconds(days * 86400),
            format.humanize_datetime(date)
        )

        await ctx.send(message)
        
    @commands.command(name="source", aliases=["src"])
    async def _source(self, ctx: commands.Context, command: str, start: typing.Optional[int], end: typing.Optional[int]):
        """
        display the source of a command

        examples:
            `>source owner` :: show the full source of `owner`
            `>source owner 2` :: show line `2` of `owner`
            `>source owner 3 5` :: show lines 3-5 of `owner`
        """

        command = ctx.bot.get_command(command)
        if (not command):
            await ctx.bot.send_help(ctx)
            return

        if (not await command.can_run(ctx)):
            await ctx.bot.send_help(ctx)
            return

        if (start):
            if ((end) and ((start < 1) or (start > end))):
                raise commands.BadArgument()
        else:
            # show all
            start, end = 1, -1

        source = inspect.getsource(command.callback)
        source = format.get_lines(source, start, end)
        
        message = format.dedent(source)
        message = message.replace("```", "``")
        
        for (page) in format.pagify(message, shorten_by=10):
            if (page):
                await ctx.send("```py\n{0}```".format(page))

    @commands.command(name="statistics", aliases=["stats"])
    async def _statistics(self, ctx: commands.Context):
        """
        display sbt's statictics
        """

        uptime = (datetime.datetime.utcnow() - ctx.bot._uptime).total_seconds()
        uptime = format.humanize_seconds(uptime, long=False)
        latency = format.humanize_seconds(ctx.bot.latency, long=False)
        version = ctx.bot.__version__

        users = 0
        for (user) in ctx.bot.users:
            if (not user.bot):
                users += 1

        channels = 0
        for (channel) in ctx.bot.get_all_channels():
            if (not isinstance(channel, discord.CategoryChannel)):
                channels += 1

        guilds = len(ctx.bot.guilds)

        color = ctx.me.color if ctx.guild else discord.Color.blurple()
        e = discord.Embed(color=color, title="Statistics")
        e.add_field(name="Uptime", value=uptime)
        e.add_field(name="Latency", value=latency)
        e.add_field(name="Version", value=version)
        e.add_field(name="Users", value=users)
        e.add_field(name="Channels", value=channels)
        e.add_field(name="Guilds", value=guilds)
        e.set_footer(
            text = "{0} | {1}".format(
                ctx.author,
                format.humanize_datetime()
            ),
            icon_url=ctx.author.avatar_url
        )

        await ctx.send(embed=e)

    @commands.command(name="unicode", aliases=["char", "character"])
    async def _unicode(self, ctx: commands.Context, *, characters: str):
        """
        show unicode information on a character

        example:
            `>unicode :zero:` :: \\U00000030\\U000020e3
        """

        message = ""

        max_ = max([len(character) for (character) in characters])

        for (character) in characters:
            digit = "{0:x}".format(ord(character))
            name = unicodedata.name(character, "unknown name")

            # fix weird bug with the enclosing keycap
            if (name in ["COMBINING ENCLOSING KEYCAP", "ZERO WIDTH SPACE"]):
                i = " "
            else:
                i = ""

            message += "\u200b {0:>{width}} {1} \\U{2:>08}  \\N{{{3}}}\n".format(
                character, i, digit, name,
                width=max_
            )

        for (page) in format.pagify(message, shorten_by=8):
            if (page):
                await ctx.send("```\n{0}```".format(page))
        
    @commands.command(name="until")
    async def _until(self, ctx: commands.Context, date: parse.FutureDate):
        """
        display distance between today and a date

        examples:
            `>until 02-22-2050`
        """
        
        now = datetime.datetime.utcnow()
        today = datetime.date(now.year, now.month, now.day)
        days = (date - today).days

        message = "{0} until {1}".format(
            format.humanize_seconds(days * 86400),
            format.humanize_datetime(date)
        )

        await ctx.send(message)

    @commands.command(name="uptime")
    async def _uptime(self, ctx: commands.Context):
        """
        show uptime in a humanized manner
        """

        uptime = datetime.datetime.utcnow() - ctx.bot._uptime
        await ctx.send("i've been online for {0}".format(format.humanize_seconds(uptime.total_seconds())))

    @commands.command(name="version")
    async def _version(self, ctx: commands.Context):
        """
        display sbt's version
        """

        sbt_version = format._version(ctx.bot.__version__)
        dpy_version = format._version(discord.__version__)

        color = ctx.me.color if ctx.guild else discord.Color.blurple()
        e = discord.Embed(color=color)
        e.add_field(name="SBT Version", value=sbt_version)
        e.add_field(name="discord.py Version", value=dpy_version)
        e.set_footer(
            text = "{0} | {1}".format(
                ctx.author,
                format.humanize_datetime()
            ),
            icon_url=ctx.author.avatar_url
        )

        await ctx.send(embed=e)

    @commands.group(name="information", aliases=["info"], invoke_without_command=True)
    async def _information(self, ctx: commands.Context):
        """
        information group
        """

        await ctx.bot.send_help(ctx)

    @_information.command(name="bot", aliases=["client"])
    async def _information_bot(self, ctx: commands.Context):
        """
        display sbt's information
        """

        user = ctx.bot.user
        authors = ctx.bot.__authors__
        authors = ", ".join([n for (n, u) in authors])
        maintainers = ctx.bot.__maintainers__
        maintainers = ", ".join([n for (n, u) in maintainers])
        version = ctx.bot.__version__

        color = ctx.me.color if ctx.guild else discord.Color.blurple()
        e = discord.Embed(color=color, title="Bot Information")

        changes = await self._commits(count=3)
        if (changes):
            e.add_field(name="Recent Changes", value=changes, inline=False)

        e.add_field(name="User", value="{0} ({0.id})".format(user), inline=False)
        e.add_field(name="Authors", value=authors)
        e.add_field(name="Maintainers", value=maintainers)
        e.add_field(name="Version", value=version)
        e.set_footer(
            text = "{0} | {1}".format(
                ctx.author,
                format.humanize_datetime()
            ),
            icon_url=ctx.author.avatar_url
        )

        await ctx.send(embed=e)

    async def _commits(self, *, count: int = None):
        # this is not ready
        return None

        github = self.bot.get_cog("github")
        if (not github):
            # github isn't loaded
            return None

        change_format = "[`{}`](https://github.com/ShineyDev/sbt/commit/{}) {}\n"

        json = {
            "since": format.iso8601(datetime.date.today()),
        }

        url = "repos/ShineyDev/sbt/commits"

        try:
            changes = await github.request("GET", url, json=json)
        except (Exception) as e:
            if (type(e).__name__ == "GitHubError"):
                return None
            elif (type(e).__name__ == "TimeoutError"):
                return None
            raise

        ...
        
    @checks.is_guild()
    @_information.command(name="channel")
    async def _information_channel(self, ctx: commands.Context, channel: typing.Optional[discord.abc.GuildChannel]):
        """
        display channel information

        defaults to the current channel
        """

        pass

    @checks.is_guild()
    @_information.command(name="emoji")
    async def _information_emoji(self, ctx: commands.Context, emoji: typing.Union[discord.Emoji, str]):
        """
        display emoji information

        if it is a unicode emoji it just invokes `>unicode`
        """

        if (isinstance(emoji, str)):
            await ctx.invoke(self._unicode, characters=emoji)
            return

        color = ctx.me.color if ctx.guild else discord.Color.blurple()
        e = discord.Embed(color=color, title="Emoji Information")
        e.add_field(name="Name", value=emoji.name)
        e.add_field(name="ID", value=emoji.id)
        e.add_field(name="Created", value=format.humanize_datetime(emoji.created_at), inline=False)
        e.add_field(name="Animated", value=emoji.animated)
        e.add_field(name="Managed", value=emoji.managed)
        
        if (emoji.roles):
            roles = [r.name for r in emoji.roles]
            e.add_field(name="Roles", value=", ".join(roles))

        await ctx.send(embed=e)
    
    @checks.is_guild()
    @_information.command(name="guild", aliases=["server"])
    async def _information_guild(self, ctx: commands.Context, guild: typing.Optional[discord.Guild]):
        """
        display guild information

        defaults to the current guild
        """

        pass

    @checks.is_guild()
    @_information.command(name="member")
    async def _information_member(self, ctx: commands.Context, member: typing.Optional[discord.Member]):
        """
        display member information

        defaults to you
        """

        pass

    @_information.command(name="message")
    async def _information_message(self, ctx: commands.Context, message: int):
        """
        display message information
        """

        try:
            message = await ctx.channel.fetch_message(message)
        except (discord.errors.NotFound) as e:
            await ctx.bot.send_help(ctx)
            return

        mentions = list()
        
        if (message.mention_everyone):
            mentions.append("@everyone")

        for (member) in message.mentions:
            mentions.append(member.mention)

        for (role) in message.role_mentions:
            mentions.append(role.mention)

        for (channel) in message.channel_mentions:
            mentions.append(channel.mention)

        color = ctx.me.color if ctx.guild else discord.Color.blurple()
        e = discord.Embed(color=color, title="Message Information")
        e.add_field(name="Content", value=message.content, inline=False)
        e.add_field(name="ID", value="{0.id}".format(message))
        e.add_field(name="Author", value="{0.name} ({0.id})".format(message.author))
        e.add_field(name="Timestamp", value=format.humanize_datetime(message.created_at), inline=False)
        e.add_field(name="TTS", value=message.tts)
        e.add_field(name="Type", value=message.type)

        if (mentions):
            e.add_field(name="Mentions [{0}]".format(len(mentions)), value=", ".join(mentions))

        e.set_footer(
            text = "{0} | {1}".format(
                ctx.author,
                format.humanize_datetime()
            ),
            icon_url=ctx.author.avatar_url
        )

        await ctx.send(embed=e)
        
    @checks.is_guild()
    @_information.command(name="role")
    async def _information_role(self, ctx: commands.Context, role: discord.Role):
        """
        display role information
        """

        pass

    @checks.is_owner()
    @_information.command(name="system")
    async def _information_system(self, ctx: commands.Context):
        """
        display system information
        """

        process = psutil.Process()
        threads = process.num_threads()
        handles = process.num_handles()
        connections = len(process.connections())
        cpu = format.humanize_percentage(process.cpu_percent(interval=.5)
                                         / psutil.cpu_count())
        memory = format.humanize_bytes(
            (psutil.virtual_memory().total / 100)
            * process.memory_percent("private"))

        color = ctx.me.color if ctx.guild else discord.Color.blurple()
        e = discord.Embed(color=color, title="System Information")
        e.add_field(name="Process Name", value=process.name())
        e.add_field(name="Process ID", value=process.pid)
        e.add_field(name="\u200b", value="\u200b")
        e.add_field(name="Threads", value=threads)
        e.add_field(name="Handles", value=handles)
        e.add_field(name="Connections", value=connections)
        e.add_field(name="CPU", value=cpu)
        e.add_field(name="Memory", value=memory)
        e.add_field(name="\u200b", value="\u200b")

        await ctx.send(embed=e)

    @_information.command(name="user")
    async def _information_user(self, ctx: commands.Context, user: discord.User):
        """
        display user information
        """

        pass

                
def setup(bot : commands.Bot):
    extension = Information(bot)
    bot.add_cog(extension)