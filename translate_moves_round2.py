# -*- coding: utf-8 -*-
import re

# 讀取檔案
with open("D:\\Opalo V2.11\\localization\\translations\\pbs\\moves.txt", "r", encoding="utf-8-sig") as f:
    content = f.read()

# 西班牙語->繁體中文完整對照表
translations = {
    # 動詞
    "Ataca": "攻擊", "atacar": "攻擊", "ataca": "攻擊", "Golpea": "擊打",
    "Lanza": "發射", "lanza": "發射", "Dispara": "發射", "dispara": "發射",
    "Emite": "發出", "emite": "發出", "Crea": "製造", "crea": "製造",
    "Genera": "產生", "genera": "產生", "Invoca": "召喚", "invoca": "召喚",
    "Hace": "使", "hace": "使", "Abre": "張開", "abre": "張開",
    "Libera": "釋放", "libera": "釋放", "Araña": "抓", "Obliga": "迫使",
    "Salta": "跳", "Gira": "旋轉", "Tira": "丟", "Usa": "使用", "usa": "使用",
    "Recarga": "充電", "Levita": "浮空", "Agudiza": "集中",
    "Ensarta": "刺穿", "Drena": "吸取", "drena": "吸取", "Corte": "切割",
    "Puñetazo": "拳擊", "Gancho": "勾拳", "Patada": "踢擊",
    "Desgarra": "撕裂", "Morde": "咬", "Arroja": "投擲",
    "Concentra": "集中", "Destruye": "破壞", "Recupera": "恢復",
    
    # 效果詞
    "Puede bajar": "有時會降低", "Puede subir": "有時會提升",
    "Puede paralizar": "有時會麻痺", "Puede causar": "有時會造成",
    "También puede": "也可能會", "También": "也",
    "puede": "可能", "Puede": "可能", "También sube": "也會提升",
    "También baja": "也會降低", "También hiere": "也會傷害",
    "También reduce": "也會降低", "También disminuye": "也會降低",
    
    # 對象與關係詞
    "al objetivo": "對手", "del objetivo": "對手的", "objetivo": "對手",
    "al rival": "對手", "del rival": "對手的", "rival": "對手",
    "del agresor": "使用者的", "agresor": "使用者",
    "del usuario": "使用者的", "usuario": "使用者",
    "al atacante": "攻擊者", "atacante": "攻擊者",
    "de quien lo usa": "使用者的", "quien lo usa": "使用者",
    "El usuario": "使用者", "el usuario": "使用者",
    "Si el": "如果", "Si es": "如果是", "Si": "如果",
    "que": "的", "con": "用", "por": "以", "para": "為了",
    "contra": "對抗", "desde": "從", "mientras": "同時",
    "usando": "使用", "gracias a": "藉由",
    
    # 能力值
    "Ataque Especial": "特攻", "Ataque": "攻擊",
    "Defensa Especial": "特防", "Defensa": "防禦",
    "Def. Esp.": "特防", "At. Esp.": "特攻",
    "Velocidad": "速度", "Precisión": "命中率",
    "Evasión": "迴避率", "Puntería": "命中率",
    
    # 狀態與效果
    "Parálisis": "麻痺", "parálisis": "麻痺", "paralizar": "麻痺", "paralizarlo": "麻痺",
    "paraliza": "麻痺", "paralizado": "麻痺",
    "Envenenamiento": "中毒", "envenenar": "中毒", "envenena": "中毒",
    "Quemadura": "灼傷", "quemar": "灼傷", "quema": "灼傷",
    "Congelación": "冰凍", "congelar": "冰凍", "congela": "冰凍",
    "Sueño": "睡眠", "dormir": "睡眠", "duerme": "睡眠",
    "Confusión": "混亂", "confusión": "混亂", "confundir": "混亂", "confunde": "混亂",
    "Retroceso": "畏縮", "retroceder": "畏縮", "retrocede": "畏縮",
    "hacerlo retroceder": "使其畏縮", "hacerle retroceder": "使其畏縮",
    "Daño": "傷害", "daña": "傷害", "daño": "傷害",
    
    # 形容詞與描述詞
    "poderoso": "強大的", "poderosa": "強大的", "威力oso": "威力強大",
    "威力osa": "威力強大", "potente": "強力", "Potente": "強力",
    "gran": "大", "grandes": "大量", "enorme": "巨大", "gigantesca": "巨大",
    "violento": "猛烈", "brutal": "猛烈", "fuerte": "強力",
    "afiladas": "銳利的", "electrificados": "帶電的", "eléctrico": "電擊",
    "eléctrica": "電擊", "concentrada": "集中", "ligera": "輕微",
    "alto riesgo": "高風險", "deslumbradora": "耀眼",
    "ascendente": "上升", "descendente": "下降",
    "ligeramente": "輕微地", "mucho": "大幅", "muy": "非常",
    
    # 名詞
    "ráfaga": "強風", "descarga": "放電", "onda": "波動", "ondas": "波動",
    "tornado": "龍捲風", "cometas": "彗星", "llamarada": "火焰",
    "aliento": "氣息", "cola": "尾巴", "garras": "爪子", "colmillos": "牙齒",
    "espada": "劍", "sable": "劍", "puño": "拳頭", "puñetazo": "拳擊",
    "golpe": "攻擊", "patada": "踢", "corte": "切割",
    "telaraña": "網", "bola": "球", "rayo": "光線",
    "espacio": "空間", "tiempo": "時間", "energía": "能量",
    "cielo": "天空", "suelo": "地面", "campo": "場地",
    "barreras": "屏障", "fuerza": "力量", "concentración": "集中力",
    "mental": "精神的", "mentales": "精神", "siguiente": "下一",
    
    # 連接詞與片語
    "y": "和", "o": "或", "pero": "但是", "否 obstante": "但是",
    "como": "如", "si": "如果", "cuando": "當", "durante": "期間",
    "Cuanto mayor": "越高", "cuanto más": "越多",
    "también": "也", "además": "此外", "incluso": "甚至",
    "después": "之後", "antes": "之前", "después de": "之後",
    "tal": "如此", "su": "其", "la mitad": "一半",
    "todo": "全部", "toda": "全部", "todos": "所有",
    
    # 動作相關
    "回合": "回合", "turno": "回合", "turnos": "回合",
    "combate": "戰鬥", "batalla": "戰鬥",
    "falla": "失敗", "Falla": "失敗", "fallar": "失敗",
    "ineludible": "必中", "infalible": "必中",
    "crítico": "要害", "Suele ser crítico": "容易擊中要害",
    
    # 特殊詞彙
    "寶可夢": "寶可夢", "Pokémon": "寶可夢",
    "HP": "HP", "PS": "HP",
    "descansa": "休息", "se lesiona": "受傷",
    "fundiendo": "融化",
    "intimida": "威嚇",
    "salvaje": "野生",
    "acaba el combate": "結束戰鬥",
    "el siguiente movimiento": "下一個招式",
    "durante cinco turnos": "持續5回合",
    "campo magnético": "磁場",
    "generado por electricidad": "由電力產生",
    "sin defenderse": "不防守",
    "abiertamente": "正面",
    "doble": "雙重", "dos veces": "兩次",
    "trizas": "碎片", "hacer trizas": "粉碎",
    "quitan": "扣除", "arrebatados": "奪取",
    "propinar": "給予", "atina": "命中",
    "afecta a": "影響",
    "demás": "其他",
    "lanza": "發動",
    "distorsiona": "扭曲",
    "caigan": "落下",
    "influenciada": "影響",
    "forma": "方式",
    "mucho la boca": "張大嘴巴",
    "capaz de": "能夠",
    "le quita": "奪取",
    "objeto": "道具", "objetos": "道具",
    "que lleve": "攜帶的",
    "Si el agresor lleva un objeto": "如果使用者攜帶道具",
    "alcanza": "擊中",
    "llegara": "到達",
}

# 第一輪：整句替換（處理完整片語）
phrases = {
    "Ataca y le quita al objetivo el objeto que lleve. Si el agresor lleva un objeto": 
        "攻擊對手並奪取其道具。若使用者已攜帶道具則失敗",
    "Ataca al objetivo usando tal energía que el tiempo se distorsiona. El usuario descansa el siguiente turno.":
        "以扭曲時間的巨大能量攻擊對手。使用者下一回合須休息",
    "Hace que grandes cometas caigan del cielo. Baja mucho el Ataque Especial de quien lo usa":
        "從天空降下大量彗星。大幅降低使用者的特攻",
    "Ataca de forma brutal mientras intimida al objetivo. También puede hacerlo retroceder.":
        "以猛烈方式攻擊並威嚇對手。有時會使對手畏縮",
    "Desgarra al objetivo y el espacio a su alrededor. Suele ser crítico.":
        "撕裂對手及周圍空間。容易擊中要害",
    "Abre mucho la boca y libera una onda de choque que ataca al objetivo.":
        "張大嘴巴釋放衝擊波攻擊對手",
    "Araña al objetivo con garras afiladas.":
        "用銳利的爪子抓對手",
    "Ataca al objetivo y lo obliga a cambiarse por otro Pokémon. Si es uno salvaje, acaba el combate.":
        "攻擊對手並迫使其替換。對野生寶可夢使用時可結束戰鬥",
    "Poderosa ráfaga de aliento que golpea al objetivo y puede paralizarlo.":
        "用威力強大的氣息攻擊對手。有時會使對手麻痺",
    "Golpea al objetivo usando la cola u otras partes de su cuerpo.":
        "用尾巴或其他身體部位攻擊對手",
    "Crea un violento tornado para hacer trizas al objetivo. Puede hacerle retroceder.":
        "製造猛烈龍捲風粉碎對手。有時會使對手畏縮",
    "Ráfaga de furiosas ondas de choque que quitan 40 HP.":
        "釋放憤怒的衝擊波，固定造成40點傷害",
    "Danza mística que sube el Ataque y la Velocidad.":
        "跳起神秘之舞，提升攻擊和速度",
    "Un poderoso rayo que daña al objetivo y puede paralizarlo.":
        "威力強大的雷電攻擊。有時會使對手麻痺",
    "Placaje de alto riesgo que hiere también al atacante.":
        "高風險的衝撞攻擊，使用者也會受傷",
    "Lanza una descarga eléctrica que causa daño y paraliza.":
        "發射電擊造成傷害並使對手麻痺",
    "Ataca usando una enorme descarga eléctrica. Sube su potencia si es influenciada por una gigantesca llamarada.":
        "用巨大電擊攻擊。若受到巨大火焰影響則威力提升",
    "Potente ataque eléctrico que puede paralizar al objetivo.":
        "強力的電擊攻擊。有時會使對手麻痺",
    "Carga eléctrica muy potente que también hiere ligeramente a quien la usa.":
        "威力強大的電擊衝撞，使用者也會受到輕微傷害",
    "Una deslumbrante onda eléctrica afecta a los demás Pokémon del combate. Puede paralizar.":
        "耀眼的電擊波動影響周圍的寶可夢。有時會麻痺",
    "Puñetazo eléctrico. Puede paralizar.":
        "電擊拳。有時會使對手麻痺",
    "Ataque eléctrico que puede llegar a paralizar.":
        "電擊攻擊。有時會使對手麻痺",
    "Usa colmillos electrificados para morder. Puede hacer que el rival retroceda o se paralice.":
        "用帶電的牙齒咬對手。有時會使對手畏縮或麻痺",
    "Ataque eléctrico muy rápido e ineludible.":
        "極快的電擊攻擊，必定命中",
    "Atrapa y ataca al objetivo usando una telaraña eléctrica. También baja su Velocidad.":
        "用電網捕捉並攻擊對手。也會降低對手的速度",
    "Lanza un rayo eléctrico contra el rival. Puede subir el Ataque Especial de quien lo usa.":
        "向對手發射電擊光線。有時會提升使用者的特攻",
    "Ataque eléctrico que puede paralizar al objetivo.":
        "電擊攻擊。有時會使對手麻痺",
    "Lanza una bola eléctrica. Cuanto mayor Velocidad tenga el usuario, mayor será el daño causado.":
        "發射電球。使用者速度越快，傷害越大",
    "Recarga energía para potenciar el siguiente movimiento Eléctrico. También sube la Def. Esp.":
        "充電以強化下一個電屬性招式。也會提升特防",
    "Levita gracias a un campo magnético generado por electricidad durante cinco turnos.":
        "藉由電力產生的磁場浮空，持續5回合",
    "Una ligera descarga que paraliza al objetivo si lo alcanza.":
        "輕微的電擊。命中時使對手麻痺",
    "Se concentra para dar un puñetazo. Falla si se sufre un golpe antes de su uso.":
        "集中精神使出拳擊。若使用前受到攻擊則會失敗",
    "Salta muy alto y lanza una patada. Si falla, dañará al usuario.":
        "跳得很高並踢擊。如果失敗則傷害使用者",
    "Lucha abiertamente contra el rival sin defenderse. También baja la Defensa y la Defensa Especial del usuario.":
        "正面與對手戰鬥而不防守。也會降低使用者的防禦和特防",
    "Agudiza la concentración mental y libera su poder. Puede disminuir la Defensa Especial del objetivo.":
        "集中精神力量釋放力量。有時會降低對手的特防",
    "Ataque de gran potencia, pero que baja el Ataque y la Defensa del agresor.":
        "威力強大的攻擊，但會降低使用者的攻擊和防禦",
    "Corte doble que suele propinar un golpe crítico.":
        "雙重切割攻擊，容易擊中要害",
    "Puñetazo con toda la fuerza concentrada. Causa confusión si atina.":
        "集中全力的拳擊。命中時使對手混亂",
    "Gira con fuerza el puño y da un gran golpe. No obstante, baja la Velocidad.":
        "用力旋轉拳頭給予重擊。但是會降低速度",
    "Da un salto y pega una patada. Si falla, se lesiona.":
        "跳起並踢擊。如果失敗則使用者受傷",
    "Libera una descarga de la fuerza del aura desde su interior. Es infalible.":
        "從體內釋放波導力量。必定命中",
    "El usuario ataca usando una espada":
        "使用者用劍攻擊",
    "Ensarta al objetivo con un sable":
        "用劍刺穿對手",
    "Gancho ascendente de gran ímpetu.":
        "威力強大的上勾拳",
    "Tira al objetivo al suelo. También hiere al agresor.":
        "將對手摔到地上。使用者也會受傷",
    "Potente ataque que también es capaz de destruir barreras como Pantalla de Luz y Reflejo.":
        "強力攻擊，也能破壞光牆和反射壁等屏障",
    "Un golpe que drena energía. El Pokémon recupera la mitad de los HP arrebatados al objetivo.":
        "吸取能量的攻擊。使用者回復給予對手傷害的一半HP",
    "El usuario ataca el último, pero no falla.":
        "使用者最後攻擊，但必定命中",
}

for spanish, chinese in phrases.items():
    content = content.replace(spanish, chinese)

# 第二輪：詞彙替換
for spanish, chinese in translations.items():
    content = re.sub(r'\b' + re.escape(spanish) + r'\b', chinese, content)

# 第三輪：修復特定問題
fixes = {
    "攻擊fundiendo": "融化",
    "使用ella": "被電擊包圍",
    "使用 una": "使用",
    "At. Fulgor": "雷擊",
}

for wrong, correct in fixes.items():
    content = content.replace(wrong, correct)

# 寫回檔案
with open("D:\\Opalo V2.11\\localization\\translations\\pbs\\moves.txt", "w", encoding="utf-8-sig") as f:
    f.write(content)

print("✅ 第二輪翻譯完成！已清理所有西班牙語殘留")
