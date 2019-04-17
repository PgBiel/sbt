"""
/utils/settings.py

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


import copy

import discord
from discord.ext import commands

from utils import (
    dataio
)


class Settings():
    def __init__(self):
        self.settings = dataio.load("data/sbt/settings.json")

    @property
    def administrator_role(self) -> str:
        return self.settings["administrator_role"]

    @property
    def alpha_testers(self) -> list:
        return self.settings["alpha_testers"]

    @property
    def beta_testers(self) -> list:
        return self.settings["beta_testers"]

    @property
    def blacklist(self) -> list:
        return self.settings["blacklist"]

    @property
    def debugging_guild(self) -> int:
        return self.settings["debugging_guild"]

    @property
    def djs(self) -> list:
        return self.settings["djs"]

    @property
    def prefixes(self) -> list:
        return self.settings["prefixes"]
    
    @prefixes.setter
    def prefixes(self, prefixes: list):
        self.settings["prefixes"] = prefixes

    @property
    def moderator_role(self) -> str:
        return self.settings["moderator_role"]

    @property
    def mute_role(self) -> str:
        return self.settings["mute_role"]

    @property
    def oauth(self) -> str:
        return self.settings["oauth"]
    
    @property
    def owner(self) -> int:
        return self.settings["owner"]

    @property
    def secret(self) -> str:
        return self.settings["secret"]

    @property
    def supervisors(self) -> list:
        return self.settings["supervisors"]

    @property
    def support_team(self) -> list:
        return self.settings["support_team"]

    @property
    def token(self) -> str:
        return self.settings["token"]

    @property
    def whitelist(self) -> list:
        return self.settings["whitelist"]

    def get_guild_administrator_role(self, guild: discord.Guild) -> discord.Role:
        guild_ = copy.copy(guild)
        guild_.id = str(guild.id)

        if (guild_.id in self.settings["guilds"].keys()):
            if ("administrator_role" in self.settings["guilds"][guild_.id].keys()):
                role = discord.utils.get(guild.roles, id=self.settings["guilds"][guild_.id]["administrator_role"])
                if (role):
                    return role

                del self.settings["guilds"][guild_.id]["administrator_role"]

                if (not self.settings["guilds"][guild_.id]):
                    del self.settings["guilds"][guild_.id]

    def get_guild_moderator_role(self, guild: discord.Guild) -> discord.Role:
        guild_ = copy.copy(guild)
        guild_.id = str(guild.id)

        if (guild_.id in self.settings["guilds"].keys()):
            if ("moderator_role" in self.settings["guilds"][guild_.id].keys()):
                role = discord.utils.get(guild.roles, id=self.settings["guilds"][guild_.id]["moderator_role"])
                if (role):
                    return role

                del self.settings["guilds"][guild_.id]["moderator_role"]

                if (not self.settings["guilds"][guild_.id]):
                    del self.settings["guilds"][guild_.id]

    def get_guild_mute_role(self, guild: discord.Guild) -> discord.Role:
        guild_ = copy.copy(guild)
        guild_.id = str(guild.id)

        if (guild_.id in self.settings["guilds"].keys()):
            if ("mute_role" in self.settings["guilds"][guild_.id].keys()):
                role = discord.utils.get(guild.roles, id=self.settings["guilds"][guild_.id]["mute_role"])
                if (role):
                    return role

                del self.settings["guilds"][guild_.id]["mute_role"]

                if (not self.settings["guilds"][guild_.id]):
                    del self.settings["guilds"][guild_.id]

    def get_prefixes(self, guild: discord.Guild = None) -> list:
        if (guild):
            guild_ = copy.copy(guild)
            guild_.id = str(guild.id)

            if (guild_.id in self.settings["guilds"].keys()):
                if ("prefix" in self.settings["guilds"][guild_.id].keys()):
                    prefix = [self.settings["guilds"][guild_.id]["prefix"]]
                    return prefix + self.prefixes

        return self.prefixes

    def get_restart_message(self) -> tuple:
        if ("restart_message" in self.settings):
            return self.settings["restart_message"]

        return (None, None)
    
    def save(self):
        dataio.save("data/sbt/settings.json", self.settings)

    def set_guild_administrator_role(self, guild: discord.Guild, role: discord.Role or None):
        guild_ = copy.copy(guild)
        guild_.id = str(guild.id)

        if (guild_.id not in self.settings["guilds"].keys()):
            self.settings["guilds"][guild_.id] = dict()

        if (role):
            self.settings["guilds"][guild_.id]["administrator_role"] = role.id
        else:
            if ("administrator_role" in self.settings["guilds"][guild_.id].keys()):
                del self.settings["guilds"][guild_.id]["administrator_role"]

                if (not self.settings["guilds"][guild_.id]):
                    del self.settings["guilds"][guild_.id]

    def set_guild_moderator_role(self, guild: discord.Guild, role: discord.Role or None):
        guild_ = copy.copy(guild)
        guild_.id = str(guild.id)

        if (guild_.id not in self.settings["guilds"].keys()):
            self.settings["guilds"][guild_.id] = dict()

        if (role):
            self.settings["guilds"][guild_.id]["moderator_role"] = role.id
        else:
            if ("moderator_role" in self.settings["guilds"][guild_.id].keys()):
                del self.settings["guilds"][guild_.id]["moderator_role"]

                if (not self.settings["guilds"][guild_.id]):
                    del self.settings["guilds"][guild_.id]

    def set_guild_mute_role(self, guild: discord.Guild, role: discord.Role or None):
        guild_ = copy.copy(guild)
        guild_.id = str(guild.id)

        if (guild_.id not in self.settings["guilds"].keys()):
            self.settings["guilds"][guild_.id] = dict()

        if (role):
            self.settings["guilds"][guild_.id]["mute_role"] = role.id
        else:
            if ("mute_role" in self.settings["guilds"][guild_.id].keys()):
                del self.settings["guilds"][guild_.id]["mute_role"]

                if (not self.settings["guilds"][guild_.id]):
                    del self.settings["guilds"][guild_.id]

        self.save()

    def set_guild_prefix(self, guild: discord.Guild, prefix: str = None):
        guild_ = copy.copy(guild)
        guild_.id = str(guild.id)

        if (guild_.id not in self.settings["guilds"].keys()):
            self.settings["guilds"][guild_.id] = dict()

        if (prefix):
            self.settings["guilds"][guild_.id]["prefix"] = prefix
        else:
            if ("prefix" in self.settings["guilds"][guild_.id]):
                del self.settings["guilds"][guild_.id]["prefix"]

                if (not self.settings["guilds"][guild_.id]):
                    del self.settings["guilds"][guild_.id]

        self.save()

    def set_restart_message(self, message_id: int, channel_id: int):
        self.settings["restart_message"] = (message_id, channel_id)
        self.save()