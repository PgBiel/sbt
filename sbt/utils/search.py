"""
/utils/search.py

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

__version_info__      = (1, 0, 0, "alpha", 0)
__version__           = "{0}.{1}.{2}{3}{4}".format(*[str(n)[0] if (i == 3) else str(n) for (i, n) in enumerate(__version_info__)])


import aiohttp
import urllib


class SearchBaseException(Exception):
    pass

class APIError(SearchBaseException):
    pass

class NoResults(SearchBaseException):
    pass

class NoMoreRequests(SearchBaseException):
    pass

class Result():
    def __init__(self, url: str, title: str, description: str, time: float, results: int):
        self.url = url
        self.title = title
        self.description = description
        self.time = time
        self.results = results

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "<Result url='{0}'>".format(self.url, self.time)

    @classmethod
    def from_raw(self, data: dict) -> list:
        results = list()

        for (result) in data["items"]:
            url = result["link"]
            title = result["title"]
            description = result["snippet"]
            time = data["searchInformation"]["searchTime"]
            results_ = int(data["searchInformation"]["totalResults"])

            results.append(self(url, title, description, time, results_))

        return results

class Search():
    def __init__(self, key: str, engine: str, *, session: aiohttp.ClientSession = None):
        self._key = key
        self._engine = engine
        self._session = session

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "<Search engine='{0}'>".format(self.engine)

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, key: str):
        self._key = key

    @property
    def engine(self) -> str:
        return self._engine

    @engine.setter
    def engine(self, engine: str):
        self._engine = engine

    @property
    def session(self) -> aiohttp.ClientSession:
        return self._session

    @session.setter
    def key(self, session: aiohttp.ClientSession):
        self._session = session

    async def search(self, query: str, *, safe: bool = True) -> list:
        if (not self._session):
            session = aiohttp.ClientSession()
        else:
            session = self._session

        safe = "active" if safe else "off"

        url = "https://www.googleapis.com/customsearch/v1?key={0}&cx={1}&q={2}&safe={3}".format(
            self._key, self._engine, urllib.parse.quote_plus(query), safe
        )

        async with session.get(url) as response:
            json_ = await response.json()

            if (error := json_.get("error")):
                if error["errors"][0]["domain"] == "usageLimits":
                    raise NoMoreRequests()
                raise APIError(error["code"])

            if (not json_.get("items")):
                raise NoResults()

        if (not self._session):
            await session.close()

        return Result.from_raw(json_)