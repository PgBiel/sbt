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
    "Null",
    "Stream",
    "Suppress",
    "Timer",
}


import sys
import time


class Null():
    """
    context_ = context.Stream if (condition) else context.Null
    with context_(target):
        ...
        # redirects stdout to target if condition

        
    context_ = context.Stream if (condition) else context.Null
    with context_(target, stream="stderr"):
        ...
        # redirects stderr to target if condition
    """

    __all__ = {
        "__init__",
        "__enter__",
        "__exit__",
        "__aenter__",
        "__aexit__",
    }

    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass

    async def __aenter__(self):
        pass

    async def __aexit__(self, *args):
        pass

class Stream():
    """
    with context.Stream(target):
        ...
        # redirects stdout to target


    with context.Stream(target, stream="stderr"):
        ...
        # redirects stderr to target
    """

    __all__ = {
        "__init__",
        "__enter__",
        "__exit__",
        "__aenter__",
        "__aexit__",
    }

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

    __all__ = {
        "__init__",
        "__enter__",
        "__exit__",
        "__aenter__",
        "__aexit__",
    }

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


    with context.Timer(timer=time.perf_counter_ns) as t:
        ...

    time = t.time
    """

    __all__ = {
        "__init__",
        "__enter__",
        "__exit__",
        "__aenter__",
        "__aexit__",
    }

    def __init__(self, *, timer = time.perf_counter):
        self._timer = timer

    def __enter__(self):
        self._start = self._timer()
        return self

    def __exit__(self, *args):
        self.time = self._timer() - self._start

    async def __aenter__(self):
        return self.__enter__()

    async def __aexit__(self, *args):
        return self.__exit__(*args)