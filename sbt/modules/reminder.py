"""
/modules/general.py

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

__level__        = 7

__all__ = {
    "Reminder",
    "setup",
}


import discord
from discord.ext import commands, tasks

from utils import (
    dataio,
)


class Reminder(commands.Cog, name="reminder"):
    """
    helper class for General._reminder
    """

    __all__ = {
        "__init__",
        "cog_unload",
        "add_reminder",
        "get_reminders",
        "load",
        "remove_reminder",
        "save",
        "send_reminders",
        "before_send_reminders",
    }

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.__authors__ = __authors__
        self.__maintainers__ = __maintainers__
        self.__version_info__ = __version_info__
        self.__version__ = __version__
        self.__level__ = __level__

        self.load()
        self.send_reminders.start()

    def cog_unload(self):
        self.send_reminders.cancel()

    def add_reminder(self, ctx: commands.Context, reminder: str):
        pass

    def get_reminders(self, member: discord.Member, max: int = None):
        i = 0
        for (reminder) in self.reminders:
            if (i == max):
                return

            if (reminder["author"] == member.id):
                yield reminder
                i += 1

    def load(self):
        self.reminders = dataio.load("data/general/reminders.json")

    def remove_reminder(self, ctx: commands.Context, id: int):
        pass

    def save(self):
        dataio.save("data/general/reminders.json", self.reminders)

    @tasks.loop(seconds=3, reconnect=True)
    async def send_reminders(self):
        pass

    @send_reminders.before_loop()
    async def before_send_reminders(self):
        await self.bot.wait_until_ready()

                
def setup(bot: commands.Bot):
    extension = Reminder(bot)
    bot.add_cog(extension)