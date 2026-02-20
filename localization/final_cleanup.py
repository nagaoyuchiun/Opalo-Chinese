# -*- coding: utf-8 -*-
import re, codecs

# 完整的描述翻譯字典（補充之前遺漏的）
desc_trans = {
    "Un fertilizante que se usa en tierra suelta. Acelera el crecimiento de las bayas, pero también seca el suelo.": "在鬆軟土壤中使用的肥料。能加快樹果生長，但也會使土壤變乾。",
    "Fertilizante para tierra suelta que ralentiza el crecimiento de las bayas y seca el suelo lentamente.": "在鬆軟土壤中使用的肥料。會減緩樹果生長，土壤也會慢慢變乾。",
    "Fertilizante para tierra suelta que retrasa la caída de las bayas maduras.": "在鬆軟土壤中使用的肥料。能讓成熟的樹果不易掉落。",
    "Fertilizante para tierra suelta que hace que broten más plantas nuevas de las plantas marchitas.": "在鬆軟土壤中使用的肥料。能讓枯萎的植物長出更多新芽。",
    "Sal pura y de sabor intenso procedente de las profund idades de la Cueva Cardumen.": "來自淺灘洞窟深處的純淨岩鹽，味道濃郁。",
    "Hermosa concha marina hallada en lo más profundo de la Cueva Cardumen. Tiene rayas azules y blancas.": "在淺灘洞窟深處發現的美麗貝殼，有著藍白相間的條紋。",
    "A veces se oyen voces en su interior.": "有時能聽到從內部傳來的聲音。",
    "Moneda de cobre ": "距今已有三千多年歷史的銅幣",
    "Moneda de plata ": "距今已有三千多年歷史的銀幣",
    "Moneda de oro ": "距今已有三千多年歷史的金幣",
    "Jarrón ": "距今已有三千多年歷史的陶罐",
    "Brazalete ": "距今已有三千多年歷史的手鐲",
    "Efigie de piedra ": "距今已有三千多年歷史的石像",
    "Corona ": "距今已有三千多年歷史的王冠",
    "El Pokémon que lo lleve flotará en el aire. Si recibe un golpe, estallará.": "讓攜帶的寶可夢浮在空中。受到攻擊時會爆炸。",
    "Lanza un destello que baja la precisión del enemigo. Debe llevarlo un Pokémon.": "發出閃光降低對手命中率。需要寶可夢攜帶。",
    "Piedra evolutiva. El Pokémon portador aumentará su Defensa y su Defensa Especial si aún puede evolucionar.": "進化奇石。如果攜帶的寶可夢仍可進化，防禦和特防將會提升。",
    "Piedra muy ligera que reduce el peso del Pokémon que la lleve.": "非常輕的石頭，能減輕攜帶寶可夢的重量。",
    "Un hilo largo y delgado de color rojo que transmite el enamoramiento del Pokémon que lo lleva a su rival.": "細長的紅線，能將攜帶寶可夢的著迷狀態傳給對手。",
    "Si el portador es alcanzado por un ataque físico, el agresor también recibe daño.": "當攜帶者受到物理攻擊時，攻擊方也會受到傷害。",
    "Si el portador es alcanzado por un ataque, saldrá del combate y será sustituido por otro Pokémon del equipo.": "攜帶者受到攻擊時，會退出戰鬥並被隊伍中的其他寶可夢替換。",
    "Una misteriosa tarjeta que permite al Pokémon que la lleve expulsar al agresor cuando este le cause daño.": "神秘的卡片，能讓攜帶的寶可夢在受到傷害時將攻擊方趕出場。",
    "En combate, esta concha desechada sirve para que un Pokémon se cambie por otro que no esté combatiendo.": "在戰鬥中，這個脫落的殼能讓寶可夢替換成未出場的隊友。",
    "Debe llevarla un Pokémon. Permite huir de combates contra Pokémon salvajes.": "需要寶可夢攜帶。能從野生寶可夢的戰鬥中逃走。",
    "Es un huevo lleno de felicidad que te hará ganar Puntos de Experiencia extra en combate. Debe llevarlo un Pokémon.": "充滿幸福的蛋，能讓攜帶的寶可夢在戰鬥中獲得額外經驗值。",
    "El Pokémon que lo lleva obtiene parte de los Puntos de Experiencia conseguidos en el combate sin participar en él.": "攜帶的寶可夢即使未參加戰鬥也能獲得一部分經驗值。",
    "Si el Pokémon que la lleva lucha en un combate, duplica las ganancias.": "攜帶的寶可夢參加戰鬥時，獲得的金錢加倍。",
    "Una campana con un tañido calmante que reconforta al Pokémon que la lleva y lo vuelve más amistoso.": "音色平和的鈴鐺，能讓攜帶的寶可夢感到安心並變得更親密。",
}

# 讀取檔案
path = "D:/Opalo V2.11/localization/translations/pbs/items.txt"
with codecs.open(path, "r", "utf-8-sig") as f:
    content = f.read()

# 應用所有翻譯
for es, zh in desc_trans.items():
    content = content.replace(es, zh)

# 移除常見殘留的西班牙語片段
cleanup_patterns = [
    (r'Sal pura y de sabor intenso procedente de las profundidades de la ([^\."]+)\.', r'來自\1深處的純淨岩鹽，味道濃郁。'),
    (r'procedente de las profundidades de la Cueva Cardumen', '來自淺灘洞窟深處'),
]

for pattern, repl in cleanup_patterns:
    content = re.sub(pattern, repl, content)

# 寫回檔案
with codecs.open(path, "w", "utf-8-sig") as f:
    f.write(content)

print("✅ 最終清理完成！")
