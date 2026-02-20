# 快速開始指南

## 安裝依賴

```bash
pip install rubymarshal
```

## 基本使用

### 1. 提取文字

```bash
cd localization/tools
python extract.py ../../Data/messages.dat -o ../translations/messages.json
```

### 2. 編輯翻譯

打開 `localization/translations/messages.json`，找到需要翻譯的條目：

```json
{
  "id": "section_0[1].0",
  "original": "¡Bienvenidos a <b>Mundo Indómito</b>!",
  "translation": "",  // 在這裡填入翻譯
  "context": {...}
}
```

填入翻譯：

```json
{
  "id": "section_0[1].0",
  "original": "¡Bienvenidos a <b>Mundo Indómito</b>!",
  "translation": "歡迎來到<b>狂野世界</b>！",
  "context": {...}
}
```

**重要提示:**
- 保留 HTML 標記如 `<b>`, `</b>`
- 保留特殊字符如 `\n` (換行)
- 使用 UTF-8 編碼保存

### 3. 重新打包

```bash
python repack.py ../translations/messages.json -o ../../patches/messages.dat
```

### 4. 測試

**重要: 先備份原始檔案！**

```bash
# 備份原始檔案
cp ../../Data/messages.dat ../../Data/messages.dat.backup

# 複製翻譯後的檔案
cp ../../patches/messages.dat ../../Data/messages.dat

# 啟動遊戲測試
```

如果有問題，恢復備份：

```bash
cp ../../Data/messages.dat.backup ../../Data/messages.dat
```

## 批量處理

處理多個檔案：

```bash
# 提取
python extract.py ../../Data/messages.dat
python extract.py ../../Data/trainers.dat
python extract.py ../../Data/moves.dat

# 翻譯後重新打包
python repack.py ../translations/messages.json
python repack.py ../translations/trainers.json
python repack.py ../translations/moves.json
```

## 驗證

運行整合測試：

```bash
python test_integration.py
```

應該看到：
```
✓ 提取功能: 正常
✓ 重新打包功能: 正常
✓ 檔案格式驗證: 通過
✓ 翻譯應用: 正常
```

## 常見問題

### Q: 翻譯沒有在遊戲中顯示？

A: 檢查：
1. patches/messages.dat 是否正確複製到 Data/messages.dat
2. JSON 中的 translation 欄位是否非空
3. 使用 extract.py 重新提取來驗證翻譯

### Q: 遊戲崩潰了？

A: 
1. 恢復備份檔案
2. 檢查是否破壞了 HTML 標記或特殊字符
3. 檢查檔案大小是否合理
4. 使用測試工具驗證

### Q: 如何只翻譯部分內容？

A: 可以！只填入你想翻譯的條目的 translation 欄位，其他留空。repack.py 只會應用非空的翻譯。

## 更多資訊

查看 [README.md](README.md) 獲取完整文檔。
