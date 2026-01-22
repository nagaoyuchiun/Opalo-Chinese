<!-- markdownlint-disable-file -->

# Task Details: Pokémon Opalo 繁體中文化

## Research Reference
**驗證日期**: 2026-01-21
**驗證結果**: 通過測試，rubymarshal 可成功讀取遊戲資料

---

## Phase 1: 工具開發

### Task 1.1: 建立文字提取工具 (extract.py)

**目標**: 從遊戲二進制檔案提取所有可翻譯文字

**技術細節**:
```python
# 使用 rubymarshal 讀取 Ruby Marshal 格式
import rubymarshal.reader as reader

def extract_strings(filepath):
    with open(filepath, 'rb') as f:
        data = reader.load(f)
    # 遞迴提取所有字串
    strings = extract_strings_recursive(data)
    return strings
```

**輸入檔案**:
- `Data/messages.dat` - 主要對話文字 (~29,392 字串)
- `Data/trainers.dat` - 訓練師資料 (~546 字串)
- `Data/Map*.rxdata` - 地圖事件 (數量眾多)

**輸出格式** (JSON):
```json
{
  "metadata": {
    "source": "messages.dat",
    "extractedAt": "2026-01-21T00:00:00Z",
    "totalStrings": 29392
  },
  "strings": [
    {"id": 1, "path": "root[0]", "original": "¡Bienvenidos!", "translated": ""},
    {"id": 2, "path": "root[1]", "original": "Profesor Ébano", "translated": ""}
  ]
}
```

**成功標準**: 
- 無錯誤完成提取
- JSON 檔案可被 Python 正常讀取

---

### Task 1.2: 建立重新打包工具 (repack.py)

**目標**: 將翻譯後的 JSON 重新打包為遊戲格式

**技術細節**:
```python
import rubymarshal.writer as writer

def repack(json_path, original_path, output_path):
    # 讀取原始結構
    with open(original_path, 'rb') as f:
        data = reader.load(f)
    
    # 讀取翻譯
    translations = json.load(open(json_path))
    
    # 替換字串
    data = replace_strings(data, translations)
    
    # 寫回二進制格式
    with open(output_path, 'wb') as f:
        writer.write(f, data)
```

**成功標準**:
- 輸出檔案大小合理
- 遊戲可正常讀取

---

### Task 1.3: 建立部署工具 (deploy.py)

**目標**: 將補丁檔案部署到遊戲目錄

**功能**:
1. 備份原始檔案到 `backup/`
2. 複製 `patches/` 到 `Data/`
3. 複製字型到 `Fonts/`

---

## Phase 2: 文字提取

### Task 2.1: 提取 messages.dat

**執行指令**:
```bash
python localization/tools/extract.py --source Data/messages.dat --output localization/translations/messages.json
```

**預期結果**:
- 輸出 ~3MB JSON 檔案
- 包含 ~29,392 個翻譯條目

---

## Phase 3: AI 翻譯

### Task 3.1: 術語對照表

**官方寶可夢中文譯名範例**:
```json
{
  "Pikachu": "皮卡丘",
  "Pokémon": "寶可夢",
  "Poké Ball": "寶貝球",
  "Profesor": "博士",
  "Gimnasio": "道館"
}
```

### Task 3.2: 翻譯規則

1. **保留格式標籤**: `<b>`, `</b>`, `\n`
2. **保留變數**: `{player}`, `{pokemon}`
3. **術語一致**: 使用官方譯名
4. **語氣適當**: 符合遊戲情境

---

## Phase 4: 字型處理

### Task 4.1: 字型需求

**建議字型**: Noto Sans TC (思源黑體)
- 下載: https://fonts.google.com/noto/specimen/Noto+Sans+TC
- 支援完整繁體中文字集

**替換對應**:
| 原始字型 | 替換為 |
|----------|--------|
| pkmndp.ttf | NotoSansTC-Regular.ttf |
| pkmndpb.ttf | NotoSansTC-Bold.ttf |

---

## Phase 5: 打包發布

### Task 5.2: 安裝器設計

```
┌─────────────────────────────────────────┐
│  Pokémon Opalo 繁體中文化補丁           │
│  版本: 1.0                              │
├─────────────────────────────────────────┤
│                                         │
│  請選擇遊戲資料夾:                       │
│  [                              ] [瀏覽] │
│                                         │
│  ☑ 備份原始檔案                          │
│  ☑ 安裝中文字型                          │
│                                         │
│          [安裝] [取消]                   │
└─────────────────────────────────────────┘
```
