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

__authors__      = [("shineydev", "contact@shiney.dev")]
__maintainers__  = [("shineydev", "contact@shiney.dev")]

__version_info__ = (2, 0, 0, "alpha", 0)
__version__      = "{0}.{1}.{2}{3}{4}".format(*[str(n)[0] if (i == 3) else str(n) for (i, n) in enumerate(__version_info__)])

__level__        = 3

__all__ = {
    "GitHub", "setup",
}


import aiohttp
import typing
import yarl

import discord
from discord.ext import commands

from utils import (
    checks,
    format,
    regex,
)


class GitHubError(Exception):
    pass


class GitHub(commands.Cog, name="github"):
    __all__ = {
        "__init__", "_github", "_github_issue",
        "_github_issue_close", "_github_issue_open",
        "_github_issue_labels", "_github_issue_labels_add",
        "_github_issue_labels_remove", "_github_pulls",
    }

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.__authors__ = __authors__
        self.__maintainers__ = __maintainers__
        self.__version_info__ = __version_info__
        self.__version__ = __version__
        self.__level__ = __level__

        super().__init__()

    @commands.group(name="github", aliases=["gh"], invoke_without_command=True)
    async def _github(self, ctx: commands.Context):
        """
        display github link
        """

        url = "{0}/".format(ctx.bot._settings.github)
        await ctx.send(format.wrap_url(url))

    @checks.is_debugging()
    @_github.group(name="issue", aliases=["issues"], invoke_without_command=True)
    async def _github_issue(self, ctx: commands.Context, id: typing.Optional[int]):
        """
        show a github issue
        """

        if (ctx.invoked_with == "issues"):
            url = "{0}/issues/".format(ctx.bot._settings.github)
        else:
            if (not id):
                await ctx.bot.send_help(ctx)
                return

            url = "{0}/issues/{1}/".format(ctx.bot._settings.github, id)

        await ctx.send(format.wrap_url(url))
        
    @checks.is_supervisor()
    @checks.is_debugging()
    @_github_issue.command(name="close")
    async def _github_issue_close(self, ctx: commands.Context, id: int):
        """
        close a github issue
        """

        pass
    
    @checks.is_supervisor()
    @checks.is_debugging()
    @_github_issue.command(name="open")
    async def _github_issue_open(self, ctx: commands.Context, id: int):
        """
        open a github issue
        """

        pass
    
    @checks.is_supervisor()
    @checks.is_debugging()
    @_github_issue.group(name="labels", aliases=["label"], invoke_without_command=True)
    async def _github_issue_labels(self, ctx: commands.Context, id: typing.Optional[int]):
        """
        show labels for a github issue
        """

        if (not id):
            try:
                labels = await self.request("GET", "repos/ShineyDev/sbt/labels")
            except (GitHubError) as e:
                await ctx.send("`{0}: {1}`".format(type(e).__name__, str(e)))
                return

            labels = [l["name"] for (l) in labels]

            if (labels):
                await ctx.send(", ".join(labels))
            else:
                await ctx.send("none")
        else:
            try:
                labels = await self.request("GET", "/repos/ShineyDev/sbt/issues/{0}/labels".format(id))
            except (GitHubError) as e:
                await ctx.send("`{0}: {1}`".format(type(e).__name__, str(e)))
                return

            labels = [l["name"] for (l) in labels]

            if (labels):
                await ctx.send(", ".join(labels))
            else:
                await ctx.send("none")
    
    @checks.is_supervisor()
    @checks.is_debugging()
    @_github_issue_labels.command(name="add")
    async def _github_issue_labels_add(self, ctx: commands.Context, id: int, *labels: str):
        """
        add labels to a github issue
        """

        if (not labels):
            await ctx.send("no labels were given")
            return

        pass
    
    @checks.is_supervisor()
    @checks.is_debugging()
    @_github_issue_labels.command(name="remove")
    async def _github_issue_labels_remove(self, ctx: commands.Context, id: int, *labels: str):
        """
        remove labels from a github issue
        """

        if (not labels):
            await ctx.send("no labels were given")
            return

        pass
    
    @checks.is_supervisor()
    @checks.is_debugging()
    @_github.command(name="labels")
    async def _github_labels(self, ctx: commands.Context):
        await ctx.invoke(self._github_issue_labels, id=None)
    
    @checks.is_debugging()
    @_github.command(name="pulls", aliases=["pr", "prs"])
    async def _github_pulls(self, ctx: commands.Context):
        """
        show pull requests
        """

        url = "{0}/pulls/".format(ctx.bot._settings.github)
        await ctx.send(format.wrap_url(url))

    async def on_message(self, message: discord.Message):
        if ((message.guild) and (message.guild.id == self.bot._settings.debugging_guild)):
            match = regex.Regex.ISSUE.search(message.content)
            if (match):
                url = "{0}/issues/{1}".format(self.bot._settings.github, match.group("number"))
                await message.channel.send(format.wrap_url(url))

    async def request(self, method: str, url: str, *, json: dict = None, headers: dict = None, session: aiohttp.ClientSession = None):
        if (not session):
            session_ = aiohttp.ClientSession()
        else:
            session_ = session

        headers_ = {
            "User-Agent": "sbt-github-manager",
            "Authorization": "token {0}".format(self.bot._settings.github_api_key)
        }

        if (headers):
            headers_.update(headers)

        url = yarl.URL("https://api.github.com") / url

        async with session_.request(method, url, json=json, headers=headers_) as response:
            remaining = response.headers.get("X-Ratelimit-Remaining")
            json_ = await response.json()

            if ((response.status == 429) or (remaining == "0")):
                raise GitHubError("ratelimit exceeded")
            elif (300 > response.status >= 200):
                return json_
            else:
                raise GitHubError(json_["message"])

        if (not session):
            await session_.close()
                

def setup(bot: commands.Bot):
    extension = GitHub(bot)

    bot.add_cog(extension)
    bot.add_listener(extension.on_message, "on_message")