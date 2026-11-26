"""Company name normalizing, shared by sponsor matching and slug guessing."""
import re

SUFFIXES = {
    "inc", "incorporated", "llc", "l l c", "ltd", "limited", "corp", "corporation", "co", "company",
    "pbc", "plc", "lp", "llp", "pllc", "pc", "gmbh", "sa", "ag", "bv", "holdings", "holding", "group",
    "usa", "us", "america", "the",
}


def norm(name: str) -> str:
    s = (name or "").lower().replace("&", " and ")
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    words = [w for w in s.split() if w]
    while words and words[-1] in SUFFIXES:
        words.pop()
    while words and words[0] == "the":
        words.pop(0)
    return " ".join(words)


def slug_guesses(name: str, first_word: bool = True) -> list[str]:
    n = norm(name)
    if not n:
        return []
    words = n.split()
    out = ["".join(words), "-".join(words)]
    trimmed = [w for w in words if w not in {"technologies", "technology", "labs", "lab", "ai", "software",
                                              "systems", "solutions", "health", "analytics", "data", "io", "hq"}]
    if trimmed and trimmed != words:
        out += ["".join(trimmed), "-".join(trimmed)]
    if first_word and len(words) > 1 and len(words[0]) >= 5:
        out.append(words[0])
    seen, uniq = set(), []
    for o in out:
        if o and o not in seen and len(o) >= 3:
            seen.add(o)
            uniq.append(o)
    return uniq
