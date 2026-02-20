# -*- coding: utf-8 -*-
"""
完整翻譯 PBS/moves.txt 腳本
使用預定義的寶可夢招式翻譯對照表
"""

import os
import re
import json
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

print("✓ 術語表載入完成")
print(f"  屬性術語: {len(type_terms)} 項\n")

# 寶可夢官方招式翻譯對照表（基於 Bulbapedia 和任天堂官方翻譯）
OFFICIAL_MOVES = {
    # Bug moves
    "Megacuerno": "超級角擊",
    "Al Ataque": "攻擊指令",
    "Zumbido": "蟲鳴",
    "Tijera X": "十字剪",
    "Doble Rayo": "訊號光束",
    "Ida y Vuelta": "急速折返",
    "Rodillo Púas": "重壓路滾",
    "Picadura": "蟲咬",
    "Viento Plata": "銀色旋風",
    "Estoicismo": "蟲之抵抗",
    "Dobleataque": "雙針",
    "Cortefuria": "連斬",
    "Chupavidas": "吸血",
    "Pin Misil": "飛彈針",
    "A Defender": "防守指令",
    "Auxilio": "回復指令",
    "Danza Aleteo": "蝶舞",
    "Polvo Ira": "憤怒粉",
    "Telaraña": "蛛網",
    "Disp. Demora": "吐絲",
    "Ráfaga": "螢火",
    
    # Dark moves
    "Juego Sucio": "欺詐",
    "Pulso Noche": "暗黑爆破",
    "Triturar": "咬碎",
    "Pulso Umbrío": "惡之波動",
    "Golpe Bajo": "突襲",
    "Tajo Umbrio": "暗襲要害",
    "Mordisco": "咬住",
    "Finta": "出奇一擊",
    "Alarido": "大聲咆哮",
    "Buena Baza": "以牙還牙",
    "Vendetta": "報仇",
    "Persecución": "追擊",
    "Ladrón": "小偷",
    "Desarme": "拍落",
    "Paliza": "圍攻",
    "Lanzamiento": "投擲",
    "Castigo": "懲罰",
    "Brecha Negra": "暗黑洞",
    "Embargo": "查封",
    "Llanto Falso": "假哭",
    "Camelo": "詭計",
    "Afilagarras": "磨爪",
    "Legado": "臨別禮物",
    "Maquinación": "詭計",
    "Último Lugar": "擋路",
    "Robo": "搶奪",
    "Trapicheo": "掉包",
    "Mofa": "挑釁",
    "Tormento": "無理取鬧",
    
    # Dragon moves
    "Distorción": "時光咆哮",
    "Cometa Draco": "流星群",
    "Enfado": "逆鱗",
    "Carga Dragón": "龍之俯衝",
    "Corte Vacío": "亞空裂斬",
    "Pulso Dragón": "龍之波動",
    "Garra Dragón": "龍爪",
    "Cola Dragón": "龍尾",
    "Dragoaliento": "龍息",
    "Golpe Bis": "二連劈",
    "Ciclón": "龍捲風",
    "Furia Dragón": "龍之怒",
    "Danza Dragón": "龍之舞",
    
    # Electric moves
    "At. Fulgor": "閃電突擊",
    "Trueno": "打雷",
    "Placaje Eléc.": "伏特攻擊",
    "Electrocañón": "電磁砲",
    "Rayo Fusión": "交錯閃電",
    "Rayo": "十萬伏特",
    "Voltio Cruel": "瘋狂伏特",
    "Chispazo": "放電",
    "Puño Trueno": "雷電拳",
    "Voltiocambio": "伏特替換",
    "Chispa": "電光",
    "Colm. Rayo": "雷電牙",
    "Onda Voltio": "電擊波",
    "Electrotela": "電網",
    "Rayo Carga": "充電光束",
    "Impactrueno": "電擊",
    "Bola Voltio": "電球",
    "Carga": "充電",
    "Levitón": "電磁飄浮",
    "Onda Trueno": "電磁波",
    
    # Fighting moves
    "Puño Certero": "真氣彈",
    "Pat. S. Alta": "飛膝踢",
    "A Bocajarro": "近身戰",
    "Onda Certera": "真氣彈",
    "Fuerza Bruta": "蠻力",
    "Tajo Cruzado": "十字劈",
    "Puñodinámico": "爆裂拳",
    "Machada": "臂錘",
    "Patada Salto": "飛踢",
    "Esfera Aural": "波導彈",
    "Espadasanta": "聖劍",
    "Sablemístico": "神秘之劍",
    "Gancho Alto": "沖天拳",
    "Sumisión": "地球上投",
    "Demolición": "劈瓦",
    "Puño Drenaje": "吸取拳",
    "Tiro Vital": "借力摔",
}

def translate_desc_smart(desc_es, move_type):
    """智能翻譯描述"""
    
    # 常用術語替換
    replacements = {
        # 能力值
        "Ataque Especial": "特攻",
        "Defensa Especial": "特防",
        "Ataque": "攻擊",
        "Defensa": "防禦",
        "Velocidad": "速度",
        "Precisión": "命中率",
        "Evasión": "迴避率",
        
        # 對象
        "objetivo": "對手",
        "rival": "對手",
        "enemigo": "敵人",
        "adversario": "對手",
        "oponente": "對手",
        "usuario": "使用者",
        "agresor": "攻擊方",
        "Pokémon": "寶可夢",
        "equipo": "隊伍",
        
        # 動作
        "Ataca": "攻擊",
        "ataca": "攻擊",
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
        
        # 其他
        "crítico": "要害",
        "golpe crítico": "要害攻擊",
        "turno": "回合",
        "daño": "傷害",
        "PS": "HP",
        "Suele ser crítico": "容易擊中要害",
        "puede": "可能會",
        "Puede": "可能會",
        "También": "同時",
        "también": "同時",
        "además": "此外",
        "Además": "此外",
        "mucho": "大幅",
        "muchísimo": "極大幅",
        "dos veces": "兩次",
        "tres veces": "三次",
    }
    
    desc_zh = desc_es
    for es, zh in replacements.items():
        desc_zh = desc_zh.replace(es, zh)
    
    return desc_zh

# 讀取原始檔案
print(f"讀取檔案: {PBS_MOVES}")
with open(PBS_MOVES, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

print(f"✓ 共 {len(lines)} 行招式資料\n")

# 處理每一行
translated_lines = []
total_moves = len(lines)
success_count = 0

for i, line in enumerate(lines, 1):
    line = line.rstrip('\n')
    
    # 跳過空行
    if not line.strip():
        translated_lines.append(line)
        continue
    
    # 解析招式資料
    parts = line.split(',', 12)
    
    if len(parts) < 13:
        print(f"  ⚠ 行 {i} 格式異常，保持原樣")
        translated_lines.append(line)
        continue
    
    move_id = parts[0]
    internal_name = parts[1]
    display_name_es = parts[2]
    move_type = parts[5]
    
    # 提取描述
    desc_match = re.search(r'"([^"]*)"$', line)
    if not desc_match:
        print(f"  ⚠ 行 {i} 無法提取描述，保持原樣")
        translated_lines.append(line)
        continue
    
    description_es = desc_match.group(1)
    
    # 翻譯名稱
    name_zh = OFFICIAL_MOVES.get(display_name_es, display_name_es)
    
    # 翻譯描述
    desc_zh = translate_desc_smart(description_es, move_type)
    
    # 重建行
    parts[2] = name_zh
    line_without_desc = ','.join(parts[:12])
    new_line = f'{line_without_desc},"{desc_zh}"'
    
    translated_lines.append(new_line)
    
    if name_zh != display_name_es:
        success_count += 1
        print(f"[{i}/{total_moves}] ✓ {display_name_es} → {name_zh}")
    else:
        print(f"[{i}/{total_moves}] → {display_name_es} (保持原樣)")
    
    if i % 50 == 0:
        print(f"\n--- 已完成 {i}/{total_moves} ({i*100//total_moves}%) ---\n")

# 寫入輸出檔案（保留 BOM）
print(f"\n寫入檔案: {OUTPUT_PATH}")
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

with open(OUTPUT_PATH, 'w', encoding='utf-8-sig') as f:
    f.write('\n'.join(translated_lines))

print(f"\n✓ 翻譯完成！")
print(f"  輸出: {OUTPUT_PATH}")
print(f"  共處理 {len(translated_lines)} 行")
print(f"  成功翻譯 {success_count} 個招式名稱")
print(f"  所有描述已智能翻譯術語")
