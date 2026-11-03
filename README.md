# hanser-lyrics

Proofread timed lyrics (LRC) for hanser songs, maintained by XPRAMT.

[繁體中文](README_TW.md)

## Files

| File | Song |
| --- | --- |
| `lyrics/2233 - 元素協奏.lrc` | 2233 - 元素協奏 |
| `lyrics/hanser - 水星.lrc` | hanser - 水星 (Japanese + Chinese translation) |

## Format

- UTF-8 (with BOM) LRC.
- Each line: `[line start]<line start>lyric<line end>`.

## Index (index.json)

MoeMusicPlayer reads `index.json` in the repository root to find lyrics by title and artist. After adding or renaming a lyrics file, run `python scripts/build_index.py` to regenerate it.

- File name format: `artist[,artist...] - title.lrc` (several artists are separated by a comma; the first " - " splits the artists from the title).
- Duration: `durations.json` maps a file name to "m:ss" (for example `"artist - title.lrc": "3:28"`); a file that is not listed uses its `[length:mm:ss]` tag if it has one, otherwise `durationMs` is `null`.
