"""
/utils/regex.py

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
    "Regex",
}


import re


class Regex:
    __all__ = {
        "WORD",
        "WORDS",
        "DIGIT",
        "DIGITS",
        "VERSION",
        "ISSUE",
        "FLAG_TOKEN",
        "HEXADECIMAL",
        "RGB",
        "CMYK",
        "MONTH",
        "DAY",
        "YEAR",
        "US_DATE",
        "EU_DATE",
        "US_DATE_TIME",
        "EU_DATE_TIME",
        "HOUR",
        "TODAY_AT_HOUR",
        "TOMORROW_AT_HOUR",
        "TIME",
        "TODAY_AT_TIME",
        "TOMORROW_AT_TIME",
        "YEARS",
        "MONTHS",
        "WEEKS",
        "DAYS",
        "HOURS",
        "MINUTES",
        "SECONDS",
        "SHORT_HUMANIZED_TIME",
        "LONG_HUMANIZED_TIME",
        "ANY_HUMANIZED_TIME",
    }

    WORD = re.compile(r"""
                          (?P<word>\W)
                       """, re.IGNORECASE | re.VERBOSE)
    
    WORDS = re.compile(r"""
                           (?P<word>\W+)
                        """, re.IGNORECASE | re.VERBOSE)

    DIGIT = re.compile(r"""
                           (?P<digit>\d)
                        """, re.VERBOSE)
    
    DIGITS = re.compile(r"""
                            (?P<digits>\d+)
                         """, re.VERBOSE)

    # modified regex from PEP 440 (Version Identification and
    # Dependency Specification)
    # https://www.python.org/dev/peps/pep-0440/#public-version-identifiers
    VERSION = re.compile(r"""
                             (?:(?P<epoch>[0-9]+)!)?
                             (?P<major>[0-9]+)
                             (?:\.(?P<minor>[0-9]+))
                             (?:\.(?P<micro>[0-9]+))?
                             (?:(?P<release_id>a|b|rc|f)(?P<release_number>[0-9]+))?
                             (?:\.post(?P<post>[0-9]+)|\.dev(?P<dev>[0-9]+))?
                          """, re.VERBOSE)

    ISSUE = re.compile(r"""
                           (?:\#\#)
                           (?P<number>\d+)
                        """, re.VERBOSE)
    
    # --flag
    # --flag=value
    FLAG_TOKEN = re.compile(r"""
                                (?:--)
                                (?P<flag>[a-z]+)
                                (?:=(?P<value>.+))?
                             """, re.VERBOSE)
    
    # 000
    # #000
    # 0x000
    # 000000
    # #000000
    # 0x000000
    HEXADECIMAL = re.compile(r"""
                                 (?:0X|\#)?
                                 (?:[A-F0-9]{6}|[A-F0-9]{3})
                              """, re.VERBOSE)
    
    # 000,000,000
    # 000, 000, 000
    # (000,000,000)
    # (000, 000, 000)
    RGB = re.compile(r"""
                         (?:\(?)
                         (?P<r>[0-9]{1,3})
                         (?:,\ ?)
                         (?P<g>[0-9]{1,3})
                         (?:,\ ?)
                         (?P<b>[0-9]{1,3})
                         (?:\)?)
                      """, re.VERBOSE)
    
    # 000,000,000,000
    # 000, 000, 000, 000
    # (000,000,000,000)
    # (000, 000, 000, 000)
    CMYK = re.compile(r"""
                          (?:\(?)
                          (?P<c>[0-9]{1,3})
                          (?:,\ ?)
                          (?P<m>[0-9]{1,3})
                          (?:,\ ?)
                          (?P<y>[0-9]{1,3})
                          (?:,\ ?)
                          (?P<k>[0-9]{1,3})
                          (?:\)?)
                       """, re.VERBOSE)

    # 12
    # 11
    # 10
    # 9
    # 8
    # 7
    # 6
    # 5
    # 4
    # 3
    # 2
    # 1
    MONTH = re.compile(r"""
                           (?P<month>(?:12|11|10|0?9|0?8|0?7|0?6|0?5|0?4|0?3|0?2|0?1))
                        """, re.VERBOSE)
    
    # 0
    # 00
    DAY = re.compile(r"""
                         (?P<day>[0-9]{1,2})
                      """, re.VERBOSE)
    
    # 00
    # 0000
    YEAR = re.compile(r"""
                          (?P<year>(?:[0-9]{4}|[0-9]{2}))
                       """, re.VERBOSE)
    
    # 12/31/00
    # 12/31/0000
    # 12-31-00
    # 12-31-0000
    # on 12/31/00
    # on 12/31/0000
    # on 12-31-00
    # on 12-31-0000
    # until 12/31/00
    # until 12/31/0000
    # until 12-31-00
    # until 12-31-0000
    US_DATE = re.compile(r"""
                             (?:on\ |until\ )?
                             (?P<month>(?:12|11|10|0?9|0?8|0?7|0?6|0?5|0?4|0?3|0?2|0?1))
                             (?:/|-)
                             (?P<day>[0-9]{1,2})
                             (?:/|-)
                             (?P<year>(?:[0-9]{4}|[0-9]{2}))
                          """, re.VERBOSE)
    
    # 31/12/00
    # 31/12/0000
    # 31-12-00
    # 31-12-0000
    # on 31/12/00
    # on 31/12/0000
    # on 31-12-00
    # on 31-12-0000
    # until 31/12/00
    # until 31/12/0000
    # until 31-12-00
    # until 31-12-0000
    EU_DATE = re.compile(r"""
                             (?:on\ |until\ )?
                             (?P<day>[0-9]{1,2})
                             (?:/|-)
                             (?P<month>(?:12|11|10|0?9|0?8|0?7|0?6|0?5|0?4|0?3|0?2|0?1))
                             (?:/|-)
                             (?P<year>(?:[0-9]{4}|[0-9]{2}))
                          """, re.VERBOSE)
    
    # 12/31/00 00:00
    # 12/31/00 at 00:00
    # 12/31/00 00:00:00
    # 12/31/00 at 00:00:00
    # 12/31/0000 00:00
    # 12/31/0000 at 00:00
    # 12/31/0000 00:00:00
    # 12/31/0000 at 00:00:00
    # 12-31-00 00:00
    # 12-31-00 at 00:00
    # 12-31-00 00:00:00
    # 12-31-00 at 00:00:00
    # 12-31-0000 00:00
    # 12-31-0000 at 00:00
    # 12-31-0000 00:00:00
    # 12-31-0000 at 00:00:00
    # on 12/31/00 00:00
    # on 12/31/00 at 00:00
    # on 12/31/00 00:00:00
    # on 12/31/00 at 00:00:00
    # on 12/31/0000 00:00
    # on 12/31/0000 at 00:00
    # on 12/31/0000 00:00:00
    # on 12/31/0000 at 00:00:00
    # on 12-31-00 00:00
    # on 12-31-00 at 00:00
    # on 12-31-00 00:00:00
    # on 12-31-00 at 00:00:00
    # on 12-31-0000 00:00
    # on 12-31-0000 at 00:00
    # on 12-31-0000 00:00:00
    # on 12-31-0000 at 00:00:00
    # until 12/31/00 00:00
    # until 12/31/00 at 00:00
    # until 12/31/00 00:00:00
    # until 12/31/00 at 00:00:00
    # until 12/31/0000 00:00
    # until 12/31/0000 at 00:00
    # until 12/31/0000 00:00:00
    # until 12/31/0000 at 00:00:00
    # until 12-31-00 00:00
    # until 12-31-00 at 00:00
    # until 12-31-00 00:00:00
    # until 12-31-00 at 00:00:00
    # until 12-31-0000 00:00
    # until 12-31-0000 at 00:00
    # until 12-31-0000 00:00:00
    # until 12-31-0000 at 00:00:00
    US_DATE_TIME = re.compile(r"""
                                  (?:on\ |until\ )?
                                  (?P<month>(?:12|11|10|0?9|0?8|0?7|0?6|0?5|0?4|0?3|0?2|0?1))
                                  (?:/|-)
                                  (?P<day>[0-9]{1,2})
                                  (?:/|-)
                                  (?P<year>(?:[0-9]{4}|[0-9]{2}))
                                  (?:\ )
                                  (?:at\ )?
                                  (?P<hour>[0-9]{2}|[0-9])
                                  (?::)
                                  (?P<minute>[0-9]{2})
                                  (?::)?
                                  (?P<second>[0-9]{2})?
                               """, re.VERBOSE)
    
    # 31/12/00 00:00
    # 31/12/00 at 00:00
    # 31/12/00 00:00:00
    # 31/12/00 at 00:00:00
    # 31/12/0000 00:00
    # 31/12/0000 at 00:00
    # 31/12/0000 00:00:00
    # 31/12/0000 at 00:00:00
    # 31-12-00 00:00
    # 31-12-00 at 00:00
    # 31-12-00 00:00:00
    # 31-12-00 at 00:00:00
    # 31-12-0000 00:00
    # 31-12-0000 at 00:00
    # 31-12-0000 00:00:00
    # 31-12-0000 at 00:00:00
    # on 31/12/00 00:00
    # on 31/12/00 at 00:00
    # on 31/12/00 00:00:00
    # on 31/12/00 at 00:00:00
    # on 31/12/0000 00:00
    # on 31/12/0000 at 00:00
    # on 31/12/0000 00:00:00
    # on 31/12/0000 at 00:00:00
    # on 31-12-00 00:00
    # on 31-12-00 at 00:00
    # on 31-12-00 00:00:00
    # on 31-12-00 at 00:00:00
    # on 31-12-0000 00:00
    # on 31-12-0000 at 00:00
    # on 31-12-0000 00:00:00
    # on 31-12-0000 at 00:00:00
    # until 31/12/00 00:00
    # until 31/12/00 at 00:00
    # until 31/12/00 00:00:00
    # until 31/12/00 at 00:00:00
    # until 31/12/0000 00:00
    # until 31/12/0000 at 00:00
    # until 31/12/0000 00:00:00
    # until 31/12/0000 at 00:00:00
    # until 31-12-00 00:00
    # until 31-12-00 at 00:00
    # until 31-12-00 00:00:00
    # until 31-12-00 at 00:00:00
    # until 31-12-0000 00:00
    # until 31-12-0000 at 00:00
    # until 31-12-0000 00:00:00
    # until 31-12-0000 at 00:00:00
    EU_DATE_TIME = re.compile(r"""
                                  (?:on\ |until\ )?
                                  (?P<day>[0-9]{1,2})
                                  (?:/|-)
                                  (?P<month>(?:12|11|10|0?9|0?8|0?7|0?6|0?5|0?4|0?3|0?2|0?1))
                                  (?:/|-)
                                  (?P<year>(?:[0-9]{4}|[0-9]{2}))
                                  (?:\ )
                                  (?:at\ )?
                                  (?P<hour>[0-9]{2}|[0-9])
                                  (?::)
                                  (?P<minute>[0-9]{2})
                                  (?::)?
                                  (?P<second>[0-9]{2})?
                               """, re.VERBOSE)
    
    # 0
    # 0am
    # 0 am
    # 0pm
    # 0 pm
    # 00
    # 00am
    # 00 am
    # 00pm
    # 00 pm
    # at 0
    # at 0am
    # at 0 am
    # at 0pm
    # at 0 pm
    # at 00
    # at 00am
    # at 00 am
    # at 00pm
    # at 00 pm
    # until 0
    # until 0am
    # until 0 am
    # until 0pm
    # until 0 pm
    # until 00
    # until 00am
    # until 00 am
    # until 00pm
    # until 00 pm
    HOUR = re.compile(r"""
                          (?:at\ |until\ )?
                          (?P<hour>[0-9]{1,2})
                          (?:\ ?)
                          (?P<meridies>am|pm)?
                       """, re.VERBOSE)
    
    # today at 0
    # today at 0am
    # today at 0 am
    # today at 0pm
    # today at 0 pm
    # today at 00
    # today at 00am
    # today at 00 am
    # today at 00pm
    # today at 00 pm
    # until today at 0
    # until today at 0am
    # until today at 0 am
    # until today at 0pm
    # until today at 0 pm
    # until today at 00
    # until today at 00am
    # until today at 00 am
    # until today at 00pm
    # until today at 00 pm
    TODAY_AT_HOUR = re.compile(r"""
                                   (?:until\ )?
                                   (?:today\ at\ )
                                   (?P<hour>[0-9]{1,2})\ ?
                                   (?P<meridies>am|pm)?
                                """, re.VERBOSE)
    
    # tomorrow at 0
    # tomorrow at 0am
    # tomorrow at 0 am
    # tomorrow at 0pm
    # tomorrow at 0 pm
    # tomorrow at 00
    # tomorrow at 00am
    # tomorrow at 00 am
    # tomorrow at 00pm
    # tomorrow at 00 pm
    # until tomorrow at 0
    # until tomorrow at 0am
    # until tomorrow at 0 am
    # until tomorrow at 0pm
    # until tomorrow at 0 pm
    # until tomorrow at 00
    # until tomorrow at 00am
    # until tomorrow at 00 am
    # until tomorrow at 00pm
    # until tomorrow at 00 pm
    TOMORROW_AT_HOUR = re.compile(r"""
                                      (?:until\ )?
                                      (?:tomorrow\ at\ )
                                      (?P<hour>[0-9]{1,2})\ ?
                                      (?P<meridies>am|pm)?
                                   """, re.VERBOSE)
    
    # 00:00
    # 00:00:00
    # at 00:00
    # at 00:00:00
    # until 00:00
    # until 00:00:00
    TIME = re.compile(r"""
                          (?:at\ |until\ )?
                          (?P<hour>[0-9]{2}|[0-9])
                          (?::)
                          (?P<minute>[0-9]{2})
                          (?::)?
                          (?P<second>[0-9]{2})?
                       """, re.VERBOSE)
    
    # today at 00:00
    # today at 00:00:00
    # until today at 00:00
    # until today at 00:00:00
    TODAY_AT_TIME = re.compile(r"""
                                   (?:until\ )?
                                   (?:today\ at\ )
                                   (?P<hour>[0-9]{2}|[0-9])
                                   (?::)
                                   (?P<minute>[0-9]{2})
                                   (?::)?
                                   (?P<second>[0-9]{2})?
                                """, re.VERBOSE)

    # tomorrow at 00:00
    # tomorrow at 00:00:00
    # until tomorrow at 00:00
    # until tomorrow at 00:00:00
    TOMORROW_AT_TIME = re.compile(r"""
                                      (?:until\ )?
                                      (?:tomorrow\ at\ )
                                      (?P<hour>[0-9]{2}|[0-9])
                                      (?::)
                                      (?P<minute>[0-9]{2})
                                      (?::)?
                                      (?P<second>[0-9]{2})?
                                   """, re.VERBOSE)
    
    # 1y
    # in 1y
    # for 1y
    # 1 year
    # in 1 year
    # for 1 year
    # 2 years
    # in 2 years
    # for 2 years
    YEARS = re.compile(r"""
                           (?:in\ |for\ )?
                           (?P<years>[0-9]+)
                           (?:y|\ years?)
                        """, re.VERBOSE)
    
    # 1mo
    # in 1mo
    # for 1mo
    # 1 month
    # in 1 month
    # for 1 month
    # 2 months
    # in 2 months
    # for 2 months
    MONTHS = re.compile(r"""
                            (?:in\ |for\ )?
                            (?P<months>[0-9]+)
                            (?:mo|\ months?)
                         """, re.VERBOSE)
    
    # 1w
    # in 1w
    # for 1w
    # 1 week
    # in 1 week
    # for 1 week
    # 2 weeks
    # in 2 weeks
    # for 2 weeks
    WEEKS = re.compile(r"""
                           (?:in\ |for\ )?
                           (?P<weeks>[0-9]+)
                           (?:w|\ weeks?)
                        """, re.VERBOSE)
    
    # 1d
    # in 1d
    # for 1d
    # 1 day
    # in 1 day
    # for 1 day
    # 2 days
    # in 2 days
    # for 2 days
    DAYS = re.compile(r"""
                          (?:in\ |for\ )?
                          (?P<days>[0-9]+)
                          (?:d|\ days?)
                       """, re.VERBOSE)
    
    # 1h
    # in 1h
    # for 1h
    # 1 hour
    # in 1 hour
    # for 1 hour
    # 2 hours
    # in 2 hours
    # for 2 hours
    HOURS = re.compile(r"""
                           (?:in\ |for\ )?
                           (?P<hours>[0-9]+)
                           (?:h|\ hours?)
                        """, re.VERBOSE)
    
    # 1m
    # in 1m
    # for 1m
    # 1 minute
    # in 1 minute
    # for 1 minute
    # 2 minutes
    # in 2 minutes
    # for 2 minutes
    MINUTES = re.compile(r"""
                             (?:in\ |for\ )?
                             (?P<minutes>[0-9]+)
                             (?:m|\ minutes?)
                          """, re.VERBOSE)
    
    # 1s
    # in 1s
    # for 1s
    # 1 second
    # in 1 second
    # for 1 second
    # 2 seconds
    # in 2 seconds
    # for 2 seconds
    SECONDS = re.compile(r"""
                             (?:in\ |for\ )?
                             (?P<seconds>[0-9]+)
                             (?:s|\ seconds?)
                          """, re.VERBOSE)

    LONG_HUMANIZED_TIME = re.compile(r"""
                                         (?:in\ |for\ )?
                                         (?:(?P<years>[0-9]+)(?:\ years?))?\ ?
                                         (?:\ ?and\ )?
                                         (?:(?P<months>[0-9]+)(?:\ months?))?\ ?
                                         (?:\ ?and\ )?
                                         (?:(?P<weeks>[0-9]+)(?:\ weeks?))?\ ?
                                         (?:\ ?and\ )?
                                         (?:(?P<days>[0-9]+)(?:\ days?))?\ ?
                                         (?:\ ?and\ )?
                                         (?:(?P<hours>[0-9]+)(?:\ hours?))?\ ?
                                         (?:\ ?and\ )?
                                         (?:(?P<minutes>[0-9]+)(?:\ minutes?))?\ ?
                                         (?:\ ?and\ )?
                                         (?:(?P<seconds>[0-9]+)(?:\ seconds?))?\ ?
                                         (?:\ ?and\ )?
                                         (?:(?P<milliseconds>[0-9]+)(?:\ milliseconds?))?\ ?
                                         (?:\ ?and\ )?
                                         (?:(?P<microseconds>[0-9]+)(?:\ microseconds?))?
                                      """, re.VERBOSE)
    
    SHORT_HUMANIZED_TIME = re.compile(r"""
                                          (?:in\ |for\ )?
                                          (?:(?P<years>[0-9]+)(?:y))?\ ?
                                          (?:\ ?&\ )?
                                          (?:(?P<months>[0-9]+)(?:mo))?\ ?
                                          (?:\ ?&\ )?
                                          (?:(?P<weeks>[0-9]+)(?:w))?\ ?
                                          (?:\ ?&\ )?
                                          (?:(?P<days>[0-9]+)(?:d))?\ ?
                                          (?:\ ?&\ )?
                                          (?:(?P<hours>[0-9]+)(?:h))?\ ?
                                          (?:\ ?&\ )?
                                          (?:(?P<minutes>[0-9]+)(?:m))?\ ?
                                          (?:\ ?&\ )?
                                          (?:(?P<seconds>[0-9]+)(?:s))?\ ?
                                          (?:\ ?&\ )?
                                          (?:(?P<milliseconds>[0-9]+)(?:ms))?\ ?
                                          (?:\ ?&\ )?
                                          (?:(?P<microseconds>[0-9]+)(?:μs))?
                                       """, re.VERBOSE)

    ANY_HUMANIZED_TIME = re.compile(r"""
                                        (?:in\ |for\ )?
                                        (?:(?P<years>[0-9]+)(?:y|\ years?))?\ ?
                                        (?:\ ?and |\ ?&\ )?
                                        (?:(?P<months>[0-9]+)(?:mo|\ months?))?\ ?
                                        (?:\ ?and |\ ?&\ )?
                                        (?:(?P<weeks>[0-9]+)(?:w|\ weeks?))?\ ?
                                        (?:\ ?and |\ ?&\ )?
                                        (?:(?P<days>[0-9]+)(?:d|\ days?))?\ ?
                                        (?:\ ?and |\ ?&\ )?
                                        (?:(?P<hours>[0-9]+)(?:h|\ hours?))?\ ?
                                        (?:\ ?and |\ ?&\ )?
                                        (?:(?P<minutes>[0-9]+)(?:m|\ minutes?))?\ ?
                                        (?:\ ?and |\ ?&\ )?
                                        (?:(?P<seconds>[0-9]+)(?:s|\ seconds?))?\ ?
                                        (?:\ ?and |\ ?&\ )?
                                        (?:(?P<milliseconds>[0-9]+)(?:ms|\ milliseconds?))?\ ?
                                        (?:\ ?and |\ ?&\ )?
                                        (?:(?P<microseconds>[0-9]+)(?:μs|\ microseconds?))?
                                     """, re.VERBOSE)