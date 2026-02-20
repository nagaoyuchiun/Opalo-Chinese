# -*- coding: utf-8 -*-
"""
完整翻譯 PBS/moves.txt 腳本
- 保留 ID、內部名稱、所有數值和標記
- 只翻譯：顯示名稱（第3欄位）和描述欄位
- 使用 glossary.json 術語
- 保留 UTF-8 BOM
"""

import os
import re
import json
import anthropic
from pathlib import Path

# 路徑設定
PBS_MOVES = r"D:\Opalo V2.11\PBS\moves.txt"
OUTPUT_PATH = r"D:\Opalo V2.11\localization\translations\pbs\moves.txt"
GLOSSARY_PATH = r"D:\Opalo V2.11\localization\glossary.json"

# 讀取術語表
with open(GLOSSARY_PATH, 'r', encoding='utf-8') as f:
    glossary = json.load(f)

# 建立術語對照
type_terms = {}
for term in glossary['categories']['pokemon_types']['terms']:
    type_terms[term['internal']] = term['zh_TW']

battle_terms = {}
for term in glossary['categories']['battle_terms']['terms']:
    battle_terms[term['es']] = term['zh_TW']

status_terms = {}
for term in glossary['categories']['status_effects']['terms']:
    status_terms[term['es']] = term['zh_TW']

print("✓ 術語表載入完成")
print(f"  屬性術語: {len(type_terms)} 項")
print(f"  戰鬥術語: {len(battle_terms)} 項")
print(f"  狀態術語: {len(status_terms)} 項")

# 初始化 Claude API
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise Exception("請設定 ANTHROPIC_API_KEY 環境變數")

client = anthropic.Anthropic(api_key=api_key)

def translate_with_claude(name_es, description_es, move_type, batch_num, total_batches):
    """使用 Claude 翻譯招式名稱和描述"""
    
    type_zh = type_terms.get(move_type, move_type)
    
    # 建立術語提示
    relevant_terms = {
        "屬性": type_zh,
        "關鍵術語": {
            "Ataque": "攻擊",
            "Defensa": "防禦",
            "Ataque Especial": "特攻",
            "Defensa Especial": "特防",
            "Velocidad": "速度",
            "Precisión": "命中率",
            "crítico": "要害",
            "objetivo": "對手/目標",
            "rival": "對手",
            "enemigo": "敵人",
            "usuario": "使用者",
            "turno": "回合",
            "PS": "HP",
            "paralizar": "麻痺",
            "envenenar": "中毒",
            "quemar": "灼傷",
            "dormir": "睡眠",
            "confundir": "混亂",
            "retroceder": "畏縮",
            "daño": "傷害",
            "bajar": "降低",
            "subir": "提高",
            "aumentar": "提高",
            "reducir": "降低"
        }
    }
    
    prompt = f'''你是寶可夢遊戲專業翻譯。請將以下招式翻譯成繁體中文：

**西班牙文招式名稱**: {name_es}
**西班牙文描述**: {description_es}
**招式屬性**: {type_zh}屬性

**翻譯要求**:
1. 招式名稱：簡潔有力，符合寶可夢官方風格（2-5字）
2. 描述：清楚說明效果，保持遊戲專業術語
3. 使用以下術語對照：{json.dumps(relevant_terms, ensure_ascii=False)}
4. 保持原文語氣（例如"puede"="可能會"）
5. 不要添加原文沒有的資訊

**輸出格式**（只輸出這兩行，無其他內容）:
NAME: [中文名稱]
DESC: [中文描述]

請開始翻譯：'''

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text.strip()
        
        # 解析回應
        name_match = re.search(r'NAME:\s*(.+)', response_text)
        desc_match = re.search(r'DESC:\s*(.+)', response_text, re.DOTALL)
        
        if name_match and desc_match:
            name_zh = name_match.group(1).strip()
            desc_zh = desc_match.group(1).strip()
            # 移除可能的多餘引號
            desc_zh = desc_zh.strip('"').strip()
            return name_zh, desc_zh
        else:
            print(f"  ⚠ 解析失敗: {response_text[:100]}")
            return name_es, description_es
            
    except Exception as e:
        print(f"  ✗ 翻譯錯誤: {e}")
        return name_es, description_es

# 讀取原始檔案
print(f"\n讀取檔案: {PBS_MOVES}")
with open(PBS_MOVES, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

print(f"✓ 共 {len(lines)} 行招式資料\n")

# 處理每一行
translated_lines = []
batch_size = 20
total_moves = len(lines)

for i, line in enumerate(lines, 1):
    line = line.rstrip('\n')
    
    # 跳過空行
    if not line.strip():
        translated_lines.append(line)
        continue
    
    # 解析招式資料
    # 格式: ID,INTERNAL,DisplayName,Code,Power,TYPE,Category,Accuracy,PP,EffectChance,Target,Priority,Flags,"Description"
    parts = line.split(',', 12)  # 最多分割12次（前12個逗號）
    
    if len(parts) < 13:
        print(f"  ⚠ 行 {i} 格式異常，保持原樣")
        translated_lines.append(line)
        continue
    
    move_id = parts[0]
    internal_name = parts[1]
    display_name_es = parts[2]
    move_type = parts[5]
    
    # 提取描述（在引號內）
    desc_match = re.search(r'"([^"]*)"$', line)
    if not desc_match:
        print(f"  ⚠ 行 {i} 無法提取描述，保持原樣")
        translated_lines.append(line)
        continue
    
    description_es = desc_match.group(1)
    
    # 翻譯
    print(f"[{i}/{total_moves}] 翻譯中: {display_name_es} ({move_type})...")
    name_zh, desc_zh = translate_with_claude(
        display_name_es, 
        description_es, 
        move_type,
        (i-1)//batch_size + 1,
        (total_moves-1)//batch_size + 1
    )
    
    # 重建行（替換第3欄位和描述）
    parts[2] = name_zh
    line_without_desc = ','.join(parts[:12])
    new_line = f'{line_without_desc},"{desc_zh}"'
    
    translated_lines.append(new_line)
    print(f"  ✓ {display_name_es} → {name_zh}")
    
    # 每20個招式暫停一下
    if i % batch_size == 0:
        print(f"\n--- 已完成 {i}/{total_moves} ({i*100//total_moves}%) ---\n")

# 寫入輸出檔案（保留 BOM）
print(f"\n寫入檔案: {OUTPUT_PATH}")
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# 寫入時加上 BOM
with open(OUTPUT_PATH, 'w', encoding='utf-8-sig') as f:
    f.write('\n'.join(translated_lines))

print(f"✓ 翻譯完成！")
print(f"  輸出: {OUTPUT_PATH}")
print(f"  共翻譯 {len(translated_lines)} 行招式")
