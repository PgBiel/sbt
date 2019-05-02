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
import traceback
import typing
import youtube_dl

import discord
from discord.ext import commands

from utils import (
    checks,
    dataio,
)


# silence youtube_dl ;(
youtube_dl.utils.bug_reports_message = lambda: ""

YOUTUBE_DL_FORMAT_OPTIONS = {
    "format": "bestaudio/best",
    "outtmpl": "data\\audio\\cache\\%(id)s.audio",
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
    "executable": "ffmpeg/ffmpeg",
    "options": "-vn",
}

PLAYER = youtube_dl.YoutubeDL(YOUTUBE_DL_FORMAT_OPTIONS)


class YoutubeDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: PLAYER.extract_info(url, download=not stream))

        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else PLAYER.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)

class Audio(commands.Cog, name="audio"):
    __all__ = {
        "__init__",
        "_join",
        "_play",
        "_stop",
        "_stream",
        "_volume",
    }

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.__authors__ = __authors__
        self.__maintainers__ = __maintainers__
        self.__version_info__ = __version_info__
        self.__version__ = __version__
        self.__level__ = __level__

        self.settings = dataio.load("data/audio/settings.json")

        super().__init__()

    def save(self):
        return dataio.save("data/audio/settings.json", self.settings)

    @checks.is_dj()
    @commands.command(name="join")
    async def _join(self, ctx: commands.Context, *, channel: typing.Optional[discord.VoiceChannel]):
        """
        join a voice channel
        """

        if (ctx.voice_client):
            if (ctx.author not in ctx.voice_client.channel.members):
                # no stealing
                raise commands.errors.MissingPermissions([])

        if (not channel):
            if (not ctx.author.voice):
                await ctx.send("you're not in a voice channel")
                return

            channel = ctx.author.voice.channel

        if (ctx.voice_client):
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()

        if (ctx.invoked_with == "join"):
            await ctx.send("done.")

    @checks.is_dj()
    @commands.command(name="play", aliases=["p"])
    async def _play(self, ctx: commands.Context, url: str):
        """
        play a url
        """

        def after(exception):
            if (exception):
                traceback.print_exception(type(exception), exception, None)

            self.__after(ctx)

        if (not ctx.voice_client):
            await ctx.invoke(self._join, channel=None)
            if (not ctx.voice_client):
                # didn't get a voice_client
                return

        url = url.strip("<>")

        async with ctx.typing():
            player = await YoutubeDLSource.from_url(url)
            ctx.voice_client.play(player, after=after)

            if (str(ctx.guild.id) in self.settings["guilds"].keys()):
                if ("volume" in self.settings["guilds"][str(ctx.guild.id)].keys()):
                    ctx.voice_client.source.volume = self.settings["guilds"][str(ctx.guild.id)]["volume"] / 100

        await ctx.send("playing `{0}`".format(player.title))

    @checks.is_dj()
    @commands.command(name="stop")
    async def _stop(self, ctx: commands.Context):
        """
        stop and disconnect
        """

        if (not ctx.voice_client):
            await ctx.send("i'm not connected to voice in this guild")
            return
        
        if (ctx.author not in ctx.voice_client.channel.members):
            # no
            raise commands.errors.MissingPermissions([])

        await ctx.voice_client.disconnect()
        await ctx.send("done.")

    @checks.is_dj()
    @checks.is_owner()
    @commands.command(name="stream")
    async def _stream(self, ctx: commands.Context, url: str):
        """
        play a stream
        """

        def after(exception):
            if (exception):
                traceback.print_exception(type(exception), exception, None)

            self.__after(ctx)

        if (not ctx.voice_client):
            await ctx.invoke(self._join, channel=None)
            if (not ctx.voice_client):
                # didn't get a voice_client
                return

        url = url.strip("<>")

        async with ctx.typing():
            player = await YoutubeDLSource.from_url(url, stream=True)
            ctx.voice_client.play(player, after=after)

        await ctx.send("streaming `{0}`".format(player.title))

    @checks.is_dj()
    @commands.command(name="volume", aliases=["vol"])
    async def _volume(self, ctx: commands.Context, volume: typing.Optional[int]):
        """
        show or change the volume
        """

        if (not ctx.voice_client):
            await ctx.send("i'm not connected to voice in this guild")
            return

        if (volume == None):
            await ctx.send("{0}%".format(int(ctx.voice_client.source.volume * 100)))
            return

        if (not (200 >= volume >= 0)):
            await ctx.send("invalid volume")
            return

        if (str(ctx.guild.id) not in self.settings["guilds"].keys()):
            self.settings["guilds"][str(ctx.guild.id)] = dict()
        self.settings["guilds"][str(ctx.guild.id)]["volume"] = volume
        self.save()

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("done.")

        if (200 >= volume > 100):
            await ctx.send("sound usually breaks when volume > 100")

    @_play.error
    @_stream.error
    async def on_command_error(self, ctx: commands.Context, exception: discord.errors.DiscordException):
        if (isinstance(exception, youtube_dl.utils.DownloadError)):
            # probably failed to rename a file, retry
            await ctx.bot.invoke(ctx)
            return

    def __after(self, ctx: commands.Context):
        pass
    

def setup(bot: commands.Bot):
    extension = Audio(bot)
    bot.add_cog(extension)