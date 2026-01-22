---
applyTo: ".copilot-tracking/changes/20260121-opalo-chinese-localization-changes.md"
---

<!-- markdownlint-disable-file -->

# Task Checklist: Pokémon Opalo 繁體中文化

## Overview
將 Pokémon Opalo V2.11 遊戲從西班牙文翻譯為繁體中文，並提供一鍵安裝的 EXE 安裝器。

## Objectives
- 提取並翻譯所有遊戲文字 (~50,000 字串)
- 建立可重複使用的中文化工具鏈
- 產出使用者友善的 EXE 安裝器

## Research Summary
- 遊戲使用 RPG Maker XP + MKXP 引擎
- messages.dat 包含 29,392 個可翻譯字串
- PBS 資料夾包含純文字格式的遊戲數據
- 可使用 Python + rubymarshal 提取/打包

---

## Implementation Checklist

### [ ] Phase 1: 工具開發
- [ ] Task 1.1: 建立文字提取工具 (extract.py)
  - Details: .copilot-tracking/details/20260121-01-localization-details.md (Lines 10-30)
  - 輸入: Data/*.dat, Data/*.rxdata
  - 輸出: localization/translations/*.json
  
- [ ] Task 1.2: 建立重新打包工具 (repack.py)
  - Details: .copilot-tracking/details/20260121-01-localization-details.md (Lines 32-50)
  - 輸入: localization/translations/*.json
  - 輸出: patches/*.dat

- [ ] Task 1.3: 建立部署工具 (deploy.py)
  - Details: .copilot-tracking/details/20260121-01-localization-details.md (Lines 52-65)
  - 功能: 複製 patches/ 到 Data/

---

### [ ] Phase 2: 文字提取
- [ ] Task 2.1: 提取 messages.dat
  - 執行: `python localization/tools/extract.py --source Data/messages.dat`
  - 預期輸出: localization/translations/messages.json (~30,000 字串)

- [ ] Task 2.2: 提取 trainers.dat
  - 執行: `python localization/tools/extract.py --source Data/trainers.dat`
  - 預期輸出: localization/translations/trainers.json (~600 字串)

- [ ] Task 2.3: 處理 PBS 檔案
  - 直接編輯 PBS/*.txt (純文字格式)
  - 優先: abilities.txt, items.txt, moves.txt

---

### [ ] Phase 3: AI 翻譯
- [ ] Task 3.1: 建立術語對照表
  - 輸出: localization/glossary.json
  - 內容: 官方寶可夢中文譯名

- [ ] Task 3.2: 批次翻譯 messages.json
  - 使用 AI 批次翻譯
  - 分批處理: 每批 500 字串

- [ ] Task 3.3: 批次翻譯 PBS 檔案
  - 優先順序: items → abilities → moves → trainers

- [ ] Task 3.4: 人工校對
  - 檢查術語一致性
  - 驗證格式標籤保留

---

### [ ] Phase 4: 字型處理
- [ ] Task 4.1: 取得中文字型
  - 下載: Noto Sans TC 或 思源黑體
  - 放置: localization/fonts/

- [ ] Task 4.2: 替換遊戲字型
  - 更新: Fonts/*.ttf
  - 輸出: patches/Fonts/

- [ ] Task 4.3: 測試字型顯示
  - 啟動遊戲驗證中文顯示正常

---

### [ ] Phase 5: 打包發布
- [ ] Task 5.1: 建立打包工具 (repack.py)
  - 將翻譯 JSON 轉回遊戲格式
  - 輸出: patches/Data/*.dat

- [ ] Task 5.2: 建立安裝器 (installer.py)
  - 使用 tkinter 建立 GUI
  - 功能: 選擇遊戲資料夾、備份、安裝

- [ ] Task 5.3: 打包 EXE
  - 執行: `pyinstaller --onefile --windowed installer.py`
  - 輸出: dist/安裝中文化.exe

- [ ] Task 5.4: 測試完整流程
  - 在乾淨環境測試安裝
  - 驗證遊戲可正常執行

---

## Dependencies
- Python 3.10+
- rubymarshal (pip install rubymarshal)
- PyInstaller (pip install pyinstaller)
- tkinter (Python 內建)

## Success Criteria
- [ ] 所有 PBS 文字翻譯完成
- [ ] messages.dat 翻譯完成
- [ ] 遊戲可正常顯示中文
- [ ] EXE 安裝器可正常使用
- [ ] 輸出 `ALL_DONE` 完成信號
