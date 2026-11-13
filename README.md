# nhl-card-db

Images of NHL hockey cards, organised by set. Used by
[FaceOff TCG](https://github.com/jaredquinn88-byte/faceoff-tcg) to build its
card catalog.

## Layout

```
<season>_<Set>/            one folder per set, e.g. 2022-23_MVP/
  <range>/                 optional, e.g. 1-99/, 100-199/
    <season>_<Set_Name>_<number>_<Player_Name>_<Front|Back>.jpg
reference-data/            scraped checklist data (unverified, see its README)
test-scans/                phone photos of real cards, for testing recognition
_review/                   images whose card isn't identified yet
scripts/                   maintenance scripts
```

**The filename is the card's record.** FaceOff TCG reads season, set, card
number and player from it, so new images must follow the pattern:

```
2022-23_Upper_Deck_MVP_73_David_Perron_Front.jpg
1990-91_Pro_Set_NNO_The_Stanley_Cup_Front.jpg     (NNO = unnumbered)
2017-18_Upper_Deck_Tim_Hortons_-_NHL_Jersey_Relics_J-TO_Jonathan_Toews_Front.jpg
```

- Words are separated by `_`; keep accents (`Éric_Dazé`).
- The card number is the first part after the set name: digits, optionally
  with a letter prefix or suffix (`T-4`, `201A`, `104-SSP`), or `NNO`.
  A number made only of letters starts with `#` (`#DM`), so it can't be
  mistaken for part of a name.
- Error cards that repeat another card's number get a letter (`2b`: 1995-96
  Stadium Club Bill Ranford, misnumbered #2 instead of #21).
- End with `_Front` or `_Back`, always, even when the set has no backs.
  (A player whose surname is Back still needs the suffix:
  `2025-26_O-Pee-Chee_257_Oskar_Back_Front.jpg`.)
- Range folders are plain numbers (`1-99/`, `100-199/`), with no `#`.

Run `python3 scripts/check_names.py` before committing new images; it lists
any file that breaks these rules and exits non-zero if there are any.

## Scripts

- `scripts/check_names.py`: checks every image name against the schema above.
- `scripts/rename_manifest.csv`: old and new path of each of the 3,634 images
  renamed in the November 2026 naming clean-up (2,851 missing `_Front`,
  782 with `#` before a numeric card number, plus truncated names such as
  `1991-92_Upper_Deck_45_The_.jpg` → `..._45_The_50-50_Club_Front.jpg`).

- `scripts/dedupe_images.py`: removes byte-identical duplicate images
  (dry run by default, `--apply` to stage). `scripts/dedupe_manifest.csv`
  records every file removed in the November 2026 clean-up and the identical
  copy that was kept.
