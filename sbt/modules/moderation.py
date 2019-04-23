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
import typing

import discord
from discord.ext import commands

from utils import (
    checks,
    parse,
)


class Moderation(commands.Cog, name="moderation"):
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
        
    @checks.is_guild()
    @checks.moderator_or_permissions(ban_members=True)
    @commands.command(name="ban")
    async def _ban(self, ctx: commands.Context, member: typing.Union[discord.Member, discord.User], days: typing.Optional[int], *, reason: typing.Optional[str]):
        """
        ban a member

        while deleting `days` worth of messages (default: 7)

        examples:
            `>ban 310418322384748544`
            `>ban 310418322384748544 bad`
        """

        if (days):
            if (days < 0):
                days = 0
            elif (days > 7):
                days = 7
        else:
            days = 7

        if (isinstance(member, discord.Member)):
            if (ctx.author != ctx.guild.owner):
                if (member.top_role >= ctx.author.top_role):
                    raise commands.errors.MissingPermissions([])
            elif (member == ctx.guild.owner):
                raise commands.errors.MissingPermissions([])

            if (not reason):
                reason = "{0} was banned by {1}".format(member.id, ctx.author.id)

            await member.ban(reason=reason, delete_message_days=days)
        else:
            if (not reason):
                reason = "{0} was hackbanned by {1}".format(member.id, ctx.author.id)

            await ctx.guild.ban(member, reason=reason, delete_message_days=days)

        await ctx.send("done.")
    
    @checks.is_guild()
    @checks.moderator_or_permissions(ban_members=True)
    @commands.command(name="hackban", aliases=["idban"])
    async def _hackban(self, ctx: commands.Context, user: discord.User, days: typing.Optional[int], *, reason: typing.Optional[str]):
        """
        ban a user

        while deleting `days` worth of messages (default: 0)

        allows you to ban a user who is no longer a member

        examples:
            `>hackban 310418322384748544`
            `>hackban 310418322384748544 spam`
        """

        if (days):
            if (days < 0):
                days = 0
            elif (days > 7):
                days = 7
        else:
            days = 0

        if (not reason):
            reason = "{0} was hackbanned by {1}".format(user.id, ctx.author.id)

        await ctx.guild.ban(user, reason=reason, delete_message_days=days)
        await ctx.send("done.")
    
    @checks.is_guild()
    @checks.moderator_or_permissions(kick_members=True)
    @commands.command(name="kick")
    async def _kick(self, ctx: commands.Context, member: discord.Member, *, reason: typing.Optional[str]):
        """
        kick a member

        examples:
            `>kick 310418322384748544`
            `>kick 310418322384748544 spam`
        """
        
        if (ctx.author != ctx.guild.owner):
            if (member.top_role >= ctx.author.top_role):
                raise commands.errors.MissingPermissions([])
        elif (member == ctx.guild.owner):
            raise commands.errors.MissingPermissions([])

        if (not reason):
            reason = "{0} was kicked by {1}".format(member.id, ctx.author.id)

        await member.kick(reason=reason)
        await ctx.send("done.")
    
    @checks.is_guild()
    @checks.moderator_or_permissions(manage_messages=True)
    @commands.command(name="mute")
    async def _mute(self, ctx: commands.Context, member: discord.Member, future: parse.FutureDateTime, *, reason: typing.Optional[str]):
        """
        mute a member

        examples:
            `>mute 310418322384748544`
            `>mute 310418322384748544 spam`
            `>mute 310418322384748544 5 spam`
        """
        
        if (ctx.author != ctx.guild.owner):
            if (member.top_role >= ctx.author.top_role):
                raise commands.errors.MissingPermissions([])
        elif (member == ctx.guild.owner):
            raise commands.errors.MissingPermissions([])

        if (not reason):
            reason = "{0} was muted by {1}".format(member.id, ctx.author.id)

        pass
    
    @checks.is_guild()
    @checks.moderator_or_permissions(manage_nicknames=True)
    @commands.command(name="names", aliases=["nicknames"])
    async def _names(self, ctx: commands.Context, member: typing.Union[discord.Member, discord.User]):
        """
        show a member's previous names and nicknames

        examples:
            `>names 310418322384748544`
        """

        pass
    
    @checks.is_guild()
    @checks.moderator_or_permissions(manage_messages=True)
    @commands.command(name="prune", aliases=["clear", "delete", "purge"])
    async def _prune(self, ctx: commands.Context, limit: int):
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
    async def _rename(self, ctx: commands.Context, member: discord.Member, *, name: typing.Optional[str]):
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
        elif (member == ctx.guild.owner):
            raise commands.errors.MissingPermissions([])

        reason = "{0} was renamed by {1}".format(member.id, ctx.author.id)
        await member.edit(nick=name, reason=reason)
        await ctx.send("done.")
        
    @checks.is_guild()
    @checks.moderator_or_permissions(ban_members=True)
    @commands.command(name="softban")
    async def _softban(self, ctx: commands.Context, member: discord.Member, *, reason: typing.Optional[str]):
        """
        ban and unban a member

        utilized to kick while deleting all messages

        examples:
            `>softban 310418322384748544`
            `>softban 310418322384748544 spam`
        """

        if (ctx.author != ctx.guild.owner):
            if (member.top_role >= ctx.author.top_role):
                raise commands.errors.MissingPermissions([])
        elif (member == ctx.guild.owner):
            raise commands.errors.MissingPermissions([])

        if (not reason):
            reason = "{0} was softbanned by {1}".format(member.id, ctx.author.id)

        await member.ban(reason=reason)
        await ctx.guild.unban(member, reason=reason)
        await ctx.send("done.")
    
    @checks.is_guild()
    @checks.moderator_or_permissions(ban_members=True)
    @commands.command(name="unban")
    async def _unban(self, ctx: commands.Context, user: discord.User, *, reason: typing.Optional[str]):
        """
        unban a user

        examples:
            `>unban 310418322384748544`
            `>unban 310418322384748544 no more spam :)`
        """

        if (not reason):
            reason = "{0} was unbanned by {1}".format(user.id, ctx.author.id)
        
        try:
            await ctx.guild.unban(user, reason=reason)
        except (discord.errors.NotFound) as e:
            await ctx.bot.send_help(ctx)
            return

        await ctx.send("done.")
    
    @checks.is_guild()
    @checks.moderator_or_permissions(manage_messages=True)
    @commands.command(name="unmute")
    async def _unmute(self, ctx: commands.Context, member: discord.Member, *, reason: typing.Optional[str]):
        """
        unmute a member

        examples:
            `>unban 310418322384748544`
            `>unban 310418322384748544 no more spam :)`
        """
        
        if (ctx.author != ctx.guild.owner):
            if (member.top_role >= ctx.author.top_role):
                raise commands.errors.MissingPermissions([])

        if (not reason):
            reason = "{0} was unmuted by {1}".format(member.id, ctx.author.id)

        pass

    @checks.is_guild()
    @checks.moderator_or_permissions(manage_roles=True)
    @commands.group(name="role", invoke_without_command=True)
    async def _role(self, ctx: commands.Context):
        """
        role group
        """

        await ctx.bot.send_help(ctx)

    @_role.command(name="add")
    async def _role_add(self, ctx: commands.Context, member: discord.Member, *roles: discord.Role):
        """
        add roles to a member
        """

        if (ctx.author != ctx.guild.owner):
            for (role) in roles:
                if (role >= ctx.author.top_role):
                    raise commands.errors.MissingPermissions([])

        reason = "{0} added roles {1} to {2}".format(ctx.author.id, ", ".join([r.name for r in roles]), member.id)
        await member.add_roles(*roles, reason=reason)
        await ctx.send("done.")

    @_role.group(name="edit", invoke_without_command=True)
    async def _role_edit(self, ctx: commands.Context):
        """
        edit a role
        """

        await ctx.bot.send_help(ctx)

    @_role_edit.command(name="color", aliases=["colour"])
    async def _role_edit_color(self, ctx: commands.Context, role: discord.Role, color: parse.Color):
        """
        edit a role's color
        """

        if (ctx.author != ctx.guild.owner):
            if (role >= ctx.author.top_role):
                raise commands.errors.MissingPermissions([])

        color = discord.Color.from_rgb(*color.result[2])
        await role.edit(color=color)
        await ctx.send("done.")
        
    @_role_edit.command(name="name")
    async def _role_edit_name(self, ctx: commands.Context, role: discord.Role, *, name: str):
        """
        edit a role's name
        """

        if (ctx.author != ctx.guild.owner):
            if (role >= ctx.author.top_role):
                raise commands.errors.MissingPermissions([])

        await role.edit(name=name)
        await ctx.send("done.")

    @_role.command(name="remove")
    async def _role_remove(self, ctx: commands.Context, member: discord.Member, *roles: discord.Role):
        """
        remove roles from a member
        """

        if (ctx.author != ctx.guild.owner):
            for (role) in roles:
                if (role >= ctx.author.top_role):
                    raise commands.errors.MissingPermissions([])

        reason = "{0} removed roles {1} from {2}".format(ctx.author.id, ", ".join([r.name for r in roles]), member.id)
        await member.remove_roles(*roles, reason=reason)
        await ctx.send("done.")


def setup(bot : commands.Bot):
    extension = Moderation(bot)
    bot.add_cog(extension)