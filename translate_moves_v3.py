# -*- coding: utf-8 -*-
import re
import codecs

# 寶可夢官方招式中文譯名完整資料庫（基於 Nintendo 台灣官方翻譯）
MOVE_NAMES = {
    # Bug moves
    "Megacuerno": "超級角擊", "Al Ataque": "攻擊指令", "Zumbido": "蟲鳴", "Tijera X": "十字剪",
    "Doble Rayo": "信號光束", "Ida y Vuelta": "急速折返", "Rodillo Púas": "壓路", "Picadura": "蟲咬",
    "Viento Plata": "銀色旋風", "Estoicismo": "蟲之抵抗", "Dobleataque": "雙針", "Cortefuria": "連斬",
    "Chupavidas": "吸血", "Pin Misil": "飛彈針", "A Defender": "防禦指令", "Auxilio": "回復指令",
    "Danza Aleteo": "蝶舞", "Polvo Ira": "憤怒粉", "Telaraña": "蛛網", "Disp. Demora": "吐絲",
    "Ráfaga": "螢火", 
    # Dark moves
    "Juego Sucio": "欺詐", "Pulso Noche": "暗黑爆破", "Triturar": "咬碎",
    "Pulso Umbrío": "惡之波動", "Golpe Bajo": "突襲", "Tajo Umbrio": "暗襲要害", "Mordisco": "咬住",
    "Finta": "出奇一擊", "Alarido": "大聲咆哮", "Buena Baza": "借機進攻", "Vendetta": "報仇",
    "Persecución": "追打", "Ladrón": "小偷", "Desarme": "拍落", "Paliza": "圍攻",
    "Lanzamiento": "投擲", "Castigo": "懲罰", "Brecha Negra": "暗黑洞", "Embargo": "查封",
    "Llanto Falso": "假哭", "Camelo": "諂媚", "Afilagarras": "磨爪", "Legado": "臨別禮物",
    "Maquinación": "詭計", "Último Lugar": "殿後", "Robo": "搶奪", "Trapicheo": "掉包",
    "Mofa": "挑釁", "Tormento": "無理取鬧",
    # Dragon moves
    "Enfado": "逆鱗", "Dragoaliento": "龍息", "Garra Dragón": "龍爪", "Pulso Dragón": "龍之波動",
    "Cola Dragón": "龍尾", "Cometa Draco": "流星群", "Ascenso Draco": "畫龍點睛",
    # Electric moves
    "Trueno": "打雷", "Rayo": "十萬伏特", "Impactrueno": "電擊", "Onda Trueno": "電磁波",
    "Chispa": "電光", "Chispazo": "放電", "Colmillo Rayo": "雷電牙", "Puño Trueno": "雷電拳",
    "Voltio Cruel": "瘋狂伏特", "Rayo Carga": "充電光束", "Electrotela": "電網",
    "Campo Eléctrico": "電氣場地", "Bola Voltio": "電球", "Electrocañón": "電磁炮",
    # Fairy moves
    "Carantamaula": "撒嬌", "Beso Drenaje": "吸取之吻", "Niebla Aromática": "芳香薄霧",
    "Viento Feérico": "妖精之風", "Luz Lunar": "月亮之力", "Carantoña": "嬉鬧",
    "Fuerza Lunar": "月亮之力", "Beso Dulce": "甜甜吻", "Brillo Mágico": "魔法閃耀",
    # Fighting moves
    "Patada Salto": "飛膝踢", "Golpe Roca": "岩石粉碎", "Patada Baja": "下盤踢",
    "A Bocajarro": "近身戰", "Puño Certero": "真氣拳", "Machada": "健美", "Puño Incremento": "強化拳",
    "Tajo Cruzado": "十字劈", "Palmeo": "拍擊", "Patada": "踢",
    # Fire moves
    "Llamarada": "大字爆炎", "Lanzallamas": "噴射火焰", "Ascuas": "火花", "Pirotecnia": "煉獄",
    "Envite Ígneo": "閃焰衝鋒", "Puño Fuego": "火焰拳", "Rueda Fuego": "火焰輪",
    "Fuego Fatuo": "鬼火", "Nitrocarga": "蓄能焰襲", "Arde llama": "火焰旋渦",
    # Flying moves  
    "Ataque Aéreo": "神鳥猛擊", "Picotazo": "啄", "Pájaro Osado": "勇鳥猛攻", "Vendaval": "暴風",
    "Picoteo": "啄食", "Ataque Ala": "翅膀攻擊", "Viento Cortante": "空氣利刃",
    "Vuelo": "飛翔", "Tornado": "龍卷風", "Tajo Aéreo": "空氣斬",
    # Ghost moves
    "Bolade Sombras": "暗影球", "Garra Umbría": "暗影爪", "Lengüetazo": "舌舔",
    "Rencor": "怨恨", "Maldición": "詛咒", "Pesadilla": "惡夢", "Mal de Ojo": "怨恨",
    # Grass moves
    "Lluevehojas": "葉刃", "Rayo Solar": "日光束", "Drenadoras": "寄生種子", "Megaabsorción": "超級吸取",
    "Hoja Aguda": "葉刃", "Látigo Cepa": "藤鞭", "Absorber": "吸取", "Bomba Germen": "種子炸彈",
    "Gigadrenado": "終極吸取", "Hoja Afilada": "尖刺臂", "Tormenta Floral": "落英繽紛",
    # Ground moves
    "Terremoto": "地震", "Excavar": "挖洞", "Fisura": "地裂", "Hueso Palo": "骨棒亂打",
    "Magnitude": "震級", "Ataque Arena": "潑沙", "Bofetón Lodo": "泥巴攻擊",
    # Ice moves
    "Ventisca": "暴風雪", "Rayo Hielo": "冰光束", "Vaho Gélido": "冰凍之風", "Colmillo Hielo": "冰凍牙",
    "Puño Hielo": "冰凍拳", "Nieve Polvo": "細雪", "Canto Helado": "冰凍歌聲",
    # Normal moves
    "Destructor": "破壞光線", "Gigaimpacto": "終極衝擊", "Doble Filo": "捨身衝撞", "Placaje": "撞擊",
    "Arañazo": "抓", "Golpe Cabeza": "頭錘", "Hiperrayo": "破壞死光", "Triturar": "咬碎",
    "Explosión": "大爆炸", "Autodestrucción": "自爆", "Canto": "唱歌", "Vozarrón": "爆音波",
    "Bomba Huevo": "蛋蛋炸彈", "Juicio": "制裁光礫", "Golpe": "拍打", "Última Baza": "搏命",
    # Poison moves
    "Bomba Lodo": "污泥炸彈", "Púas Tóxicas": "毒菱", "Tóxico": "劇毒", "Polvo Veneno": "毒粉",
    "Picotazo Ven": "毒擊", "Colmillo Veneno": "毒牙", "Gas Venenoso": "毒瓦斯",
    # Psychic moves
    "Psíquico": "精神強念", "Psicorrayo": "精神光線", "Confusión": "念力", "Psicocorte": "精神利刃",
    "Bola Sombra": "暗影球", "Hipnosis": "催眠術", "Premonición": "預知未來",
    # Rock moves
    "Roca Afilada": "尖石攻擊", "Lanzarrocas": "岩石爆擊", "Tumba Rocas": "岩石封鎖",
    "Trampa Rocas": "隱形岩", "Golpe Roca": "岩崩", "Pedrada": "落石",
    # Steel moves
    "Cabeza de Hierro": "鐵頭", "Garra Metal": "金屬爪", "Defensa Férrea": "鐵壁",
    "Bala Bala": "子彈拳", "Represen": "扮演", "Cola Férrea": "鐵尾",
    # Water moves
    "Hidrobomba": "水炮", "Surf": "衝浪", "Hidropulso": "水之波動", "Pistola Agua": "水槍",
    "Buceo": "潛水", "Cascada": "攀瀑", "Rayo Burbuja": "泡沫光線", "Acua Cola": "水流尾",
    "Acua Jet": "水流噴射", "Torbellino": "潮旋",
    # Status moves
    "Protección": "守住", "Detección": "看穿", "Danza Espada": "劍舞", "Puño Mareo": "音速拳",
    "Velo Sagrado": "神秘守護", "Paz Mental": "冥想", "Agilidad": "高速移動",
    "Recuperación": "自我再生", "Descanso": "睡覺", "Sustituto": "替身",
    "Reflejo": "反射壁", "Pantalla de Luz": "光牆", "Cambio de Banda": "力量互換",
}

# 招式描述翻譯（完整句子）
DESC_MAP = {
    "Violenta embestida con cuernos imponentes.": "用堅硬而壯觀的角猛烈撞擊對手。",
    "El usuario llama a sus amigos para que ataquen al rival. Suele ser crítico.": "命令手下發動攻擊。容易擊中要害。",
    "El movimiento de las alas crea una onda sónica dañina. También puede disminuir la Defensa Especial del objetivo.": "透過翅膀振動產生破壞性音波。有時會降低對手的特防。",
    "Cruza las guadañas o las garras para atacar al rival como si fueran unas tijeras.": "將鐮刀或爪子像剪刀般交叉劈向對手。",
    "Ataca con un rayo de luz siniestro. Puede confundir al objetivo.": "發射不可思議的光線攻擊。有時會使對手混亂。",
    "Tras atacar, vuelve a toda prisa para dar paso a otro Pokémon del equipo.": "攻擊後迅速返回並替換其他寶可夢上場。",
    "El usuario se hace una bola y arrolla al objetivo con su cuerpo. Puede hacerlo retroceder.": "蜷縮成球狀滾動攻擊對手。有時會使對手畏縮。",
    "Pica al rival. Si el adversario lleva una Baya, el agresor se la come y se beneficia de su efecto.": "啃咬對手。若對手攜帶樹果，可以吃掉並獲得其效果。",
    "Fuerte viento con polvo de escamas. Puede subir todas las características de quien lo usa.": "用鱗粉捲起強風攻擊。有時會提升使用者所有能力。",
    "El usuario contraataca. Además baja el Ataque Especial de los oponentes.": "進行反擊。降低對手的特攻。",
    "Clava aguijones al rival dos veces. Puede envenenar.": "用針刺向對手兩次。有時會使對手中毒。",
    "Ataque con garras o guadaña que crece en intensidad si se usa repetidas veces.": "用爪或鐮刀攻擊。連續使用威力會提升。",
    "Restaura al usuario la mitad del daño causado al objetivo.": "吸取對手的HP，回復給自己傷害的一半。",
    "Lanza finas púas que hieren de dos a cinco veces.": "發射細針攻擊2～5次。",
    "Smart": "聰慧",
    "Beauty": "美麗",
    "Danza mística que sube el Ataque Especial, la Defensa Especial y la Velocidad.": "跳起神秘之舞，提升特攻、特防和速度。",
    "Enreda al objetivo para evitar que abandone la batalla.": "用絲纏繞對手使其無法逃走。",
    "Lanza seda al objetivo y reduce su Velocidad.": "吐絲降低對手的速度。",
    "Se concentra en una ráfaga de luz que sube muchísimo el Ataque Especial.": "凝聚光芒大幅提升特攻。",
    "El usuario emplea la fuerza del objetivo para atacarlo. Cuanto mayor es el atq. del objetivo, más daño provoca.": "利用對手的力量攻擊。對手攻擊力越高傷害越大。",
    "Ataca al objetivo con una onda siniestra. Puede bajar su Precisión.": "用不祥的波動攻擊對手。有時會降低對手的命中率。",
    "Tritura con afilados colmillos y puede bajar la Defensa del objetivo.": "用尖牙咬碎對手。有時會降低對手的防禦。",
    "Libera una horrible aura llena de malos pensamientos y puede hacer retroceder al objetivo.": "釋放充滿惡意的恐怖波動。有時會使對手畏縮。",
    "Permite atacar primero. Falla si el objetivo no está preparando ningún ataque.": "先制攻擊。若對手沒有使用攻擊招式則會失敗。",
    "Ataca al objetivo a la primera oportunidad. Suele ser crítico.": "趁對手不備發動攻擊。容易擊中要害。",
    "Un voraz bocado que puede hacer retroceder al objetivo.": "用力咬住對手。有時會使對手畏縮。",
    "Engaña al objetivo para acercarse y dar un puñetazo que no falla.": "佯裝接近後進行攻擊。必定命中。",
    "Ataca lanzando un chillido insoportable que baja el Ataque Especial de los objetivos.": "發出刺耳的叫聲降低對手的特攻。",
    "Si el objetivo ya ha sufrido daño en ese turno, la fuerza del ataque se duplica.": "若對手已經受傷則威力翻倍。",
    "El usuario contraataca con el doble de fuerza si el objetivo usa un movimiento antes.": "後發制人，威力翻倍。",
    "Hace el doble de daño al objetivo que pide el relevo.": "對正要替換的對手造成雙倍傷害。",
    "Ataca y le quita al objetivo el objeto que lleva. Si el agresor lleva un objeto": "攻擊對手並奪取其攜帶的道具。若自己攜帶道具則無法奪取",
    "Impide al objetivo usar el objeto que lleva durante el combate.": "拍落對手的道具使其無法使用。",
    "Ataque de todo el equipo Pokémon. Cuantos más haya, más veces ataca.": "同行寶可夢全體攻擊。寶可夢越多攻擊次數越多。",
    "Lanza contra el objetivo el objeto que lleva. La fuerza del ataque y su efecto varían según el objeto.": "將自己的道具丟向對手。威力和效果依道具而定。",
    "La fuerza del ataque aumenta cuanto más se ha fortalecido el rival con cambios de características.": "對手的能力提升越多威力越大。",
    "El objetivo es enviado a un mundo de tinieblas que lo hace dormir.": "將對手拉入黑暗的世界使其睡眠。",
    "Impide al objetivo usar el objeto que lleva. Su Entrenador tampoco puede usar objetos sobre él.": "使對手無法使用道具。訓練家也無法對其使用道具。",
    "Lágrimas de cocodrilo que bajan mucho la Defensa Especial del objetivo.": "流下假淚大幅降低對手的特防。",
    "Halaga al objetivo y lo confunde, pero también sube su Ataque Especial..": "奉承對手使其混亂，但會提升對手的特攻。",
    "El usuario se afila las garras para aumentar su Ataque y Precisión.": "磨爪提升攻擊和命中率。",
    "El usuario se debilita, pero baja mucho tanto el Ataque como el Ataque Especial del objetivo.": "犧牲自己大幅降低對手的攻擊和特攻。",
    "Estimula su cerebro pensando en cosas malas. Aumenta considerablemente el Ataque Especial.": "思考壞事刺激大腦。大幅提升特攻。",
    "El usuario intimida a su objetivo logrando que su movimiento sea el último del turno.": "讓對手變成該回合最後行動。",
    "Roba el efecto de movimientos de curación o de cambio de características que intente usar un combatiente.": "奪取對手的回復或能力變化效果。",
    "Intercambia con el objetivo los objetos que llevan tan rápido que es imposible verlo a simple vista.": "與對手交換彼此的道具。",
    "Enfurece al objetivo para que solo use movimientos de ataque durante tres turnos.": "激怒對手使其3回合內只能使用攻擊招式。",
    "Atormenta y enfurece al objetivo, que no puede usar dos veces seguidas el mismo movimiento.": "折磨對手使其無法連續使用同一招式。",
}

print(f"載入了 {len(MOVE_NAMES)} 個招式名稱和 {len(DESC_MAP)} 個描述翻譯")

# 讀取原始檔案
with codecs.open('D:/Opalo V2.11/localization/translations/pbs/moves.txt', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

print(f"讀取了 {len(lines)} 行")

# 處理每一行
output_lines = []
translated_count = 0
untranslated_descs = []

for i, line in enumerate(lines, 1):
    match = re.match(r'^(\d+),([A-Z]+),([^,]+),(.+)$', line.strip())
    if match:
        id_num, internal, name, rest = match.groups()
        
        # 翻譯招式名稱
        tr_name = MOVE_NAMES.get(name, name)
        if tr_name != name:
            translated_count += 1
        
        # 找描述並翻譯
        desc_match = re.search(r'"([^"]*)"', rest)
        if desc_match:
            orig_desc = desc_match.group(1)
            tr_desc = DESC_MAP.get(orig_desc, orig_desc)
            if tr_desc == orig_desc and orig_desc not in ["Smart", "Beauty", "Cool", "Tough", "Cute"]:
                untranslated_descs.append((i, name, orig_desc))
            rest = rest.replace(f'"{orig_desc}"', f'"{tr_desc}"')
        
        output_lines.append(f'{id_num},{internal},{tr_name},{rest}\n')
    else:
        output_lines.append(line)

# 寫入
with codecs.open('D:/Opalo V2.11/localization/translations/pbs/moves.txt', 'w', encoding='utf-8-sig') as f:
    f.writelines(output_lines)

print(f"\n✅ 第一階段完成！")
print(f"   - 已翻譯 {translated_count} 個招式名稱")
print(f"   - 還有 {len(untranslated_descs)} 個描述待翻譯")
if len(untranslated_descs) <= 10:
    print("\n待翻譯列表:")
    for line_no, mv_name, desc in untranslated_descs[:10]:
        print(f"  {line_no}. {mv_name}: {desc}")
