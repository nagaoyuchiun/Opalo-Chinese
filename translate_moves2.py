# -*- coding: utf-8 -*-
import re
import json
import codecs

# 官方寶可夢招式中文譯名對照表
OFFICIAL_MOVES = {
    "Megacuerno": "超級角擊", "Al Ataque": "攻擊指令", "Zumbido": "蟲鳴", "Tijera X": "十字剪",
    "Doble Rayo": "信號光束", "Ida y Vuelta": "急速折返", "Rodillo Púas": "壓路", "Picadura": "蟲咬",
    "Viento Plata": "銀色旋風", "Estoicismo": "蟲之抵抗", "Dobleataque": "雙針", "Cortefuria": "連斬",
    "Chupavidas": "吸血", "Pin Misil": "飛彈針", "A Defender": "防禦指令", "Auxilio": "回復指令",
    "Danza Aleteo": "蝶舞", "Polvo Ira": "憤怒粉", "Telaraña": "蛛網", "Disp. Demora": "吐絲",
    "Ráfaga": "螢火", "Juego Sucio": "欺詐", "Pulso Noche": "暗黑爆破", "Triturar": "咬碎",
    "Pulso Umbrío": "惡之波動", "Golpe Bajo": "突襲", "Tajo Umbrio": "暗襲要害", "Mordisco": "咬住",
    "Finta": "出奇一擊", "Alarido": "大聲咆哮", "Buena Baza": "借機進攻", "Vendetta": "報仇",
    "Persecución": "追打", "Ladrón": "小偷", "Desarme": "拍落", "Paliza": "圍攻",
    "Lanzamiento": "投擲", "Castigo": "懲罰", "Brecha Negra": "暗黑洞", "Embargo": "查封",
    "Llanto Falso": "假哭", "Camelo": "諂媚", "Afilagarras": "磨爪", "Legado": "臨別禮物",
    "Maquinación": "詭計", "Último Lugar": "殿後", "Robo": "搶奪", "Trapicheo": "掉包",
    "Mofa": "挑釁", "Tormento": "無理取鬧"
}

# 完整描述翻譯映射
DESC_TRANSLATIONS = {
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
    "Atormenta y enfurece al objetivo, que no puede usar dos veces seguidas el mismo movimiento.": "折磨對手使其無法連續使用同一招式。"
}

def translate_description(text):
    """翻譯招式描述 - 優先使用完整句子匹配"""
    # 先嘗試完整匹配
    if text in DESC_TRANSLATIONS:
        return DESC_TRANSLATIONS[text]
    
    # 如果沒有完整匹配，保留原文（需要後續手動翻譯）
    return text

def translate_move_name(name):
    """翻譯招式名稱"""
    if name in OFFICIAL_MOVES:
        return OFFICIAL_MOVES[name]
    return name

# 讀取原始檔案（保留 BOM）
with codecs.open('D:/Opalo V2.11/localization/translations/pbs/moves.txt', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

# 處理每一行
translated_lines = []
untranslated_descs = set()

for line in lines:
    # 解析 PBS 格式
    match = re.match(r'^(\d+),([A-Z]+),([^,]+),(.+)$', line.strip())
    if match:
        id_num = match.group(1)
        internal = match.group(2)
        name = match.group(3)
        rest = match.group(4)
        
        # 翻譯名稱
        translated_name = translate_move_name(name)
        
        # 找到描述部分（在引號內）
        desc_match = re.search(r'"([^"]*)"', rest)
        if desc_match:
            original_desc = desc_match.group(1)
            translated_desc = translate_description(original_desc)
            
            if translated_desc == original_desc and original_desc not in ["Smart", "Beauty"]:
                untranslated_descs.add(original_desc)
            
            # 替換描述
            new_rest = rest.replace(f'"{original_desc}"', f'"{translated_desc}"')
        else:
            new_rest = rest
        
        # 重組行
        new_line = f'{id_num},{internal},{translated_name},{new_rest}\n'
        translated_lines.append(new_line)
    else:
        # 保留無法解析的行
        translated_lines.append(line)

# 寫入檔案（保留 BOM）
with codecs.open('D:/Opalo V2.11/localization/translations/pbs/moves.txt', 'w', encoding='utf-8-sig') as f:
    f.writelines(translated_lines)

print(f'✅ 翻譯完成！處理了 {len(translated_lines)} 行')
print(f'⚠️ 有 {len(untranslated_descs)} 個描述需要補充翻譯')
if len(untranslated_descs) > 0 and len(untranslated_descs) <= 10:
    print('\n未翻譯的描述:')
    for desc in list(untranslated_descs)[:10]:
        print(f'  - {desc}')
