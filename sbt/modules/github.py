"""
/modules/github.py

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

__level__             = 3


import discord
from discord.ext import commands

from utils import (
    format,
    regex,
)


class GitHub(commands.Cog, name="github"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot._extensions.add_extension(self)

        self.__authors__ = __authors__
        self.__maintainers__ = __maintainers__
        self.__version_info__ = __version_info__
        self.__version__ = __version__
        self.__level__ = __level__

        super().__init__()

    def cog_unload(self):
        del self.bot._extensions.extensions[self.qualified_name]

    @commands.group(name="github", aliases=["gh"], invoke_without_command=True)
    async def _github(self, ctx: commands.Context):
        """
        display github link
        """

        github = ctx.bot._settings.github
        await ctx.send(format.wrap_url(github))

    @_github.command(name="close")
    async def _github_close(self, ctx: commands.Context, id: int, *labels: str):
        """
        close a github issue with optional labels
        """

        pass

    @_github.command(name="open")
    async def _github_open(self, ctx: commands.Context, id: int):
        """
        open a github issue
        """

        pass

    @_github.group(name="labels", aliases=["label"], invoke_without_command=True)
    async def _github_labels(self, ctx: commands.Context, id: int):
        """
        show labels for a github issue
        """

        pass

    @_github_labels.command(name="add")
    async def _github_labels_add(self, ctx: commands.Context, id: int, *labels: str):
        """
        add labels to a github issue
        """

        pass

    @_github_labels.command(name="remove")
    async def _github_labels_remove(self, ctx: commands.Context, id: int, *labels: str):
        """
        remove labels from a github issue
        """

        pass

    async def on_message(self, message: discord.Message):
        if ((message.guild) and (message.guild.id == self.bot._settings.debugging_guild)):
            match = regex.Regex.ISSUE.search(message.content)
            if (match):
                url = "https://github.com/ShineyDev/sbt/issues/{0}"
                await message.channel.send(url.format(match.group("number")))
                

def setup(bot: commands.Bot):
    extension = GitHub(bot)

    bot.add_cog(extension)
    bot.add_listener(extension.on_message, "on_message")