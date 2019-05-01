"""
/modules/audio.py

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
    "Audio",
    "setup",
}


import asyncio
import typing
import youtube_dl

import discord
from discord.ext import commands

from utils import (
    checks,
)


# silence youtube_dl ;(
youtube_dl.utils.bug_reports_message = lambda: ""

YOUTUBE_DL_FORMAT_OPTIONS = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
}

FFMPEG_OPTIONS = {
    "options": "-vn"
}

PLAYER = youtube_dl.YoutubeDL(YOUTUBE_DL_FORMAT_OPTIONS)


class YoutubeDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(self, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: PLAYER.extract_info(url, download=not stream))

        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else PLAYER.prepare_filename(data)
        return self(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)

class Audio(commands.Cog, name="audio"):
    __all__ = {
        "__init__",
        "join",
        "stop",
    }

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.__authors__ = __authors__
        self.__maintainers__ = __maintainers__
        self.__version_info__ = __version_info__
        self.__version__ = __version__
        self.__level__ = __level__

        super().__init__()

    @checks.is_dj()
    @commands.command(name="join")
    async def _join(self, ctx: commands.Context, *, channel: typing.Optional[discord.VoiceChannel]):
        """
        join a voice channel
        """

        if (not channel):
            if (not ctx.author.voice):
                await ctx.send("you're not in a voice channel")
                return

            channel = ctx.author.voice.channel

        if (ctx.voice_client):
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()

        await ctx.send("done.")

    @checks.is_dj()
    @commands.command(name="play", aliases=["p"])
    async def _play(self, ctx: commands.Context, url: str):
        """
        play a url
        """

        if (not ctx.voice_client):
            await ctx.send("i'm not connected to voice in this guild")
            return

        url = url.strip("<>")

        async with ctx.typing():
            player = await YoutubeDLSource.from_url(url)
            ctx.voice_client.play(player, after=lambda e: print(e) if e else None)

        await ctx.send("playing {0}".format(player.title))

    @checks.is_dj()
    @commands.command(name="stop")
    async def _stop(self, ctx: commands.Context):
        """
        stop and disconnect
        """

        if (not ctx.voice_client):
            await ctx.send("i'm not connected to voice in this guild")
            return

        await ctx.voice_client.disconnect()
        await ctx.send("done.")
    

def setup(bot: commands.Bot):
    extension = Audio(bot)
    bot.add_cog(extension)