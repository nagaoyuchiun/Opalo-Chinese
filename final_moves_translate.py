import json
import re
from pathlib import Path

# 超級完整的寶可夢招式名稱翻譯對照表（中西文）
# 基於官方繁體中文譯名
MOVE_TRANSLATIONS = {
    "Megacuerno": "超級角擊", "Al Ataque": "攻擊指令", "Zumbido": "蟲鳴",
    "Tijera X": "十字剪", "Doble Rayo": "信號光束", "Ida y Vuelta": "急速折返",
    "Rodillo Púas": "重壓", "Picadura": "蟲咬", "Viento Plata": "銀色旋風",
    "Estoicismo": "蟲之抵抗", "Dobleataque": "雙針", "Cortefuria": "連斬",
    "Chupavidas": "吸血", "Pin Misil": "飛彈針", "A Defender": "防禦指令",
    "Auxilio": "回復指令", "Danza Aleteo": "蝶舞", "Polvo Ira": "憤怒粉",
    "Telaraña": "蜘蛛網", "Disp. Demora": "吐絲", "Ráfaga": "尾巴發光",
    "Juego Sucio": "欺詐", "Pulso Noche": "暗黑爆破", "Triturar": "咬碎",
    "Pulso Umbrío": "惡之波動", "Golpe Bajo": "突襲", "Tajo Umbrio": "暗襲要害",
    "Mordisco": "咬住", "Finta": "出奇一擊", "Alarido": "大聲咆哮",
    "Buena Baza": "以牙還牙", "Vendetta": "報仇", "Persecución": "追打",
    "Ladrón": "小偷", "Desarme": "拍落", "Paliza": "圍攻",
    "Lanzamiento": "投擲", "Castigo": "懲罰", "Brecha Negra": "暗黑洞",
    "Embargo": "查封", "Llanto Falso": "假哭", "Camelo": "吹捧",
    "Afilagarras": "磨爪", "Legado": "臨別禮物", "Maquinación": "詭計",
    "Último Lugar": "殿後", "Robo": "搶奪", "Trapicheo": "掉包",
    "Mofa": "挑釁", "Tormento": "無理取鬧", "Distorción": "時光咆哮",
    "Cometa Draco": "流星群", "Enfado": "逆鱗", "Carga Dragón": "龍之俯衝",
    "Corte Vacío": "亞空裂斬", "Pulso Dragón": "龍之波動", "Garra Dragón": "龍爪",
    "Cola Dragón": "龍尾", "Dragoaliento": "龍息", "Golpe Bis": "二連劈",
    "Ciclón": "龍捲風", "Furia Dragón": "龍之怒", "Danza Dragón": "龍之舞",
    "At. Fulgor": "閃電交擊", "Trueno": "打雷", "Placaje Eléc.": "伏特攻擊",
    "Electrocañón": "電磁炮", "Rayo Fusión": "交錯閃電", "Rayo": "十萬伏特",
    "Voltio Cruel": "瘋狂伏特", "Chispazo": "放電", "Puño Trueno": "雷電拳",
    "Voltiocambio": "伏特替換", "Chispa": "電光", "Colm. Rayo": "雷電牙",
    "Onda Voltio": "電擊波", "Electrotela": "電網", "Rayo Carga": "充電光束",
    "Impactrueno": "電擊", "Bola Voltio": "電球", "Carga": "充電",
    "Levitón": "電磁飄浮", "Onda Trueno": "電磁波", "Puño Certero": "真氣拳",
    "Pat. S. Alta": "飛膝踢", "A Bocajarro": "近身戰", "Onda Certera": "真氣彈",
    "Fuerza Bruta": "蠻力", "Tajo Cruzado": "十字劈", "Puñodinámico": "爆裂拳",
    "Machada": "臂錘", "Patada Salto": "飛踢", "Esfera Aural": "波導彈",
    "Espadasanta": "聖劍", "Sablemístico": "神秘之劍", "Gancho Alto": "衝天拳",
    "Sumisión": "地球上投", "Demolición": "劈瓦", "Puño Drenaje": "吸取拳",
    "Tiro Vital": "借力摔", "Llave Giro": "巴投", "Palmeo": "發勁",
    "Puntapié": "下踢", "Desquite": "報復", "Patada Giro": "迴旋踢",
    "Espabila": "喚醒巴掌", "Golpe Karate": "空手劈", "Ultrapuño": "音速拳",
    "Golpe Roca": "碎岩", "Llave Corsé": "山嵐摔", "Onda Vacío": "真空波",
    "Doble Patada": "二連踢", "Empujón": "猛推", "Triplepatada": "三連踢",
    "Contrataque": "雙倍奉還", "Sacrificio": "搏命", "Patada Baja": "踢倒",
    "Inversión": "起死回生", "Mov. Sísmico": "地球上投", "Corpulencia": "健美",
    "Detección": "看穿", "Anticipo": "快速防守", "V de Fuego": "V熱焰",
    "Anillo Ígneo": "爆炸烈焰", "Estallido": "噴火", "Sofoco": "過熱",
    "Llama Azul": "青焰", "Llamarada": "大字爆炎", "Envite Ígneo": "閃焰衝鋒",
    "Lluvia Ígnea": "熔岩風暴", "Ascuas": "火花", "Lanzallamas": "噴射火焰",
    "Nitrocarga": "蓄能焰襲", "Colm. Igneo": "火焰牙", "Humareda": "噴煙",
    "Rueda Fuego": "火焰輪", "Infierno": "煉獄", "Pirotecnia": "爆炸烈焰",
    "Giro Fuego": "火焰輪", "Puño Fuego": "火焰拳", "Ascua": "火花",
    "Polvo Ira": "憤怒粉", "Incinerar": "燒淨", "Humareda": "煙幕",
    "Rueda F": "火焰輪", "Garra Ígnea": "火焰拳", "Colm": "牙",
    "Vendaval Ígneo": "熱風", "Pirotecnia": "噴火", "Luz de Ruina": "破滅之光"
}

# 由於有 600+ 個招式，我們將採用混合策略：
# 1. 已知的用字典翻譯
# 2. 未知的保留西班牙文或使用音譯
# 3. 描述部分只做術語替換，不翻譯完整句子（避免錯誤）

# 術語替換表（從 glossary 提取）
TERMS = {
    "Ataque": "攻擊", "Defensa": "防禦", "Velocidad": "速度",
    "Ataque Especial": "特攻", "Defensa Especial": "特防",
    "Puntos de Salud": "HP", "Precisión": "命中率", "Evasión": "迴避率",
    "objetivo": "對手", "rival": "對手", "oponente": "對手",
    "usuario": "使用者", "Pokémon": "寶可夢", "movimiento": "招式",
    "turno": "回合", "combate": "對戰", "batalla": "戰鬥",
    "efecto": "效果", "poder": "威力", "daño": "傷害",
    "crítico": "會心一擊", "paralizar": "麻痺", "envenenar": "中毒",
    "quemar": "灼傷", "congelar": "冰凍", "dormir": "睡眠",
    "confundir": "混亂", "retroceder": "畏縮",
    # 屬性
    "BUG": "蟲", "DARK": "惡", "DRAGON": "龍", "ELECTRIC": "電",
    "FIGHTING": "格鬥", "FIRE": "火", "FLYING": "飛行", "GHOST": "幽靈",
    "GRASS": "草", "GROUND": "地面", "ICE": "冰", "NORMAL": "一般",
    "POISON": "毒", "PSYCHIC": "超能力", "ROCK": "岩石", "STEEL": "鋼",
    "WATER": "水", "FAIRY": "妖精",
    # 分類
    "Physical": "物理", "Special": "特殊", "Status": "變化"
}

def clean_and_translate_desc(text):
    """只替換已知術語，保留句子結構"""
    for es, zh in TERMS.items():
        # 使用單詞邊界進行替換
        text = re.sub(r'\b' + re.escape(es) + r'\b', zh, text, flags=re.IGNORECASE)
    return text

# 處理檔案
with open('PBS/moves.txt', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

output_lines = []
stats = {"translated": 0, "untranslated": 0}

for line in lines:
    if not line.strip():
        output_lines.append(line)
        continue
    
    parts = line.strip().split(',')
    if len(parts) < 13:
        output_lines.append(line)
        continue
    
    move_id, internal, spanish_name = parts[0], parts[1], parts[2]
    
    # 提取描述
    desc_match = re.search(r',"(.+)"$', line.strip())
    spanish_desc = desc_match.group(1) if desc_match else ""
    
    # 翻譯招式名稱
    chinese_name = MOVE_TRANSLATIONS.get(spanish_name, spanish_name)
    if chinese_name != spanish_name:
        stats["translated"] += 1
    else:
        stats["untranslated"] += 1
    
    # 清理描述（只替換術語）
    chinese_desc = clean_and_translate_desc(spanish_desc)
    
    # 重建行
    new_parts = parts[:2] + [chinese_name] + parts[3:-1]
    new_line = ','.join(new_parts) + f',"{chinese_desc}"\n'
    
    output_lines.append(new_line)

# 寫入
output_path = Path('localization/translations/pbs/moves.txt')
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, 'w', encoding='utf-8-sig') as f:
    f.writelines(output_lines)

print(f"✓ 完成翻譯！")
print(f"  已翻譯招式：{stats['translated']}")
print(f"  保留原文：{stats['untranslated']}")
print(f"  總計：{stats['translated'] + stats['untranslated']}")
print(f"  輸出：{output_path}")
