"""
/utils/dataio.py

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

__version_info__      = (3, 0, 0, "final", 6)
__version__           = "{0}.{1}.{2}{3}{4}".format(*[str(n)[0] if (i == 3) else str(n) for (i, n) in enumerate(__version_info__)])


import json
import os
import random


def save(file_path: str, data: dict) -> int:
    id = random.randint(1000, 9999)
    path, _ = os.path.splitext(file_path)

    file_path_temp = "{0}-{1}.tmp".format(path, id)
    
    try:
        _ = __save(file_path_temp, data)
        _ = __load(file_path_temp)
    except (json.decoder.JSONDecodeError) as e:
        return 1

    os.replace(file_path_temp, file_path)
    return 0

def __save(file_path: str, data: dict):
    with open(file_path, encoding="utf-8", mode="w") as file_stream:
        json.dump(data, file_stream, indent=4, separators=(",", ": "))

def load(file_path: str) -> dict:
    return __load(file_path)

def __load(file_path: str) -> dict:
    with open(file_path, encoding="utf-8", mode="r") as file_stream:
        data = json.load(file_stream)

    return data

def is_valid(file_path: str) -> bool:
    try:
        _ = __load(file_path)
        return True
    except (json.decoder.JSONDecodeError) as e:
        return False