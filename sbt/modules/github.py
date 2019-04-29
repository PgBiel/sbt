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


VALID_LOCK_REASONS = {
    "off-topic",
    "too heated",
    "resolved",
    "spam",
}


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

        json = {
            "state": "closed",
        }

        # https://developer.github.com/v3/issues/#edit-an-issue
        url = "repos/ShineyDev/sbt/issues/{0}".format(id)

        try:
            await self.request("PATCH", url, json=json)
        except (GitHubError) as e:
            await ctx.send("`{0}: {1}`".format(type(e).__name__, str(e)))
            return

        await ctx.send("done.")
    
    @checks.is_supervisor()
    @checks.is_debugging()
    @_github_issue.group(name="labels", aliases=["label"], invoke_without_command=True)
    async def _github_issue_labels(self, ctx: commands.Context, id: typing.Optional[int]):
        """
        show labels for a github issue
        """

        if (not id):
            # https://developer.github.com/v3/issues/labels/#list-all-labels-for-this-repository
            url = "repos/ShineyDev/sbt/labels"
        else:
            # https://developer.github.com/v3/issues/labels/#list-labels-on-an-issue
            url = "repos/ShineyDev/sbt/issues/{0}/labels".format(id)

        try:
            labels = await self.request("GET", url)
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

        json = {
            "labels": list(labels),
        }
        
        # https://developer.github.com/v3/issues/labels/#add-labels-to-an-issue
        url = "repos/ShineyDev/sbt/issues/{0}/labels".format(id)

        try:
            await self.request("POST", url, json=json)
        except (GitHubError) as e:
            await ctx.send("`{0}: {1}`".format(type(e).__name__, str(e)))
            return

        await ctx.send("done.")
    
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

        # we gotta do some weird shit for this one because there are
        # only endpoints for removing one or all labels from an issue,
        # so we have to get current labels, remove `labels` and then
        # PUT that back into the issue :/

        # https://developer.github.com/v3/issues/labels/#list-labels-on-an-issue
        url = "repos/ShineyDev/sbt/issues/{0}/labels".format(id)

        try:
            labels_ = await self.request("GET", url)
            labels_ = [l["name"] for (l) in labels_]
        except (GitHubError) as e:
            await ctx.send("`{0}: {1}`".format(type(e).__name__, str(e)))
            return

        for (label) in labels:
            if (label in labels_):
                labels_.remove(label)

        json = {
            "labels": list(labels_),
        }

        # https://developer.github.com/v3/issues/labels/#replace-all-labels-for-an-issue
        url = "repos/ShineyDev/sbt/issues/{0}/labels".format(id)

        try:
            await self.request("PUT", url, json=json)
        except (GitHubError) as e:
            await ctx.send("`{0}: {1}`".format(type(e).__name__, str(e)))
            return

        await ctx.send("done.")
    
    @checks.is_supervisor()
    @checks.is_debugging()
    @_github_issue.command(name="list")
    async def _github_issue_list(self, ctx: commands.Context):
        """
        list open issues
        """

        # https://developer.github.com/v3/issues/#list-issues-for-a-repository
        url = "repos/ShineyDev/sbt/issues"

        try:
            issues = await self.request("GET", url)
        except (GitHubError) as e:
            await ctx.send("`{0}: {1}`".format(type(e).__name__, str(e)))
            return

        message = ""

        for (issue) in issues:
            if (issue.get("pull_request")):
                # not an issue, i will never understand why prs show as
                # issues ¯\_(ツ)_/¯
                continue
            elif (issue.get("state") == "closed"):
                continue

            url = format.wrap_url(issue.get("html_url"))
            message += "{0}\n".format(url)

        if (not message):
            await ctx.send("none")
            return

        for (page) in format.pagify(message):
            if (page):
                await ctx.send(page)
    
    @checks.is_supervisor()
    @checks.is_debugging()
    @_github_issue.command(name="lock")
    async def _github_issue_lock(self, ctx: commands.Context, id: int, reason: str):
        """
        lock an issue
        """

        if (reason not in VALID_LOCK_REASONS):
            await ctx.send("reason must be one of\n{0}".format(
                ", ".join(VALID_LOCK_REASONS)))
            return

        json = {
            "locked": True,
            "active_lock_reason": reason,
        }

        # https://developer.github.com/v3/issues/#lock-an-issue
        url = "repos/ShineyDev/sbt/issues/{0}/lock".format(id)

        try:
            await self.request("PUT", url, json=json)
        except (GitHubError) as e:
            await ctx.send("`{0}: {1}`".format(type(e).__name__, str(e)))
            return

        await ctx.send("done.")
    
    @checks.is_supervisor()
    @checks.is_debugging()
    @_github_issue.command(name="open")
    async def _github_issue_open(self, ctx: commands.Context, id: int):
        """
        open a github issue
        """

        json = {
            "state": "open",
        }

        # https://developer.github.com/v3/issues/#edit-an-issue
        url = "repos/ShineyDev/sbt/issues/{0}".format(id)

        try:
            await self.request("PATCH", url, json=json)
        except (GitHubError) as e:
            await ctx.send("`{0}: {1}`".format(type(e).__name__, str(e)))
            return

        await ctx.send("done.")
    
    @checks.is_supervisor()
    @checks.is_debugging()
    @_github_issue.command(name="unlock")
    async def _github_issue_unlock(self, ctx: commands.Context, id: int):
        """
        unlock an issue
        """

        # https://developer.github.com/v3/issues/#unlock-an-issue
        url = "repos/ShineyDev/sbt/issues/{0}/lock".format(id)

        try:
            await self.request("DELETE", url)
        except (GitHubError) as e:
            await ctx.send("`{0}: {1}`".format(type(e).__name__, str(e)))
            return

        await ctx.send("done.")
    
    @checks.is_supervisor()
    @checks.is_debugging()
    @_github.command(name="labels")
    async def _github_labels(self, ctx: commands.Context):
        """
        show labels for the sbt repo
        """

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
                url = "{0}/issues/{1}/".format(self.bot._settings.github, match.group("number"))
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

            if ((response.status == 429) or (remaining == "0")):
                raise GitHubError("ratelimit exceeded")
            elif (300 > response.status >= 200):
                try:
                    json_ = await response.json()
                    return json_
                except (aiohttp.ContentTypeError) as e:
                    pass
            else:
                try:
                    json_ = await response.json()
                    raise GitHubError(json_["message"])
                except (aiohttp.ContentTypeError) as e:
                    pass

        if (not session):
            await session_.close()
                

def setup(bot: commands.Bot):
    extension = GitHub(bot)

    bot.add_cog(extension)
    bot.add_listener(extension.on_message, "on_message")