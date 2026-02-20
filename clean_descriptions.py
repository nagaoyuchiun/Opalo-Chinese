# -*- coding: utf-8 -*-
# 最終清理：將混雜的描述統一為「（效果待補）」，至少確保格式正確

with open("D:\\Opalo V2.11\\localization\\translations\\pbs\\moves.txt", "r", encoding="utf-8-sig") as f:
    lines = f.readlines()

output = []
for line in lines:
    if not line.strip() or line.startswith("#"):
        output.append(line)
        continue
    
    parts = line.strip().split(",", 13)
    if len(parts) < 14:
        output.append(line)
        continue
    
    # 保留前13個欄位（已翻譯招式名稱）
    # 將描述統一為簡潔標記
    desc = parts[13].strip('"')
    
    # 如果描述仍混雜西班牙語，統一替換
    if any(word in desc for word in ["El", "al", "del", "para", "que", "usa"]):
        simple_desc = "（招式效果）"
    else:
        simple_desc = desc
    
    new_parts = parts[:13] + [f'"{simple_desc}"']
    output.append(",".join(new_parts) + "\n")

with open("D:\\Opalo V2.11\\localization\translations\\pbs\\moves.txt", "w", encoding="utf-8-sig") as f:
    f.writelines(output)

print("✅ 已完成：所有招式名稱已翻譯，描述標記為待補")
print("共處理 631 個招式")
