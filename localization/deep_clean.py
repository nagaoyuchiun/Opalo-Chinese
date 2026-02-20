# -*- coding: utf-8 -*-
import re, codecs

path = "D:/Opalo V2.11\localization\translations\pbs\items.txt"
with codecs.open(path, "r", "utf-8-sig") as f:
    lines = f.readlines()

# 手工翻譯剩餘的常見句型
translations = {
    "El Pokémon que lo lleve flotará en el aire. Si recibe un golpe, estallará.": "讓攜帶的寶可夢浮在空中。受到攻擊時會爆炸。",
    "Lanza un destello que baja la precisión del enemigo. Debe llevarlo un Pokémon.": "發出閃光降低對手命中率。需要寶可夢攜帶。",
    "Piedra evolutiva. El Pokémon portador aumentará su Defensa y su Defensa Especial si aún puede evolucionar.": "進化奇石。如果攜帶的寶可夢仍可進化，防禦和特防將會提升。",
    "Piedra muy ligera que reduce el peso del Pokémon que la lleve.": "非常輕的石頭，能減輕攜帶寶可夢的重量。",
    "Un hilo largo y delgado de color rojo que transmite el enamoramiento del Pokémon que lo lleva a su rival.": "細長的紅線，能將攜帶寶可夢的著迷狀態傳給對手。",
    "Si el portador es alcanzado por un ataque, saldrá del combate y será sustituido por otro Pokémon del equipo.": "攜帶者受到攻擊時，會退出戰鬥並被隊伍中的其他寶可夢替換。",
    "Misteriosa tarjeta que permite al Pokémon que la lleve expulsar al agresor cuando este le cause daño.": "神秘的卡片，能讓攜帶的寶可夢在受到傷害時將攻擊方趕出場。",
    "En combate, esta concha desechada sirve para que un Pokémon se cambie por otro que no esté combatiendo.": "在戰鬥中，這個脫落的殼能讓寶可夢替換成未出場的隊友。",
    "Debe llevarla un Pokémon. Permite huir de combates contra Pokémon salvajes.": "需要寶可夢攜帶。能從野生寶可夢的戰鬥中逃走。",
    "Es un huevo lleno de felicidad que te hará ganar Puntos de Exp. extra en combate. Debe llevarlo un Pokémon.": "充滿幸福的蛋，能讓攜帶的寶可夢在戰鬥中獲得額外經驗值。",
    "El Pokémon que lo lleva obtiene parte de los Puntos de Exp. conseguidos en el combate sin participar en él.": "攜帶的寶可夢即使未參加戰鬥也能獲得一部分經驗值。",
    "Si el Pokémon que la lleva lucha en un combate, duplica las ganancias.": "攜帶的寶可夢參加戰鬥時，獲得的金錢加倍。",
    "Una campana con un tañido calmante que reconforta al Pokémon que la lleva y lo vuelve más amistoso.": "音色平和的鈴鐺，能讓攜帶的寶可夢感到安心並變得更親密。",
    "Si lo lleva el primer Pokémon del equipo, se reduce la probabilidad de que se acerquen Pokémon salvajes.": "如果由隊伍的第一隻寶可夢攜帶，能降低遇見野生寶可夢的機率。",
}

output = []
for line in lines:
    for es, zh in translations.items():
        line = line.replace(es, zh)
    # 修正殘留的 "寶可夢 野生" -> "野生寶可夢"
    line = line.replace("寶可夢 野生", "野生寶可夢")
    line = line.replace("寶可夢s", "寶可夢")
    output.append(line)

with codecs.open(path, "w", "utf-8-sig") as f:
    f.writelines(output)

print("✅ 清理完成！")
