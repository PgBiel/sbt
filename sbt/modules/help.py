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
    "COMMANDS_PER_PAGE",
    "_chunks",
    "Help",
    "setup",
}


import asyncio

import discord
from discord.ext import commands

from utils import (
    format,
    paginate,
)


COMMANDS_PER_PAGE = 6


class Help(commands.Cog, name="help"):
    __all__ = {
        "__init__",
        "cog_unload",
        "_help",
        "_help_cog",
        "_help_command",
        "_help_old",
        "paginate",
        "_format_signature",
        "_cog_commands_embedinator",
        "_command_commands_embedinator",
        "_command_embedinator",
        "_cog_sort",
        "_command_sort",
        "help",
        "cog_help",
        "command_help",
        "_paginate",
        "send_old_help",
    }

    def __init__(self, bot: commands.Bot):
        self.bot = bot

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

    @commands.cooldown(1, 120, commands.cooldowns.BucketType.user)
    @commands.group(name="help", aliases=["h"], hidden=True, invoke_without_command=True)
    async def _help(self, ctx: commands.Context, *, thing: str = None):
        """
        show paginated help

        examples:
            `>help`
            `>help roll`
            `>help general`
        """

        if (ctx.guild and (not ctx.me.guild_permissions.embed_links)
                      and (not ctx.me.guild_permissions.administrator)):
            # we don't have permission to send embeds,
            # send old help instead of raising exceptions
            await self.send_old_help(ctx, thing)
            return

        if (thing):
            cog = ctx.bot.get_cog(thing)
            if (cog):
                embeds = await self.cog_help(ctx, cog)
                await self.paginate(ctx, embeds)
                return

            command = ctx.bot.get_command(thing)
            if (command):
                embeds = await self.command_help(ctx, command)
                await self.paginate(ctx, embeds)
                return

        embeds = await self.help(ctx)
        await self.paginate(ctx, embeds)

    @_help.command(name="cog", aliases=["extension", "module"])
    async def _help_cog(self, ctx: commands.Context, *, cog: str):
        """
        show paginated help for a cog

        example:
            `>help cog general`
        """

        if (ctx.guild and (not ctx.guild.me.guild_permissions.embed_links)
                      and (not ctx.me.guild_permissions.administrator)):
            # we don't have permission to send embeds,
            # send old help instead of raising exceptions
            await self.send_old_help(ctx, cog)
            return

        cog = ctx.bot.get_cog(cog)
        if (cog):
            embeds = await self.cog_help(ctx, cog)
            await self.paginate(ctx, embeds)
            return

        embeds = await self.help(ctx)
        await self.paginate(ctx, embeds)

    @_help.command(name="command")
    async def _help_command(self, ctx: commands.Context, *, command: str):
        """
        show paginated help for a command

        example:
            `>help command roll`
        """

        if (ctx.guild and (not ctx.guild.me.guild_permissions.embed_links)
                      and (not ctx.me.guild_permissions.administrator)):
            # we don't have permission to send embeds,
            # send old help instead of raising exceptions
            await self.send_old_help(ctx, command)
            return

        command = ctx.bot.get_command(command)
        if (command):
            embeds = await self.command_help(ctx, command)
            await self.paginate(ctx, embeds)
            return

        embeds = await self.help(ctx)
        await self.paginate(ctx, embeds)

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

    async def paginate(self, ctx: commands.Context, embeds: list):
        if (len(embeds) > 5):
            menu = paginate.LongMenu
        else:
            menu = paginate.Menu

        menu = menu(ctx)
        menu.appends(embeds)
        await menu.start()

    def _format_signature(self, ctx: commands.Context, command: commands.Command, *, ignore_aliases: bool = False):
        if (command.aliases and (not ignore_aliases)):
            aliases = [command.name]
            aliases.extend(command.aliases)
            aliases = "|".join(aliases)

            if (not command.full_parent_name):
                signature = "{0}[{1}] {2}".format(
                    ctx.prefix, aliases, command.signature)
            else:
                signature = "{0}{1} [{2}] {3}".format(
                    ctx.prefix, command.full_parent_name, aliases, command.signature)
        else:
            if (not command.full_parent_name):
                signature = "{0}{1} {2}".format(
                    ctx.prefix, command.name, command.signature)
            else:
                signature = "{0}{1} {2} {3}".format(
                    ctx.prefix, command.full_parent_name, command.name, command.signature)

        return signature.strip()

    def _cog_commands_embedinator(self, ctx, cog: commands.Cog, commands_: list) -> list:
        embeds = list()

        for (i, chunk) in enumerate(paginate._chunk(commands_, COMMANDS_PER_PAGE), 1):
            color = ctx.me.color if ctx.guild else discord.Color.blurple()
            e = discord.Embed(color=color)
            e.set_author(name="{0} ({1}-{2} / {3})".format(
                "{0} commands".format(cog.qualified_name),
                (i * COMMANDS_PER_PAGE) - (COMMANDS_PER_PAGE - 1),
                min([i * COMMANDS_PER_PAGE, len(commands_)]),
                len(commands_)))

            if (cog.__doc__):
                e.description = cog.__doc__

            for (command_) in chunk:
                e.add_field(name=self._format_signature(ctx, command_, ignore_aliases=True),
                            value=command_.short_doc or "no description",
                            inline=False)

            e.set_footer(
                text = "{0} | {1}".format(
                    ctx.author,
                    format.humanize_datetime(),
                ),
                icon_url = ctx.author.avatar_url,
            )

            embeds.append(e)

        return embeds

    def _command_commands_embedinator(self, ctx, command: commands.Command, commands_: list) -> list:
        embeds = list()

        for (i, chunk) in enumerate(paginate._chunk(commands_, COMMANDS_PER_PAGE), 1):
            color = ctx.me.color if ctx.guild else discord.Color.blurple()
            e = discord.Embed(color=color)
            e.set_author(name="{0} ({1}-{2} / {3})".format(
                self._format_signature(ctx, command),
                (i * COMMANDS_PER_PAGE) - (COMMANDS_PER_PAGE - 1),
                min([i * COMMANDS_PER_PAGE, len(commands_)]),
                len(commands_)))

            if (command.help):
                e.description = command.help

            for (command_) in chunk:
                e.add_field(name=self._format_signature(ctx, command_, ignore_aliases=True),
                            value=command_.short_doc or "no description",
                            inline=False)

            e.set_footer(
                text = "{0} | {1}".format(
                    ctx.author,
                    format.humanize_datetime(),
                ),
                icon_url = ctx.author.avatar_url,
            )

            embeds.append(e)
        
        return embeds

    def _command_embedinator(self, ctx, command: commands.command) -> list:
        color = ctx.me.color if ctx.guild else discord.Color.blurple()
        e = discord.Embed(color=color)
        e.set_author(name=self._format_signature(ctx, command))
    
        if (command.help):
            e.description = command.help

        e.set_footer(
            text = "{0} | {1}".format(
                ctx.author,
                format.humanize_datetime(),
            ),
            icon_url = ctx.author.avatar_url,
        )

        return [e]

    def _cog_sort(self, cog: tuple) -> str:
        return cog[0]

    def _command_sort(self, command: commands.Command) -> tuple:
        return (isinstance(command, commands.Group), command.name)

    async def help(self, ctx: commands.Context) -> list:
        embeds = list()

        # for some reason this kept breaking when i had the sort after this
        # block so i moved it here :)
        cogs = dict(sorted(ctx.bot.cogs.items(), key=self._cog_sort))
        for (cog_name, cog) in cogs.items():
            commands_ = list()
            for (command) in cog.get_commands():
                if (not await command.can_run(ctx)):
                    continue
                elif (command.hidden):
                    continue

                commands_.append(command)

            commands_.sort(key=self._command_sort)
            cogs[cog_name] = (cog, commands_)

        # at this point we have Dict<cog_name, (cog, List<commands.Command, ...>)>
        # which has 'cogs' sorted 0-9a-z by name and commands sorted by
        # command type and then 0-9a-z by name
    
        for (_, (cog, commands_)) in cogs.items():
            embeds.extend(self._cog_commands_embedinator(ctx, cog, commands_))

        return embeds

    async def cog_help(self, ctx: commands.Context, cog: commands.Cog) -> list:
        commands_ = list()
        for (command) in cog.get_commands():
            if (not await command.can_run(ctx)):
                continue
            elif (command.hidden):
                continue

            commands_.append(command)

        if (commands_):
            commands_.sort(key=self._command_sort)

        # at this point we have List<commands.Command, ...> which has
        # commands sorted by command type and then 0-9a-z

        return self._cog_commands_embedinator(ctx, cog, commands_)

    async def command_help(self, ctx: commands.Context, command: commands.Command) -> list:
        if (isinstance(command, commands.Group)):
            commands_ = list()
            for (command_) in command.commands:
                if (not await command_.can_run(ctx)):
                    continue
                elif (command_.hidden):
                    continue

                commands_.append(command_)

            if (commands_):
                commands_.sort(key=self._command_sort)

            # at this point we have List<commands.Command, ...> which has
            # commands sorted by command type and then 0-9a-z

            return self._command_commands_embedinator(ctx, command, commands_)
        else:
            if (not await command.can_run(ctx)):
                return list()

            return self._command_embedinator(ctx, command)

    async def _paginate(self, ctx: commands.Context, input_: list):
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