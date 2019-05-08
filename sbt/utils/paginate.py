"""
/utils/paginate.py

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

__all__ = {
    "cog_sort",
    "command_sort",
    "_cog_commands_embedinator",
    "_command_commands_embedinator",
    "_command_embedinator",
    "help",
    "cog_help",
    "command_help",
    "Button",
    "Menu",
    "LongMenu",
}


import asyncio
import collections
import typing

import discord
from discord.ext import commands

from utils import (
    context,
)


def _cog_sort(cog: tuple) -> str:
    return cog[0]

def _command_sort(command: commands.Command) -> tuple:
    return (isinstance(comamnd, commands.Group), command.name)

def _cog_commands_embedinator(cog: commands.Cog, commands_: list) -> list:
    embeds = list()

    ...

    return embeds

def _command_commands_embedinator(command: commands.Command, commands_: list) -> list:
    embeds = list()

    ...

    return embeds

def _command_embedinator(command: commands.command) -> list:
    ...

    return [e]

async def help(ctx: commands.Context) -> list:
    embeds = list()

    cogs = dict()
    for (_, cog) in ctx.bot.cogs.items():
        commands_ = list()
        for (command) in cog.get_commands():
            if (not await command.can_run(ctx)):
                continue
            elif (command.hidden):
                continue

            commands_.append(command)
        if (commands_):
            # just don't add the cog if it's empty
            commands_.sort(key=_command_sort)
            cogs[cog.__cog_name__] = (cog, commands_)

    cogs = dict(sorted(cogs, key=_cog_sort))

    # at this point we have Dict<cog_name, (cog, List<commands.Command, ...>)>
    # which has 'cogs' sorted 0-9a-z by name and commands sorted by
    # command type and then 0-9a-z by name
    
    for (_, (cog, commands_)) in cogs:
        embeds.extend(_cog_commands_embedinator(cog, commands_))

    return embeds

async def cog_help(ctx: commands.Context, cog: commands.Cog) -> list:
    commands_ = list()
    for (command) in cog.get_commands():
        if (not await command.can_run(ctx)):
            continue
        elif (command.hidden):
            continue

        commands_.append(command)

    if (commands_):
        commands_.sort(key=_command_sort)

    # at this point we have List<commands.Command, ...> which has
    # commands sorted by command type and then 0-9a-z

    return _cog_commands_embedinator(cog, commands_)

async def command_help(ctx: commands.Context, command: commands.Command) -> list:
    if (isinstance(command, commands.Group)):
        commands_ = list()
        for (command_) in command.commands:
            if (not await command_.can_run(ctx)):
                continue
            elif (command_.hidden):
                continue

            commands_.append(command_)

        if (commands_):
            commands_.sort(key=_command_sort)

        # at this point we have List<commands.Command, ...> which has
        # commands sorted by command type and then 0-9a-z

        return _command_commands_embedinator(command, commands_)
    else:
        return _command_embedinator(command)


class Button():
    __all__ = {
        "__init__",
    }

    def __init__(self, callback: typing.Callable, *, emoji: str):
        self.callback = callback
        self.emoji = emoji

class Menu():
    __all__ = {
        "__init__",
        "append",
        "appends",
        "appendleft",
        "appendlefts",
        "pop",
        "pops",
        "popleft",
        "poplefts",
        "start",
        "stop",
        "send",
        "edit",
        "register_buttons",
        "_check_buttons",
        "_add_buttons",
        "_remove_buttons",
        "_back",
        "_choose",
        "_forward",
        "_close",
    }

    def __init__(self, ctx: commands.Context):
        self.ctx = ctx
        self._pages = collections.deque()
        self._index = 0

    def append(self, page: typing.Union[dict, str, discord.Embed]):
        if (isinstance(page, str)):
            page = {"content": page}
        elif (isinstance(page, discord.Embed)):
            page = {"embed": page}

        self._pages.append(page)

    def appends(self, pages: list):
        for (page) in pages:
            self.append(page)

    def appendleft(self, page: typing.Union[dict, str, discord.Embed]):
        if (isinstance(page, str)):
            page = {"content": page}
        elif (isinstance(page, discord.Embed)):
            page = {"embed": page}

        self._pages.appendleft(page)

    def appendlefts(self, pages: list):
        for (page) in pages:
            self.appendleft(page)

    def pop(self, index: int) -> dict:
        if (not self._pages):
            raise RuntimeError("this menu contains no pages")
        elif (index not in range(len(self._pages) - 1)):
            raise IndexError("index out of range")

        return self._pages.pop(index)

    def pops(self, indexes: list) -> list:
        popped = list()

        for (page) in pages:
            popped.append(self.pop(page))

        return popped

    def popleft(self, index: int) -> dict:
        if (not self._pages):
            raise RuntimeError("this menu contains no pages")
        elif (index not in range(len(self._pages) - 1)):
            raise IndexError("index out of range")

        return self._pages.popleft(index)

    def poplefts(self, indexes: list) -> list:
        popped = list()

        for (page) in pages:
            popped.append(self.popleft(page))

        return popped

    async def start(self):
        if (not self._pages):
            raise RuntimeError("this menu contains no pages")

        self._message = await self.send(self._pages[self._index])

        if (len(self._pages) == 1):
            return

        await self.register_buttons()
        await self._check_buttons()
        await self._add_buttons()

        def message_check(message: discord.Message):
            if (message.author.id == self.ctx.bot._settings.owner):
                return True
            elif (message.author.id in self.ctx.bot._settings.supervisors):
                return True
            elif (message.author == self.ctx.author):
                if (message.channel == self.ctx.channel):
                    return True

        def reaction_check(reaction: discord.Reaction, user: discord.User):
            if (user.id == self.ctx.bot._settings.owner):
                return True
            elif (user.id in self.ctx.bot._settings.supervisors):
                return True
            elif (user == self.ctx.author):
                if (reaction.message == self._message):
                    if (str(reaction.emoji) in [b.emoji for b in self._buttons]):
                        return True

        self._stopped = False
        while (not self._stopped):
            tasks = {
                asyncio.create_task(self.ctx.bot.wait_for("reaction_add", check=reaction_check)),
                asyncio.create_task(self.ctx.bot.wait_for("reaction_remove", check=reaction_check)),
            }

            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED, timeout=120)

            try:
                reaction, _ = done.pop().result()
            except (asyncio.TimeoutError):
                await self.stop()
                break

            for (task) in pending:
                task.cancel()

            dict_ = {
                button.emoji: button.callback
                for button in self._buttons
            }

            callback = dict_[str(reaction.emoji)]
            page = await callback()

            #with context.Suppress(discord.Forbidden):
            #    await self.ctx.message.remove_reaction(str(reaction.emoji), self.ctx.author)
            #
            # i'm removing this with indirect advice from Danny,
            # removing the reaction here and then waiting for removed
            # reactions later on causes unnecessary race conditions
            #
            # i will consider this my warning not to bring this back

            if (page):
                await self.edit(page)

        await self._remove_buttons()

    async def stop(self):
        self._stopped = True

    async def send(self, page: dict):
        content = page.get("content", None)
        embed = page.get("embed", None)

        if (not isinstance(content, str)):
            raise RuntimeError("content should be of type 'str'")
        elif (not isinstance(embed, discord.Embed)):
            raise RuntimeError("embed should be of type 'discord.Embed'")

        await self.ctx.send(content=content, embed=embed)

    async def edit(self, page: dict):
        if (not hasattr(self, "_message")):
            raise RuntimeError("menu has no message to update")

        content = page.get("content", None)
        embed = page.get("embed", None)

        if (not isinstance(content, str)):
            raise RuntimeError("content should be of type 'str'")
        elif (not isinstance(embed, discord.Embed)):
            raise RuntimeError("embed should be of type 'discord.Embed'")

        await self._message.edit(content=content, embed=embed)

    async def register_buttons(self):
        """
        this method should be overridden in subclasses and defines the
        buttons that will be used by the menu
        """

        self._buttons = [
            Button(self._back, emoji="\U000025c0"),
            Button(self._choose, emoji="\U00000023\U000020e3"),
            Button(self._forward, emoji="\U000025b6"),
            Button(self._close, emoji="\U0001f5d1"),
        ]

    async def _check_buttons(self):
        for (button) in self.buttons:
            if (not callable(button.callback)):
                raise RuntimeError("button.callback should be a callable")
            elif (not asyncio.iscoroutine(button.callback)):
                raise RuntimeError("button.callback should be a coroutine")

    async def _add_buttons(self):
        try:
            for (button) in self._buttons:
                await self.ctx.message.add_reaction(button.emoji)
        except (discord.Forbidden):
            await self.stop()
            raise

    async def _remove_buttons(self):
        try:
            await self.ctx.message.clear_reactions()
        except (discord.Forbidden) as e:
            for (button) in self._buttons:
                with context.Suppress(discord.Forbidden):
                    await self.ctx.message.remove_reaction(button.emoji)

    """
    all methods from this point are button methods
    """

    async def _back(self) -> int:
        ...
        
    async def _choose(self) -> int:
        ...
        
    async def _forward(self) -> int:
        ...
        
    async def _close(self) -> int:
        await self.stop()

class LongMenu(Menu):
    __all__ = {
        "register_buttons",
        "_back_all",
        "_back_5",
        "_back",
        "_choose",
        "_forward",
        "_forward_5",
        "_forward_all",
        "_close",
    }

    async def register_buttons(self):
        self._buttons = [
            Button(self._back_all, emoji="\U000023ee"),
            Button(self._back_5, emoji="\U000023ea"),
            Button(self._back, emoji="\U000025c0"),
            Button(self._choose, emoji="\U00000023\U000020e3"),
            Button(self._forward, emoji="\U000025b6"),
            Button(self._forward_5, emoji="\U000023e9"),
            Button(self._forward_all, emoji="\U000023ed"),
            Button(self._close, emoji="\U0001f5d1"),
        ]

    """
    all methods from this point are button methods
    """

    async def _back_all(self) -> int:
        ...

    async def _back_5(self) -> int:
        ...

    async def _back(self) -> int:
        await super()._back()
        
    async def _choose(self) -> int:
        await super()._choose()
        
    async def _forward(self) -> int:
        await super()._forward()
        
    async def _forward_5(self) -> int:
        ...
        
    async def _forward_all(self) -> int:
        ...
        
    async def _close(self) -> int:
         await super()._close()