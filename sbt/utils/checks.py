"""
/utils/checks.py

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


import discord
from discord.ext import commands


"""
the checks tree is as follows:

is_owner
 +-- is_alpha
 |    +-- is_beta
 +-- is_dj
 +-- is_supervisor
      +-- administrator_or_permissions
      |    +-- moderator_or_permissions
      +-- is_support
      +-- permissions

is_guild
"""


def is_owner() -> bool:
    return commands.check(is_owner_check)

def is_owner_check(ctx: commands.Context) -> bool:
    return ctx.author.id == ctx.bot._settings.owner


def is_supervisor() -> bool:
    return commands.check(is_supervisor_check)

def is_supervisor_check(ctx: commands.Context) -> bool:
    if (is_owner_check(ctx)):
        return True

    return ctx.author.id in ctx.bot._settings.supervisors


def is_support() -> bool:
    return commands.check(is_support_check)

def is_support_check(ctx: commands.Context) -> bool:
    if (is_supervisor_check(ctx)):
        return True

    return ctx.author.id in ctx.bot._settings.support_team


def is_alpha() -> bool:
    return commands.check(is_alpha_check)

def is_alpha_check(ctx: commands.Context) -> bool:
    if (is_owner_check(ctx)):
        return True

    if (not ctx.guild):
        return False

    if (ctx.guild.id != ctx.bot._settings.debugging_guild):
        return False

    return ctx.author.id in ctx.bot._settings.alpha_testers


def is_beta() -> bool:
    return commands.check(is_beta_check)

def is_beta_check(ctx: commands.Context) -> bool:
    if (is_alpha_check(ctx)):
        return True

    if (not ctx.guild):
        return False

    if (ctx.guild.id != ctx.bot._settings.debugging_guild):
        return False

    return ctx.author.id in ctx.bot._settings.beta_testers


def is_dj() -> bool:
    return commands.check(is_dj_check)

def is_dj_check(ctx: commands.Context) -> bool:
    if (is_owner_check(ctx)):
        return True

    return ctx.author.id in ctx.bot._settings.djs


def is_guild() -> bool:
    if (not commands.check(is_guild_check)):
        raise commands.NoPrivateMessage
    return commands.check(is_guild_check)

def is_guild_check(ctx: commands.Context) -> bool:
    if (ctx.guild):
        return True
    return False


def has_permissions(**required) -> bool:
    def predicate(ctx: commands.Context):
        return _permissions(**required)

    return commands.check(predicate)

def administrator_or_permissions(**required) -> bool:
    def predicate(ctx: commands.Context):
        return _administrator(ctx) or _permissions(ctx, **required)

    return commands.check(predicate)

def moderator_or_permissions(**required) -> bool:
    def predicate(ctx: commands.Context):
        return _moderator(ctx) or _permissions(ctx, **required)

    return commands.check(predicate)

def _administrator(ctx: commands.Context):
    administrator_role = ctx.bot._settings.get_guild_administrator_role(ctx.guild)
    if (not administrator_role):
        administrator_role = ctx.bot._settings.administrator_role
    
    if (isinstance(administrator_role, str)):
        for (role) in ctx.author.roles:
            if (role.name == administrator_role):
                return True
    elif (administrator_role):
        for (role) in ctx.author.roles:
            if (role.id == administrator_role.id):
                return True

    return False

def _moderator(ctx: commands.Context):
    if (_administrator(ctx)):
        return True

    moderator_role = ctx.bot._settings.get_guild_moderator_role(ctx.guild)
    if (not moderator_role):
        moderator_role = ctx.bot._settings.moderator_role
    
    if (isinstance(moderator_role, str)):
        for (role) in ctx.author.roles:
            if (role.name == moderator_role):
                return True
    elif (moderator_role):
        for (role) in ctx.author.roles:
            if (role.id == moderator_role.id):
                return True

    return False

def _permissions(ctx: commands.Context, **required) -> bool:
    if (is_supervisor_check(ctx)):
        return True

    if (not ctx.gulid):
        return True

    if (required):
        if (all([getattr(ctx.channel.permissions_for(ctx.author), name, None) == value for (name, value) in required.items()])):
            return True

    return False