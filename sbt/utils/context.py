"""
/utils/context.py

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

__version_info__ = (1, 0, 0, "alpha", 0)
__version__      = "{0}.{1}.{2}{3}{4}".format(*[str(n)[0] if (i == 3) else str(n) for (i, n) in enumerate(__version_info__)])

__all__ = {
    "Stream",
    "Suppress",
    "Timer",
}


import sys
import time


class Stream():
    """
    with context.Stream(target):
        ...
        # redirects stdout to target


    with context.Stream(target, stream="stderr"):
        ...
        # redirects stderr to target
    """

    def __init__(self, target, *, stream: str = "stdout"):
        self._target = target
        self._stream = stream

        self._old_targets = list()

    def __enter__(self):
        self._old_targets.append(getattr(sys, self._stream))
        setattr(sys, self._stream, self._target)
    
    def __exit__(self, *args):
        setattr(sys, self._stream, self._old_targets.pop())

    async def __aenter__(self):
        return self.__enter__()

    async def __aexit__(self, *args):
        return self.__exit__(*args)

class Suppress():
    """
    with context.Suppress(discord.errors.HTTPException):
	    await ctx.send(message)

    # execution resumes here even if discord throws a HTTPException
    """

    def __init__(self, *exceptions: Exception):
        self._exceptions = exceptions

    def __enter__(self):
        pass

    def __exit__(self, exception_type, exception_class, traceback):
        if (not exception_type):
            return True
        elif (issubclass(exception_type, self._exceptions)):
            return True
        return False

    async def __aenter__(self):
        return self.__enter__()

    async def __aexit__(self, *args):
        return self.__exit__(*args)

class Timer():
    """
    with context.Timer() as t:
        ...

    time = t.time


    with context.Timer(timer=time.perf_counter) as t:
        ...

    time = t.time
    """

    def __init__(self, *, timer = time.clock):
        self._timer = timer

    def __enter__(self):
        self._start = timer()
        return self

    def __exit__(self, *args):
        self.time = timer() - self._start

    async def __aenter__(self):
        return self.__enter__()

    async def __aexit__(self, *args):
        return self.__exit__(*args)