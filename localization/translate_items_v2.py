import json
import re

# 載入術語表
with open("D:/Opalo V2.11/localization/glossary.json", "r", encoding="utf-8") as f:
    glossary = json.load(f)

# 建立基礎術語對照表
glossary_map = {}
for category_key, category in glossary["categories"].items():
    if "terms" in category:
        for term in category["terms"]:
            if isinstance(term, dict) and "es" in term and "zh_TW" in term:
                glossary_map[term["es"]] = term["zh_TW"]
    if "subcategories" in category:
        for subcat_key, subcat in category["subcategories"].items():
            if "terms" in subcat:
                for term in subcat["terms"]:
                    if isinstance(term, dict) and "es" in term and "zh_TW" in term:
                        glossary_map[term["es"]] = term["zh_TW"]

print(f"已載入 {len(glossary_map)} 個術語對照")

# 建立完整替換表（處理完整描述）
desc_templates = {
    r"Repele Pokémon salvajes débiles en un recorrido de (\d+) pasos\.": r"讓弱小的野生寶可夢不易出現，效果可持續\1步。",
    r"Flauta de cristal negro cuya melodía ayuda a reducir las probabilidades de encontrarse con Pokémon salvajes\.": "黑色玻璃製笛子。吹奏的旋律能降低遇見野生寶可夢的機率。",
    r"Flauta de cristal blanco cuya melodía ayuda a aumentar las probabilidades de encontrarse con Pokémon salvajes\.": "白色玻璃製笛子。吹奏的旋律能提高遇見野生寶可夢的機率。",
    r"Su delicioso aroma atrae a Pokémon salvajes si se usa en zonas de hierba alta, cuevas o árboles especiales\.": "散發香甜氣味，能在草叢、洞窟或特殊樹木中吸引野生寶可夢。",
    r"Cuerda larga y resistente que sirve para huir de cuevas y sitios cerrados en general\.": "能從洞窟等封閉場所逃脫的堅韌長繩。",
    r"Un pequeño fragmento (rojo|amarillo|azul|verde)\. Parece formar parte de algún tipo de herramienta antigua\.": lambda m: f"{{'rojo':'紅色','amarillo':'黃色','azul':'藍色','verde':'綠色'}}[m.group(1)]的小碎片。似乎是某種古代道具的一部分。",
    r"Curiosa piedra que hace evolucionar a determinadas especies de Pokémon\. Es amarilla con una marca naranja\.": "能讓特定寶可夢進化的神奇石頭。呈黃色並帶有橙色紋路。",
    r"Curiosa piedra que hace evolucionar a determinadas especies de Pokémon\. Tiene dibujado un rayo\.": "能讓特定寶可夢進化的神奇石頭。上面刻有閃電圖案。",
    r"Curiosa piedra que hace evolucionar a determinadas especies de Pokémon\. Es de color azul, como el agua\.": "能讓特定寶可夢進化的神奇石頭。呈現如水般的藍色。",
    r"Curiosa piedra que hace evolucionar a determinadas especies de Pokémon\. Tiene dibujada una hoja\.": "能讓特定寶可夢進化的神奇石頭。上面刻有葉子圖案。",
    r"Curiosa piedra que hace evolucionar a determinadas especies de Pokémon\. Es negra como el azabache\.": "能讓特定寶可夢進化的神奇石頭。呈現漆黑如墨的顏色。",
    r"Curiosa piedra que hace evolucionar a determinadas especies de Pokémon\. Es roja como el núcleo del sol\.": "能讓特定寶可夢進化的神奇石頭。呈現如太陽核心般的赤紅。",
    r"Una piedra peculiar que hace evolucionar a algunos Pokémon\. Es oscura como la noche\.": "能讓特定寶可夢進化的神奇石頭。漆黑如夜。",
    r"Una piedra peculiar que hace evolucionar a algunos Pokémon\. Brilla como un lucero\.": "能讓特定寶可夢進化的神奇石頭。如晨星般閃耀。",
    r"Una piedra peculiar que hace evolucionar a algunos Pokémon\. Tiene un brillo espectacular\.": "能讓特定寶可夢進化的神奇石頭。綻放璀璨光芒。",
    r"Bonguri de color (rojo|amarillo|azul|verde|rosa|blanco|negro) y aroma (.+)\.": lambda m: f"{{'rojo':'紅色','amarillo':'黃色','azul':'藍色','verde':'綠色','rosa':'粉色','blanco':'白色','negro':'黑色'}[m.group(1)]}的球果，{{'muy penetrante':'氣味強烈','refrescante':'氣味清爽','tierno':'氣味柔和','peculiar que recuerda al café tostado':'特殊氣味宛如烘焙咖啡','dulce':'氣味甜美','indescriptible':'氣味難以形容'}[m.group(2).rstrip('.')]}。",
    r"Fósil de un Pokémon ancestral que vivió en el fondo del mar\. Parece ser un fragmento de concha marina\.": "生活在海底的古代寶可夢化石，似乎是貝殼的一部分。",
    r"Fósil de un Pokémon ancestral que vivió en el fondo del mar\. Parece ser un fragmento de concha\.": "生活在海底的古代寶可夢化石，似乎是甲殼的一部分。",
    r"Fragmento de ámbar que contiene información genética de un Pokémon ancestral\. Es de color amarillo\.": "內含古代寶可夢遺傳基因的琥珀碎片，呈黃色。",
    r"Fósil de un Pokémon ancestral que vivió en el fondo del mar\. Parece ser parte de una raíz\.": "生活在海底的古代寶可夢化石，似乎是根部的一部分。",
    r"Fósil de un Pokémon ancestral que vivió en el fondo del mar\. Parece ser parte de una garra\.": "生活在海底的古代寶可夢化石，似乎是爪子的一部分。",
    r"Fósil de un Pokémon prehistórico terrestre\. Parece ser parte de una cabeza\.": "生活在陸地的史前寶可夢化石，似乎是頭部的一部分。",
    r"Fósil de un Pokémon prehistórico terrestre\. Parece ser un fragmento del cuello\.": "生活在陸地的史前寶可夢化石，似乎是頸部的碎片。",
    r"Fósil de un Pokémon ancestral que surcó los cielos\. Parece ser parte de un ala suya\.": "翱翔天際的古代寶可夢化石，似乎是翅膀的一部分。",
    r"Pluma normal y corriente\. Muy bonita, pero no sirve para nada\.": "普通的羽毛。雖然很漂亮，但沒什麼用處。",
    r"Seta pequeña y poco común bastante popular entre determinados grupos de gourmets\.": "小而稀有的蘑菇，深受美食家喜愛。",
    r"Seta grande y poco común muy popular entre determinados grupos de gourmets\.": "大而稀有的蘑菇，深受美食家喜愛。",
    r"Extraña seta que desprende un agradable aroma\. Muy apreciada por los gourmets\.": "散發宜人香氣的稀有蘑菇，深受美食家珍視。",
    r"Brillante perla plateada de tamaño más bien pequeño que no alcanza mucho precio en las tiendas\.": "銀白色的小珍珠，價格不高。",
    r"Brillante perla plateada de gran tamaño que puede venderse a buen precio en las tiendas\.": "銀白色的大珍珠，能賣不錯的價錢。",
    r"Brillantes perlas plateadas de gran tamaño\. Muy valoradas por los coleccionistas\.": "銀白色的大珍珠串，深受收藏家喜愛。",
    r"Bonita arena roja de tacto sedoso que alcanza un alto precio en las tiendas\.": "觸感絲滑的美麗紅沙，能賣出高價。",
    r"Fragmento de una bonita gema roja que puede venderse muy caro en las tiendas\.": "美麗的紅色寶石碎片，能賣出高價。",
    r"Fragmento de un cometa caído al suelo al atravesar la atmósfera\. Muy valorado por los coleccionistas\.": "彗星穿越大氣層墜落的碎片，深受收藏家喜愛。",
    r"Pepita de oro puro que desprende un brillo espectacular\. Puede venderse muy cara en las tiendas\.": "閃耀璀璨光芒的純金塊，能賣出高價。",
    r"Pepita grande de oro puro que desprende un brillo espectacular\. Muy valorada por los coleccionistas\.": "閃耀璀璨光芒的大金塊，深受收藏家喜愛。",
    r"Bella escama con forma de corazón que brilla con los colores del arco iris\. Es muy poco común\.": "心形的美麗鱗片，綻放彩虹般的光芒。非常稀有。",
    r"Cola de origen desconocido y muy sabrosa\. Se vende muy cara\.": "來源不明但味道鮮美的尾巴，售價很高。",
}

# 通用片段替換
word_replacements = {
    "Pokémon": "寶可夢",
    "salvajes": "野生",
    "débiles": "弱小的",
    "pasos": "步",
    "débil": "弱小",
    "salvaje": "野生",
    "especies": "種類",
    "determinadas": "特定",
    "algunos": "某些",
    "rojo": "紅色",
    "amarillo": "黃色",
    "azul": "藍色",
    "verde": "綠色",
    "negro": "黑色",
    "blanco": "白色",
    "rosa": "粉色",
}

def translate_text(text):
    if not text:
        return text
    
    # 1. 嘗試完整匹配模板
    for pattern, replacement in desc_templates.items():
        match = re.search(pattern, text)
        if match:
            if callable(replacement):
                return replacement(match)
            elif '\\1' in replacement:
                return re.sub(pattern, replacement, text)
            else:
                return replacement
    
    # 2. 套用術語表
    result = text
    sorted_terms = sorted(glossary_map.keys(), key=len, reverse=True)
    for es_term in sorted_terms:
        if es_term in result:
            result = result.replace(es_term, glossary_map[es_term])
    
    # 3. 通用詞彙替換
    for es, zh in word_replacements.items():
        result = result.replace(es, zh)
    
    return result

# 讀取並翻譯
input_path = "D:/Opalo V2.11/localization/translations/pbs/items.txt"
with open(input_path, "r", encoding="utf-8-sig") as f:
    lines = f.readlines()

print(f"讀取 {len(lines)} 行資料")

output_lines = []
success_count = 0

for line_num, line in enumerate(lines, 1):
    parts = line.strip().split(',')
    if len(parts) >= 10:
        id_num = parts[0]
        internal = parts[1]
        name = parts[2]
        plural = parts[3]
        pocket = parts[4]
        price = parts[5]
        desc = parts[6]
        rest = ','.join(parts[7:])
        
        # 翻譯
        name_zh = translate_text(name)
        plural_zh = translate_text(plural)
        desc_zh = translate_text(desc)
        
        # 重組
        new_line = f'{id_num},{internal},{name_zh},{plural_zh},{pocket},{price},{desc_zh},{rest}\n'
        output_lines.append(new_line)
        success_count += 1
        
        if line_num % 50 == 0:
            print(f"  處理進度: {line_num}/{len(lines)}")
    else:
        output_lines.append(line)

# 寫回檔案（保留 BOM）
with open(input_path, "w", encoding="utf-8-sig") as f:
    f.writelines(output_lines)

print(f"\n✅ 翻譯完成！")
print(f"   總計翻譯 {success_count} 個道具")
print(f"   檔案已更新: {input_path}")
