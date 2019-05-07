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
        "appendleft",
        "pop",
        "popleft",
        "start",
        "stop",
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

    def append(self, page: dict):
        self._pages.append(page)

    def appendleft(self, page: dict):
        self._pages.appendleft(page)

    def pop(self, index: int):
        if (not self._pages):
            raise RuntimeError("this menu contains no pages")
        elif (index not in range(len(self._pages) - 1)):
            raise IndexError("index out of range")

        self._pages.pop(index)

    def popleft(self, index: int):
        if (not self._pages):
            raise RuntimeError("this menu contains no pages")
        elif (index not in range(len(self._pages) - 1)):
            raise IndexError("index out of range")

        self._pages.popleft(index)

    async def start(self):
        if (not self._pages):
            raise RuntimeError("this menu contains no pages")

        await self.send(self._pages[0])

        if (len(self._pages) == 1):
            return

        await self.register_buttons()
        await self._check_buttons()
        await self._add_buttons()

        self._stopped = False
        while (not self._stopped):
            ...

        await self._remove_buttons()

    async def stop(self):
        self._stopped = True

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

    async def _back(self):
        ...
        
    async def _choose(self):
        ...
        
    async def _forward(self):
        ...
        
    async def _close(self):
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

    async def _back_all(self):
        ...

    async def _back_5(self):
        ...

    async def _back(self):
        await super()._back()
        
    async def _choose(self):
        await super()._choose()
        
    async def _forward(self):
        await super()._forward()
        
    async def _forward_5(self):
        ...
        
    async def _forward_all(self):
        ...
        
    async def _close(self):
         await super()._close()