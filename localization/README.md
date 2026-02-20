# Pokémon Opalo 本地化專案

本目錄包含 Pokémon Opalo V2.11 繁體中文化的所有工具、翻譯檔案與資源。

## 目錄結構

```
localization/
├── tools/                # 提取、翻譯、打包工具
│   ├── extract.py        # 從 Data/messages.dat 提取對話文字
│   ├── extract_pbs.py    # 從 PBS/ 提取遊戲資料文字
│   ├── repack.py         # 將翻譯後的 JSON 打包回 messages.dat
│   ├── deploy.py         # 部署補丁到遊戲目錄
│   ├── translate.py      # 自動翻譯工具（西→繁中）
│   ├── translate_pbs.py  # PBS 檔案翻譯工具
│   ├── translate_abilities.py  # 特性翻譯工具
│   └── gen_items.py      # 道具資料生成工具
├── translations/         # 翻譯檔案（JSON 格式）
│   ├── messages.json     # 主要對話翻譯
│   ├── items.json        # 道具名稱與描述
│   ├── moves.json        # 招式名稱與描述
│   ├── types.json        # 屬性名稱
│   ├── trainers.json     # 訓練家資料
│   ├── trainertypes.json # 訓練家類型
│   ├── townmap.json      # 城鎮地圖
│   └── phone.json        # 電話對話
├── fonts/                # 中文字型檔案
├── glossary.json         # 術語表（統一翻譯用語）
├── installer/            # Windows 安裝器
│   ├── install.bat       # 安裝腳本
│   ├── uninstall.bat     # 解除安裝腳本
│   └── setup.iss         # Inno Setup 設定檔
├── releases/             # 發佈用補丁包
└── test_extract.py       # 測試腳本
```

## 工具使用方法

### 1. 提取文字 (extract.py)

從遊戲的 `Data/messages.dat` 提取所有對話文字為 JSON 格式：

```bash
python localization/tools/extract.py
```

輸出檔案：`localization/translations/messages.json`

### 2. 翻譯 (translate.py)

使用自動翻譯工具將西班牙文翻譯為繁體中文：

```bash
# 翻譯對話文字
python localization/tools/translate.py

# 翻譯 PBS 檔案
python localization/tools/translate_pbs.py
```

翻譯時會參照 `glossary.json` 術語表確保用語一致。

### 3. 打包 (repack.py)

將翻譯後的 JSON 打包回遊戲可讀取的 `.dat` 格式：

```bash
python localization/tools/repack.py
```

輸出檔案：`patches/messages.dat`

### 4. 部署 (deploy.py)

將補丁檔案部署到遊戲目錄：

```bash
python localization/tools/deploy.py
```

## 翻譯工作流程

```
提取 → 翻譯 → 校對 → 打包 → 測試 → 發佈
```

1. **提取**：執行 `extract.py` 從遊戲資料提取原文
2. **翻譯**：編輯 `translations/` 下的 JSON 檔案，或使用 `translate.py`
3. **校對**：檢查翻譯品質，參照術語表統一用語
4. **打包**：執行 `repack.py` 生成補丁檔案
5. **測試**：在遊戲中測試翻譯效果
6. **發佈**：打包為 ZIP 放入 `releases/`

## 術語表 (glossary.json)

術語表用於統一翻譯用語，格式如下：

```json
{
  "Pokémon": "寶可夢",
  "Entrenador": "訓練家",
  "Medalla": "徽章",
  "Pokédex": "寶可夢圖鑑"
}
```

翻譯工具會自動套用術語表中的對應翻譯，確保全專案用語一致。
如需新增術語，請直接編輯 `glossary.json`。

## 翻譯進度

| 類別 | 已翻譯 | 總計 | 進度 |
|------|--------|------|------|
| 對話文字 | 350 | 28,599 | ~1.2% |
| 道具 | ✅ | - | 完成 |
| 招式 | ✅ | - | 完成 |
| 屬性 | ✅ | - | 完成 |

## 注意事項

- 翻譯 JSON 檔案時，只修改 `"zh"` 欄位，不要更動 `"es"` 原文
- 遊戲使用 Ruby Marshal 格式，需安裝 `rubymarshal` 套件
- 測試前請備份原始遊戲檔案
