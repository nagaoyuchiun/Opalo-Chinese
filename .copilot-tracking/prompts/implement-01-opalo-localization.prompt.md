---
agent: opalo-localizer
model: Claude Sonnet 4.5
---

<!-- markdownlint-disable-file -->

# Implementation Prompt: Pokémon Opalo 繁體中文化

## Instructions

1. 建立變更追蹤檔案如果不存在
2. 遵循 `task-execution` skill 工作流程
3. 系統性地實作 #file:../plans/20260121-01-opalo-chinese-localization-plan.instructions.md
4. 如果 phaseStop=true: 每個 Phase 完成後停止等待審核
5. 完成時: 刪除此 prompt 檔案

## Ralph Wiggum Loop Configuration

```json
{
  "completionPromise": "ALL_DONE",
  "maxIterations": 100,
  "phaseStop": false,
  "autoRetry": 3
}
```

## Execution Order

1. Phase 1: 工具開發 → 驗證提取功能
2. Phase 2: 文字提取 → 產出 JSON
3. Phase 3: AI 翻譯 → 完成翻譯
4. Phase 4: 字型處理 → 驗證顯示
5. Phase 5: 打包發布 → 產出 EXE

## Success Criteria

- [ ] 所有計畫項目已實作
- [ ] 變更追蹤檔案持續更新
- [ ] 遊戲可正常顯示中文
- [ ] EXE 安裝器功能正常

## Completion Signal

完成所有任務後，輸出: **ALL_DONE**

失敗時，輸出: **FAILED: [錯誤描述]**
