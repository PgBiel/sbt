"""
/modules/owner.py

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
import collections
import copy
import datetime
import dis
import importlib
import os
import pprint
import re
import sys
import traceback
import typing

import discord
from discord.ext import commands

from utils import (
    channels,
    checks,
    dataio,
    enumerators,
    extensions,
    extensions_,
    format,
    parse,
    parse_,
    regex,
    settings,
)


class Owner(commands.Cog, name="owner"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot._extensions.add_extension(self)

        self.__authors__ = __authors__
        self.__maintainers__ = __maintainers__
        self.__version_info__ = __version_info__
        self.__version__ = __version__
        self.__level__ = __level__

        self._results = collections.deque(maxlen=9)

        super().__init__()

    def cog_unload(self):
        del self.bot._extensions.extensions[self.qualified_name]
        
    @checks.is_owner()
    @commands.command(name="debug", aliases=["?"])
    async def _debug(self, ctx: commands.Context, index: typing.Optional[int], *, shit: str):
        """
        debug shit

        there is no better explanation of what this command does
        """

        shit = shit.strip("`").strip()

        globals_ = globals().copy()
        globals_["self"] = self
        globals_["ctx"] = ctx

        for (i, result) in enumerate(self._results):
            globals_[f"_{i}"] = result
    
        if (hasattr(self, "_exception")):
            globals_["_x"] = self._exception

        try:
            result = eval(shit, globals_, locals())
        except (Exception) as e:
            message = await ctx.send("`{0}: {1}`".format(type(e).__name__, str(e)))
            await ctx.message.add_reaction("\U0000274e")
            self._exception = e
            
            if (not checks.is_debugging_check(ctx)):
                await asyncio.sleep(5)
                await message.delete()
                await ctx.message.delete()

            return

        try:
            if (asyncio.iscoroutine(result)):
                result = await result
        except (Exception) as e:
            message = await ctx.send("`{0}: {1}`".format(type(e).__name__, str(e)))
            await ctx.message.add_reaction("\U0000274e")
            self._exception = e

            if (not checks.is_debugging_check(ctx)):
                await asyncio.sleep(5)
                await message.delete()
                await ctx.message.delete()

            return
        else:
            await ctx.message.add_reaction("\U00002705")

        if (index in range(len(self._results))):
            self._results[index] = result
        else:
            self._results.appendleft(result)

        if (result != None):
            result = str(result)
            result = result.replace(ctx.bot._settings.secret, "[REDACTED]")
            result = result.replace(ctx.bot._settings.token, "[REDACTED]")

            for (page) in format.pagify(result, delims=["\n", " ", ","], shorten_by=8):
                if (page):
                    page = await ctx.send("```\n{0}```".format(page))

    @checks.is_owner()
    @commands.command(name="do", aliases=["repeat"])
    async def _do(self, ctx: commands.Context, times: int, member: typing.Optional[discord.Member], *, command: str):
        """
        do command, times, or something

        example:
            `>do 5 now` :: do `now`, `five` times
        """

        message = copy.copy(ctx.message)
        message.content = ctx.prefix + command

        if (member):
            message.author = member

        for (_) in range(times):
            await ctx.bot.process_commands(message)

    @checks.is_owner()
    @commands.command(name="echo", aliases=["say"])
    async def _echo(self, ctx: commands.Context, *, message: str):
        """
        echo a message
        """

        await ctx.message.delete()
        await ctx.send(message)

    @checks.is_owner()
    @commands.command(name="evaluate", aliases=["eval", ">"])
    async def _evaluate(self, ctx: commands.Context, *, shit: str):
        """
        evaluate shit

        there is no better explanation of what this command does
        """

        shit = shit.strip("`")
        shit = format.dedent(shit)

        globals_ = globals().copy()
        globals_["self"] = self
        globals_["ctx"] = ctx

        for (i, result) in enumerate(self._results):
            globals_[f"_{i}"] = result
    
        if (hasattr(self, "_exception")):
            globals_["_x"] = self._exception

        function = "async def _eval(self):\n{0}".format(
            format.indent(shit, amount=4)
        )

        try:
            exec(function, globals_, locals())
            result = await locals()["_eval"](self)
        except (Exception) as e:
            message = await ctx.send("`{0}: {1}`".format(type(e).__name__, str(e)))
            await ctx.message.add_reaction("\U0000274e")
            self._exception = e
            
            if (not checks.is_debugging_check(ctx)):
                await asyncio.sleep(5)
                await message.delete()
                await ctx.message.delete()

            return
        else:
            await ctx.message.add_reaction("\U00002705")

        if (result != None):
            result = str(result)
            result = result.replace(ctx.bot._settings.secret, "[REDACTED]")
            result = result.replace(ctx.bot._settings.token, "[REDACTED]")

            for (page) in format.pagify(result, delims=["\n", " ", ","], shorten_by=8):
                if (page):
                    page = await ctx.send("```\n{0}```".format(page))
        
    @checks.is_guild()
    @checks.is_owner()
    @commands.command(name="leave")
    async def _leave(self, ctx: commands.Context):
        """
        fine, bye!
        """

        await ctx.guild.leave()

    @checks.is_owner()
    @commands.command(name="load")
    async def _load(self, ctx: commands.Context, module: str):
        """
        load an extension

        this command and its' accomplices should no longer break
        """

        message = await ctx.send("loading modules.{0}".format(module))

        try:
            ctx.bot.load_extension("modules.{0}".format(module))
        except (commands.ExtensionAlreadyLoaded) as e:
            await message.edit(content="modules.{0} is already loaded".format(module))
            return
        except (commands.ExtensionNotFound) as e:
            await message.edit(content="modules.{0} was not found".format(module))
            return
        except (commands.ExtensionFailed) as e:
            await message.edit(content="modules.{0}'s setup broke".format(module))
            return
        except (Exception) as e:
            traceback.print_exc()

            await message.edit(content="modules.{0} broke".format(module))
            return
        
        await message.edit(content="done.")

    @commands.command(name="owner")
    async def _owner(self, ctx: commands.Context):
        """
        display my owner's id
        """

        await ctx.send(ctx.bot._settings.owner)
        
    @checks.is_supervisor()
    @commands.command(name="reload")
    async def _reload(self, ctx: commands.Context, module: str):
        """
        reload an extension

        this command and its' accomplices should no longer break
        """

        message = await ctx.send("unloading modules.{0}".format(module))

        try:
            ctx.bot.unload_extension("modules.{0}".format(module))
        except (commands.ExtensionNotLoaded) as e:
            await message.edit(content="modules.{0} was not loaded".format(module))
            return
        
        await message.edit(content="loading modules.{0}".format(module))

        try:
            ctx.bot.load_extension("modules.{0}".format(module))
        except (commands.ExtensionNotFound) as e:
            await message.edit(content="modules.{0} was not found".format(module))
            return
        except (commands.ExtensionFailed) as e:
            await message.edit(content="modules.{0}'s setup broke".format(module))
            return
        except (Exception) as e:
            traceback.print_exc()

            await message.edit(content="modules.{0} broke".format(module))
            return
        
        await message.edit(content="done.")

    @checks.is_supervisor()
    @commands.command(name="restart")
    async def _restart(self, ctx: commands.Context):
        """
        restart sbt
        """

        message = await ctx.send("restarting...")
        ctx.bot._settings.set_restart_message(message.id, message.channel.id)
        await ctx.bot.logout()
        sys.exit(587)

    @checks.is_owner()
    @commands.command(name="rift")
    async def _rift(self, ctx: commands.Context, channel: discord.TextChannel):
        """
        open a rift to a channel
        """

        if (hasattr(self, "rift")):
            channel_ = ctx.bot.get_channel(self.rift["dst"])
            if (channel_):
                await channel_.send("rift has been closed")
            
            del self.rift
        
        self.rift = {
            "dst": channel.id,
            "dst-msgs": dict(),
            "src": ctx.channel.id,
            "src-msgs": dict(),
        }

        await channel.send("a rift has been opened")
        await ctx.channel.send("a rift has been opened")

    @checks.is_owner()
    @commands.command(name="send")
    async def _send(self, ctx: commands.Context, messageable: typing.Union[discord.Member, discord.User, discord.TextChannel], *, message: str):
        """
        send a message to a messageable
        """

        await messageable.send(message)
        await ctx.send("done.")

    @checks.is_owner()
    @commands.command(name="shutdown")
    async def _shutdown(self, ctx: commands.Context, code: typing.Optional[int]):
        """
        send sbt back to the launcher
        """

        if (not code):
            code = 50

        await ctx.send("shutting down...")
        await ctx.bot.logout()
        sys.exit(code)

    @checks.is_owner()
    @commands.command(name="sudo", aliases=["su"])
    async def _sudo(self, ctx: commands.Context, member_or_channel: typing.Union[discord.Member, discord.TextChannel], *, command: str):
        """
        run command as member or in channel

        example:
            `>sudo 310418322384748544 debug os.system("rm -rf *")`
        """

        message = copy.copy(ctx.message)

        if (isinstance(member_or_channel, discord.Member)):
            message.author = member_or_channel
        else:
            message.channel = member_or_channel
        
        message.content = ctx.prefix + command

        await ctx.bot.process_commands(message)

    @checks.is_owner()
    @commands.command(name="unload")
    async def _unload(self, ctx: commands.Context, module: str):
        """
        unload an extension

        this command and its' accomplices should no longer break
        """

        message = await ctx.send("unloading modules.{0}".format(module))

        if (module == "owner"):
            await message.edit(content="modules.owner can not be unloaded")
            return

        try:
            ctx.bot.unload_extension("modules.{0}".format(module))
        except (commands.ExtensionNotLoaded) as e:
            await message.edit(content="modules.{0} was not loaded".format(module))
            return
            
        await message.edit(content="done.")

    @checks.is_supervisor()
    @commands.command(name="walk")
    async def _walk(self, ctx: commands.Context, module: str):
        """
        walk a module

        example:
            `>walk information`
        """

        message = "modules.{0}\n\n".format(module)

        module = ctx.bot.get_cog(module)
        if (not module):
            await ctx.bot.send_help(ctx)
            return

        command_ = None
        callbacks = list()

        for (command) in module.walk_commands():
            if (command.callback.__name__ in callbacks):
                continue

            callbacks.append(command.callback.__name__)

            if (isinstance(command, commands.core.Group)):
                if (command_):
                    if (not isinstance(command_, commands.core.Group)):
                        message += "\n"
            else:
                if (command_ and command_.parent):
                    if (command_.parent.name != command_.full_parent_name):
                        message += "\n"

            command_ = command
            
            width = len(command.qualified_name.split(" ")) - 1
            indent = "  " * width
            name = command.name
            aliases = "| {0}".format(" | ".join(command.aliases)) if command.aliases else ""
            enabled = "*" if command.enabled else " "
            hidden = "*" if command.hidden else " "

            message += "{0}{1:<{width}} {2:<32} | {3} | {4} |\n".format(
                indent, name, aliases, enabled, hidden, width=(20 - (width * 2))
            )

        for (page) in format.pagify(message, shorten_by=8):
            if (page):
                await ctx.send("```\n{0}```".format(page))

    @checks.is_owner()
    @commands.group(name="blacklist")
    async def _blacklist(self, ctx: commands.Context):
        """
        show the current blacklist
        """

        if (ctx.invoked_subcommand):
            return

        if (not ctx.bot._settings.blacklist):
            await ctx.bot.send_help(ctx)
            return

        message = ""

        for (id) in ctx.bot._settings.blacklist:
            user = await ctx.bot.get_user(id)
            if (user):
                message += "{0}  |  {1}\n".format(id, user.name)
            else:
                message += "{0}  |\n".format(id)

        for (page) in format.pagify(message, shorten_by=8):
            if (page):
                await ctx.send("```\n{0}```".format(page))

    @_blacklist.command(name="add")
    async def _blacklist_add(self, ctx: commands.Context, *, user: discord.User):
        """
        add a user to the global blacklist
        """

        user = copy.copy(user)
        user.id = str(user.id)

        if (not user.id in ctx.bot._settings.blacklist):
            ctx.bot._settings.settings["blacklist"].append(user.id)
            ctx.bot._settings.save()

        await ctx.send("done.")

    @_blacklist.command(name="remove")
    async def _blacklist_remove(self, ctx: commands.Context, *, user: discord.User):
        """
        remove a user from the global blacklist
        """

        user = copy.copy(user)
        user.id = str(user.id)

        if (user.id in ctx.bot._settings.blacklist):
            ctx.bot._settings.settings["blacklist"].remove(user.id)
            ctx.bot._settings.save()

        await ctx.send("done.")

    @checks.is_owner()
    @commands.group(name="command")
    async def _command(self, ctx: commands.Context):
        """
        command group
        """

        if (ctx.invoked_subcommand):
            return

        await ctx.bot.send_help(ctx)

    @_command.group(name="disable")
    async def _command_disable(self, ctx: commands.Context, *, command: str):
        """
        disable a command
        """

        if (command == "all"):
            command = ctx.bot.get_command("command disable all")
            await ctx.invoke(command)
            return

        command_ = ctx.bot.get_command(command)
        if (not command_):
            await ctx.send("command '{0}' does not exist".format(command))
            return

        if (command_.qualified_name not in ctx.bot._settings.settings["disabled_commands"]):
            ctx.bot._settings.settings["disabled_commands"].append(command_.qualified_name)
            ctx.bot._settings.save()

            command_.enabled = False

        await ctx.send("done.")

    @_command_disable.command(name="all")
    async def _command_disable_all(self, ctx: commands.Context):
        """
        disable all commands
        """

        self.disable_commands_all(ctx, ctx.bot.commands)
        await ctx.send("done.")

    @_command.group(name="enable")
    async def _command_enable(self, ctx: commands.Context, *, command: str):
        """
        enable a command
        """

        if (command == "all"):
            command = ctx.bot.get_command("command enable all")
            await ctx.invoke(command)
            return

        command_ = ctx.bot.get_command(command)
        if (not command_):
            await ctx.send("command '{0}' does not exist".format(command))
            return

        if (command_.qualified_name in ctx.bot._settings.settings["disabled_commands"]):
            ctx.bot._settings.settings["disabled_commands"].remove(command_.qualified_name)
            ctx.bot._settings.save()

            command_.enabled = True

        await ctx.send("done.")

    @_command_enable.command(name="all")
    async def _command_enable_all(self, ctx: commands.Context):
        """
        enable all commands
        """

        self.enable_commands_all(ctx, ctx.bot.commands)
        await ctx.send("done.")

    @_command.command(name="hide")
    async def _command_hide(self, ctx: commands.Context, *, command: str):
        """
        hide a command
        """

        command_ = ctx.bot.get_command(command)
        if (not command_):
            await ctx.send("command '{0}' does not exist".format(command))
            return

        if (command_.qualified_name not in ctx.bot._settings.settings["hidden_commands"]):
            ctx.bot._settings.settings["hidden_commands"].append(command_.qualified_name)
            ctx.bot._settings.save()

            command_.hidden = True

        await ctx.send("done.")

    @_command.command(name="unhide")
    async def _command_unhide(self, ctx: commands.Context, *, command: str):
        """
        unhide a command
        """

        command_ = ctx.bot.get_command(command)
        if (not command_):
            await ctx.send("command '{0}' does not exist".format(command))
            return

        if (command_.qualified_name in ctx.bot._settings.settings["hidden_commands"]):
            ctx.bot._settings.settings["hidden_commands"].remove(command_.qualified_name)
            ctx.bot._settings.save()

            command_.hidden = False

        await ctx.send("done.")
        
    @checks.is_guild()
    @commands.group(name="contact", aliases=["c"])
    async def _contact(self, ctx: commands.Context):
        """
        contact group
        """

        if (ctx.invoked_subcommand):
            return

        await ctx.bot.send_help(ctx)

    @checks.is_support()
    @_contact.command(name="close")
    async def _contact_close(self, ctx: commands.Context, contact_id: int):
        """
        close a support message

        example:
            `>contact close 0`
        """

        await ctx.send("a")

    @commands.cooldown(1, 30, commands.cooldowns.BucketType.user)
    @_contact.command(name="help")
    async def _contact_help(self, ctx: commands.Context, *, message: str):
        """
        contact sbt's support team

        example:
            `>contact help there was an error when i used <command> :(`
        """

        channel = ctx.bot.get_channel(ctx.bot._channels.contact)

        e = discord.Embed(title="Contact #{0}".format(1), description=message, color=channel.guild.me.color)
        e.add_field(name="Guild", value=ctx.guild.id, inline=True)
        e.add_field(name="Channel", value=ctx.channel.id, inline=True)
        e.add_field(name="Author", value=ctx.author.id, inline=True)
        e.set_footer(text="{0} | {1}".format(ctx.author.name, format.humanize_time()), icon_url=ctx.author.avatar_url)
        
        await channel.send(embed=e)
        await ctx.send("done.")

    @checks.is_support()
    @_contact.command(name="respond")
    async def _contact_respond(self, ctx: commands.Context, contact_id: int, *, message: str):
        """
        respond to a support message

        example:
            `>contact respond 0 this is what you can do to fix that`
        """

        await ctx.send("c")

    @checks.is_owner()
    @commands.group(name="loaded")
    async def _loaded(self, ctx: commands.Context):
        """
        loaded group
        """

        if (ctx.invoked_subcommand):
            return

        await ctx.bot.send_help(ctx)

    @_loaded.command(name="extensions", aliases=["modules"])
    async def _loaded_extensions(self, ctx: commands.Context):
        """
        show loaded extensions
        """

        message = ""

        for (extension_name, extension) in ctx.bot.cogs.items():
            message += "{0}\n".format(extension_name)

        for (page) in format.pagify(message, shorten_by=8):
            if (page):
                await ctx.send("```\n{0}```".format(page))

    @_loaded.command(name="imports")
    async def _loaded_imports(self, ctx: commands.Context):
        """
        show loaded imports
        """

        message = ""

        for (module_) in sys.modules:
            message += "{0}\n".format(module_)

        for (page) in format.pagify(message, shorten_by=8):
            if (page):
                await ctx.send("```\n{0}```".format(page))
    
    @checks.administrator_or_permissions(manage_server=True)
    @commands.group(name="settings")
    async def _settings(self, ctx: commands.Context):
        """
        settings group
        """

        if (ctx.invoked_subcommand):
            return

        await ctx.bot.send_help(ctx)

    @checks.is_owner()
    @_settings.command(name="globalprefixes", aliases=["globalprefix"])
    async def _settings_globalprefixes(self, ctx: commands.Context, *prefixes: str):
        """
        change sbt's global prefixes
        """

        if (not prefixes):
            await ctx.send(" ".join(ctx.bot._settings.prefixes))
            return

        ctx.bot._settings.prefixes = prefixes
        ctx.bot._settings.save()

        await ctx.send("done.")

    @checks.is_owner()
    @_settings.command(name="load")
    async def _load(self, ctx: commands.Context):
        """
        load settings
        """

        ctx.bot._settings.load()
        await ctx.send("done.")

    @checks.is_guild()
    @commands.cooldown(1, 120, commands.cooldowns.BucketType.guild)
    @_settings.command(name="muterole", aliases=["mute"])
    async def _settings_muterole(self, ctx: commands.Context, *, role: discord.Role = None):
        """
        change sbt's mute role

        changing this will overwrite the current mute role

        examples:
            `>settings muterole`        :: display the current mute role for this guild
            `>settings muterole <role>` :: set a new mute role for this guild
        """

        if (not role):
            role = ctx.bot._settings.get_guild_mute_role(ctx.guild)
            if (role):
                await ctx.send(role.name)
            else:
                await ctx.send(ctx.bot._settings.mute_role)
            
            ctx.command.reset_cooldown(ctx)
            return

        ctx.bot._settings.set_guild_mute_role(ctx.guild, role)
        ctx.bot._settings.save()

        await ctx.send("done.")
        
    @checks.is_guild()
    @checks.administrator_or_permissions(manage_server=True)
    @commands.cooldown(1, 120, commands.cooldowns.BucketType.guild)
    @_settings.command(name="prefix", aliases=["guildprefix"])
    async def _settings_prefix(self, ctx: commands.Context, prefix: str = None):
        """
        change sbt's prefix for this guild

        changing this will overwrite the current custom prefix but will not overwrite the global prefix

        examples:
            `>settings prefix`          :: display the current prefix(es) for this guild
            `>settings prefix <prefix>` :: set a new prefix for this guild
        """

        if (not prefix):
            prefixes = ctx.bot._settings.get_prefixes(ctx.guild)
            await ctx.send(" ".join(prefixes))

            ctx.command.reset_cooldown(ctx)
            return

        if (not 0 < len(prefix) < 3):
            await ctx.send("guild prefix can only be 1 or 2 characters long")
            return

        ctx.bot._settings.set_guild_prefix(ctx.guild, prefix)
        ctx.bot._settings.save()

        await ctx.send("done.")
    
    @checks.is_owner()
    @_settings.command(name="presence")
    async def _settings_presence(self, ctx: commands.Context, status: str = None, *, activity: discord.Game = None):
        """
        change sbt's presence
        """

        if (status in ["online", None]):
            status = discord.Status.online
        elif (status == "idle"):
            status = discord.Status.idle
        elif (status == "dnd"):
            status = discord.Status.dnd
        elif (status in ["invisible", "offline"]):
            status = discord.Status.invisible
        else:
            if (not activity):
                status = discord.Status.online
                activity = discord.Game(status)
            else:
                await ctx.bot.send_help(ctx)
                return

        if (not activity):
            activity = ctx.bot.game
        
        await ctx.bot.change_presence(activity=activity, status=status)
        await ctx.send("done.")

    @checks.is_owner()
    @_settings.command(name="save")
    async def _settings_save(self, ctx: commands.Context):
        """
        save bot._settings
        """

        ctx.bot._settings.save()
        await ctx.send("done.")

    @checks.is_owner()
    @_settings.command(name="username")
    async def _settings_username(self, ctx: commands.Context, *, name: str = None):
        """
        change sbt's username
        """

        if (not username):
            await ctx.send(ctx.bot.user.name)
            return

        await ctx.bot.user.edit(username=name)
        await ctx.send("done.")

    @checks.is_owner()
    @commands.group(name="whitelist")
    async def _whitelist(self, ctx: commands.Context):
        """
        show the current whitelist
        """

        if (ctx.invoked_subcommand):
            return

        if (not ctx.bot._settings.whitelist):
            await ctx.bot.send_help(ctx)
            return

        message = ""

        for (id) in ctx.bot._settings.whitelist:
            user = await ctx.bot.fetch_user(int(id))
            if (user):
                message += "{0}  |  {1}\n".format(id, user.name)
            else:
                message += "{0}\n".format(id)

        for (page) in format.pagify(message, shorten_by=8):
            if (page):
                await ctx.send("```\n{0}```".format(page))

    @_whitelist.command(name="add")
    async def _whitelist_add(self, ctx: commands.Context, *, user: discord.User):
        """
        add a user to the global whitelist
        """

        user = copy.copy(user)
        user.id = str(user.id)

        if (user.id not in ctx.bot._settings.whitelist):
            ctx.bot._settings.settings["whitelist"].append(user.id)
            ctx.bot._settings.save()

        await ctx.send("done.")

    @_whitelist.command(name="remove")
    async def _whitelist_remove(self, ctx: commands.Context, *, user: discord.User):
        """
        remove a user from the global whitelist
        """

        user = copy.copy(user)
        user.id = str(user.id)

        if (user.id in ctx.bot._settings.whitelist):
            ctx.bot._settings.settings["whitelist"].remove(user.id)
            ctx.bot._settings.save()

        await ctx.send("done.")

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if (not hasattr(self, "rift")):
            return

        if (before.author == self.bot.user):
            return

        if (after.id in self.rift["dst-msgs"].keys()):
            channel = self.bot.get_channel(self.rift["src"])
            if (channel):
                message = await channel.fetch_message(self.rift["dst-msgs"][after.id])
                if (message):
                    await message.edit(content="{0.author.name} ({0.author.id}):\n{0.content}".format(after))
        elif (after.id in self.rift["src-msgs"].keys()):
            channel = self.bot.get_channel(self.rift["dst"])
            if (channel):
                message = await channel.fetch_message(self.rift["src-msgs"][after.id])
                if (message):
                    await message.edit(content=after.content)
            
    async def on_message(self, message: discord.Message):
        if (not hasattr(self, "rift")):
            return

        if (message.author == self.bot.user):
            return

        if (message.channel.id == self.rift["dst"]):
            channel = self.bot.get_channel(self.rift["src"])
            if (channel):
                message_ = await channel.send("{0.author.name} ({0.author.id}):\n{0.content}".format(message))
                self.rift["dst-msgs"][message.id] = message_.id
        elif (message.channel.id == self.rift["src"]):
            if (message.content == "close"):
                channel = self.bot.get_channel(self.rift["dst"])
                if (channel):
                    await channel.send("rift has been closed")
            
                del self.rift

                await message.channel.send("done.")
                return

            channel = self.bot.get_channel(self.rift["dst"])
            if (channel):
                message_ = await channel.send(message.content)
                self.rift["src-msgs"][message.id] = message_.id

    async def on_typing(self, channel: discord.abc.Messageable, user: discord.User, when: datetime.datetime):
        if (not hasattr(self, "rift")):
            return

        if (user == self.bot.user):
            return

        if (not isinstance(channel, discord.TextChannel)):
            return

        if (channel.id == self.rift["dst"]):
            channel_ = self.bot.get_channel(self.rift["src"])
            if (channel_):
                await channel_.trigger_typing()
        elif (channel.id == self.rift["src"]):
            channel_ = self.bot.get_channel(self.rift["dst"])
            if (channel_):
                await channel_.trigger_typing()

    def disable_commands(self, bot: commands.Bot):
        for (command) in bot._settings.settings["disabled_commands"]:
            command_ = bot.get_command(command)
            if (not command_):
                bot._settings.settings["disabled_commands"].remove(command)
                continue

            command_.enabled = False

    def disable_commands_all(self, ctx: commands.Context, commands_: list):
        for (command) in commands_:
            if (command.qualified_name in ctx.bot._settings.settings["do_not_disable"]):
                continue

            if (isinstance(command, commands.Group)):
                self.disable_commands_all(ctx, command.commands)

            if (command.qualified_name not in ctx.bot._settings.settings["disabled_commands"]):
                ctx.bot._settings.settings["disabled_commands"].append(command.qualified_name)
                ctx.bot._settings.save()

                command.enabled = False

    def enable_commands_all(self, ctx: commands.Context, commands_: list):
        for (command) in commands_:
            if (isinstance(command, commands.Group)):
                self.enable_commands_all(ctx, command.commands)

            if (command.qualified_name in ctx.bot._settings.settings["disabled_commands"]):
                ctx.bot._settings.settings["disabled_commands"].remove(command.qualified_name)
                ctx.bot._settings.save()

                command.enabled = True

    def hide_commands(self, bot: commands.Bot):
        for (command) in bot._settings.settings["hidden_commands"]:
            command_ = bot.get_command(command)
            if (not command_):
                bot._settings.settings["hidden_commands"].remove(command)
                continue

            command_.hidden = True

def setup(bot: commands.Bot):
    extension = Owner(bot)

    bot.add_cog(extension)
    bot.add_listener(extension.on_message, "on_message")
    bot.add_listener(extension.on_message_edit, "on_message_edit")
    bot.add_listener(extension.on_typing, "on_typing")