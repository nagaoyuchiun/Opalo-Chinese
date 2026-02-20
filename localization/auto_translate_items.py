# -*- coding: utf-8 -*-
import re
import codecs

# 完整翻譯字典
item_names = {
    # 化石
    "Fósil Raíz": "根狀化石", "Fósil Garra": "爪子化石", "Fósil Cráneo": "頭蓋化石",
    "Fósil Coraza": "盾甲化石", "Fósil Tapa": "蓋子化石", "Fósil Pluma": "羽毛化石",
    
    # 其他物品  
    "Pluma Bella": "美麗羽毛", "Mini Seta": "小蘑菇", "Seta Grande": "大蘑菇",
    "Seta Aroma": "香氣蘑菇", "Perla": "珍珠", "Perla Grande": "大珍珠",
    "Sarta Perlas": "珍珠串", "Polvoestelar": "星星沙子", "Trozo Estrella": "星星碎片",
    "Fragmento Cometa": "彗星碎片", "Pepita": "金珠", "Maxipepita": "大金珠",
    "Escama Corazón": "心之鱗片", "Cola Slowpoke": "呆呆獸尾巴",
    "Hueso Raro": "珍貴骨頭", "Real Cobre": "銅幣", "Real Plata": "銀幣",
    "Real Oro": "金幣", "Ánfora": "古代壺", "Brazal": "手環",
    "Efigie Antigua": "古代雕像", "Corona Antigua": "古代王冠",
    
    # 肥料/培土
    "Abono Rápido": "速效肥", "Abono Lento": "緩效肥",
    "Abono Fijador": "固定肥", "Abono Brote": "發芽肥",
    
    # 特殊道具
    "Sal Cardumen": "淺灘之鹽", "Concha Cardumen": "淺灘之貝",
    "Piedra Espíritu": "靈界之布", "Globo Helio": "氣球",
    "Polvo Brillo": "光粉", "Mineral Evolutivo": "進化奇石",
    "Piedra Pómez": "輕石", "Lazo Destino": "紅線",
    "Casco Dentado": "凸凸頭盔", "Botón Escape": "逃脫按鈕",
    "Tarjeta Roja": "紅牌", "Muda Concha": "脫殼", "Bola Humo": "煙霧球",
    "Huevo Suerte": "幸運蛋", "Repartir Exp": "學習裝置",
    "Moneda Amuleto": "護符金幣", "Cascabel Alivio": "安撫之鈴",
    "Amuleto": "除魔小判", "Cinta Elección": "講究頭帶",
    "Gafas Elección": "講究眼鏡", "Pañuelo Elección": "講究圍巾",
    "Roca Calor": "炎熱岩石", "Roca Lluvia": "潮濕岩石",
    "Roca Suave": "沙沙岩石", "Roca Helada": "冰冷岩石",
    "Refleluz": "光之粘土", "Garra Garfio": "緊纏鉤爪",
    "Banda Atadura": "緊纏頭帶", "Raíz Grande": "大根莖",
    "Lodo Negro": "黑色淤泥", "Restos": "吃剩的東西",
    "Cascabel Concha": "貝殼之鈴", "Hierba Mental": "心靈香草",
    "Hierba Blanca": "白色香草", "Hierba Única": "強力香草",
    "Tubérculo": "球根", "Pila": "電池", "Vidasfera": "生命玉",
}

# 複數形式通常相同
item_plurals = {k: v for k, v in item_names.items()}
item_plurals.update({
    "Partes Rojas": "紅色碎片", "Partes Amarillas": "黃色碎片",
    "Partes Azules": "藍色碎片", "Partes Verdes": "綠色碎片",
    "Piedras Fuego": "火之石", "Piedras Trueno": "雷之石",
    "Piedras Agua": "水之石", "Piedras Hoja": "葉之石",
    "Piedras Lunar": "月之石", "Piedras Solar": "日之石",
    "Piedras Noche": "暗之石", "Piedras Alba": "光之石",
    "Bonguris Roja": "紅色球果", "Bonguris Amarilla": "黃色球果",
    "Bonguris Azul": "藍色球果", "Bonguris Verde": "綠色球果",
    "Bonguris Rosa": "粉色球果", "Bonguris Blanca": "白色球果",
    "Bonguris Negra": "黑色球果",
    "Fósiles Helix": "貝殼化石", "Fósiles Domo": "甲殼化石",
    "Ámbares Viejos": "秘琥珀", "Fósiles Raíz": "根狀化石",
    "Fósiles Garra": "爪子化石", "Fósiles Cráneo": "頭蓋化石",
    "Fósiles Coraza": "盾甲化石", "Fósiles Tapa": "蓋子化石",
    "Fósiles Pluma": "羽毛化石",
    "Plumas Bellas": "美麗羽毛", "Mini Setas": "小蘑菇",
    "Setas Grandes": "大蘑菇", "Setas Aroma": "香氣蘑菇",
    "Perlas": "珍珠", "Perlas Grandes": "大珍珠",
    "Sartas Perlas": "珍珠串", "Polvoestelares": "星星沙子",
    "Trozos Estrella": "星星碎片", "Fragmentos Cometa": "彗星碎片",
    "Pepitas": "金珠", "Maxipepitas": "大金珠",
    "Escamas Corazón": "心之鱗片", "Colas Slowpoke": "呆呆獸尾巴",
    "Huesos Raros": "珍貴骨頭", "Reales Cobre": "銅幣",
    "Reales Plata": "銀幣", "Reales Oro": "金幣",
    "Ánforas": "古代壺", "Brazales": "手環",
    "Efigies Antiguas": "古代雕像", "Coronas Antiguas": "古代王冠",
    "Abonos Rápidos": "速效肥", "Abonos Lentos": "緩效肥",
    "Abonos Fijadores": "固定肥", "Abonos Brotes": "發芽肥",
    "Sales Cardumen": "淺灘之鹽", "Conchas Cardumen": "淺灘之貝",
    "Piedras Espíritu": "靈界之布", "Globos Helio": "氣球",
    "Polvos Brillo": "光粉", "Minerales Evolutivos": "進化奇石",
    "Piedras Pómez": "輕石", "Lazos Destino": "紅線",
    "Cascos Dentados": "凸凸頭盔", "Botones Escape": "逃脫按鈕",
    "Tarjetas Rojas": "紅牌", "Muda Conchas": "脫殼",
    "Bolas Humo": "煙霧球", "Huevos Suerte": "幸運蛋",
    "Cascabeles Alivio": "安撫之鈴", "Cintas Elección": "講究頭帶",
    "Pañuelos Elección": "講究圍巾", "Rocas Calor": "炎熱岩石",
    "Rocas Lluvia": "潮濕岩石", "Rocas Suave": "沙沙岩石",
    "Rocas Helada": "冰冷岩石", "Refleluces": "光之粘土",
    "Garras Garfio": "緊纏鉤爪", "Bandas Atadura": "緊纏頭帶",
    "Raíces Grandes": "大根莖", "Lodos Negros": "黑色淤泥",
    "Cascabeles Concha": "貝殼之鈴", "Hierbas Mentales": "心靈香草",
    "Hierbas Blancas": "白色香草", "Hierbas Únicas": "強力香草",
    "Tubérculos": "球根", "Pilas": "電池",
})

# 描述翻譯模板（簡化版）
def translate_desc(desc):
    desc = re.sub(r"Fósil de un Pokémon ancestral que viv(ió|e) en el fondo del mar\. Parece ser (un fragmento|parte) de (.+)\.", 
                  lambda m: f"生活在海底的古代寶可夢化石。似乎是{{'concha marina':'貝殼','concha':'甲殼','una raíz':'根部','una garra':'爪子'}}[m.group(3)]的一部分。" if m.group(3) in ['concha marina','concha','una raíz','una garra'] else desc, desc)
    desc = re.sub(r"Fósil de un Pokémon prehistórico terrestre\. Parece ser (un fragmento|parte) de (.+)\.",
                  lambda m: f"生活在陸地的史前寶可夢化石。似乎是{{'una cabeza':'頭部','l cuello':'頸部',' del cuello':'頸部'}}[m.group(2)]的一部分。" if m.group(2) in ['una cabeza','l cuello',' del cuello'] else desc, desc)
    desc = re.sub(r"Fósil de un Pokémon ancestral que surcó los cielos\. Parece ser parte de un ala suya\.",
                  "翱翔天際的古代寶可夢化石。似乎是翅膀的一部分。", desc)
    desc = re.sub(r"Fragmento de ámbar que contiene información genética de un Pokémon ancestral\. Es de color amarillo\.",
                  "內含古代寶可夢遺傳基因的琥珀碎片，呈黃色。", desc)
    desc = re.sub(r"Pluma normal y corriente\. Muy bonita, pero no sirve para nada\.",
                  "普通的羽毛。雖然很漂亮，但沒什麼用處。", desc)
    desc = re.sub(r"Seta pequeña y poco común bastante popular entre determinados grupos de gourmets\.",
                  "小而稀有的蘑菇，深受美食家喜愛。", desc)
    desc = re.sub(r"Seta grande y poco común muy popular entre determinados grupos de gourmets\.",
                  "大而稀有的蘑菇，深受美食家喜愛。", desc)
    desc = re.sub(r"Extraña seta que desprende un agradable aroma\. Muy apreciada por los gourmets\.",
                  "散發宜人香氣的稀有蘑菇，深受美食家珍視。", desc)
    desc = re.sub(r"Brillante perla plateada de tamaño más bien pequeño que no alcanza mucho precio en las tiendas\.",
                  "銀白色的小珍珠，價格不高。", desc)
    desc = re.sub(r"Brillante perla plateada de gran tamaño que puede venderse a buen precio en las tiendas\.",
                  "銀白色的大珍珠，能賣不錯的價錢。", desc)
    desc = re.sub(r"Brillantes perlas plateadas de gran tamaño\. Muy valoradas por los coleccionistas\.",
                  "銀白色的大珍珠串，深受收藏家喜愛。", desc)
    desc = re.sub(r"Bonita arena roja de tacto sedoso que alcanza un alto precio en las tiendas\.",
                  "觸感絲滑的美麗紅沙，能賣出高價。", desc)
    desc = re.sub(r"Fragmento de una bonita gema roja que puede venderse muy caro en las tiendas\.",
                  "美麗的紅色寶石碎片，能賣出高價。", desc)
    desc = re.sub(r"Fragmento de un cometa caído al suelo al atravesar la atmósfera\. Muy valorado por los coleccionistas\.",
                  "彗星穿越大氣層墜落的碎片，深受收藏家喜愛。", desc)
    desc = re.sub(r"Pepita de oro puro que desprende un brillo espectacular\. Puede venderse muy cara en las tiendas\.",
                  "閃耀璀璨光芒的純金塊，能賣出高價。", desc)
    desc = re.sub(r"Pepita grande de oro puro que desprende un brillo espectacular\. Muy valorada por los coleccionistas\.",
                  "閃耀璀璨光芒的大金塊，深受收藏家喜愛。", desc)
    desc = re.sub(r"Bella escama con forma de corazón que brilla con los colores del arco iris\. Es muy poco común\.",
                  "心形的美麗鱗片，綻放彩虹般的光澤。非常稀有。", desc)
    desc = re.sub(r"Cola de origen desconocido y muy sabrosa\. Se vende muy cara\.",
                  "來源不明但味道鮮美的尾巴，售價很高。", desc)
    
    # 通用替換
    replacements = [
        ("Pokémon", "寶可夢"),
        ("salvajes", "野生"),
        ("salvaje", "野生"),
        (r"de más de tres mil años de antigüedad\. Muy valorad[ao] por los coleccionistas\.", "距今已有三千多年歷史，深受收藏家喜愛。"),
        (r"Un hueso de gran valor arqueológico que puede alcanzar un alto precio en las tiendas\.", "具有極高考古價值的骨頭，能賣出高價。"),
    ]
    for es, zh in replacements:
        desc = re.sub(es, zh, desc)
    
    return desc

# 主程式
input_path = "D:/Opalo V2.11/localization/translations/pbs/items.txt"
with codecs.open(input_path, "r", "utf-8-sig") as f:
    lines = f.readlines()

output = []
for line in lines:
    match = re.match(r'^(\d+),([^,]+),([^,]+),([^,]+),([^,]+),([^,]+),"([^"]+)",(.+)$', line.strip())
    if match:
        id_num, internal, name_es, plural_es, pocket, price, desc_es, rest = match.groups()
        
        name_zh = item_names.get(name_es, name_es)
        plural_zh = item_plurals.get(plural_es, plural_es if plural_es == name_zh else plural_es)
        desc_zh = translate_desc(desc_es)
        
        output.append(f'{id_num},{internal},{name_zh},{plural_zh},{pocket},{price},"{desc_zh}",{rest}\n')
    elif line.strip():
        output.append(line)

with codecs.open(input_path, "w", "utf-8-sig") as f:
    f.writelines(output)

print(f"✅ 翻譯完成！處理了 {len(output)} 行")
