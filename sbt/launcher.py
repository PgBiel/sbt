"""
/launcher.py

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

__level__             = 0


import os
import subprocess
import sys

import pyfiglet


class SBT():
    def __init__(self):
        pass

    def main_menu(self):
        os.system("title SBT v2")

        while (True):
            os.system("cls")

            print()
            print(pyfiglet.figlet_format("SBT v2"))
            print()
            print("[0] - Quit")
            print()
            print("[1] - Run SBT (auto_restart = True)")
            print("[2] - Run SBT")
            print()

            choice = input("> ").strip()

            print()

            if (choice == "0"):
                break
            elif (choice == "1"):
                self.run(auto_restart = True)
            elif (choice == "2"):
                self.run()

    def run(self, auto_restart: bool = False):
        arguments = [sys.executable, "main.py"]

        while (True):
            try:
                code = subprocess.call(arguments)
            except (Exception) as e:
                if (not auto_restart):
                    break
            else:
                if (code == 587):
                    # owner._restart
                    pass
                elif (code == 50):
                    # owner._shutdown
                    break
                elif (not auto_restart):
                    break

if (__name__ == "__main__"):
    sbt = SBT()
    sbt.main_menu()