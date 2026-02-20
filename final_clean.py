# -*- coding: utf-8 -*-

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
    
    desc = parts[13].strip('"')
    
    # 保留已完全翻譯的描述，清理混雜的
    if len(desc) < 50 and all(ord(c) > 127 or not c.isalpha() for c in desc.replace("（", "").replace("）", "")):
        simple_desc = desc  # 保留純中文描述
    else:
        simple_desc = "（招式效果）"  # 混雜或過長的統一標記
    
    new_parts = parts[:13] + [f'"{simple_desc}"']
    output.append(",".join(new_parts) + "\n")

with open("D:\\Opalo V2.11\\localization\\translations\\pbs\\moves.txt", "w", encoding="utf-8-sig") as f:
    f.writelines(output)

print("✅ 完成")
