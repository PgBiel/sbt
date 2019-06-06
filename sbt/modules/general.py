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

__authors__     = [("shineydev", "contact@shiney.dev")]
__maintainers__ = [("shineydev", "contact@shiney.dev")]

__level__ = 3


import aiohttp
import asyncio
import collections
import datetime
import json
import random
import re
import typing
import urllib

import discord
from discord.ext import commands, tasks

import pyfiglet

from utils import (
    channels,
    context,
    dataio,
    enumerators,
    error,
    checks,
    format,
    fuzzywuzzy,
    paginate,
    parse,
    regex,
    search,
    settings,
)


class General(commands.Cog, name="general"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.__authors__ = __authors__
        self.__maintainers__ = __maintainers__
        self.__level__ = __level__
        
    @commands.command(name="2D", aliases=["ascii"])
    async def _2D(self, ctx: commands.Context, *, text: str):
        """
        2D-ify text

        example:
            `>2D text` :: display "text" in ascii-style font

        references:
            <http://www.figlet.org/examples.html>
        """

        text = pyfiglet.figlet_format(text, font="big")
        if (len(text) > 1992):
            await ctx.send("too long.")
            return

        await ctx.send("```\n{0}```".format(text))
        
    @commands.command(name="3D")
    async def _3D(self, ctx: commands.Context, *, text: str):
        """
        3D-ify text

        example:
            `>3D text` :: display "text" in larry3d-style font

        references:
            <http://www.figlet.org/examples.html>
        """

        text = pyfiglet.figlet_format(text, font="larry3d")
        if (len(text) > 1992):
            await ctx.send("too long.")
            return

        await ctx.send("```\n{0}```".format(text))

    @commands.command(name="choose", aliases=["random"])
    async def _choose(self, ctx: commands.Context, *things: str):
        """
        randomly choose a thing from a list of things

        separate things by spaces
        use quotes to create multi-word strings

        examples:
            `>choose 1 2 3`   :: randomly choose from (1, 2, 3)
            `>choose "1 2" 3` :: randomly choose from ("1 2", 3)
        """

        if (not things):
            await ctx.bot.send_help(ctx)
            return

        thing = random.choice(things)
        await ctx.send(thing)

    @commands.command(name="eightball", aliases=["8"])
    async def _eightball(self, ctx: commands.Context, *, question: str):
        """
        ask 8 a yes or no question

        feel free not to take these answers seriously :)

        example:
            `>eightball do you love me?` :: you may rely on it
        """

        # i like things to be in alpha-numerical order :)
        choices = [
            "as I see it, yes",
            "ask again later",
            "better not tell you now",
            "cannot predict now",
            "concentrate and ask again",
            "don't count on it",
            "it is certain",
            "it is decidedly so",
            "maybe",
            "most likely",
            "my sources say no",
            "no",
            "outlook not so good",
            "outlook good",
            "reply hazy, try again",
            "signs point to yes",
            "very doubtful",
            "without a doubt",
            "yes",
            "you may rely on it",
        ]

        choice = random.choice(choices)
        await ctx.send(choice)

    @commands.cooldown(1, 300, commands.BucketType.user)
    @commands.command(name="embed")
    async def _embed(self, ctx: commands.Context):
        """
        create and edit an embed, then get either the json or the
        code given back to you :)
        """

        previous = collections.deque(maxlen=3)
        current = format.embed()
        next = collections.deque(maxlen=3)

        message = await ctx.send(embed=current)

        keys = [
            "title",
            "description",
            "color", "colour",
            "thumbnail",
            "author",
            "author_url",
            "author_icon_url",
            "field",
            "image",
            "footer",
            "footer_icon_url",
        ]

        reactions = [
            "\U0001f4dd",
            "\U0001f4dc",
            "\U00002b05",
            "\U000027a1",
            "\U00002705",
            "\U0000267b",
            "\U0001f5d1",
        ]

        for (reaction) in reactions:
            await message.add_reaction(reaction)

        while (True):
            def check(reaction: discord.Reaction, member: discord.Member):
                if (member == ctx.author):
                    if (reaction.message.id == message.id):
                        if (str(reaction.emoji) in reactions):
                            return True

                return False

            tasks = {
                asyncio.create_task(ctx.bot.wait_for("reaction_add", check=check, timeout=120)),
                asyncio.create_task(ctx.bot.wait_for("reaction_remove", check=check, timeout=120)),
            }

            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

            try:
                reaction, _ = done.pop().result()
            except (asyncio.TimeoutError) as e:
                await message.clear_reactions()
                ctx.command.reset_cooldown(ctx)
                return

            for (task) in pending:
                task.cancel()

            if (str(reaction.emoji) == reactions[0]):
                def check(message: discord.Message):
                    if (message.author == ctx.author):
                        if (message.channel == ctx.channel):
                            if ("=" in message.content):
                                if (message.content.split("=", 1)[0] in keys):
                                    if (message.content.startswith("field")):
                                        if (message.content.count("|") == 1):
                                            return True
                                        elif (message.content.count("|") == 2):
                                            _, _, inline = message.content.split("|")
                                            if (inline.isdigit()):
                                                if (int(inline) in [0, 1]):
                                                    return True
                                    else:
                                        return True
                            elif (message.content == "field-"):
                                return True

                try:
                    message_ = await ctx.bot.wait_for("message", check=check, timeout=60)
                except (asyncio.TimeoutError) as e:
                    await message.remove_reaction(str(reaction.emoji), ctx.author)
                    continue
                else:
                    if (message_.content == "field-"):
                        if (len(current.fields) != 0):
                            current.remove_field(len(current.fields) - 1)
                            await message.edit(embed=current)
                    else:
                        key, value = message_.content.split("=", 1)

                        if ((len(value) + len(current)) > 6000):
                            await message_.delete()
                            await message.remove_reaction(str(reaction.emoji), ctx.author)
                            continue

                        current_ = current.copy()

                        try:
                            if (key == "title"):
                                if (len(value) <= 256):
                                    previous.append(current.copy())
                                    current_.title = value
                                    next.clear()
                            elif (key == "description"):
                                previous.append(current.copy())
                                current_.description = value
                                next.clear()
                            elif ((key == "color") or (key == "colour")):
                                if (len(value) == 3):
                                    value = "".join(i * 2 for i in value)

                                if (len(value) == 6):
                                    try:
                                        color = int(value, 16)
                                    except (ValueError) as e:
                                        pass
                                    else:
                                        previous.append(current.copy())
                                        current_.color = color
                                        next.clear()
                            elif (key == "thumbnail"):
                                previous.append(current.copy())
                                current_.set_thumbnail(url=value)
                                next.clear()
                            elif (key == "author"):
                                if (len(value) <= 256):
                                    previous.append(current.copy())
                                    current_.set_author(name=value, url=current.author.url, icon_url=current.author.icon_url)
                                    next.clear()
                            elif (key == "author_url"):
                                if (current.author.name != discord.Embed.Empty):
                                    previous.append(current.copy())
                                    current_.set_author(name=current.author.name, url=value, icon_url=current.author.icon_url)
                                    next.clear()
                            elif (key == "author_icon_url"):
                                if (current.author.name != discord.Embed.Empty):
                                    previous.append(current.copy())
                                    current_.set_author(name=current.author.name, url=current.author.url, icon_url=value)
                                    next.clear()
                            elif (key == "field"):
                                if (len(current.fields) < 25):
                                    if (value.count("|") == 1):
                                        name, value = value.split("|")
                                
                                        if (len(name) <= 256):
                                            previous.append(current.copy())
                                            current_.add_field(name=name, value=value)
                                            next.clear()
                                    else:
                                        name, value, inline = value.split("|")

                                        if (len(name) <= 256):
                                            previous.append(current.copy())
                                            current_.add_field(name=name, value=value, inline=bool(int(inline)))
                                            next.clear()
                            elif (key == "image"):
                                previous.append(current.copy())
                                current_.set_image(url=value)
                                next.clear()
                            elif (key == "footer"):
                                previous.append(current.copy())
                                current_.set_footer(text=value, icon_url=current.footer.icon_url)
                                next.clear()
                            elif (key == "footer_icon_url"):
                                if (current.footer.text != discord.Embed.Empty):
                                    previous.append(current.copy())
                                    current_.set_footer(text=current.footer.text, icon_url=value)
                                    next.clear()

                            await message.edit(embed=current_)
                        except (discord.HTTPException) as e:
                            pass
                        else:
                            current = current_.copy()
                        
                await message_.delete()
            elif (str(reaction.emoji) == reactions[1]):
                def check(message: discord.Message):
                    if (message.author == ctx.author):
                        if (message.channel == ctx.channel):
                            try:
                                json.loads(message.content, encoding="utf-8")
                                return True
                            except (json.JSONDecodeError) as e:
                                pass
                try:
                    message_ = await ctx.bot.wait_for("message", check=check, timeout=60)
                except (asyncio.TimeoutError) as e:
                    await message.remove_reaction(str(reaction.emoji), ctx.author)
                    continue
                else:
                    json_ = json.loads(message_.content, encoding="utf-8")
                    dict_ = current.to_dict()
                    dict_.update(json_)

                    previous.append(current.copy())
                    current = discord.Embed.from_dict(dict_)
                    next.clear()

                    await message.edit(embed=current)

                await message_.delete()
            elif (str(reaction.emoji) == reactions[2]):
                if (previous):
                    next.appendleft(current.copy())
                    current = previous.pop()
                    
                    await message.edit(embed=current)
            elif (str(reaction.emoji) == reactions[3]):
                if (next):
                    previous.append(current.copy())
                    current = next.popleft()
                    
                    await message.edit(embed=current)
            elif (str(reaction.emoji) == reactions[4]):
                await message.clear_reactions()

                json_ = current.to_dict()
                if (json_):
                    json_ = json.dumps(json_, indent=2)
                    
                    for (page) in format.pagify(json_, shorten_by=8):
                        await ctx.send("```\n{0}```".format(page))
                        
                    ctx.command.reset_cooldown(ctx)
                    return
            elif (str(reaction.emoji) == reactions[5]):
                previous.append(current.copy())
                current = format.embed()
                next.clear()

                await message.edit(embed=current)
            elif (str(reaction.emoji) == reactions[6]):
                await message.delete()
                ctx.command.reset_cooldown(ctx)
                return

            await message.remove_reaction(str(reaction.emoji), ctx.author)
            
    @commands.command(name="figlet", aliases=["figletformat", "ff", "font"])
    async def _figlet(self, ctx: commands.Context, font: str, *, text: str):
        """
        figlet format text

        fonts can be found in the below reference

        example:
            `>figlet lean text` :: display "text" in lean-style font

        references:
            <http://www.figlet.org/examples.html>
        """

        try:
            text = pyfiglet.figlet_format(text, font=font)
        except (pyfiglet.FontNotFound) as e:
            await ctx.bot.send_help(ctx)
            return

        if (len(text) > 1992):
            await ctx.send("too long.")
            return

        await ctx.send("```\n{0}```".format(text))

    @commands.command(name="flip", aliases=["coin"])
    async def _flip(self, ctx: commands.Context):
        """
        flip a coin

        identical to `>choose heads tails`
        """

        choices = [
            "heads",
            "tails",
        ]

        choice = random.choice(choices)
        await ctx.send(choice)

    @commands.cooldown(1, 30, commands.cooldowns.BucketType.user)
    @commands.command(name="google", aliases=["g"])
    async def _google(self, ctx: commands.Context, *, query: str):
        """
        search google

        using this command in an nsfw-marked channel will disable the safe filter

        example:
            `>google weather in michigan` :: search google for "weather in michigan"
        """

        url = "https://www.google.com/search?q={}".format(urllib.parse.quote_plus(query))

        safe = False
        if (ctx.guild):
            if (not ctx.channel.is_nsfw()):
                safe = True

        try:
            search_ = search.Google(ctx.bot._settings.google_api_key, ctx.bot._settings.google_engine_id)
            results = await search_.search(query, safe=safe)
        except (search.NoResults) as e:
            await ctx.send("no results")
            return
        except (search.NoMoreRequests) as e:
            await ctx.send(format.wrap_url(url))
            return
        except (search.APIError) as e:
            await ctx.send("api error ;(")
            return

        footer = "safe={0} results={1} time={2}".format(
            "on" if safe else "off", results[0].results, results[0].time)
        
        menu = paginate.Menu(ctx)
        menu.appends(self._google_embedinator(ctx, url, footer, results[:9]))
        await menu.start()

    @commands.command(name="hoi", hidden=True)
    async def _hoi(self, ctx: commands.Context, member: typing.Optional[discord.Member]):
        if (not member):
            member = ctx.author

        await ctx.send("`(>'')> {0}`".format(member.display_name))
    
    @commands.command(name="intellect", aliases=["intellectify", "mock"])
    async def _intellect(self, ctx: commands.Context, *, text: str):
        """
        iNtELlEcTIfy text

        this is also known as "mockery text" or "sarcasm text"

        example:
            `>intellect ooooooooooooooooooooooooo` :: spooky
        """

        await ctx.trigger_typing()

        intellect = ""
        for (character) in text:
            intellect += random.choice([character.upper(), character.lower()])
        
        await ctx.send(intellect)

    @commands.command(name="morse")
    async def _morse(self, ctx: commands.Context, *, text: str):
        """
        morse-ify text

        example:
            `>morse text` :: display "text" in morse

        references:
            <http://www.figlet.org/examples.html>
        """

        text = pyfiglet.figlet_format(text, font="morse")
        if (len(text) > 1992):
            await ctx.send("too long.")
            return

        await ctx.send("```\n{0}```".format(text))

    @commands.command(name="pigeonify", aliases=["piglatin", "latin"])
    async def _pigeonify(self, ctx: commands.Context, *words: str):
        """
        pig latin
        """

        if (not words):
            await ctx.bot.send_help(ctx)
            return

        message = ""

        for (word) in words:
            message += word[1:] + word[0] + "ay"
            message += " "

        await ctx.send(message)

    @commands.command(name="reverse")
    async def _reverse(self, ctx: commands.Context, *words: str):
        """
        esrever text

        examples:
            `>reverse "does this need an example?"` :: ?elpmaxe na deen siht seod
            `>reverse does this need an example?`   :: seod siht deen na ?elpmaxe
        """

        if (not words):
            await ctx.bot.send_help(ctx)
            return

        message = ""

        for (word) in words:
            message += word[::-1]
            message += " "

        await ctx.send(message)

    @commands.command(name="roll")
    async def _roll(self, ctx: commands.Context, count: int = 1, sides: int = 6):
        """
        roll count die with sides

        english is hard

        examples:
            `>roll`      :: roll `one`, `six` sided die
            `>roll 2`    :: roll `two`, `six` sided dice
            `>roll 3 10` :: roll `three`, `ten` sided dice
        """

        if ((count < 1) or (sides < 1)):
            await ctx.bot.send_help(ctx)
            return

        rolls = list()

        for (_) in range(count):
           roll = random.randint(1, sides)
           rolls.append(str(roll))

        message = ", ".join(rolls)

        for (page) in format.pagify(message, delims=[" "]):
            if (page):
                await ctx.send(page)

    @commands.command(name="rps")
    async def _rps(self, ctx: commands.Context, choice: parse.RPS):
        """
        play rock, paper, scissors against sbt

        examples:
            `>rps rock`             :: play rock
            `>rps r`                :: play rock
            `>rps :moyai:`          :: play rock
            `>rps paper`            :: play paper
            `>rps p`                :: play paper
            `>rps :page_facing_up:` :: play paper
            `>rps scissors`         :: play scissors
            `>rps s`                :: play scissors
            `>rps :scissors:`       :: play scissors
        """

        player_choice = choice.choice
        player_symbol = getattr(enumerators.RPS, player_choice)
        sbt_choice = random.choice(["r", "p", "s"])
        sbt_symbol = getattr(enumerators.RPS, sbt_choice)

        conditions = {
            ("r", "r"): None,
            ("r", "p"): False,
            ("r", "s"): True,
            ("p", "r"): True,
            ("p", "p"): None,
            ("p", "s"): False,
            ("s", "r"): False,
            ("s", "p"): True,
            ("s", "s"): None,
        }

        outcome = conditions[(player_choice, sbt_choice)]
        
        if (outcome is None):
            await ctx.send("{0} vs {1} -- we tied!".format(player_symbol, sbt_symbol))
            return

        if (outcome):
            await ctx.send("{0} vs {1} -- you win!".format(player_symbol, sbt_symbol))
        else:
            await ctx.send("{0} vs {1} -- you lose!".format(player_symbol, sbt_symbol))

    @commands.command(name="scramble")
    async def _scramble(self, ctx: commands.Context, *words: str):
        """
        barcmesl text

        examples:
            `>scramble "does this need an example?"` :: miaxsnhe tdlds ee en?poe a
            `>scramble does this need an example?`   :: deso stih nede an xplm?eea
        """

        if (not words):
            await ctx.bot.send_help(ctx)
            return

        message = list()

        for (word) in words:
            word = "".join([letter for letter in random.sample(word, len(word))])
            message.append(word)

        await ctx.send(" ".join(message))

    @commands.command(name="semiscramble", aliases=["sscramble", "ss"])
    async def _semiscramble(self, ctx: commands.Context, *words: str):
        """
        smarimlescbe text

        examples:
            `>sscramble "does this need an example?"` :: denleh snesptai emoda e x?
            `>sscramble does this need an example?`   :: deos tihs need an elpxema?
        """

        if (not words):
            await ctx.bot.send_help(ctx)
            return

        message = list()

        for (word) in words:
            if (len(word) in [1, 2, 3]):
                message.append(word)
                continue

            first = word[0]
            last = word[-1]

            word = word[1:-1]
            word = "".join([letter for letter in random.sample(word, len(word))])
            word = first + word + last

            message.append(word)

        await ctx.send(" ".join(message))

    @commands.command(name="spellout")
    async def _spellout(self, ctx: commands.Context, *, text: str):
        """
        s p e l l o u t text

        yeah i think you understand what this one does
        """

        message = ""
        for (character) in text:
            message += "{0} ".format(character)

        for (page) in format.pagify(message, delims=[" "]):
            if (page):
                await ctx.send(page)

    @commands.command(name="steam")
    async def _steam(self, ctx: commands.Context, *, search: str):
        """
        search steam

        example:
            `>steam thing` :: search steam for "thing"
        """

        pass

    @commands.command(name="stopwatch", aliases=["sw"])
    async def _stopwatch(self, ctx: commands.Context):
        """
        do stopwatch things

        stopwatch things == start / stop
        """

        if (not hasattr(self, "stopwatches")):
            self.stopwatches = dict()

        if (str(ctx.author.id) not in self.stopwatches):
            self.stopwatches[str(ctx.author.id)] = datetime.datetime.utcnow()
            await ctx.send("stopwatch started")
        else:
            seconds = (datetime.datetime.utcnow() - self.stopwatches.pop(str(ctx.author.id))).total_seconds()
            await ctx.send("stopwatch stopped")
            await ctx.send(format.humanize_seconds(seconds))

    @checks.is_guild()
    @commands.command(name="topic")
    async def _topic(self, ctx: commands.Context, channel: typing.Optional[discord.TextChannel]):
        """
        display the topic of a channel

        defaults to the current channel
        """

        if (not channel):
            channel = ctx.channel

        if (not channel.topic):
            await ctx.send("this channel has no topic")
            return

        await ctx.send(channel.topic)

    @commands.cooldown(1, 30, commands.cooldowns.BucketType.user)
    @commands.command(name="urban")
    async def _urban(self, ctx: commands.Context, *, search: str):
        """
        search urban dictionary

        should be used in an nsfw-marked channel

        example:
            `>urban thing` :: search urban dictionary for "thing"
        """

        if (not ctx.channel.is_nsfw()):
            await ctx.send("this command should be used in an nsfw-marked channel")
            ctx.command.reset_cooldown(ctx)
            return

        search = urllib.parse.quote_plus(search, encoding="utf-8", errors="replace")
        url = "http://api.urbandictionary.com/v0/define?term={0}".format(search)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if (response.status != 200):
                    await ctx.send(response.status)
                    ctx.command.reset_cooldown(ctx)
                    return

                json_ = await response.json()

        results = json_["list"]

        if (not results):
            await ctx.send("no results")
            ctx.command.reset_cooldown(ctx)
            return

        color = ctx.guild.me.color if ctx.guild else None
        embeds = list()
        for (i, result) in enumerate(results, 1):
            title = "{0} {1}/{2}".format(result["word"], i, len(results))
            if (len(title) > 256):
                title = "{0}...".format(title[:253])

            description = re.sub(r"\[([a-zA-Z0-9\']+)\]",
                                 r"[\1](https://www.urbandictionary.com/define.php?term=\1)",
                                 result["definition"])
            if (len(description) > 2048):
                description = "{0}...".format(description[:2045])

            example = re.sub(r"\[([a-zA-Z0-9\']+)\]",
                             r"[\1](https://www.urbandictionary.com/define.php?term=\1)",
                             result["example"])
            if (not example):
                example = "no example"
            elif (len(example) > 1024):
                example = "{0}...".format(example[1021])

            e = format.embed(description=description,
                             color=color,
                             author=title,
                             author_url=result["permalink"],
                             fields=[
                                 ("Example", example)
                             ],
                             footer="{0} | {1}".format(
                                 ctx.author,
                                 format.humanize_datetime()
                             ),
                             footer_icon_url=ctx.author.avatar_url)

            embeds.append(e)

        message = await ctx.send(embed=embeds[0])

        if (len(embeds) == 1):
            ctx.command.reset_cooldown(ctx)
            return

        current = 0

        reactions = [
            "\U000023ea",
            "\U00000023\U000020e3",
            "\U000023e9",
            "\U0001f5d1",
        ]

        for (reaction) in reactions:
            await message.add_reaction(reaction)

        while (True):
            def check(reaction: discord.Reaction, member: discord.Member):
                if (member == ctx.author):
                    if (reaction.message.id == message.id):
                        if (str(reaction.emoji) in reactions):
                            return True

            tasks = {
                asyncio.create_task(ctx.bot.wait_for("reaction_add", check=check, timeout=120)),
                asyncio.create_task(ctx.bot.wait_for("reaction_remove", check=check, timeout=120)),
            }

            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

            try:
                reaction, _ = done.pop().result()
            except (asyncio.TimeoutError) as e:
                await message.clear_reactions()
                return

            for (task) in pending:
                task.cancel()

            if (str(reaction.emoji) == reactions[0]):
                current -= 1
                if (current < 0):
                    current = len(embeds) - 1
            elif (str(reaction.emoji) == reactions[1]):
                def check(message: discord.Message):
                    if (message.author == ctx.author):
                        if (message.channel == ctx.channel):
                            if (message.content.isdigit()):
                                if (int(message.content) >= 1):
                                    if (int(message.content) <= len(embeds)):
                                        return True

                message_ = await ctx.send("choose a page (1-{0})".format(len(embeds)))

                try:
                    page = await ctx.bot.wait_for("message", check=check, timeout=60)
                except (asyncio.TimeoutError) as e:
                    await message_.delete()
                    await message.remove_reaction(str(reaction.emoji), ctx.author)
                    continue

                await message_.delete()
                await page.delete()

                if (current == (int(page.content) - 1)):
                    continue
            
                current = int(page.content) - 1
            elif (str(reaction.emoji) == reactions[2]):
                current += 1
                if (current > (len(embeds) - 1)):
                    current = 0
            elif (str(reaction.emoji) == reactions[3]):
                await message.clear_reactions()
                ctx.command.reset_cooldown(ctx)
                return

            await message.remove_reaction(str(reaction.emoji), ctx.author)
            await message.edit(embed=embeds[current])

    @commands.group(name="regex", aliases=["re"], invoke_without_command=True)
    async def _regex(self, ctx: commands.Context):
        """
        do regex things
        """

        await ctx.bot.send_help(ctx)

    @_regex.command(name="findall")
    async def _regex_findall(self, ctx: commands.Context, pattern: str, *, string: str):
        r"""
        re.findall

        example:
            `>regex \d test123`
        """

        try:
            pattern = re.compile(pattern)
        except (re.error) as e:
            await ctx.send("couldn't compile regex pattern")
            return

        matches = re.findall(pattern, string)
        if (not matches):
            await ctx.send("no matches")
            return

        # cont
        
    @_regex.command(name="fullmatch")
    async def _regex_fullmatch(self, ctx: commands.Context, pattern: str, *, string: str):
        r"""
        re.fullmatch

        example:
            `regex fullmatch r"https?://(?:.+)\.dev/?" https://shiney.dev/`
        """

        try:
            pattern = re.compile(pattern)
        except (re.error) as e:
            await ctx.send("couldn't compile regex pattern")
            return

        match = re.fullmatch(pattern, string)
        if (not match):
            await ctx.send("no match")
            return

        for (group) in match.groups():
            pass

        # cont

    def _google_embedinator(self, ctx: commands.Context, url: str, footer: str, results: list):
        embeds = list()

        color = random.choice([0xDB4437, 0x0F9D58, 0x4285F4, 0xF4B400])

        for (chunk) in paginate._chunk(results, search.RESULTS_PER_PAGE):
            e = discord.Embed(color=color)
            e.set_author(name="Google", url=url, icon_url=search.GOOGLE_ICON)

            for (result) in chunk:
                value = "{0}\n{1}".format(result.url, result.description)
                e.add_field(name=result.title, value=value, inline=False)

            e.set_footer(
                text = "{0} | {1}".format(
                    ctx.author,
                    footer,
                ),
                icon_url = ctx.author.avatar_url,
            )

            embeds.append(e)

        return embeds
                

def setup(bot: commands.Bot):
    extension = General(bot)
    bot.add_cog(extension)