#!/usr/bin/env python3
"""Check that every card image follows the naming schema in README.md.

    <season>_<Set_Name>_<number>_<Player_Name>_<Front|Back>.jpg

Run from the repository root:

    python3 scripts/check_names.py            # report problems, exit 1 if any
    python3 scripts/check_names.py --quiet    # only the summary line

Only folders whose names start with a season (e.g. 2022-23_MVP/) are checked;
_review/, test-scans/ and reference-data/ are skipped.
"""
import os
import re
import sys

# Card number: digits with an optional letter prefix/suffix (T-4, 201A,
# 104-SSP, J-TO, SS-SC), NNO for unnumbered, or #LETTERS for letters-only.
NUMBER = r"(?:[A-Za-z]{1,5}-)?[A-Za-z]{0,3}\d+[A-Za-z]{0,2}(?:-[A-Za-z0-9]+)?|[A-Za-z]{1,5}-[A-Za-z]{1,5}|NNO|#[A-Za-z]+"
NAME_RE = re.compile(
    r"^(?P<season>\d{4}(?:-\d{2})?)_(?P<set>.+?)_(?P<number>" + NUMBER + r")_"
    r"(?P<player>.+)_(?P<side>Front|Back)\.jpg$"
)


def problems(folder, filename):
    out = []
    if not filename.endswith(".jpg"):
        out.append("extension must be .jpg")
    if not re.search(r"_(Front|Back)\.[^.]+$", filename):
        out.append("must end with _Front or _Back")
    if " " in filename:
        out.append("contains a space (use _)")
    if "__" in filename:
        out.append("contains a double underscore")
    if re.search(r"_#\d", filename):
        out.append("# is only for letters-only numbers (#DM), not digits")
    season = folder.split("_", 1)[0]
    if not filename.startswith(season + "_"):
        out.append(f"season does not match folder ({season})")
    if not out and not NAME_RE.match(filename):
        out.append("does not match <season>_<Set>_<number>_<Player>_<Front|Back>.jpg")
    return out


def main():
    quiet = "--quiet" in sys.argv
    total = bad = 0
    for top in sorted(os.listdir(".")):
        if not os.path.isdir(top) or not re.match(r"^\d{4}", top):
            continue
        for dirpath, _, files in os.walk(top):
            for f in sorted(files):
                total += 1
                p = problems(top, f)
                if p:
                    bad += 1
                    if not quiet:
                        print(f"{os.path.join(dirpath, f)}: {'; '.join(p)}")
    print(f"{total} images checked, {bad} with naming problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
