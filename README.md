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
- End with `_Front` or `_Back`.

## Scripts

- `scripts/dedupe_images.py`: removes byte-identical duplicate images
  (dry run by default, `--apply` to stage). `scripts/dedupe_manifest.csv`
  records every file removed in the November 2026 clean-up and the identical
  copy that was kept.
