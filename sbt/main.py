"""
/main.py

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

__level__        = 0

__all__ = {
    "EXTENSIONS",
    "prefix_manager",
    "Bot",
    "init",
    "load_extensions",
    "main",
}


import aiohttp
import asyncio
import datetime
import os
import traceback
import typing

import discord
from discord.ext import commands
import pyfiglet

from utils import (
    channels,
    checks,
    error,
    format,
    settings,
)


EXTENSIONS = [os.path.splitext(f)[0] for (f) in os.listdir("modules") if os.path.isfile(os.path.join("modules", f))]


def prefix_manager(bot: commands.Bot, message: discord.Message) -> list:
    return bot._settings.get_prefixes(message.guild)


class Bot(commands.Bot):
    __all__ = {
        "__init__",
        "run",
        "send_help",
        "user_allowed",
    }

    def __init__(self, *args, **kwargs):
        self._channels = channels.Channels()
        self._settings = settings.Settings()

        self.__authors__ = __authors__
        self.__maintainers__ = __maintainers__
        self.__version_info__ = __version_info__
        self.__version__ = __version__
        self.__level__ = __level__
        
        super().__init__(*args, command_prefix=prefix_manager, **kwargs)

    def run(self):
        super().run(self._settings.token)

    async def send_help(self, ctx: commands.Context):
        help = self.get_cog("help")
        if (help):
            try:
                await help.paginate(ctx, await help.command_help(ctx, ctx.command))
                return
            except (discord.Forbidden) as e:
                pass

        await ctx.send_help(ctx.command)
        return

    def user_allowed(self, message: discord.Message) -> bool:
        if (message.author.bot):
            return False

        if (message.author.id == self._settings.owner):
            return True

        # ignore dpy
        #if (message.guild.id == self._settings.dpy):
        #    return False

        if (message.author.id in self._settings.blacklist):
            return False
        if (message.author.id in self._settings.whitelist):
            return True

        if (isinstance(message.channel, discord.abc.GuildChannel)):
            def check(role: typing.Union[int, str]):
                if (isinstance(role, int)):
                    # we have an id
                    if (message.author._roles.has(role)):
                        return True
                elif (isinstance(role, str)):
                    # we have a name
                    if (discord.utils.get(message.author.roles, name=name)):
                        return True

            names = (self._settings.get_guild_administrator_role(message.guild),
                     self._settings.get_guild_moderator_role(message.guild))

            if (any(map(check, names))):
                return True

            moderation = self.get_cog("Moderation")
            if (moderation):
                if (message.guild.id in moderation.ignore_list["guilds"]):
                    return False
                if (message.channel.id in moderation.ignore_list["channels"]):
                    return False

        return True


def init() -> commands.Bot:
    bot = Bot(description="SBT v2", help_command=commands.DefaultHelpCommand(dm_help=None, command_attrs={"hidden": True}))

    @bot.event
    async def on_ready():
        """
        Called when the client is done preparing the data received from Discord.
        Usually after login is successful and the Client.guilds and co. are filled up.

        Warning This function is not guaranteed to be the first event called.
        Likewise, this function is not guaranteed to only be called once.
        This library implements reconnection logic and thus will end up calling this event whenever a RESUME request fails.
        """

        try:
            message_id, channel_id = bot._settings.get_restart_message()
            if (message_id and channel_id):
                channel = bot.get_channel(channel_id)
                if (channel):
                    message = await channel.fetch_message(message_id)
                    if (message):
                        await message.edit(content="am back")
        except (BaseException) as e:
            pass
        finally:
            if ("restart_message" in bot._settings.settings):
                del bot._settings.settings["restart_message"]
                bot._settings.save()

        bot._uptime = datetime.datetime.utcnow()

        os.system("cls")

        print()
        print(pyfiglet.figlet_format("SBT v2"))
        print()
        print("Client:")
        print(" {0} ({1})".format(bot.user, bot.user.id))

        owner = bot.get_cog("owner")
        if (owner):
            owner.disable_commands(bot)
            owner.hide_commands(bot)

    @bot.event
    async def on_message(message: discord.Message):
        """
        Called when a Message is created and sent.
        """

        if (bot.user_allowed(message)):
            await bot.process_commands(message)

    @bot.event
    async def on_command_error(ctx: commands.Context, exception: discord.errors.DiscordException):
        """
        An error handler that is called when an error is raised inside a command either through user input error, check failure, or an error in your own code.

        the exception tree is as follows:

        DiscordException
         +-- CommandError
              +-- CheckFailure
              |    +-- BotMissingPermissions
              |    +-- MissingPermissions
              |    +-- NotOwner
              |    +-- NoPrivateMessage
              +-- CommandInvokeError
              +-- CommandNotFound
              +-- CommandOnCooldown
              +-- ConversionError
              +-- DisabledCommand
              +-- UserInputError
                   +-- ArgumentParsingError
                   |    +-- ExpectedClosingQuoteError
                   |    +-- InvalidEndOfQuotedStringError
                   |    +-- UnexpectedQuoteError
                   +-- BadArgument
                   +-- BadUnionArgument
                   +-- MissingRequiredArgument
                   +-- TooManyArguments
        """

        if (hasattr(exception, "original")):
            if (isinstance(exception.original, discord.errors.Forbidden)):
                await ctx.send("i don't have permission to do that")
                return

            if (isinstance(exception.original, discord.errors.HTTPException)):
                await ctx.send("i tried to send something that was too large :/")
                return

            if (isinstance(exception.original, asyncio.TimeoutError)):
                await ctx.send("timed out :/")
                return

            if (isinstance(exception.original, aiohttp.client_exceptions.ClientOSError)):
                await ctx.bot.invoke(ctx)
                return

            if (isinstance(exception, error.ParserError)):
                await ctx.send(exception.original)
                return

        if (isinstance(exception, commands.errors.CheckFailure)):
            if (isinstance(exception, commands.errors.BotMissingPermissions)):
                await ctx.send("i don't have permission to do that")
                return

            if (isinstance(exception, commands.errors.MissingPermissions)):
                await ctx.send("you don't have permission to do that")
                return

            if (isinstance(exception, commands.errors.NotOwner)):
                return

            if (isinstance(exception, commands.errors.NoPrivateMessage)):
                await ctx.send("that command is unavailable in PMs")
                return

            return

        if (isinstance(exception, commands.errors.CommandInvokeError)):
            pass

        if (isinstance(exception, commands.errors.CommandNotFound)):
            return

        if (isinstance(exception, commands.errors.CommandOnCooldown)):
            if (exception.retry_after < 1):
                async with ctx.typing():
                    await asyncio.sleep(exception.retry_after)
                    await ctx.bot.invoke(ctx)
                    return
            elif (checks.is_supervisor_check(ctx)):
                # supervisors bypass cooldowns
                ctx.command.reset_cooldown(ctx)
                await ctx.bot.invoke(ctx)
                return

            await ctx.send("that command is on cooldown, try again in {0}".format(format.humanize_seconds(exception.retry_after)))

            if (ctx.command.qualified_name == "help"):
                help = ctx.bot.get_cog("help")
                if (help):
                    await ctx.send("you can also remove this cooldown by closing your current help session")

            return

        if (isinstance(exception, commands.errors.ConversionError)):
            pass

        if (isinstance(exception, commands.errors.DisabledCommand)):
            if (str(ctx.message.author.id) == bot._settings.owner):
                await ctx.send("that command is disabled")

            return

        if (isinstance(exception, commands.errors.UserInputError)):
            if (isinstance(exception, commands.errors.ArgumentParsingError)):
                if (isinstance(exception, commands.errors.ExpectedClosingQuoteError)):
                    await ctx.bot.send_help(ctx)
                    return

                if (isinstance(exception, commands.errors.InvalidEndOfQuotedStringError)):
                    await ctx.bot.send_help(ctx)
                    return

                if (isinstance(exception, commands.errors.UnexpectedQuoteError)):
                    await ctx.bot.send_help(ctx)
                    return

                pass

            if (isinstance(exception, commands.errors.BadArgument)):
                await ctx.bot.send_help(ctx)
                return

            if (isinstance(exception, commands.errors.BadUnionArgument)):
                await ctx.bot.send_help(ctx)
                return

            if (isinstance(exception, commands.errors.MissingRequiredArgument)):
                await ctx.bot.send_help(ctx)
                return

            if (isinstance(exception, commands.errors.TooManyArguments)):
                await ctx.bot.send_help(ctx)
                return

            pass

        if (ctx.command.qualified_name not in bot._settings.settings["disabled_commands"]):
            bot._settings.settings["disabled_commands"].append(ctx.command.qualified_name)
            bot._settings.save()
            ctx.command.enabled = False

        await ctx.send("something went wrong! i disabled the command to reduce future errors but you should report this to the deveolper.")
        traceback.print_exception(type(exception), exception, None)

    return bot


def load_extensions(bot: commands.Bot):
    for (extension) in EXTENSIONS:
        try:
            bot.load_extension("modules.{0}".format(extension))
        except (Exception) as e:
            print("{0}: {1}".format(type(e).__name__, str(e)))
            traceback.print_exc()
            os.system("pause")

    print()

def main(bot: commands.Bot):
    load_extensions(bot)

    print("Logging into Discord...")
    bot.run()


if (__name__ == "__main__"):
    bot = init()

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(bot))
    except (Exception) as e:
        loop.run_until_complete(bot.logout())
    finally:
        loop.close()