# hanser-lyrics

XPRAMT 校對過的 hanser 歌曲時間軸歌詞（LRC）。

[English](README.md)

## 格式

- UTF-8（含 BOM）LRC。
- 每行格式：`[行首時間]<行首時間>歌詞<行尾時間>`。

## 清單（index.json）

MoeMusicPlayer 用根目錄的 `index.json` 依標題與演唱者找到歌詞。新增或改名歌詞檔後，執行 `python scripts/build_index.py` 重新產生。 `index.json` 最上層的 `name` 是 MoeMusicPlayer 顯示的來源名稱，App 即時讀取，改了不用更新 App。

- 檔名格式：`演唱者[,演唱者…] - 標題.lrc`（多位演唱者用半形逗號分隔；以第一個「 - 」分開演唱者與標題）。
- 新增的歌詞檔會依檔名產生一筆，`album` 與 `durationMs`（毫秒）先是 `null`；已經在清單裡的項目不會被覆蓋，要改標題、演唱者、專輯或時長，直接編輯 `index.json`。檔案刪除後對應的項目會被移除。
