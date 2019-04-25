"""
/utils/fuzzywuzzy.py

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


import difflib
import heapq
import re
import typing

from utils import (
    regex,
)


def ratio(a: str, b: str):
    matcher = difflib.SequenceMatcher(None, a, b)
    return int(round(matcher.ratio() * 100))

def quick_ratio(a: str, b: str):
    matcher = difflib.SequenceMatcher(None, a, b)
    return int(round(matcher.quick_ratio() * 100))

def real_quick_ratio(a: str, b: str):
    matcher = difflib.SequenceMatcher(None, a, b)
    return int(round(matcher.real_quick_ratio() * 100))

def partial_ratio(a: str, b: str):
    short, long_ = (a, b) if len(a) <= len(b) else (b, a)
    matcher = difflib.SequenceMatcher(None, short, long_)

    blocks = matcher.get_matching_blocks()

    scores = list()
    for (i, j, n) in blocks:
        start = max(j - i, 0)
        end = start + len(short)

        score = ratio(short, long_[start:end])
        scores.append(score)

    return max(scores)

def quick_partial_ratio(a: str, b: str):
    short, long_ = (a, b) if len(a) <= len(b) else (b, a)
    matcher = difflib.SequenceMatcher(None, short, long_)

    blocks = matcher.get_matching_blocks()

    scores = list()
    for (i, j, n) in blocks:
        start = max(j - i, 0)
        end = start + len(short)

        score = quick_ratio(short, long_[start:end])
        scores.append(score)

    return max(scores)

def real_quick_partial_ratio(a: str, b: str):
    short, long_ = (a, b) if len(a) <= len(b) else (b, a)
    matcher = difflib.SequenceMatcher(None, short, long_)

    blocks = matcher.get_matching_blocks()

    scores = list()
    for (i, j, n) in blocks:
        start = max(j - i, 0)
        end = start + len(short)

        score = real_quick_ratio(short, long_[start:end])
        scores.append(score)

    return max(scores)

def _sort_tokens(a: str):
    a = regex.Regex.WORD.sub(" ", a).lower().strip()
    return " ".join(sorted(a.split()))

def token_sort_ratio(a: str, b: str):
    a = _sort_tokens(a)
    b = _sort_tokens(b)
    return ratio(a, b)

def quick_token_sort_ratio(a: str, b: str):
    a = _sort_tokens(a)
    b = _sort_tokens(b)
    return quick_ratio(a, b)

def real_quick_token_sort_ratio(a: str, b: str):
    a = _sort_tokens(a)
    b = _sort_tokens(b)
    return real_quick_ratio(a, b)

def partial_token_sort_ratio(a: str, b: str):
    a = _sort_tokens(a)
    b = _sort_tokens(b)
    return partial_ratio(a, b)

def quick_partial_token_sort_ratio(a: str, b: str):
    a = _sort_tokens(a)
    b = _sort_tokens(b)
    return quick_partial_ratio(a, b)

def real_quick_partial_token_sort_ratio(a: str, b: str):
    a = _sort_tokens(a)
    b = _sort_tokens(b)
    return real_quick_partial_ratio(a, b)

def _extractor(query: str, choices: typing.Union[dict, list], *, scorer: typing.Callable, score_cutoff: int):
    if (isinstance(choices, dict)):
        for (key, value) in choices.items():
            score = scorer(query, key)
            if (score >= score_cutoff):
                yield (score, key, value)
    else:
        for (key) in choices:
            score = scorer(query, key)
            if (score >= score_cutoff):
                yield (score, key)

def extract(query: str, choices: typing.Union[dict, list], *, scorer: typing.Callable = ratio, score_cutoff: int = 0, limit: int = None):
    iterable = _extractor(query, choices, scorer=scorer, score_cutoff=score_cutoff)
    key = lambda t: t[0]

    if (limit):
        return heapq.nlargest(limit, iterable, key=key)
    return sorted(iterable, key=key, reverse=True)