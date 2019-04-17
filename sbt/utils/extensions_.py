"""
/utils/extensions.py

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
__version__           = ".".join([str(n) for n in __version_info__[:3:]]) + "".join([str(n)[0] for n in __version_info__[3:]])


class Extensions():
    def __init__(self):
        self.extensions = {
            "alias": {
                "commands": {},
                "groups": {
                    "_aliassettings": (
                        ["_alias"],
                        ["self", "ctx"],
                        "alias group",
                        {
                            "_aliassettings_add": (
                                ["_aliassettings_create"],
                                ["self", "ctx", "name"],
                                "create an alias",
                                {},
                            ),
                            "_aliassettings_help": (
                                [],
                                ["self", "ctx", "name"],
                                "display help for the base command of an alias",
                                {},
                            ),
                            "_aliassettings_list": (
                                [],
                                ["self", "ctx"],
                                "list aliases",
                                {},
                            ),
                            "_aliassettings_remove": (
                                ["_aliassettings_delete"],
                                ["self", "ctx", "name"],
                                "delete an alias",
                                {},
                            ),
                        },
                    ),
                },
                "level": "2",
                "listeners": {
                    "_on_message",
                },
                "loops": [],
            },
            "alpha": {
                "commands": {},
                "groups": {},
                "level": "5",
                "listeners": [],
                "loops": [],
            },
            "analytics": {
                "commands": {},
                "groups": {
                    "_analytics": (
                        [],
                        ["self", "ctx"],
                        "all analytics",
                        {
                            "_analytics_channel": (
                                [],
                                ["self", "ctx"],
                                "channel analytics",
                                {},
                            ),
                            "_analytics_cog": (
                                [],
                                ["self", "ctx"],
                                "channel analytics",
                                {},
                            ),
                            "_analytics_command": (
                                [],
                                ["self", "ctx"],
                                "channel analytics",
                                {},
                            ),
                            "_analytics_guild": (
                                [],
                                ["self", "ctx"],
                                "guild analytics",
                                {},
                            ),
                            "_analytics_level": (
                                [],
                                ["self", "ctx"],
                                "channel analytics",
                                {},
                            ),
                            "_analytics_user": (
                                [],
                                ["self", "ctx"],
                                "user analytics",
                                {},
                            ),
                        },
                    ),
                },
                "level": "4",
                "listeners": [
                    "_on_channel_create",
                    "_on_channel_delete",
                    "_on_channel_update",
                    "_on_command",
                    "_on_command_error",
                    "_on_group_join",
                    "_on_group_remove",
                    "_on_member_ban",
                    "_on_member_join",
                    "_on_member_remove",
                    "_on_member_unban",
                    "_on_member_update",
                    "_on_message",
                    "_on_message_delete",
                    "_on_message_edit",
                    "_on_ready",
                    "_on_reaction_add",
                    "_on_reaction_clear",
                    "_on_reaction_remove",
                    "_on_resumed",
                    "_on_guild_available",
                    "_on_guild_emojis_update",
                    "_on_guild_join",
                    "_on_guild_remove",
                    "_on_guild_role_create",
                    "_on_guild_role_delete",
                    "_on_guild_role_update",
                    "_on_guild_update",
                    "_on_guild_unavailable",
                    "_on_socket_raw_recieve",
                    "_on_socket_raw_send",
                    "_on_typing",
                    "_on_voice_state_update",
                ],
                "loops": [
                    "_autosave",
                ],
            },
            "audio": {
                "commands": {
                    "_disconnect": (
                        [],
                        ["self", "ctx", "guild"],
                        "disconnect sbt from all voice channels",
                    ),
                    "_pause": (
                        [],
                        ["self", "ctx"],
                        "pause playback",
                    ),
                    "_play": (
                        [],
                        ["self", "ctx", "url"],
                        "play a song",
                    ),
                    "_previous": (
                        ["_prev"],
                        ["self", "ctx"],
                        "go back to the previous song",
                    ),
                    "_queue": (
                        [],
                        ["self", "ctx", "url"],
                        "queue a song",
                    ),
                    "_resume": (
                        [],
                        ["self", "ctx"],
                        "resume playback",
                    ),
                    "_shuffle": (
                        [],
                        ["self", "ctx"],
                        "shuffle the queue",
                    ),
                    "_skip": (
                        ["_next"],
                        ["self", "ctx"],
                        "skip to the next song",
                    ),
                    "_song": (
                        [],
                        ["self", "ctx"],
                        "display information on the current song",
                    ),
                    "_stop": (
                        [],
                        ["self", "ctx"],
                        "stop playing music",
                    ),
                },
                "groups": {
                    "_audiosettings": (
                        ["_audio"],
                        ["self", "ctx"],
                        "show current settings",
                        {
                            "_audiosettings_notifications": (
                                ["_audiosettings_nowplaying"],
                                ["self", "ctx", "channel"],
                                "toggle 'now playing' notifications",
                                {},
                            ),
                            "_audiosettings_volume": (
                                [],
                                ["self", "ctx", "volume"],
                                "change the volume",
                                {},
                            ),
                        },
                    ),
                    "_cache": (
                        [],
                        ["self", "ctx"],
                        "cache group",
                        {
                            "_cache_dump": (
                                [],
                                ["self", "ctx"],
                                "dump audio cache files",
                                {},
                            ),
                        },
                    ),
                    "_playlist": (
                        [],
                        ["self", "ctx"],
                        "playlist group",
                        {
                            "_playlist_add": (
                                ["_playlist_append"],
                                ["self", "ctx", "name", "url"],
                                "add a song to a playlist",
                                {},
                            ),
                            "_playlist_create": (
                                [],
                                ["self", "ctx", "name"],
                                "create a playlist",
                                {},
                            ),
                            "_playlist_list": (
                                [],
                                ["self", "ctx"],
                                "list local and global playlists",
                                {},
                            ),
                            "_playlist_mix": (
                                ["_playlist_shuffle"],
                                ["self", "ctx", "name"],
                                "start an already-shuffled playlist",
                                {},
                            ),
                            "_playlist_delete": (
                                ["_playlist_remove"],
                                ["self", "ctx", "name"],
                                "delete a playlist",
                                {},
                            ),
                            "_playlist_start": (
                                ["_playlist_play"],
                                ["self", "ctx", "name"],
                                "start a playlist",
                                {},
                            ),
                        },
                    ),
                    "_repeat": (
                        [],
                        ["self", "ctx"],
                        "repeat group",
                        {
                            "_repeat_song": (
                                [],
                                ["self", "ctx"],
                                "repeat the current song",
                                {},
                            ),
                            "_repeat_queue": (
                                [],
                                ["self", "ctx"],
                                "repeat the current queue",
                                {},
                            ),
                        },
                    ),
                },
                "level": "2",
                "listeners": [
                    "_on_voice_state_update",
                ],
                "loops": [
                    "_queue_scheduler",
                    "_disconnect_timer",
                    "_reload_monitor",
                    "_cache_scheduler",
                    "_ws_reset_timer",
                ],
            },
            "autorole": {
                "commands": {},
                "groups": {
                    "_autorolesettings": (
                        ["_autorole"],
                        ["self", "ctx"],
                        "autorole group",
                        {
                            "_autorolesettings_add": (
                                ["_autorolesettings_create"],
                                ["self", "ctx", "role"],
                                "create an autorole",
                                {},
                            ),
                            "_autorolesettings_list": (
                                [],
                                ["self", "ctx"],
                                "list autoroles",
                                {},
                            ),
                            "_autorolesettings_remove": (
                                ["_autorolesettings_delete"],
                                ["self", "ctx", "role"],
                                "delete an autorole",
                                {},
                            ),
                            "_autorolesettings_toggle": (
                                [],
                                ["self", "ctx", "role"],
                                "toggle autoroles",
                                {},
                            ),
                        },
                    ),
                },
                "level": "2",
                "listeners": [
                    "_on_member_join",
                ],
                "loops": [],
            },
            "beta": {
                "commands": {},
                "groups": {},
                "level": "5",
                "listeners": [],
                "loops": [],
            },
            "customcommands": {
                "commands": {},
                "groups": {
                    "_customcommand": (
                        ["_cc"],
                        ["self", "ctx"],
                        {
                            "_customcommand_create": (
                                ["_customcommand_add"],
                                ["self", "ctx", "name", "text"],
                                "create a custom command",
                                {},
                            ),
                            "_customcommand_edit": (
                                [],
                                ["self", "ctx", "name", "text"],
                                "edit a custom command",
                                {},
                            ),
                            "_customcommand_list": (
                                [],
                                ["self", "ctx"],
                                "list custom commands",
                                {},
                            ),
                            "_customcommand_delete": (
                                ["_customcommand_remove"],
                                ["self", "ctx", "name"],
                                "delete a custom command",
                                {},
                            ),
                        },
                    ),
                },
                "level": "3",
                "listeners": [
                    "_on_message",
                ],
                "loops": [],
            },
            "economy": {
                "commands": {
                    "_payday": (
                        [],
                        ["self", "ctx"],
                        "collect your payday",
                    ),
                    "_slot": (
                        ["_bet"],
                        ["self", "ctx", "bet"],
                        "play on the slot machine",
                    ),
                },
                "groups": {
                    "_bank": (
                        ["_account"],
                        ["self", "ctx"],
                        "",
                        {
                            "_bank_balance": (
                                [],
                                ["self", "ctx", "user"],
                                "display a users bank balance",
                                {},
                            ),
                            "_bank_reset": (
                                [],
                                ["self", "ctx", "guild"],
                                "reset a users bank account",
                                {},
                            ),
                            "_bank_set": (
                                [],
                                ["self", "ctx", "user"],
                                "set a users bank account",
                                {
                                    "_bank_set_balance": (
                                        [],
                                        ["self", "ctx", "balance"],
                                        "set a users bank balance",
                                        {},
                                    ),
                                },
                            ),
                            "_bank_transfer": (
                                ["_bank_send"],
                                ["self", "ctx", "user", "amount"],
                                "transfer credits to a user",
                                {},
                            ),
                        },
                    ),
                    "_economysettings": (
                        ["_economy"],
                        ["self", "ctx"],
                        "economy settings group",
                        {
                            "_economysettings_payday": (
                                [],
                                ["self", "ctx"],
                                "payday group",
                                {
                                    "_economysettings_payday_credits": (
                                        [],
                                        ["self", "ctx", "amount"],
                                        "set the amount of credits given on a payday",
                                        {},
                                    ),
                                    "_economysettings_payday_time": (
                                        [],
                                        ["self", "ctx", "time"],
                                        "set the amount of time between ",
                                        {},
                                    ),
                                },
                            ),
                            "_economysettings_slot": (
                                [],
                                ["self", "ctx"],
                                "slot group",
                                {
                                    "_economysettings_slot_maximum": (
                                        ["_economysettings_bet_maximum"],
                                        ["self", "ctx", "amount"],
                                        "set the maximum bet",
                                        {},
                                    ),
                                    "_economysettings_slot_minimum": (
                                        ["_economysettings_bet_minimum"],
                                        ["self", "ctx", "amount"],
                                        "set the minimum bet",
                                        {},
                                    ),
                                    "_economysettings_slot_time": (
                                        ["_economysettings_bet_time"],
                                        ["self", "ctx", "time"],
                                        "set the minimum time between bets",
                                        {},
                                    ),
                                },
                            ),
                        },
                    ),
                    "_leaderboard": (
                        [],
                        ["self", "ctx"],
                        "display this guild's leaderboard",
                        {
                            "_leaderboard_global": (
                                [],
                                ["self", "ctx"],
                                "display the global leaderboard",
                                {},
                            ),
                        },
                    ),
                },
                "level": "2",
                "listeners": [],
                "loops": [],
            },
            "general": {
                "commands": {
                    "_2D": (
                        ["_ascii"],
                        ["self", "ctx", "text"],
                        "2D-ify text",
                    ),
                    "_choose": (
                        ["_random"],
                        ["self", "ctx", "choices"],
                        "randomly choose a thing",
                    ),
                    "_eightball": (
                        ["_8"],
                        ["self", "ctx", "question"],
                        "ask 8 a yes or no question",
                    ),
                    "_flip": (
                        ["_coin"],
                        ["self", "ctx"],
                        "flip a coin",
                    ),
                    "_google": (
                        ["_g"],
                        ["self", "ctx", "search"],
                        "search google",
                    ),
                    "_intellect": (
                        [],
                        ["self", "ctx", "text"],
                        "iNtELlEcTIfy text",
                    ),
                    "_regex": (
                        ["_re"],
                        ["self", "ctx", "regex", "text"],
                        "do regex things",
                    ),
                    "_reverse": (
                        [],
                        ["self", "ctx", "text"],
                        "esrever text",
                    ),
                    "_roll": (
                        [],
                        ["self", "ctx", "sides", "count"],
                        "roll count die with sides",
                    ),
                    "_rps": (
                        [],
                        ["self", "ctx", "choice"],
                        "play rock, paper, scissors against sbt",
                    ),
                    "_scramble": (
                        [],
                        ["self", "ctx", "text"],
                        "barcmesl text",
                    ),
                    "_spellout": (
                        [],
                        ["self", "ctx", "text"],
                        "s p e l l o u t text",
                    ),
                    "_steam": (
                        [],
                        ["self", "ctx", "search"],
                        "search steam",
                    ),
                    "_stopwatch": (
                        ["_sw"],
                        ["self", "ctx"],
                        "do stopwatch things",
                    ),
                    "_3D": (
                        ["_threedee"],
                        ["self", "ctx", "text"],
                        "3D-ify text",
                    ),
                    "_urban": (
                        [],
                        ["self", "ctx", "search"],
                        "search urban dictionary",
                    ),
                },
                "groups": {},
                "level": "2",
                "listeners": [],
                "loops": [],
            },
            "information": {
                "commands": {
                    "_color": (
                        ["_colour"],
                        ["self", "ctx", "code"],
                        "parse and display a color",
                    ),
                    "_contributors": (
                        ["_affiliates"],
                        ["self", "ctx"],
                        "display sbt's contributors",
                    ),
                    "_daysuntil": (
                        ["_dayssince"],
                        ["self", "ctx", "month", "day", "year"],
                        "display distance between two times",
                    ),
                    "_discriminator": (
                        ["_discrim"],
                        ["self", "ctx", "discriminator"],
                        "display all users with a discriminator",
                    ),
                    "_flags": (
                        [],
                        ["self", "ctx", "user"],
                        "display a user's flags",
                    ),
                    "_invite": (
                        [],
                        ["self", "ctx"],
                        "display sbt's invite links",
                    ),
                    "_messagecount": (
                        ["_messages"],
                        ["self", "ctx", "user"],
                        "display how many messages a user has sent in the past 24 hours",
                    ),
                    "_now": (
                        ["_time", "_pytz"],
                        ["self", "ctx", "timezone"],
                        "display the current time",
                    ),
                    "_latency": (
                        ["_ping"],
                        ["self", "ctx"],
                        "display sbt's latency",
                    ),
                    "_rtfd": (
                        ["_rtd"],
                        ["self", "ctx", "section"],
                        "read the fucking documentation",
                    ),
                    "_statistics": (
                        ["_stats"],
                        ["self", "ctx"],
                        "display sbt's statictics",
                    ),
                    "_version": (
                        [],
                        ["self", "ctx"],
                        "display sbt's versions",
                    ),
                },
                "groups": {
                    "_information": (
                        ["_info"],
                        ["self", "ctx"],
                        "information group",
                        {
                            "_information_bot": (
                                ["_information_client"],
                                ["self", "ctx"],
                                "display sbt's information",
                                {},
                            ),
                            "_information_channel": (
                                [],
                                ["self", "ctx", "channel"],
                                "display channel information",
                                {},
                            ),
                            "_information_guild": (
                                [],
                                ["self", "ctx", "guild"],
                                "display guild information",
                                {},
                            ),
                            "_information_message": (
                                [],
                                ["self", "ctx", "message"],
                                "display message information",
                                {},
                            ),
                            "_information_role": (
                                [],
                                ["self", "ctx", "role"],
                                "display role information",
                                {},
                            ),
                            "_information_system": (
                                [],
                                ["self", "ctx"],
                                "display system information",
                                {},
                            ),
                            "_information_user": (
                                [],
                                ["self", "ctx", "user"],
                                "display user information",
                                {},
                            ),
                        },
                    ),
                    "_permissions": (
                        ["_perms"],
                        ["self", "ctx"],
                        "permissions group",
                        {
                            "_permissions_number": (
                                [],
                                ["self", "ctx", "number"],
                                "display a number's permissions",
                                {},
                            ),
                            "_permissions_role": (
                                [],
                                ["self", "ctx", "role"],
                                "display a role's permissions",
                                {},
                            ),
                            "_permissions_user": (
                                [],
                                ["self", "ctx", "user"],
                                "display a user's permissions",
                                {},
                            ),
                        },
                    ),
                },
                "level": "2",
                "listeners": [],
                "loops": [],
            },
            "logging": {
                "commands": {},
                "groups": {
                    "_loggingsettings": (
                        ["_logging"],
                        ["self", "ctx"],
                        "",
                        {
                            "_loggingsettings_setup": (
                                [],
                                ["self", "ctx"],
                                "",
                                {},
                            ),
                            "_loggingsettings_status": (
                                [],
                                ["self", "ctx"],
                                "display current logging status",
                                {},
                            ),
                            "_loggingsettings_toggle": (
                                [],
                                ["self", "ctx"],
                                "toggle a logging event",
                                {},
                            ),
                        },
                    ),
                },
                "level": "4",
                "listeners": [
                    "_on_channel_create",
                    "_on_channel_delete",
                    "_on_channel_update",
                    "_on_member_ban",
                    "_on_member_join",
                    "_on_member_remove",
                    "_on_member_unban",
                    "_on_member_update",
                    "_on_message",
                    "_on_message_delete",
                    "_on_message_edit",
                    "_on_ready",
                    "_on_resumed",
                    "_on_guild_available",
                    "_on_guild_emojis_update",
                    "_on_guild_join",
                    "_on_guild_remove",
                    "_on_guild_role_create",
                    "_on_guild_role_delete",
                    "_on_guild_role_update",
                    "_on_guild_unavailable",
                    "_on_guild_update",
                    "_on_voice_state_update",
                ],
                "loops": [],
            },
            "moderation": {
                "commands": {
                    "_ban"         : ([],         ["self", "ctx", "user", "time", "reason"], "Ban a user, deleting messages in the time frame given."),
                    "_discordbans" : (["_dbans"], ["self", "ctx", "user"],                   "Check for a user in the discordbans API."),
                    "_hackban"     : (["_idban"], ["self", "ctx", "id", "reason"],           "Ban a user who no longer exists in the guild as a Member."),
                    "_kick"        : ([],         ["self", "ctx", "user", "reason"],         "Kick a user from the guild."),
                    "_mute"        : ([],         ["self", "ctx", "user", "time", "reason"], "Mute a user for the length of time given."),
                    "_names"       : ([],         ["self", "ctx", "user"],                   "Display recent name changes for a user."),
                    "_reason"      : ([],         ["self", "ctx", "case", "reason"],         "Edit the reason for a case."),
                    "_rename"      : ([],         ["self", "ctx", "user", "nickname"],       "Rename a user."),
                    "_softban"     : ([],         ["self", "ctx", "user", "reason"],         "Ban and unban a user; kick, while deleting messages."),
                    "_unban"       : ([],         ["self", "ctx", "user", "reason"],         "Unban a user."),
                    "_unmute"      : ([],         ["self", "ctx", "user", "reason"],         "Unmute a user."),
                    "_warn"        : ([],         ["self", "ctx", "user", "reason"],         "Warn a user.")
                },
                "groups": {
                    "_clear" : (["_delete"], ["self", "ctx"], {
                        "_clear_after" : ([], ["self", "ctx", "day", "month", "year"], "Delete all messages sent after the given date."),
                        "_clear_self"  : ([], ["self", "ctx", "amount"],               "Delete an amount of messages sent by SBT."),
                        "_clear_text"  : ([], ["self", "ctx", "text", "amount"],       "Delete an amount of messages containing the given text."),
                        "_clear_user"  : ([], ["self", "ctx", "user", "amount"],       "Delete an amount of messages sent by a user.")
                    }),
                    "_linkfilter" : ([], ["self", "ctx"], {
                        "_linkfilter_toggle" : ([], ["self", "ctx"], "Toggle the linkfilter.")
                    }),
                    "_moderationsettings" : (["_moderation"], ["self", "ctx"], {
                        "_moderationsettings_banmentionspam" : ([],                          ["self", "ctx", "amount"],         ""),
                        "_moderationsettings_casereset"      : ([],                          ["self", "ctx"],                   ""),
                        "_moderationsettings_casesettings"   : ([],                          ["self", "ctx", "case", "toggle"], ""),
                        "_moderationsettings_deletedelay"    : ([],                          ["self", "ctx", "time"],           ""),
                        "_moderationsettings_deleterepeats"  : ([],                          ["self", "ctx"],                   ""),
                        "_moderationsettings_hierarchy"      : ([],                          ["self", "ctx"],                   ""),
                        "_moderationsettings_logging"        : (["_moderationsettings_log"], ["self", "ctx", "channel"],        "")
                    }),
                    "_role" : ([], ["self", "ctx"], {
                        "_role_add"       : ([],               ["self", "ctx", "user", "role"],     ""),
                        "_role_bots"      : ([],               ["self", "ctx", "role"],             ""),
                        "_role_color"     : (["_role_colour"], ["self", "ctx", "role", "code"],     ""),
                        "_role_create"    : ([],               ["self", "ctx", "role"],             ""),
                        "_role_delete"    : ([],               ["self", "ctx", "role"],             ""),
                        "_role_everyone"  : ([],               ["self", "ctx", "role"],             ""),
                        "_role_humans"    : ([],               ["self", "ctx", "role"],             ""),
                        "_role_name"      : ([],               ["self", "ctx", "role", "name"],     ""),
                        "_role_position"  : ([],               ["self", "ctx", "role", "position"], ""),
                        "_role_rbots"     : ([],               ["self", "ctx", "role"],             ""),
                        "_role_remove"    : ([],               ["self", "ctx", "user", "role"],     ""),
                        "_role_removeall" : ([],               ["self", "ctx", "user"],             ""),
                        "_role_reveryone" : ([],               ["self", "ctx", "role"],             ""),
                        "_role_rhumans"   : ([],               ["self", "ctx", "role"],             "")
                    }),
                    "_wordfilter" : ([], ["self", "ctx"], {
                        "_wordfilter_add"    : ([], ["self", "ctx", "word"], ""),
                        "_wordfilter_clear"  : ([], ["self", "ctx"],         ""),
                        "_wordfilter_remove" : ([], ["self", "ctx", "word"], ""),
                        "_wordfilter_toggle" : ([], ["self", "ctx"],         "")
                    })
                },
                "level": "1",
                "listeners": {
                    "_on_command"       : "Called when any type command is called, returns the command object.",
                    "_on_message"       : "Called when a message is created and sent to a guild.",
                    "_on_message_edit"  : "Called when a message receives an update event. If the message is not found in the Client.messages cache, then these events will not be called. This happens if the message is too old or the client is participating in high traffic guilds. To fix this, increase the max_messages option of Client.",
                    "_on_member_ban"    : "Called when a Member gets banned from a guild. This is NOT called if initiated by a HTTP request.",
                    "_on_member_join"   : "Called when a Member joins a guild.",
                    "_on_member_unban"  : "Called when a User gets unbanned from a guild. This is NOT called if initiated by a HTTP request.",
                    "_on_member_update" : "Called when a Member updates their profile. e.g. status, game playing, avatar, nickname, roles."
                },
                "loops": {},
            },
            "owner": {
                "commands": {
                    "_debug"      : (["_eval"],    ["self", "ctx", "shit"],              "debug shit"),
                    "_do"         : ([],           ["self", "ctx", "times", "command"],  "do command, time -- or something"),
                    "_echo"       : (["_say"],     ["self", "ctx", "message"],           "echo a message"),
                    "_extensions" : (["_modules"], ["self", "ctx"],                      "displays a list of loaded and unloaded extensions"),
                    "_leave"      : ([],           ["self", "ctx", "guild"],             "fine, bye!"),
                    "_load"       : ([],           ["self", "ctx", "module"],            "load an extension"),
                    "_reload"     : ([],           ["self", "ctx", "module"],            "reload an extension"),
                    "_restart"    : ([],           ["self", "ctx"],                      "restart sbt"),
                    "_shutdown"   : ([],           ["self", "ctx"],                      "send sbt back to the launcher"),
                    "_sudo"       : ([],           ["self", "ctx", "member", "command"], "run command as member"),
                    "_unload"     : ([],           ["self", "ctx", "module"],            "unload an extension"),
                    "_uptime"     : ([],           ["self", "ctx"],                      "show uptime in a humanized manner"),
                    "_walk"       : ([],           ["self", "ctx", "module"],            "walk a module"),
                    "_whisper"    : ([],           ["self", "ctx", "member", "command"], "send a message to member"),
                },
                "groups": {
                    "_blacklist" : ([], ["self", "ctx"], "show the current blacklist", {
                        "_blacklist_add"    : ([], ["self", "ctx", "user"], "add a user to the global blacklist"),
                        "_blacklist_remove" : ([], ["self", "ctx", "user"], "remove a user from the global blacklist"),
                    }),
                    "_command" : ([], ["self", "ctx"], "command group", {
                        "_command_disable" : ([], ["self", "ctx", "command"], "disable a command"),
                        "_command_enable"  : ([], ["self", "ctx", "command"], "enable a command"),
                        "_command_hide"    : ([], ["self", "ctx", "command"], "hide a command"),
                        "_command_unhide"  : ([], ["self", "ctx", "command"], "unhide a command"),
                    }),
                    "_contact" : (["_c"], ["self", "ctx", "message"], "contact sbt's support team", {
                        "_contact_respond" : ([], ["self", "ctx", "contact_id", "message"], "respond to a support message"),
                    }),
                    "_loaded" : ([], ["self", "ctx"], "loaded group", {
                        "_loaded_extensions" : (["_loaded_modules"], ["self", "ctx"], "show loaded extensions"),
                        "_loaded_imports"    : ([],                  ["self", "ctx"], "show loaded imports"),
                    }),
                    "_settings" : ([], ["self", "ctx"], "show current settings", {
                        "_settings_game"           : (["_settings_playing"],      ["self", "ctx", "game"],     "change sbt's game"),
                        "_settings_globalprefixes" : (["_settings_globalprefix"], ["self", "ctx", "prefixes"], "change sbt's global prefix"),
                        "_settings_guildprefix"    : (["_settings_prefix"],       ["self", "ctx", "prefix"],   "change sbt's prefix for this guild"),
                        "_settings_muterole"       : (["_settings_mute"],         ["self", "ctx", "role"],     "change sbt's mute role"),
                        "_settings_username"       : ([],                         ["self", "ctx", "name"],     "change sbt's username"),
                        "_settings_nickname"       : ([],                         ["self", "ctx", "name"],     "change sbt's nickname"),
                        "_settings_status"         : ([],                         ["self", "ctx", "status"],   "change sbt's status"),
                    }),
                    "_whitelist" : ([], ["self", "ctx"], "show the current whitelist", {
                        "_whitelist_add"    : ([], ["self", "ctx", "user"], "add a user to the global whitelist"),
                        "_whitelist_remove" : ([], ["self", "ctx", "user"], "remove a user from the global whitelist"),
                    }),
                },
                "level": "1",
                "listeners": {},
                "loops": {},
            },
            "selfrole": {
                "commands": {
                    "_selfrole" : ([], ["self", "ctx", "role"], "")
                },
                "groups": {
                    "_selfrolesettings" : ([], ["self", "ctx"], {
                        "_selfrolesettings_add"    : (["_selfrolesettings_create"], ["self", "ctx", "role"], ""),
                        "_selfrolesettings_list"   : ([],                           ["self", "ctx"],         ""),
                        "_selfrolesettings_remove" : (["_selfrolesettings_delete"], ["self", "ctx", "role"], ""),
                        "_selfrolesettings_toggle" : ([],                           ["self", "ctx"],         "")
                    })
                },
                "level": "2",
                "listeners": {},
                "loops": {},
            },
            "trigger": {
                "commands": {},
                "groups": {
                    "_triggersettings" : (["_trigger"], ["self", "ctx"], {
                        "_triggersettings_add"    : (["_triggersettings_create"], ["self", "ctx", "trigger", "text"], ""),
                        "_triggersettings_list"   : ([],                          ["self", "ctx"],                    ""),
                        "_triggersettings_remove" : (["_triggersettings_delete"], ["self", "ctx", "trigger"],         ""),
                        "_triggersettings_toggle" : ([],                          ["self", "ctx"],                    "")
                    })
                },
                "level": "2",
                "listeners": {
                    "_on_message" : "Called when a message is created and sent to a guild."
                },
                "loops": {},
            },
            "utils": {
                "commands": {
                    "_afk"        : (["_away"],     ["self", "ctx", "time", "text"],     ""),
                    "_do"         : ([],            ["self", "ctx", "command", "times"], ""),
                    "_echo"       : ([],            ["self", "ctx", "text"],             ""),
                    "_openrift"   : (["_rift"],     ["self", "ctx", "channel"],          ""),
                    "_remindme"   : (["_reminder"], ["self", "ctx", "time", "text"],     ""),
                    "_say"        : ([],            ["self", "ctx", "text"],             ""),
                    "_guildlock" : ([],            ["self", "ctx", "time"],             ""),
                    "_sudo"       : ([],            ["self", "ctx", "user", "command"],  ""),
                    "_whisper"    : (["_pm"],       ["self", "ctx", "user", "text"],     "")
                },
                "groups": {},
                "level": "2",
                "listeners": {
                    "_on_message"      : "Called when a message is created and sent to a guild.",
                    "_on_message_edit" : "Called when a message receives an update event. If the message is not found in the Client.messages cache, then these events will not be called. This happens if the message is too old or the client is participating in high traffic guilds. To fix this, increase the max_messages option of Client.",
                    "_on_guild_join"  : "Called when a guild is either created by the Client or when the Client joins a guild.",
                    "_on_typing"       : "Called when someone begins typing a message."
                },
                "loops": {},
            },
            "welcomefarewell": {
                "commands": {},
                "groups": {
                    "_welcfarewsettings" : (["_welcfarew"], ["self", "ctx"], {
                        "_welcfarewsettings_ban"     : ([], ["self", "ctx", "message"], "Set the ban message sent to your WelcomeFarewell channel."),
                        "_welcfarewsettings_channel" : ([], ["self", "ctx", "channel"], "Set the WelcomeFarewell channel."),
                        "_welcfarewsettings_join"    : ([], ["self", "ctx", "message"], "Set the join message sent to your WelcomeFarewell channel."),
                        "_welcfarewsettings_leave"   : ([], ["self", "ctx", "message"], "Set the leave message sent to your WelcomeFarewell channel."),
                        "_welcfarewsettings_toggle"  : ([], ["self", "ctx"],            "Toggle WelcomeFarewell"),
                        "_welcfarewsettings_unban"   : ([], ["self", "ctx", "message"], "Set the unban message sent to your WelcomeFarewell channel.")
                    })
                },
                "level": "2",
                "listeners": {
                    "_on_member_ban"    : "Called when a Member gets banned from a guild. This is NOT called if initiated by a HTTP request.",
                    "_on_member_join"   : "Called when a Member joins a guild.",
                    "_on_member_remove" : "Called when a Member leaves a guild.",
                    "_on_member_unban"  : "Called when a User gets unbanned from a guild. This is NOT called if initiated by a HTTP request."
                },
                "loops": {},
            }
        }
    
    def exists(self, *args):
        """
        check if a key exists in self.extensions
        
        arguments:
            args :: tuple :: a tuple of search queries
        
        returns:
            bool :: ``True`` or ``False`` for key existance
        """
        
        searches = list(set(args))
        results = {}
        
        for (search) in searches:
            if (search in self.search(search).keys()):
                results[search] = True
            else:
                results[search] = False
        
        return results
    
    def search(self, *args):
        """
        search for a key in self.extensions
        
        arguments:
            args :: tuple :: a tuple of search queries
        
        returns:
            the value corresponding to the key searched OR ``None`` if no key was found
        """
        
        searches = list(set(args))
        results = {}
        
        for (search) in searches:
            for (extension, dictionary) in self.extensions.items():
                if (search == extension):
                    # (e.g. "alias")
                    results[search] = dictionary
                    break
                
                for (command, tuple) in dictionary["commands"].items():
                    if (search == command):
                        # (e.g. "_disconnect")
                        results[search] = tuple
                        break
                    
                    for (alias) in tuple[0]:
                        if (search == alias):
                            # (e.g. "_prev")
                            results[search] = tuple
                            break
                
                for (group, tuple) in dictionary["groups"].items():
                    if (search == group):
                        # (e.g. "_aliassettings")
                        results[search] = tuple
                        break
                    
                    for (alias) in tuple[0]:
                        if (search == alias):
                            # (e.g. "_alias")
                            results[search] = tuple
                            break
                    
                    gtuple = tuple
                    # temporary fix for group alias subcommands
                    
                    for (command, tuple) in tuple[2].items():
                        if (search == command):
                            # (e.g. "_aliassettings_add")
                            results[search] = tuple
                            break
                        
                        for (alias) in gtuple[0]:
                            # (e.g. "_alias_add")
                            if (search == command.replace(group, alias)):
                                results[search] = tuple
                                break
                        
                        for (alias) in tuple[0]:
                            if (search == alias):
                                # (e.g. "_aliassettings_create")
                                results[search] = tuple
                                break
                            
                            gcalias = alias
                            # temporary fix for group alias subcommands
                            
                            for (alias) in gtuple[0]:
                                # (e.g. "_alias_create")
                                if (search == gcalias.replace(group, alias)):
                                    results[search] = tuple
                                    break
        
        return results