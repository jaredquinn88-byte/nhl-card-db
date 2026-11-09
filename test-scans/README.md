# Scanner test photos

Phone photos of physical cards (on a table, at an angle, with glare). They
are a test set for FaceOff TCG's card recognition: each photo's expected card
is in `labels.csv`.

The photo filenames are the card numbers. `label_status`:

- `confirmed`: the player name printed on the card in the photo matches the
  expected card.
- `unchecked`: the name isn't readable at this size; the label comes from the
  filename only.
- `wrong`: the photo shows a different card (see `note`).

These are not catalog images: the FaceOff TCG catalog builder ignores this
folder.
