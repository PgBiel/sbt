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

__version_info__ = (2, 0, 0, "alpha", 0)
__version__      = "{0}.{1}.{2}{3}{4}".format(*[str(n)[0] if (i == 3) else str(n) for (i, n) in enumerate(__version_info__)])

__all__ = {

}


import time


class Timer():
    """
    with context.Timer() as t:
        ...

    time = t.time
    """

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.time = time.perf_counter() - self._start

    async def __aenter__(self):
        return self.__enter__()

    async def __aexit__(self, *args):
        return self.__exit__(*args)

class Catch():
    """
    with context.Catch(OSError, ValueError):
        raise ValueError
        # exception is not raised
    """

    def __init__(self, *exceptions):
        self._exceptions = exceptions

    def __enter__(self):
        pass

    def __exit__(self, exception_type, exception_class, traceback):
        if (not exception_type):
            # no exception
            return True
        elif (issubclass(exception_type, self._exceptions)):
            # caught exception
            return True

        # uncaught exception
        return False

    async def __aenter__(self):
        pass

    async def __aexit__(self, *args):
        return self.__exit__(*args)