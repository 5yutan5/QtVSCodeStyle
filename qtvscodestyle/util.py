from __future__ import annotations

import re


# https://gist.github.com/bgusach/a967e0587d6e01e889fd1d776c5f3729
def multireplace(target: str, replacements: dict[str, str]) -> str:
    replacements_sorted = sorted(replacements, key=len, reverse=True)
    replacements_escaped = [re.escape(i) for i in replacements_sorted]
    pattern = re.compile("|".join(replacements_escaped))
    return pattern.sub(lambda match: replacements[match.group()], target)
