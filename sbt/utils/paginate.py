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
    "_chunk",
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
    format,
)


def _chunk(iterable: typing.Iterable, chunk_size: int):
    for (i) in range(0, len(iterable), chunk_size):
        yield iterable[i:i + chunk_size]


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
        "register_checks",
        "_check_checks",
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

        await self.register_checks()
        await self._check_checks()
        await self.register_buttons()
        await self._check_buttons()
        await self._add_buttons()

        self._stopped = False
        while (not self._stopped):
            tasks = {
                asyncio.create_task(self.ctx.bot.wait_for("reaction_add", check=self._reaction_check)),
                asyncio.create_task(self.ctx.bot.wait_for("reaction_remove", check=self._reaction_check)),
            }

            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED, timeout=120)

            try:
                reaction, _ = done.pop().result()
            except (Exception) as e:
                await self.stop()
                break

            for (task) in pending:
                task.cancel()

            dict_ = {
                button.emoji: button.callback
                for button in self._buttons
            }

            callback = dict_[str(reaction.emoji)]
            index = await callback()

            # with context.Suppress(discord.Forbidden):
            #     await self.ctx.message.remove_reaction(str(reaction.emoji), self.ctx.author)
            #
            # i'm removing this with indirect advice from Danny,
            # removing the reaction here and then waiting for removed
            # reactions later on causes unnecessary race conditions
            #
            # i will consider this my warning not to bring this back

            if (index != None):
                if (index != self._index):
                    self._index = index
                    await self.edit(self._pages[index])

        await self._remove_buttons()

    async def stop(self):
        self._stopped = True

    async def send(self, page: dict):
        content = page.get("content", None)
        embed = page.get("embed", None)

        if (not isinstance(embed, (discord.Embed, None))):
            raise RuntimeError("embed should be of type 'discord.Embed' or None")

        message = await self.ctx.send(content=content, embed=embed)
        return message

    async def edit(self, page: dict):
        if (not hasattr(self, "_message")):
            raise RuntimeError("menu has no message to update")

        content = page.get("content", None)
        embed = page.get("embed", None)

        if (not isinstance(embed, (discord.Embed, None))):
            raise RuntimeError("embed should be of type 'discord.Embed' or None")

        await self._message.edit(content=content, embed=embed)

    async def register_checks(self):
        def message_check(message: discord.Message):
            if (message.author.id == self.ctx.bot._settings.owner):
                return True
            elif (message.author.id in self.ctx.bot._settings.supervisors):
                return True
            elif (message.author.id == self.ctx.author.id):
                if (message.channel.id == self.ctx.channel.id):
                    return True

        self._message_check = message_check

        def reaction_check(reaction: discord.Reaction, user: discord.User):
            if (user.id == self.ctx.bot._settings.owner):
                return True
            elif (user.id in self.ctx.bot._settings.supervisors):
                return True
            elif (user.id == self.ctx.author.id):
                if (reaction.message.id == self._message.id):
                    if (str(reaction.emoji) in [b.emoji for b in self._buttons]):
                        return True

        self._reaction_check = reaction_check

    async def _check_checks(self):
        if (not hasattr(self, "_message_check")):
            raise RuntimeError("missing self._message_check")
        elif (not callable(self._message_check)):
            raise RuntimeError("self._reaction_check must be a callable")
        elif (not hasattr(self, "_reaction_check")):
            raise RuntimeError("missing self._reaction_check")
        elif (not callable(self._reaction_check)):
            raise RuntimeError("self._reaction_check must be a callable")

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
        for (button) in self._buttons:
            if (not callable(button.callback)):
                raise RuntimeError("button.callback should be a callable")

    async def _add_buttons(self):
        try:
            for (button) in self._buttons:
                await self._message.add_reaction(button.emoji)
        except (discord.Forbidden):
            await self.stop()
            raise

    async def _remove_buttons(self):
        try:
            await self._message.clear_reactions()
        except (discord.Forbidden) as e:
            for (button) in self._buttons:
                with context.Suppress(discord.Forbidden):
                    await self._message.remove_reaction(button.emoji, ctx.bot.user)

    """
    all methods from this point are button methods
    """

    async def _back(self) -> int:
        index = self._index - 1
        if (index in range(0, len(self._pages))):
            return index
        return len(self._pages) - 1
        
    async def _choose(self) -> int:
        message = await self.ctx.send("choose a page (1-{0})".format(len(self._pages)))

        try:
            page = await self.ctx.bot.wait_for("message", check=self._message_check, timeout=30)
        except (asyncio.TimeoutError) as e:
            await message.delete()
        else:
            await message.delete()
            await page.delete()

            page = page.content
            if (page.isdigit()):
                page = int(page) - 1
                if (page in range(0, len(self._pages))):
                    return page
        
    async def _forward(self) -> int:
        index = self._index + 1
        if (index in range(0, len(self._pages))):
            return index
        return 0
        
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
        return 0

    async def _back_5(self) -> int:
        index = self._index

        for (_) in range(5):
            index -= 1

            if (index not in range(0, len(self._pages))):
                index = len(self._pages) - 1

        return index

    async def _back(self) -> int:
        index = await super()._back()
        return index
        
    async def _choose(self) -> int:
        index = await super()._choose()
        return index
        
    async def _forward(self) -> int:
        index = await super()._forward()
        return index
        
    async def _forward_5(self) -> int:
        index = self._index

        for (_) in range(5):
            index += 1

            if (index not in range(0, len(self._pages))):
                index = 0

        return index
        
    async def _forward_all(self) -> int:
        return len(self._pages) - 1
        
    async def _close(self) -> int:
        index = await super()._close()
        return index