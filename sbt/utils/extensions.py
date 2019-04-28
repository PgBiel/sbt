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

__authors__      = [("shineydev", "contact@shiney.dev")]
__maintainers__  = [("shineydev", "contact@shiney.dev")]

__version_info__ = (2, 0, 0, "alpha", 0)
__version__      = "{0}.{1}.{2}{3}{4}".format(*[str(n)[0] if (i == 3) else str(n) for (i, n) in enumerate(__version_info__)])

__all__ = {
    "Extensions",
}


from discord.ext import commands


class Extensions():
    __all__ = {
        "__init__", "add_extension", "find", "open_path",
    }

    def __init__(self):
        self.extensions = dict()

    def add_extension(self, class_: commands.Cog):
        self.extensions[class_.qualified_name] = dict()
        self.extensions[class_.qualified_name]["commands"] = dict()
        self.extensions[class_.qualified_name]["listeners"] = list()

        for (command) in class_.walk_commands():
            path = [c for c in "{0} {1}".format(command.full_parent_name, command.name).split(" ") if (c)]
            start = self.extensions[class_.qualified_name]["commands"]

            if (len(path) == 1):
                start[command.name] = dict()
            else:
                for (i) in path[:-1]:
                    if ("commands" in start.keys()):
                        start = start["commands"]

                    start = start[i]

                start = start["commands"]
                start[command.name] = dict()

            dict_ = {
                "aliases": command.aliases,
                "commands": dict(),
            }

            start[command.name] = dict_

        for (listener, _) in class_.get_listeners():
            self.extensions[class_.qualified_name]["listeners"].append(listener)

    def find(self, query: str) -> list:
        results = list()

        # cont

    def open_path(self, start: dict, path: list):
        dict_ = start

        for (i) in path:
            dict_ = dict_[i]

        return dict_