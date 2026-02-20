import json
import re
import sys

# 載入術語表
with open("D:/Opalo V2.11/localization/glossary.json", "r", encoding="utf-8") as f:
    glossary = json.load(f)

# 建立 ES -> ZH_TW 對照表
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

# 擴充翻譯規則
translation_rules = {
    # 進化石
    "Piedra Fuego": "火之石",
    "Piedras Fuego": "火之石",
    "Piedra Trueno": "雷之石",
    "Piedras Trueno": "雷之石",
    "Piedra Agua": "水之石",
    "Piedras Agua": "水之石",
    "Piedra Hoja": "葉之石",
    "Piedras Hoja": "葉之石",
    "Piedra Lunar": "月之石",
    "Piedras Lunar": "月之石",
    "Piedra Solar": "日之石",
    "Piedras Solar": "日之石",
    "Piedra Noche": "暗之石",
    "Piedras Noche": "暗之石",
    "Piedra Alba": "光之石",
    "Piedras Alba": "光之石",
    "Piedra Día": "光之石",
    "Piedras Día": "光之石",
    
    # 噴霧
    "Repelente": "除蟲噴霧",
    "Repelentes": "除蟲噴霧",
    "Superrepelente": "白銀噴霧",
    "Superrepelentes": "白銀噴霧",
    "Repelente Máximo": "黃金噴霧",
    "Repelentes Máximos": "黃金噴霧",
    
    # 笛子
    "Flauta Negra": "黑色笛子",
    "Flautas Negras": "黑色笛子",
    "Flauta Blanca": "白色笛子",
    "Flautas Blancas": "白色笛子",
    
    # 其他道具
    "Miel": "甜甜蜜",
    "Mieles": "甜甜蜜",
    "Cuerda Huida": "逃脫繩",
    "Cuerdas Huida": "逃脫繩",
    "Escama Corazón": "心之鱗片",
    "Escamas Corazón": "心之鱗片",
    
    # 碎片
    "Parte Roja": "紅色碎片",
    "Partes Rojas": "紅色碎片",
    "Parte Amarilla": "黃色碎片",
    "Partes Amarillas": "黃色碎片",
    "Parte Azul": "藍色碎片",
    "Partes Azules": "藍色碎片",
    "Parte Verde": "綠色碎片",
    "Partes Verdes": "綠色碎片",
    
    # 化石
    "Fósil Helix": "貝殼化石",
    "Fósiles Helix": "貝殼化石",
    "Fósil Domo": "甲殼化石",
    "Fósiles Domo": "甲殼化石",
    "Ámbar Viejo": "秘琥珀",
    "Ámbares Viejos": "秘琥珀",
    "Fósil Raíz": "根狀化石",
    "Fósiles Raíz": "根狀化石",
    "Fósil Garra": "爪子化石",
    "Fósiles Garra": "爪子化石",
    "Fósil Cráneo": "頭蓋化石",
    "Fósiles Cráneo": "頭蓋化石",
    "Fósil Coraza": "盾甲化石",
    "Fósiles Coraza": "盾甲化石",
    "Fósil Tapa": "蓋子化石",
    "Fósiles Tapa": "蓋子化石",
    "Fósil Pluma": "羽毛化石",
    "Fósiles Pluma": "羽毛化石",
    
    # 其他物品
    "Pluma Bella": "美麗羽毛",
    "Plumas Bellas": "美麗羽毛",
    "Mini Seta": "小蘑菇",
    "Mini Setas": "小蘑菇",
    "Seta Grande": "大蘑菇",
    "Setas Grandes": "大蘑菇",
    "Seta Aroma": "香氣蘑菇",
    "Setas Aroma": "香氣蘑菇",
    "Perla": "珍珠",
    "Perlas": "珍珠",
    "Perla Grande": "大珍珠",
    "Perlas Grandes": "大珍珠",
    "Sarta Perlas": "珍珠串",
    "Sartas Perlas": "珍珠串",
    "Polvoestelar": "星星沙子",
    "Polvoestelares": "星星沙子",
    "Trozo Estrella": "星星碎片",
    "Trozos Estrella": "星星碎片",
    "Fragmento Cometa": "彗星碎片",
    "Fragmentos Cometa": "彗星碎片",
    "Pepita": "金珠",
    "Pepitas": "金珠",
    "Maxipepita": "大金珠",
    "Maxipepitas": "大金珠",
    "Cola Slowpoke": "呆呆獸尾巴",
    "Colas Slowpoke": "呆呆獸尾巴",
    
    # Bonguri
    "Bonguri Roja": "紅色球果",
    "Bonguris Roja": "紅色球果",
    "Bonguri Amarilla": "黃色球果",
    "Bonguris Amarilla": "黃色球果",
    "Bonguri Azul": "藍色球果",
    "Bonguris Azul": "藍色球果",
    "Bonguri Verde": "綠色球果",
    "Bonguris Verde": "綠色球果",
    "Bonguri Rosa": "粉色球果",
    "Bonguris Rosa": "粉色球果",
    "Bonguri Blanca": "白色球果",
    "Bonguris Blanca": "白色球果",
    "Bonguri Negra": "黑色球果",
    "Bonguris Negra": "黑色球果",
}

translation_rules.update(glossary_map)

# 文字替換函數
def translate_text(text):
    if not text:
        return text
    
    # 完全匹配優先
    if text in translation_rules:
        return translation_rules[text]
    
    # 部分匹配（最長優先）
    result = text
    sorted_terms = sorted(translation_rules.keys(), key=len, reverse=True)
    for es_term in sorted_terms:
        if es_term in result:
            result = result.replace(es_term, translation_rules[es_term])
    
    # 通用替換
    replacements = {
        "Pokémon": "寶可夢",
        "pasos": "步",
        "débiles": "弱小的",
        "salvajes": "野生的",
        "salvaje": "野生",
        "débil": "弱小",
        "un recorrido de": "在",
        "Repele": "驅除",
        "especies": "種類",
        "determinadas": "特定",
        "Curiosa piedra que hace evolucionar a": "能讓特定寶可夢進化的神奇石頭。",
        "Una piedra peculiar que hace evolucionar a algunos": "能讓特定寶可夢進化的神奇石頭。",
        "Es amarilla con una marca naranja": "呈黃色帶有橙色紋路",
        "Tiene dibujado un rayo": "上面有閃電圖案",
        "Es de color azul, como el agua": "呈水藍色",
        "Tiene dibujada una hoja": "上面有葉子圖案",
        "Es negra como el azabache": "漆黑如墨",
        "Es roja como el núcleo del sol": "如太陽核心般赤紅",
        "Es oscura como la noche": "漆黑如夜",
        "Brilla como un lucero": "像晨星般閃耀",
        "Tiene un brillo espectacular": "綻放璀璨光芒",
        "cuya melodía": "其旋律能",
        "ayuda a reducir las probabilidades de encontrarse con": "降低遇見",
        "ayuda a aumentar las probabilidades de encontrarse con": "提高遇見",
        "的機率": "的機率",
        "de cristal negro": "黑色玻璃",
        "de cristal blanco": "白色玻璃",
        "Su delicioso aroma atrae a": "其香甜的氣味能吸引",
        "si se usa en zonas de": "在",
        "hierba alta": "草叢",
        "cuevas": "洞窟",
        "árboles especiales": "特殊樹木",
        "中使用時": "中使用時",
        "Cuerda larga y resistente que sirve para huir de": "能從",
        "y sitios cerrados en general": "等封閉場所脫出的長繩",
        "Un pequeño fragmento": "小碎片",
        "Parece formar parte de algún tipo de herramienta antigua": "似乎是某種古代道具的一部分",
        "Fósil de un": "某種古代",
        "ancestral": "的",
        "que vivió en el fondo del mar": "生活在海底",
        "prehistórico terrestre": "史前陸地",
        "que surcó los cielos": "翱翔天際",
        "Parece ser un fragmento de": "似乎是",
        "Parece ser parte de": "似乎是",
        "concha marina": "貝殼",
        "concha": "甲殼",
        "una raíz": "根部",
        "una garra": "爪子",
        "una cabeza": "頭部",
        "del cuello": "頸部",
        "un ala suya": "翅膀",
        "的碎片": "的化石碎片",
        "Fragmento de ámbar que contiene información genética de un": "內含古代",
        "Es de color amarillo": "呈琥珀色",
        "遺傳基因的琥珀": "遺傳基因的琥珀",
        "Pluma normal y corriente": "普通的羽毛",
        "Muy bonita, pero no sirve para nada": "很漂亮但沒有用處",
        "Seta": "蘑菇",
        "pequeña y poco común": "小而稀有的",
        "grande y poco común": "大而稀有的",
        "bastante popular": "深受",
        "muy popular": "深受",
        "entre determinados grupos de gourmets": "美食家的喜愛",
        "Extraña seta que desprende un agradable aroma": "散發宜人香氣的稀有蘑菇",
        "Muy apreciada por los gourmets": "深受美食家珍視",
        "Brillante perla": "閃亮的珍珠",
        "plateada": "銀白色",
        "de tamaño más bien pequeño": "尺寸較小",
        "que no alcanza mucho precio en las tiendas": "商店售價不高",
        "de gran tamaño": "尺寸很大",
        "que puede venderse a buen precio en las tiendas": "商店售價高",
        "Muy valoradas por los coleccionistas": "深受收藏家喜愛",
        "Bonita arena": "美麗的沙",
        "roja": "紅色",
        "de tacto sedoso": "觸感絲滑",
        "que alcanza un alto precio en las tiendas": "商店售價高",
        "Fragmento de una bonita gema": "美麗寶石的碎片",
        "que puede venderse muy caro en las tiendas": "商店售價很高",
        "Fragmento de un cometa caído al suelo al atravesar la atmósfera": "彗星穿越大氣層墜落地面時的碎片",
        "Pepita de oro puro que desprende un brillo espectacular": "閃耀璀璨光芒的純金塊",
        "Puede venderse muy cara en las tiendas": "商店售價很高",
        "grande": "大",
        "Bella escama con forma de corazón": "心形的美麗鱗片",
        "que brilla con los colores del arco iris": "綻放彩虹般的光澤",
        "Es muy poco común": "非常稀有",
        "Cola de origen desconocido y muy sabrosa": "來源不明但美味的尾巴",
        "Se vende muy cara": "售價很高",
    }
    
    for es, zh in replacements.items():
        result = result.replace(es, zh)
    
    return result

# 讀取原檔案（保留 BOM）
input_path = "D:/Opalo V2.11/localization/translations/pbs/items.txt"
with open(input_path, "r", encoding="utf-8-sig") as f:
    lines = f.readlines()

print(f"讀取 {len(lines)} 行資料")

# 翻譯並重組
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
