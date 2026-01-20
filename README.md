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
- [ ] 提取所有遊戲文字
- [ ] 翻譯 messages.dat
- [ ] 翻譯 PBS 檔案
- [ ] 替換中文字型
- [ ] 測試驗證

## 授權
本專案為同人翻譯，原遊戲版權歸 Pokémon Opalo 開發團隊所有。
