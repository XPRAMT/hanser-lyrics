# hanser-lyrics

Proofread timed lyrics (LRC) for hanser songs, maintained by XPRAMT.

[繁體中文](README_TW.md)

## Format

- UTF-8 (with BOM) LRC.
- Each line: `[line start]<line start>lyric<line end>`.

## Index (index.json)

MoeMusicPlayer reads `index.json` in the repository root to find lyrics by title and artist. After adding or renaming a lyrics file, run `python scripts/build_index.py` to regenerate it. The top-level `name` in `index.json` is the source name MoeMusicPlayer shows; the app reads it live, so changing it needs no app update.

- File name format: `artist[,artist...] - title.lrc` (several artists are separated by a comma; the first " - " splits the artists from the title).
- A new lyrics file gets an entry made from its file name, with `album` and `durationMs` (milliseconds) set to `null`; entries already in the list are never overwritten, so edit the title, artists, album or duration directly in `index.json`. An entry whose file is deleted is removed.
