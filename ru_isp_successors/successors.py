"""Find successors of Russian service providers and print a transition history.

Usage:
    python successors.py "Интел-Тел" --period 2010-2015
    python successors.py "Gorcom" --period 2012 --min-confidence low
"""
import argparse
import json
import re
import sys
from pathlib import Path

DATA = Path(__file__).with_name("data.json")
RANK = {"unverified": 0, "low": 1, "medium": 2, "high": 3}

_TRANSLIT = str.maketrans({
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "zh",
    "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o",
    "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h", "ц": "c",
    "ч": "ch", "ш": "sh", "щ": "sh", "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu",
    "я": "ya",
})
_LEGAL = re.compile(r"\b(ооо|зао|ао|оао|пао|llc|ltd|jsc)\b")


def norm(name):
    """Lowercase, drop legal-form words/punctuation, transliterate, merge k/c and i/y spellings."""
    s = _LEGAL.sub(" ", name.lower().replace("ё", "е"))
    s = re.sub(r"[^\w]+", "", s).translate(_TRANSLIT)
    return s.replace("c", "k").replace("y", "i").replace("intel", "int")


def parse_date(s, end=False):
    """'2013' / '2013-12' / '2013-12-05' -> comparable (y, m, d); None stays None."""
    if not s:
        return None
    p = [int(x) for x in s.split("-")]
    y = p[0]
    m = p[1] if len(p) > 1 else (12 if end else 1)
    d = p[2] if len(p) > 2 else (31 if end else 1)
    return (y, m, d)


def parse_period(s):
    if not s:
        return None, None
    a, _, b = s.partition("-") if re.fullmatch(r"\d{4}-\d{4}", s) else (s, "", s)
    return parse_date(a), parse_date(b, end=True)


def overlaps(edge, lo, hi):
    """Edge with unknown dates is treated as always overlapping."""
    es, ee = parse_date(edge["start"]), parse_date(edge["end"], end=True)
    if lo and ee and ee < lo:
        return False
    if hi and es and es > hi:
        return False
    return True


def load():
    return json.loads(DATA.read_text(encoding="utf-8"))


def find_entities(db, name):
    q = norm(name)
    exact = [k for k, e in db["entities"].items() if any(norm(n) == q for n in e["names"])]
    if exact:
        return exact
    return [k for k, e in db["entities"].items()
            if any(q and (q in norm(n) or norm(n) in q) for n in e["names"])]


def successors(db, start_ids, lo=None, hi=None, min_conf="unverified"):
    """BFS over edges; returns list of (edge, depth) in discovery order."""
    seen, out = set(start_ids), []
    frontier, depth = list(start_ids), 0
    while frontier:
        depth += 1
        nxt = []
        for node in frontier:
            for e in db["edges"]:
                if e["from"] != node or not overlaps(e, lo, hi):
                    continue
                if RANK[e["confidence"]] < RANK[min_conf]:
                    continue
                out.append((e, depth))
                if e["to"] not in seen:
                    seen.add(e["to"])
                    nxt.append(e["to"])
        frontier = nxt
    return out


def label(db, k):
    e = db["entities"][k]
    extra = f" (ИНН {e['inn']})" if e.get("inn") else ""
    return e["names"][0] + extra


def report(db, name, period=None, min_conf="unverified"):
    lo, hi = parse_period(period)
    ids = find_entities(db, name)
    lines = [f"Query: {name!r}  period: {period or 'any'}"]
    if not ids:
        lines.append("No match in the knowledge base. Add the entity to data.json "
                     "(look up the INN/OGRN in egrul.nalog.ru).")
        return "\n".join(lines), 1
    for k in ids:
        ent = db["entities"][k]
        lines += ["", f"Matched: {label(db, k)} [{ent.get('kind', '')}]"]
        if ent.get("notes"):
            lines.append(f"  Note: {ent['notes']}")
        chain = successors(db, [k], lo, hi, min_conf)
        if not chain:
            lines.append("  No successors recorded for this period/confidence.")
            continue
        lines.append("  Transition history:")
        for e, d in chain:
            when = f"{e['start'] or '?'} -> {e['end'] or 'present/unknown'}"
            lines.append(f"  {'  ' * (d - 1)}{label(db, e['from'])} => {label(db, e['to'])}")
            lines.append(f"  {'  ' * (d - 1)}  {e['type']}; {when}; confidence: {e['confidence']}")
            lines.append(f"  {'  ' * (d - 1)}  source: {e['source']}")
            if e["note"]:
                lines.append(f"  {'  ' * (d - 1)}  note: {e['note']}")
        finals = {e["to"] for e, _ in chain} - {e["from"] for e, _ in chain}
        if finals:
            lines.append("  Current service point(s) for existing clients: "
                         + "; ".join(label(db, f) for f in sorted(finals)))
    return "\n".join(lines), 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name")
    ap.add_argument("--period", help="year 'YYYY' or range 'YYYY-YYYY' when the provider was active")
    ap.add_argument("--min-confidence", choices=list(RANK), default="unverified")
    a = ap.parse_args(argv)
    text, code = report(load(), a.name, a.period, a.min_confidence)
    print(text)
    return code


if __name__ == "__main__":
    sys.exit(main())
