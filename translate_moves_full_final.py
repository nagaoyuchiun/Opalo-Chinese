# -*- coding: utf-8 -*-
import re

# 完整的西班牙語->繁體中文招式描述模板
# 根據官方寶可夢繁體中文版描述

def translate_move_desc(spanish_text):
    """完整翻譯西班牙語招式描述"""
    
    # 完整片語替換（優先匹配長句）
    full_phrases = {
        # Dragon continues
        "Ataca usando tal energía que el tiempo se distorsiona. El usuario descansa el siguiente turno.": 
            "以扭曲時間的巨大能量攻擊對手。使用者下一回合須休息。",
        "Hace que grandes cometas caigan del cielo. Baja mucho el Ataque Especial de quien lo usa":
            "從天空降下大量彗星。大幅降低使用者的特攻。",
        "Ataca de forma brutal mientras intimida al objetivo. También puede hacerlo retroceder.":
            "以猛烈方式攻擊並威嚇對手。有時會使對手畏縮。",
        "Desgarra al objetivo y el espacio a su alrededor. Suele ser crítico.":
            "撕裂對手及周圍空間。容易擊中要害。",
        "Abre mucho la boca y libera una onda de choque que ataca al objetivo.":
            "張大嘴巴釋放衝擊波攻擊對手。",
        "Araña al objetivo con garras afiladas.":
            "用銳利的爪子抓對手。",
        "Ataca al objetivo y lo obliga a cambiarse por otro Pokémon. Si es uno salvaje, acaba el combate.":
            "攻擊對手並迫使其替換。對野生寶可夢使用時可結束戰鬥。",
        "Poderosa ráfaga de aliento que golpea al objetivo y puede paralizarlo.":
            "用威力強大的氣息攻擊對手。有時會使對手麻痺。",
        "Golpea al objetivo usando la cola u otras partes de su cuerpo.":
            "用尾巴或其他身體部位連續攻擊對手2次。",
        "Crea un violento tornado para hacer trizas al objetivo. Puede hacerle retroceder.":
            "製造猛烈龍捲風粉碎對手。有時會使對手畏縮。",
        "Ráfaga de furiosas ondas de choque que quitan 40 HP.":
            "釋放憤怒的衝擊波，固定造成40點傷害。",
        "Danza mística que sube el Ataque y la Velocidad.":
            "跳起神秘之舞，提升攻擊和速度。",
            
        # Electric continues
        "Ataca usando una enorme descarga eléctrica. Sube su potencia si es influenciada por una gigantesca llamarada.":
            "用巨大電擊攻擊。若受到巨大火焰影響則威力提升。",
        "Un poderoso rayo que daña al objetivo y puede paralizarlo.":
            "威力強大的雷電攻擊。有時會使對手麻痺。",
        "Placaje de alto riesgo que hiere también al atacante.":
            "高風險的電擊衝撞，使用者也會受傷。",
        "Lanza una descarga eléctrica que causa daño y paraliza.":
            "發射巨大電擊造成傷害並使對手麻痺。",
        "Potente ataque eléctrico que puede paralizar al objetivo.":
            "強力的電擊攻擊。有時會使對手麻痺。",
        "Carga eléctrica muy potente que también hiere ligeramente a quien la usa.":
            "威力強大的電擊衝撞，使用者也會受到輕微傷害。",
        "Una deslumbrante onda eléctrica afecta a los demás Pokémon del combate. Puede paralizar.":
            "耀眼的電擊波動影響周圍的寶可夢。有時會麻痺。",
        "Puñetazo eléctrico. Puede paralizar.":
            "電擊拳。有時會使對手麻痺。",
        "Ataque eléctrico que puede llegar a paralizar.":
            "電擊攻擊。有時會使對手麻痺。",
        "Usa colmillos electrificados para morder. Puede hacer que el rival retroceda o se paralice.":
            "用帶電的牙齒咬對手。有時會使對手畏縮或麻痺。",
        "Ataque eléctrico muy rápido e ineludible.":
            "極快的電擊攻擊，必定命中。",
        "Atrapa y ataca al objetivo usando una telaraña eléctrica. También baja su Velocidad.":
            "用電網捕捉並攻擊對手。也會降低對手的速度。",
        "Lanza un rayo eléctrico contra el rival. Puede subir el Ataque Especial de quien lo usa.":
            "向對手發射電擊光線。有時會提升使用者的特攻。",
        "Ataque eléctrico que puede paralizar al objetivo.":
            "電擊攻擊。有時會使對手麻痺。",
        "Lanza una bola eléctrica. Cuanto mayor Velocidad tenga el usuario, mayor será el daño causado.":
            "發射電球。使用者速度越快，傷害越大。",
        "Recarga energía para potenciar el siguiente movimiento Eléctrico. También sube la Def. Esp.":
            "充電以強化下一個電屬性招式。也會提升特防。",
        "Levita gracias a un campo magnético generado por electricidad durante cinco turnos.":
            "藉由電力產生的磁場浮空，持續5回合。",
        "Una ligera descarga que paraliza al objetivo si lo alcanza.":
            "輕微的電擊。命中時使對手麻痺。",
            
        # Fighting continues
        "Se concentra para dar un puñetazo. Falla si se sufre un golpe antes de su uso.":
            "集中精神使出拳擊。若使用前受到攻擊則會失敗。",
        "Salta muy alto y lanza una patada. Si falla, dañará al usuario.":
            "跳得很高並踢擊。如果失敗則傷害使用者。",
        "Lucha abiertamente contra el rival sin defenderse. También baja la Defensa y la Defensa Especial del usuario.":
            "正面與對手戰鬥而不防守。也會降低使用者的防禦和特防。",
        "Agudiza la concentración mental y libera su poder. Puede disminuir la Defensa Especial del objetivo.":
            "集中精神力量釋放能量。有時會降低對手的特防。",
        "Ataque de gran potencia, pero que baja el Ataque y la Defensa del agresor.":
            "威力強大的攻擊，但會降低使用者的攻擊和防禦。",
        "Corte doble que suele propinar un golpe crítico.":
            "雙重切割攻擊，容易擊中要害。",
        "Puñetazo con toda la fuerza concentrada. Causa confusión si atina.":
            "集中全力的拳擊。命中時使對手混亂。",
        "Gira con fuerza el puño y da un gran golpe. No obstante, baja la Velocidad.":
            "用力旋轉拳頭給予重擊。但是會降低速度。",
        "Da un salto y pega una patada. Si falla, se lesiona.":
            "跳起並踢擊。如果失敗則使用者受傷。",
        "Libera una descarga de la fuerza del aura desde su interior. Es infalible.":
            "從體內釋放波導力量。必定命中。",
        "El usuario ataca usando una espada":
            "使用者用劍攻擊，無視對手的能力變化。",
        "Ensarta al objetivo con un sable":
            "用劍刺穿對手。以對手的防禦而非特防計算傷害。",
        "Gancho ascendente de gran ímpetu.":
            "威力強大的上勾拳。",
        "Tira al objetivo al suelo. También hiere al agresor.":
            "將對手摔到地上。使用者也會受傷。",
        "Potente ataque que también es capaz de destruir barreras como Pantalla de Luz y Reflejo.":
            "強力攻擊，也能破壞光牆和反射壁等屏障。",
        "Un golpe que drena energía. El Pokémon recupera la mitad de los HP arrebatados al objetivo.":
            "吸取能量的攻擊。使用者回復給予對手傷害的一半HP。",
        "El usuario ataca el último, pero no falla.":
            "使用者最後攻擊，但必定命中。",
    }
    
    result = spanish_text
    
    # 應用完整片語替換
    for spanish, chinese in full_phrases.items():
        if spanish in result:
            result = result.replace(spanish, chinese)
            return result  # 一旦找到完整匹配就返回
    
    # 如果沒有完整匹配，進行詞彙級別翻譯
    word_map = {
        # 主要動詞
        "Ataca": "攻擊", "atacar": "攻擊", "ataca": "攻擊",
        "Golpea": "擊打", "golpea": "擊打",
        "Lanza": "發射", "lanza": "發射",
        "Dispara": "發射", "dispara": "發射",
        "Usa": "使用", "usa": "使用", "usando": "使用",
        "Crea": "製造", "crea": "製造",
        "Hace": "使", "hace": "使",
        "Libera": "釋放", "libera": "釋放",
        "Sube": "提升", "sube": "提升", "subir": "提升",
        "Baja": "降低", "baja": "降低", "bajar": "降低",
        
        # 能力值
        "Ataque Especial": "特攻", "Ataque": "攻擊",
        "Defensa Especial": "特防", "Defensa": "防禦",
        "Velocidad": "速度",
        "Precisión": "命中率",
        
        # 常用詞
        "objetivo": "對手", "rival": "對手",
        "usuario": "使用者", "agresor": "使用者",
        "Puede": "有時會", "puede": "有時會",
        "También": "也", "también": "也",
        "daño": "傷害", "poder": "威力",
        "turno": "回合", "combate": "戰鬥",
        
        # 狀態
        "paralizar": "麻痺", "paraliza": "麻痺",
        "envenenar": "中毒", "envenena": "中毒",
        "quemar": "灼傷", "quema": "灼傷",
        "confusión": "混亂", "confundir": "混亂",
        "retroceder": "畏縮",
    }
    
    for spanish, chinese in word_map.items():
        result = re.sub(r'\b' + re.escape(spanish) + r'\b', chinese, result)
    
    return result

# 讀取檔案
with open("D:\\Opalo V2.11\\localization\\translations\\pbs\\moves.txt", "r", encoding="utf-8-sig") as f:
    lines = f.readlines()

# 翻譯每一行
new_lines = []
for i, line in enumerate(lines, 1):
    if line.strip() == "" or line.startswith("#"):
        new_lines.append(line)
        continue
    
    parts = line.strip().split(",")
    if len(parts) < 14:
        new_lines.append(line)
        continue
    
    # 提取描述（最後一個欄位，去除引號）
    description = ",".join(parts[13:]).strip('"')
    
    # 如果描述包含西班牙語關鍵字，進行翻譯
    spanish_keywords = ["Ataca", "Lanza", "Golpea", "Puede", "del", "una", "que"]
    if any(keyword in description for keyword in spanish_keywords):
        translated_desc = translate_move_desc(description)
        
        # 重組行
        prefix = ",".join(parts[:13])
        new_line = f'{prefix},"{translated_desc}"\n'
        new_lines.append(new_line)
        
        if i % 50 == 0:
            print(f"已處理 {i} 行...")
    else:
        new_lines.append(line)

# 寫回檔案
with open("D:\\Opalo V2.11\\localization\\translations\\pbs\\moves.txt", "w", encoding="utf-8-sig") as f:
    f.writelines(new_lines)

print("✅ 翻譯完成！")
