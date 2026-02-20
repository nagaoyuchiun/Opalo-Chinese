import json
import re
import time
from pathlib import Path

# 載入詞彙表
with open('localization/glossary.json', 'r', encoding='utf-8') as f:
    glossary = json.load(f)

# 建立西班牙文到中文的對照字典
term_map = {}
for category in glossary['categories'].values():
    if 'terms' in category:
        for term in category['terms']:
            term_map[term['es']] = term['zh_TW']
    if 'subcategories' in category:
        for subcat in category['subcategories'].values():
            if 'terms' in subcat:
                for term in subcat['terms']:
                    term_map[term['es']] = term['zh_TW']

# 建立專用的術語替換函數
def apply_glossary(text):
    """使用詞彙表替換文本中的術語"""
    # 按長度排序，優先替換長詞
    sorted_terms = sorted(term_map.items(), key=lambda x: len(x[0]), reverse=True)
    for es_term, zh_term in sorted_terms:
        # 使用單詞邊界匹配，避免部分匹配
        pattern = r'\b' + re.escape(es_term) + r'\b'
        text = re.sub(pattern, zh_term, text, flags=re.IGNORECASE)
    return text

# 西班牙文到中文的手動翻譯字典 (針對招式名稱)
move_name_translations = {
    # 已知招式（使用官方譯名）
    "Megacuerno": "超級角擊",
    "Al Ataque": "攻擊指令",
    "Zumbido": "蟲鳴",
    "Tijera X": "十字剪",
    "Doble Rayo": "信號光束",
    "Ida y Vuelta": "急速折返",
    "Rodillo Púas": "重壓",
    "Picadura": "蟲咬",
    "Viento Plata": "銀色旋風",
    "Estoicismo": "蟲之抵抗",
    "Dobleataque": "雙針",
    "Cortefuria": "連斬",
    "Chupavidas": "吸血",
    "Pin Misil": "飛彈針",
    "A Defender": "防禦指令",
    "Auxilio": "回復指令",
    "Danza Aleteo": "蝶舞",
    "Polvo Ira": "憤怒粉",
    "Telaraña": "蜘蛛網",
    "Disp. Demora": "吐絲",
    "Ráfaga": "尾巴發光",
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
    "Persecución": "追打",
    "Ladrón": "小偷",
    "Desarme": "拍落",
    "Paliza": "圍攻",
    "Lanzamiento": "投擲",
    "Castigo": "懲罰",
    "Brecha Negra": "暗黑洞",
    "Embargo": "查封",
    "Llanto Falso": "假哭",
    "Camelo": "吹捧",
    "Afilagarras": "磨爪",
    "Legado": "臨別禮物",
    "Maquinación": "詭計",
    "Último Lugar": "殿後",
    "Robo": "搶奪",
    "Trapicheo": "掉包",
    "Mofa": "挑釁",
    "Tormento": "無理取鬧",
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
    "At. Fulgor": "閃電交擊",
    "Trueno": "打雷",
    "Placaje Eléc.": "伏特攻擊",
    "Electrocañón": "電磁炮",
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
    "Puño Certero": "真氣拳",
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
    "Gancho Alto": "衝天拳",
    "Sumisión": "地球上投",
    "Demolición": "劈瓦",
    "Puño Drenaje": "吸取拳",
    "Tiro Vital": "借力摔",
}

# 讀取原始檔案
with open('PBS/moves.txt', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

print(f'總共 {len(lines)} 行')

# 批量處理翻譯
translated_lines = []
for i, line in enumerate(lines, 1):
    if not line.strip():
        translated_lines.append(line)
        continue
    
    # 解析格式：ID,INTERNAL,Name,Code,Power,Type,Category,Accuracy,PP,Effect,Target,Priority,Flags,Description
    parts = line.strip().split(',')
    if len(parts) < 13:
        translated_lines.append(line)
        continue
    
    # 提取招式名稱和描述
    move_id = parts[0]
    internal_name = parts[1]
    spanish_name = parts[2]
    # 描述在最後一個引號中
    desc_match = re.search(r',"(.+)"$', line.strip())
    spanish_desc = desc_match.group(1) if desc_match else ""
    
    # 翻譯招式名稱
    if spanish_name in move_name_translations:
        chinese_name = move_name_translations[spanish_name]
    else:
        # 使用詞彙表進行簡單替換
        chinese_name = apply_glossary(spanish_name)
        if chinese_name == spanish_name:  # 如果沒有變化，保留西班牙文
            chinese_name = spanish_name
            print(f"警告：第{i}行 招式名稱 '{spanish_name}' 未找到翻譯")
    
    # 翻譯描述（應用詞彙表）
    chinese_desc = apply_glossary(spanish_desc)
    
    # 重建行（保留所有原始參數）
    # 格式：ID,INTERNAL,Name_ZH,Code,Power,Type,Category,Accuracy,PP,Effect,Target,Priority,Flags,"Description_ZH"
    new_line_parts = parts[:2] + [chinese_name] + parts[3:-1]
    new_line = ','.join(new_line_parts) + f',"{chinese_desc}"\n'
    
    translated_lines.append(new_line)
    
    if i % 50 == 0:
        print(f'處理進度：{i}/{len(lines)} ({i/len(lines)*100:.1f}%)')

# 寫入檔案（保留 UTF-8 BOM）
output_path = Path('localization/translations/pbs/moves.txt')
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, 'w', encoding='utf-8-sig') as f:
    f.writelines(translated_lines)

print(f'\n完成！翻譯檔案已儲存至：{output_path}')
print(f'總共翻譯 {len(translated_lines)} 行')
