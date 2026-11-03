# hanser-lyrics

XPRAMT 校對過的 hanser 歌曲時間軸歌詞（LRC）。

[English](README.md)

## 格式

- UTF-8（含 BOM）LRC。
- 每行格式：`[行首時間]<行首時間>歌詞<行尾時間>`。

## 清單（index.json）

MoeMusicPlayer 用根目錄的 `index.json` 依標題與演唱者找到歌詞。新增或改名歌詞檔後，執行 `python scripts/build_index.py` 重新產生。

- 檔名格式：`演唱者[,演唱者…] - 標題.lrc`（多位演唱者用半形逗號分隔；以第一個「 - 」分開演唱者與標題）。
- 時長：在 `durations.json` 用檔名對應「m:ss」（例如 `"演唱者 - 標題.lrc": "3:28"`）；沒列的檔案若 LRC 有 `[length:mm:ss]` 標籤也會採用，否則 `durationMs` 為 `null`。
