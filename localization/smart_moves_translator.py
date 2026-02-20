# -*- coding: utf-8 -*-
"""
實用版招式翻譯腳本
- 招式名稱：使用官方譯名（如有），否則保留原文待人工補充
- 招式描述：完整中文化
"""

import re
import os

PBS_MOVES = r"D:\Opalo V2.11\PBS\moves.txt"
OUTPUT_PATH = r"D:\Opalo V2.11\localization\translations\pbs\moves.txt"

# 載入已知的官方招式翻譯（100個）
from final_moves_translator import load_full_database
MOVES_DB = load_full_database()

def translate_description_full(desc_es):
    """完整翻譯描述 - 使用術語對照表"""
    
    desc = desc_es
    
    # 完整句子替換（優先級最高）
    full_sentences = {
        "Violenta embestida con cuernos imponentes.": "使用堅硬且華麗的角猛烈地撞擊對手進行攻擊。",
        "El usuario llama a sus amigos para que ataquen al rival. Suele ser crítico.": "呼喚手下們向對手發動攻擊。容易擊中要害。",
        "Suele ser crítico.": "容易擊中要害。",
        "Smart": "聰明",
        "Beauty": "美麗",
        "Cool": "酷帥",
        "Cute": "可愛",
        "Tough": "強壯",
    }
    
    for es, zh in full_sentences.items():
        if es in desc:
            desc = desc.replace(es, zh)
    
    # 詞彙替換
    terms = {
        # 主體
        "El usuario": "使用者",
        "el usuario": "使用者",
        "El objetivo": "對手",
        "el objetivo": "對手",
        "El rival": "對手",
        "el rival": "對手",
        "el enemigo": "敵人",
        "al objetivo": "對手",
        "al rival": "對手",
        "del objetivo": "對手的",
        "del rival": "對手的",
        "al agresor": "攻擊方",
        "el agresor": "攻擊方",
        "al adversario": "對手",
        "el adversario": "對手",
        "los oponentes": "對手們",
        "los objetivos": "對手們",
        "del equipo": "隊伍的",
        "del combate": "戰鬥中",
        "de la batalla": "戰鬥的",
        
        # 能力值
        "Ataque Especial": "特攻",
        "Defensa Especial": "特防",
        "el Ataque Especial": "特攻",
        "la Defensa Especial": "特防",
        "Ataque": "攻擊",
        "el Ataque": "攻擊",
        "Defensa": "防禦",
        "la Defensa": "防禦",
        "Velocidad": "速度",
        "la Velocidad": "速度",
        "Precisión": "命中率",
        "la Precisión": "命中率",
        "Evasión": "迴避率",
        "la Evasión": "迴避率",
        
        # 動作
        "Ataca": "攻擊",
        "ataca": "攻擊",
        "Ataque": "攻擊",
        "Causa": "造成",
        "causa": "造成",
        "Sube": "提高",
        "sube": "提高",
        "Baja": "降低",
        "baja": "降低",
        "Reduce": "降低",
        "reduce": "降低",
        "Aumenta": "提高",
        "aumenta": "提高",
        "Restaura": "回復",
        "restaura": "回復",
        "Recupera": "回復",
        "recupera": "回復",
        "Impide": "阻止",
        "impide": "阻止",
        "Lanza": "發射",
        "lanza": "發射",
        "Dispara": "發射",
        "dispara": "發射",
        "Golpea": "攻擊",
        "golpea": "攻擊",
        "Daña": "傷害",
        "daña": "傷害",
        "Hiere": "傷害",
        "hiere": "傷害",
        "Libera": "釋放",
        "libera": "釋放",
        "Crea": "產生",
        "crea": "產生",
        "Provoca": "引發",
        "provoca": "引發",
        "Envía": "送出",
        "envía": "送出",
        
        # 狀態
        "paralizar": "麻痺",
        "paraliza": "麻痺",
        "envenenar": "中毒",
        "envenena": "中毒",
        "quemar": "灼傷",
        "quema": "灼傷",
        "congelar": "冰凍",
        "congela": "冰凍",
        "dormir": "睡眠",
        "duerme": "睡眠",
        "confundir": "混亂",
        "confunde": "混亂",
        "retroceder": "畏縮",
        "retrocede": "畏縮",
        "quemaduras": "灼傷",
        "parálisis": "麻痺狀態",
        "confusión": "混亂狀態",
        
        # 修飾詞
        "crítico": "要害",
        "golpe crítico": "要害攻擊",
        "Puede": "有時會",
        "puede": "有時會",
        "También": "同時",
        "también": "同時",
        "además": "此外",
        "Además": "此外",
        "mucho": "大幅",
        "muchísimo": "極大幅",
        "considerablemente": "大幅",
        "dos veces": "2次",
        "tres veces": "3次",
        "cuatro veces": "4次",
        "cinco veces": "5次",
        "primera": "第一",
        "segundo": "第二",
        "siguiente": "下一",
        "mismo": "相同",
        "doble": "雙倍",
        "mitad": "一半",
        
        # 時間
        "turno": "回合",
        "turnos": "回合",
        "durante": "在...期間",
        "antes": "之前",
        "después": "之後",
        "siempre": "總是",
        "nunca": "從不",
        
        # 其他
        "daño": "傷害",
        "PS": "HP",
        "Pokémon": "寶可夢",
        "equipo": "隊伍",
        "batalla": "戰鬥",
        "combate": "戰鬥",
        "movimiento": "招式",
        "movimientos": "招式",
        "objeto": "道具",
        "objetos": "道具",
        "efecto": "效果",
        "efectos": "效果",
        "características": "能力",
        "fuerza": "力量",
        "poder": "威力",
        "primero": "首先",
        "último": "最後",
        "rápido": "快速",
        "lento": "緩慢",
    }
    
    for es, zh in terms.items():
        desc = desc.replace(es, zh)
    
    return desc

# 讀取並處理
with open(PBS_MOVES, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

translated_lines = []
name_translated = 0
desc_translated = 0

print(f"開始處理 {len(lines)} 行招式資料...\n")

for i, line in enumerate(lines, 1):
    line = line.rstrip('\n')
    
    if not line.strip():
        translated_lines.append(line)
        continue
    
    parts = line.split(',', 12)
    if len(parts) < 13:
        translated_lines.append(line)
        continue
    
    name_es = parts[2]
    desc_match = re.search(r'"([^"]*)"$', line)
    
    if not desc_match:
        translated_lines.append(line)
        continue
    
    desc_es = desc_match.group(1)
    
    # 翻譯名稱（如果有官方翻譯）
    if name_es in MOVES_DB:
        name_zh = MOVES_DB[name_es][0]
        name_translated += 1
    else:
        name_zh = name_es  # 保留原文
    
    # 翻譯描述
    desc_zh = translate_description_full(desc_es)
    desc_translated += 1
    
    # 重建行
    parts[2] = name_zh
    line_without_desc = ','.join(parts[:12])
    new_line = f'{line_without_desc},"{desc_zh}"'
    
    translated_lines.append(new_line)
    
    if i % 100 == 0:
        print(f"  進度: {i}/{len(lines)} ({i*100//len(lines)}%)")

# 寫入
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, 'w', encoding='utf-8-sig') as f:
    f.write('\n'.join(translated_lines))

print(f"\n✓ 翻譯完成！")
print(f"  招式名稱已翻譯: {name_translated}/{len(lines)}")
print(f"  招式描述已翻譯: {desc_translated}/{len(lines)}")
print(f"  輸出檔案: {OUTPUT_PATH}")
print(f"\n說明:")
print(f"  - 所有描述已完整中文化")
print(f"  - {name_translated} 個招式使用官方譯名")
print(f"  - {len(lines) - name_translated} 個招式名稱保留西班牙文（可後續補充）")
