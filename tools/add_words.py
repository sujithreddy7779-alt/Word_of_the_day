#!/usr/bin/env python3
"""Add new entries to words.js, or check the ones already there.

New words go in a plain text file, one entry per line, fields separated by |

    group|word|pronunciation|type|meaning|example|present|past|future|present continuous|present perfect

  group          h = interesting word, e = everyday word, t = phrase or slang
  pronunciation  simple respelling with the stressed part in capitals, like ser-un-DIP-uh-tee
                 (leave it empty for phrases and slang)
  type           noun, verb, adjective, adverb, phrase or slang
  sentences      five sentences in the tense order above, with *stars* around the word

Lines that are blank or start with # are skipped.

Usage:
    python3 tools/add_words.py new_words.txt [more.txt ...]   add the entries to words.js
    python3 tools/add_words.py --check                        check every entry in words.js
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORDS = ROOT / "words.js"
HEADER = (
    "// Word list for Word of the Day, one entry per line:\n"
    "// [group, word, pronunciation, type, meaning, example, [present, past, future, present continuous, present perfect]]\n"
    "// group: \"h\" interesting word, \"e\" everyday word, \"t\" phrase or slang. *Stars* mark the word in each sentence.\n"
    "// To add words, see tools/add_words.py.\n"
    "window.WOTD_WORDS = [\n"
)
FOOTER = "\n];\n"
TYPES = {"noun", "verb", "adjective", "adverb", "phrase", "slang"}
MARK = re.compile(r"\*[^*]+\*")


def load():
    if not WORDS.exists():
        return []
    text = WORDS.read_text(encoding="utf-8")
    start = text.index("[", text.index("window.WOTD_WORDS"))
    end = text.rindex("]")
    return json.loads(text[start:end + 1])


def save(rows):
    body = ",\n".join(json.dumps(r, ensure_ascii=False) for r in rows)
    WORDS.write_text(HEADER + body + FOOTER, encoding="utf-8")


def problems(row):
    out = []
    group, word, say, kind, meaning, example, sents = row
    if group not in ("h", "e", "t"):
        out.append("group must be h, e or t")
    if not word or len(word) > 28:
        out.append("word is empty or longer than 28 characters")
    if kind not in TYPES:
        out.append("type must be one of " + ", ".join(sorted(TYPES)))
    if group == "t" and say:
        out.append("phrases and slang have no pronunciation")
    if not meaning or len(meaning) > 170:
        out.append("meaning is empty or too long")
    if not example or len(example) > 150:
        out.append("example is empty or too long")
    if not isinstance(sents, list) or len(sents) != 5:
        out.append("needs exactly 5 sentences")
    else:
        for i, s in enumerate(sents, 1):
            if not MARK.search(s):
                out.append("sentence %d has no *marked* word" % i)
            if len(s) > 170:
                out.append("sentence %d is too long" % i)
    for field in (word, say, meaning, example) + tuple(sents or ()):
        if "|" in field:
            out.append("contains |")
    return out


def parse(line):
    parts = [p.strip() for p in line.split("|")]
    if len(parts) != 11:
        return None, "expected 11 fields, found %d" % len(parts)
    return parts[:6] + [parts[6:]], None


def main(args):
    rows = load()
    if args == ["--check"]:
        bad = 0
        seen = set()
        for r in rows:
            issues = problems(r)
            if r[1].lower() in seen:
                issues.append("duplicate")
            seen.add(r[1].lower())
            if issues:
                bad += 1
                print("%s: %s" % (r[1], "; ".join(issues)))
        counts = {g: sum(1 for r in rows if r[0] == g) for g in "het"}
        print("%d entries (%d interesting, %d everyday, %d phrases/slang), %d with problems"
              % (len(rows), counts["h"], counts["e"], counts["t"], bad))
        return 1 if bad else 0

    if not args:
        print(__doc__)
        return 2

    seen = {r[1].lower() for r in rows}
    added, skipped, failed = 0, [], []
    for name in args:
        for n, line in enumerate(pathlib.Path(name).read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            row, err = parse(line)
            if err:
                failed.append("%s:%d %s" % (name, n, err))
                continue
            issues = problems(row)
            if issues:
                failed.append("%s:%d %s: %s" % (name, n, row[1], "; ".join(issues)))
                continue
            if row[1].lower() in seen:
                skipped.append(row[1])
                continue
            seen.add(row[1].lower())
            rows.append(row)
            added += 1
    save(rows)
    print("Added %d. Total now %d." % (added, len(rows)))
    if skipped:
        print("Already in the list, skipped: " + ", ".join(skipped))
    for f in failed:
        print("Not added, " + f)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
