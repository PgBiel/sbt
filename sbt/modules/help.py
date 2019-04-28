"""
/modules/help.py

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

__level__        = 2

__all__ = {
    "COMMANDS_PER_PAGE", "_chunks", "Help", "setup",
}


import asyncio

import discord
from discord.ext import commands

from utils import (
    format,
)


COMMANDS_PER_PAGE = 8


def _chunks(list_: list, number: int):
    for (i) in range(0, len(list_), number):
        yield list_[i:i + number]


class Help(commands.Cog, name="help"):
    __all__ = {
        "__init__", "cog_unload", "_help", "_help_cog",
        "_help_command", "_help_old", "all_help", "cog_help",
        "command_help", "paginate", "send_old_help",
    }

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot._extensions.add_extension(self)

        self.__authors__ = __authors__
        self.__maintainers__ = __maintainers__
        self.__version_info__ = __version_info__
        self.__version__ = __version__
        self.__level__ = __level__

        command = bot.get_command("help")
        self.old_help = commands.Command(command.callback, name="help", hidden=True)

        bot.remove_command("help")

        super().__init__()

    def cog_unload(self):
        self.bot.remove_command("help")
        self.bot.add_command(self.old_help)

        del self.bot._extensions.extensions[self.qualified_name]

    @commands.cooldown(1, 300, commands.cooldowns.BucketType.user)
    @commands.group(name="help", aliases=["h"], hidden=True, invoke_without_command=True)
    async def _help(self, ctx: commands.Context, *, thing: str = None):
        """
        show paginated help

        examples:
            `>help`
            `>help roll`
            `>help general`
        """

        if (ctx.guild and (not ctx.guild.me.guild_permissions.embed_links)):
            # we don't have permission to send embeds,
            # send old help instead of raising exceptions
            await self.send_old_help(ctx, thing)
            return

        if (not thing):
            await self.paginate(ctx, await self.all_help(ctx))
            return

        cog = ctx.bot.get_cog(thing)
        if (cog):
            await self.paginate(ctx, await self.cog_help(ctx, cog))
            return

        command = ctx.bot.get_command(thing)
        if (command):
            await self.paginate(ctx, await self.command_help(ctx, command))
            return

        await self.paginate(ctx, await self.all_help(ctx))

    @_help.command(name="cog", aliases=["extension", "module"])
    async def _help_cog(self, ctx: commands.Context, *, cog: str):
        """
        show paginated help for a cog

        example:
            `>help cog general`
        """

        if (ctx.guild and (not ctx.guild.me.guild_permissions.embed_links)):
            # we don't have permission to send embeds,
            # send old help instead of raising exceptions
            await self.send_old_help(ctx, cog)
            return

        cog = ctx.bot.get_cog(cog)
        if (cog):
            await self.paginate(ctx, await self.cog_help(ctx, cog))
            return

        await self.paginate(ctx, await self.all_help(ctx))

    @_help.command(name="command")
    async def _help_command(self, ctx: commands.Context, *, command: str):
        """
        show paginated help for a command

        example:
            `>help command roll`
        """

        if (ctx.guild and (not ctx.guild.me.guild_permissions.embed_links)):
            # we don't have permission to send embeds,
            # send old help instead of raising exceptions
            await self.send_old_help(ctx, command)
            return

        command = ctx.bot.get_command(command)
        if (command):
            await self.paginate(ctx, await self.command_help(ctx, command))
            return

        await self.paginate(ctx, await self.all_help(ctx))

    @_help.command(name="old")
    async def _help_old(self, ctx: commands.Context, *, thing: str):
        """
        show help in the old format

        examples:
            `>help old`
            `>help old general`
            `>help old roll`
        """

        await self.send_old_help(ctx, thing)
        ctx.command.reset_cooldown(ctx)

    async def all_help(self, ctx: commands.Context) -> list:
        embeds = list()

        for (cog) in ctx.bot.cogs:
            cog = ctx.bot.get_cog(cog)

            commands = list()
            for (command) in cog.get_commands():
                if (not await command.can_run(ctx)):
                    continue

                if (not ctx.author.id == ctx.bot._settings.owner):
                    if (command.hidden):
                        continue

                commands.append(command)

            for (j, chunk) in enumerate(_chunks(commands, COMMANDS_PER_PAGE), 1):
                color = ctx.guild.me.color if ctx.guild else discord.Color.blurple()
                e = discord.Embed(color = color)

                e.set_author(
                    name="{0} ({1}-{2} / {3})".format(
                        cog.qualified_name,
                        (j * COMMANDS_PER_PAGE) - (COMMANDS_PER_PAGE - 1),
                        min([j * COMMANDS_PER_PAGE, len(commands)]),
                        len(commands)
                    )
                )

                if (cog.__doc__):
                    e.description = cog.__doc__

                for (command) in chunk:
                    signature = "{0}{1} {2}".format(ctx.prefix, command.qualified_name, command.signature)

                    help = command.short_doc
                    if (not help):
                        help = "no description"

                    e.add_field(name=signature, value=help, inline=False)

                e.set_footer(
                    text = "{0} | {1}".format(
                        ctx.author.name,
                        format.humanize_datetime()
                    ),
                    icon_url = ctx.author.avatar_url
                )
            
                embeds.append(e)

        return embeds

    async def cog_help(self, ctx: commands.Context, cog: commands.Cog) -> list:
        embeds = list()

        commands = list()
        for (command) in cog.get_commands():
            if (not await command.can_run(ctx)):
                continue

            if (not ctx.author.id == ctx.bot._settings.owner):
                if (command.hidden):
                    continue

            commands.append(command)

        for (i, chunk) in enumerate(_chunks(commands, COMMANDS_PER_PAGE), 1):
            color = ctx.guild.me.color if ctx.guild else discord.Color.blurple()
            e = discord.Embed(color = color)

            e.set_author(
                name="{0} ({1}-{2} / {3})".format(
                    cog.qualified_name,
                    (i * COMMANDS_PER_PAGE) - (COMMANDS_PER_PAGE - 1),
                    min([i * COMMANDS_PER_PAGE, len(commands)]),
                    len(commands)
                )
            )

            if (cog.__doc__):
                e.description = cog.__doc__

            for (command) in chunk:
                signature = "{0}{1} {2}".format(ctx.prefix, command.qualified_name, command.signature)

                help = command.short_doc
                if (not help):
                    help = "no description"

                e.add_field(name=signature, value=help, inline=False)

            e.set_footer(
                text = "{0} | {1}".format(
                    ctx.author.name,
                    format.humanize_datetime()
                ),
                icon_url = ctx.author.avatar_url
            )
            
            embeds.append(e)

        return embeds

    async def command_help(self, ctx: commands.Context, command: commands.Command) -> list:
        embeds = list()

        if (hasattr(command, "commands")):
            commands = list()
            for (command_) in command.commands:
                if (not await command_.can_run(ctx)):
                    continue

                if (not ctx.author.id == ctx.bot._settings.owner):
                    if (command_.hidden):
                        continue

                commands.append(command_)

            for (i, chunk) in enumerate(_chunks(commands, COMMANDS_PER_PAGE), 1):
                color = ctx.guild.me.color if ctx.guild else discord.Color.blurple()
                e = discord.Embed(color = color)

                if (command.aliases):
                    if (len(command.qualified_name.split(" ")) != 1):
                        command_ = "{0} ".format(" ".join(command.qualified_name.split(" ")[:-1]))
                    else:
                        command_ = ""

                    aliases = "|".join(command.aliases)
                    signature = "{0}{1}[{2}|{3}] {4}".format(ctx.prefix, command_, command.name, aliases, command.signature)
                else:
                    signature = "{0}{1} {2}".format(ctx.prefix, command.qualified_name, command.signature)

                e.set_author(
                    name="{0} ({1}-{2} / {3})".format(
                        signature,
                        (i * COMMANDS_PER_PAGE) - (COMMANDS_PER_PAGE - 1),
                        min([i * COMMANDS_PER_PAGE, len(commands)]),
                        len(commands)
                    )
                )

                if (command.short_doc):
                    e.description = command.short_doc

                for (command) in chunk:
                    signature = "{0}{1} {2}".format(ctx.prefix, command.qualified_name, command.signature)

                    help = command.short_doc
                    if (not help):
                        help = "no description"

                    e.add_field(name=signature, value=help, inline=False)

                e.set_footer(
                    text = "{0} | {1}".format(
                        ctx.author.name,
                        format.humanize_datetime()
                    ),
                    icon_url = ctx.author.avatar_url
                )
            
                embeds.append(e)
        else:
            if (not await command.can_run(ctx)):
                return list()
        
            if (not ctx.author.id == ctx.bot._settings.owner):
                if (command.hidden):
                    return list()

            color = ctx.guild.me.color if ctx.guild else discord.Color.blurple()
            e = discord.Embed(color = color)

            e.set_author(name = "{0}{1} {2}".format(ctx.prefix, command.qualified_name, command.signature))

            if (command.help):
                e.description = command.help

            e.set_footer(
                text = "{0} | {1}".format(
                    ctx.author.name,
                    format.humanize_datetime()
                ),
                icon_url = ctx.author.avatar_url
            )

            embeds.append(e)

        return embeds

    async def paginate(self, ctx: commands.Context, input_: list):
        if (len(input_) == 0):
            await self.paginate(ctx, await self.all_help(ctx))
            return

        try:
            help = await ctx.send(embed = input_[0])
        except (AttributeError, TypeError) as e:
            await ctx.send(embed = input_)
            ctx.command.reset_cooldown(ctx)
            return

        if (len(input_) == 1):
            ctx.command.reset_cooldown(ctx)
            return

        current = 0
    
        reactions = [
            "\U000023ee",
            "\U000023ea",
            "\U00000023\U000020e3",
            "\U000023e9",
            "\U000023ed",
            "\U0001f5d1",
        ]

        for (reaction) in reactions:
            await help.add_reaction(reaction)
        
        while (True):
            def check(reaction: discord.Reaction, member: discord.Member):
                if (member == ctx.author):
                    if (reaction.message.id == help.id):
                        if (str(reaction.emoji) in reactions):
                            return True

            tasks = {
                asyncio.create_task(ctx.bot.wait_for("reaction_add", check=check, timeout=120)),
                asyncio.create_task(ctx.bot.wait_for("reaction_remove", check=check, timeout=120)),
            }

            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

            try:
                reaction, _ = done.pop().result()
            except (asyncio.TimeoutError) as e:
                try:
                    await help.clear_reactions()
                except (discord.Forbidden) as e:
                    pass

                return

            for (task) in pending:
                task.cancel()

            if (str(reaction.emoji) == reactions[0]):
                if (current == 0):
                    try:
                        await help.remove_reaction(str(reaction.emoji), ctx.author)
                    except (discord.Forbidden) as e:
                        pass

                    continue

                current = 0
            elif (str(reaction.emoji) == reactions[1]):
                current -= 1
                if (current < 0):
                    current = len(input_) - 1
            elif (str(reaction.emoji) == reactions[2]):
                def check(message: discord.Message):
                    if (message.author == ctx.author):
                        if (message.channel == ctx.channel):
                            if (message.content.isdigit()):
                                if (int(message.content) >= 1):
                                    if (int(message.content) <= len(input_)):
                                        return True

                message = await ctx.send("choose a page (1-{0})".format(len(input_)))

                try:
                    page = await ctx.bot.wait_for("message", check=check, timeout=60)
                except (asyncio.TimeoutError) as e:
                    await message.delete()

                    try:
                        await help.remove_reaction(str(reaction.emoji), ctx.author)
                    except (discord.Forbidden) as e:
                        pass

                    continue

                await message.delete()

                try:
                    await page.delete()
                except (discord.Forbidden) as e:
                    pass

                if (current == (int(page.content) - 1)):
                    continue
            
                current = int(page.content) - 1
            elif (str(reaction.emoji) == reactions[3]):
                current += 1
                if (current > (len(input_) - 1)):
                    current = 0
            elif (str(reaction.emoji) == reactions[4]):
                if (current == (len(input_) - 1)):
                    try:
                        await help.remove_reaction(str(reaction.emoji), ctx.author)
                    except (discord.Forbidden) as e:
                        pass

                    continue

                current = len(input_) - 1
            elif (str(reaction.emoji) == reactions[5]):
                try:
                    await help.clear_reactions()
                except (discord.Forbidden) as e:
                    pass

                ctx.command.reset_cooldown(ctx)
                return

            try:
                await help.remove_reaction(str(reaction.emoji), ctx.author)
            except (discord.Forbidden) as e:
                pass

            await help.edit(embed=input_[current])

    async def send_old_help(self, ctx: commands.Context, thing: str = None):
        if (thing):
            command = ctx.bot.get_command(thing)
            if (command):
                await ctx.send_help(command)
                return
            
            cog = ctx.bot.get_cog(thing)
            if (cog):
                await ctx.send_help(cog)
                return

        await ctx.send_help()


def setup(bot: commands.Bot):
    extension = Help(bot)
    bot.add_cog(extension)