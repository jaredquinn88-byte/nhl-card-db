#!/usr/bin/env python3
"""Remove byte-identical duplicate card images and fold card-images/ into the
per-set folders at the repo root.

For every image, git's blob id identifies its exact content. Among files with
the same content, one is kept (see keep_score) and the rest are deleted.
Images that exist only under card-images/ are moved to the matching set folder
at the root. Every action is written to scripts/dedupe_manifest.csv so any
deleted path can be traced to the identical file that was kept.

Dry run (default) prints a summary. --apply stages the changes with git.
Usage: python3 scripts/dedupe_images.py [--apply]
"""

import csv
import os
import re
import subprocess
import sys
from collections import defaultdict

IMAGE_EXT = ('.jpg', '.jpeg', '.png', '.webp')
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(REPO, 'scripts', 'dedupe_manifest.csv')
UNSORTED = '_unsorted'

# card-images/<folder> names that don't follow the "<season>_<Set>" pattern.
ODD_FOLDER = re.compile(r'^\d{4}-\d{2}-')  # e.g. 1991-92-pro-set
RANGE_DIR = re.compile(r'^#?\d+-#?\d+$')   # e.g. 1-99, #1-#662
SERIES_DIR = re.compile(r'series|extended|update|insert', re.I)
SCRAPE_TAB_DIRS = {'overview', 'pricing', 'hall of famers'}


def git(*args, input_bytes=None):
    return subprocess.run(['git', '-C', REPO, *args], input=input_bytes,
                          capture_output=True, check=True).stdout


def list_images():
    out = git('ls-tree', '-r', '-z', 'HEAD')
    for rec in out.split(b'\0'):
        if not rec:
            continue
        meta, path = rec.split(b'\t', 1)
        path = path.decode('utf-8')
        if path.lower().endswith(IMAGE_EXT):
            yield meta.split()[2].decode(), path


def zone(path):
    if path.startswith('AI_Pilot_Batch/'):
        return 3
    if path.startswith('card-images/output/'):
        return 2
    if path.startswith('card-images/'):
        return 1
    return 0


def keep_score(path):
    """Lower is better."""
    parts = path.split('/')[1:-1] if zone(path) == 0 else []
    s = zone(path) * 1000
    names = [p.lower() for p in parts]
    if any(n in SCRAPE_TAB_DIRS for n in names):
        s += 500                     # copies saved from website tabs
    if any(RANGE_DIR.match(p) for p in parts):
        s += 0                       # tidy "1-99/100-199" layout: best
    elif any(SERIES_DIR.search(p) for p in parts):
        s += 10
    elif 'base_images' in names:
        s += 40
    else:
        s += 30                      # "Base Set", "1991-92 Upper Deck", ...
    return (s, len(path), path)


def move_target(path):
    """Where an image that only exists under card-images/ should go."""
    rel = path[len('card-images/'):]
    folder = rel.split('/', 1)[0]
    if ODD_FOLDER.match(folder) or '_' not in folder:
        return f'{UNSORTED}/{rel}'
    return rel


def main(apply):
    by_blob = defaultdict(list)
    for blob, path in list_images():
        by_blob[blob].append(path)
    existing = {p for ps in by_blob.values() for p in ps}

    actions = []  # (action, path, kept_or_target)
    for blob, paths in by_blob.items():
        paths.sort(key=keep_score)
        keeper = paths[0]
        if keeper.startswith('card-images/'):
            if zone(keeper) != 1:
                raise SystemExit(f'unexpected keeper outside root/card-images: {keeper}')
            target = move_target(keeper)
            if target in existing:
                raise SystemExit(f'move target already exists with other content: {target}')
            actions.append(('move', keeper, target))
            keeper = target
        for p in paths[1:]:
            actions.append(('delete', p, keeper))

    counts = defaultdict(int)
    for a, _, _ in actions:
        counts[a] += 1
    print(f'images: {len(existing)}  unique contents: {len(by_blob)}')
    print(f'delete: {counts["delete"]}  move: {counts["move"]}')
    print(f'images after: {len(existing) - counts["delete"]}')

    if not apply:
        print('dry run; pass --apply to stage changes')
        return

    with open(MANIFEST, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['action', 'path', 'kept_copy_or_new_path'])
        for row in sorted(actions, key=lambda r: (r[0], r[1])):
            w.writerow(row)

    deletes = [p for a, p, _ in actions if a == 'delete']
    git('rm', '-q', '--cached', '--pathspec-from-file=-', '--pathspec-file-nul',
        input_bytes='\0'.join(deletes).encode())
    for p in deletes:
        full = os.path.join(REPO, p)
        if os.path.exists(full):
            os.remove(full)
    for a, src, dst in actions:
        if a == 'move':
            os.makedirs(os.path.dirname(os.path.join(REPO, dst)), exist_ok=True)
            git('mv', src, dst)
    # Drop now-empty directories.
    for root, dirs, files in os.walk(REPO, topdown=False):
        if '.git' in root.split(os.sep):
            continue
        if not dirs and not files and root != REPO:
            os.rmdir(root)
        elif not os.listdir(root) and root != REPO:
            os.rmdir(root)
    print(f'staged; manifest written to {os.path.relpath(MANIFEST, REPO)}')


if __name__ == '__main__':
    main('--apply' in sys.argv[1:])
