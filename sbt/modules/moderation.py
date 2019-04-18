"""
/modules/moderation.py

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

__level__             = 1


import asyncio

import discord
from discord.ext import commands

from utils import (
    checks,
)


class Moderation(commands.Cog, name="moderation"):
    def __init__(self, bot : commands.Bot):
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
        
    @checks.is_guild()
    @checks.moderator_or_permissions(ban_members=True)
    @commands.command(name="ban")
    async def _ban(self, ctx : commands.Context, member : discord.Member, *, reason : str = None):
        """
        ban a member

        examples:
            `>ban 310418322384748544`
            `>ban 310418322384748544 spam`
        """

        if (ctx.author != ctx.guild.owner):
            if (member.top_role >= ctx.author.top_role):
                raise commands.errors.MissingPermissions([])

        await member.ban(reason=reason)
        await ctx.send("done.")
    
    @checks.is_guild()
    @checks.moderator_or_permissions(ban_members=True)
    @commands.command(name="hackban", aliases=["idban"])
    async def _hackban(self, ctx : commands.Context, user : discord.User, *, reason : str = None):
        """
        ban a user

        allows you to ban a user who is no longer a member

        examples:
            `>hackban 310418322384748544`
            `>hackban 310418322384748544 spam`
        """

        await ctx.guild.ban(user, reason=reason)
        await ctx.send("done.")
    
    @checks.is_guild()
    @checks.moderator_or_permissions(kick_members=True)
    @commands.command(name="kick")
    async def _kick(self, ctx : commands.Context, member : discord.Member, *, reason : str = None):
        """
        kick a member

        examples:
            `>kick 310418322384748544`
            `>kick 310418322384748544 spam`
        """
        
        if (ctx.author != ctx.guild.owner):
            if (member.top_role >= ctx.author.top_role):
                raise commands.errors.MissingPermissions([])

        await member.kick(reason=reason)
        await ctx.send("done.")
    
    @checks.is_guild()
    @checks.moderator_or_permissions(manage_messages=True)
    @commands.command(name="mute")
    async def _mute(self, ctx : commands.Context, member : discord.Member, seconds : int, *, reason : str = None):
        """
        mute a member

        examples:
            `>mute 310418322384748544`
            `>mute 310418322384748544 spam`
        """
        
        if (ctx.author != ctx.guild.owner):
            if (member.top_role >= ctx.author.top_role):
                raise commands.errors.MissingPermissions([])

        pass
    
    @checks.is_guild()
    @checks.moderator_or_permissions(manage_nicknames=True)
    @commands.command(name="names", aliases=["nicknames"])
    async def _names(self, ctx : commands.Context, member : discord.Member):
        """
        show a member's previous names and nicknames

        examples:
            `>names 310418322384748544`
        """

        pass
    
    @checks.is_guild()
    @checks.moderator_or_permissions(manage_messages=True)
    @commands.command(name="prune", aliases=["clear", "delete", "purge"])
    async def _prune(self, ctx : commands.Context, limit : int):
        """
        prune a number of messages

        example:
            `>prune 5`
        """

        if (ctx.invoked_subcommand):
            return
        
        await ctx.message.delete()
        await ctx.channel.purge(limit=limit)

        message = await ctx.send("done.")
        await asyncio.sleep(1)
        await message.delete()

    @checks.is_guild()
    @checks.moderator_or_permissions(manage_nicknames=True)
    @commands.command(name="rename")
    async def _rename(self, ctx : commands.Context, member : discord.Member, *, name : str = None):
        """
        change a member's nickname

        examples:
            `>rename 310418322384748544`         :: remove current nickname
            `>rename 310418322384748544 st00p1d`
        """

        if (ctx.author != ctx.guild.owner):
            if (member.top_role > ctx.author.top_role):
                raise commands.errors.MissingPermissions([])
            elif (member == ctx.author):
                if (not ctx.author.guild_permissions.change_nickname):
                    raise commands.errors.MissingPermissions([])

        await member.edit(nick=name, reason="edited by {0}".format(ctx.author.name))
        await ctx.send("done.")
        
    @checks.is_guild()
    @checks.moderator_or_permissions(ban_members=True)
    @commands.command(name="softban")
    async def _softban(self, ctx : commands.Context, member : discord.Member, *, reason : str = None):
        """
        ban and unban a member

        utilized to kick while deleting all messages

        examples:
            `>softban 310418322384748544`
            `>softban 310418322384748544 spam`
        """

        if (member.top_role >= ctx.author.top_role):
            raise commands.errors.MissingPermissions([])

        await member.ban(reason=reason)
        await ctx.guild.unban(member, reason=reason)
        await ctx.send("done.")
    
    @checks.is_guild()
    @checks.moderator_or_permissions(ban_members=True)
    @commands.command(name="unban")
    async def _unban(self, ctx : commands.Context, user : discord.User, *, reason : str = None):
        """
        unban a user

        examples:
            `>unban 310418322384748544`
            `>unban 310418322384748544 no more spam :)`
        """
        
        try:
            await ctx.guild.unban(user, reason=reason)
        except (discord.errors.NotFound) as e:
            await ctx.bot.send_help(ctx)
            return

        await ctx.send("done.")
    
    @checks.is_guild()
    @checks.moderator_or_permissions(manage_messages=True)
    @commands.command(name="unmute")
    async def _unmute(self, ctx : commands.Context, member : discord.Member, *, reason : str = None):
        """
        unmute a member

        examples:
            `>unban 310418322384748544`
            `>unban 310418322384748544 no more spam :)`
        """
        
        if (ctx.author != ctx.guild.owner):
            if (member.top_role >= ctx.author.top_role):
                raise commands.errors.MissingPermissions([])

        pass


def setup(bot : commands.Bot):
    extension = Moderation(bot)
    bot.add_cog(extension)