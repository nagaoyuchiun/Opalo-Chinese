# Pokémon Opalo 中文化專案

## 概述
將 Pokémon Opalo V2.11 (西班牙文) 翻譯為繁體中文。

## 專案結構
```
localization/
├── tools/          # 提取/打包工具
├── translations/   # 翻譯檔案 (JSON)
└── fonts/          # 中文字型
PBS/                # 遊戲文字資料
patches/            # 修改後的遊戲檔案
```

## 快速開始

### 1. 安裝依賴
```bash
pip install rubymarshal
```

### 2. 提取文字
```bash
python localization/tools/extract.py
```

### 3. 翻譯後打包
```bash
python localization/tools/repack.py
```

## 進度追蹤
- [x] 提取所有遊戲文字
- [x] 翻譯 messages.dat（部分）
- [x] 翻譯 PBS 檔案（道具、招式、屬性）
- [ ] 替換中文字型
- [ ] 測試驗證

## 繁體中文化

### 安裝方式

**方式一：使用安裝器（推薦）**

1. 下載 `localization/releases/opalo-v2.11-zhtw-patch.zip`
2. 解壓縮後執行 `installer/install.bat`
3. 選擇遊戲安裝目錄，依指示完成安裝

**方式二：手動複製**

1. 下載補丁包並解壓縮
2. 將 `messages.dat` 複製到遊戲的 `Data/` 資料夾，覆蓋原檔
3. 將翻譯後的 PBS 檔案複製到遊戲的 `PBS/` 資料夾

### 翻譯進度

| 類別 | 狀態 | 說明 |
|------|------|------|
| 對話文字 | 350 / 28,599 已翻譯 | 約 1.2% 完成 |
| 道具 (items) | ✅ 已完成 | PBS 檔案 |
| 招式 (moves) | ✅ 已完成 | PBS 檔案 |
| 屬性 (types) | ✅ 已完成 | PBS 檔案 |

### 繼續翻譯

如果你想幫助翻譯，請參考 `localization/README.md` 的完整說明。

```bash
# 安裝依賴
pip install rubymarshal

# 使用自動翻譯工具
python localization/tools/translate.py

# 翻譯後打包
python localization/tools/repack.py
```

翻譯時請參照 `localization/glossary.json` 術語表，確保用語統一。

### 致謝

感謝所有參與翻譯的貢獻者。本中文化為社群同人翻譯專案，
旨在讓更多中文玩家能夠體驗 Pokémon Opalo 的精彩冒險。

## 授權
本專案為同人翻譯，原遊戲版權歸 Pokémon Opalo 開發團隊所有。
