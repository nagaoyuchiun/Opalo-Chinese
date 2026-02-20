# -*- coding: utf-8 -*-
"""Translate abilities.txt from Spanish to Traditional Chinese"""
import csv
import io
import sys

INPUT = r"D:\Opalo V2.11\localization\translations\pbs\abilities.txt"

abilities_zh = {
    "Hedor": ("惡臭", "令對手厭惡的臭氣，在首發時降低野生寶可夢遭遇率。"),
    "Llovizna": ("降雨", "出場時會引發下雨。"),
    "Impulso": ("加速", "每回合速度逐漸提升。"),
    "Armadura Batalla": ("戰鬥盔甲", "堅硬的鎧甲使對手無法擊中要害。"),
    "Robustez": ("結實", "不會被一擊打倒。"),
    "Humedad": ("濕氣", "使周圍全部潮濕，防止自爆等爆炸類招式的使用。"),
    "Flexibilidad": ("柔軟", "因為身體柔軟，不會陷入麻痺狀態。"),
    "Velo arena": ("沙隱", "沙暴時迴避率提升。"),
    "Elec. Estática": ("靜電", "身上帶有靜電，接觸到的對手會陷入麻痺狀態。"),
    "Absorbe Elec.": ("蓄電", "受到電屬性招式攻擊時不會受傷，反而會回復HP。"),
    "Absorbe Agua": ("儲水", "受到水屬性招式攻擊時不會受傷，反而會回復HP。"),
    "Despiste": ("遲鈍", "因為感覺遲鈍，不會陷入著迷狀態。"),
    "Aclimatación": ("無關天氣", "使所有天氣的影響都消失。"),
    "Ojocompuesto": ("複眼", "因為擁有複眼，招式的命中率會提升。"),
    "Insomnio": ("不眠", "因為有不眠的體質，不會陷入睡眠狀態。"),
    "Cambio Color": ("變色", "自己的屬性會變為受到的招式的屬性。"),
    "Inmunidad": ("免疫", "因為體內有免疫物質，不會陷入中毒狀態。"),
    "Absorbe Fuego": ("引火", "受到火屬性招式攻擊時，吸收火焰使自己的火屬性招式變強。"),
    "Polvo Escudo": ("鱗粉", "被鱗粉守護著，不會受到招式的追加效果影響。"),
    "Ritmo Propio": ("我行我素", "有著我行我素的性格，不會陷入混亂狀態。"),
    "Ventosas": ("吸盤", "用吸盤牢牢貼住，不會被迫替換。"),
    "Intimidación": ("威嚇", "出場時威嚇對手使其退縮，降低對手的攻擊。"),
    "Sombratrampa": ("踩影", "踩住對手的影子使其無法逃走或替換。"),
    "Piel Tosca": ("粗糙皮膚", "受到攻擊時，用粗糙的皮膚弄傷接觸到自己的對手。"),
    "Superguarda": ("神奇守護", "不可思議的力量，只有效果絕佳的招式才能擊中。"),
    "Levitación": ("漂浮", "從地面浮起，對地面屬性招式免疫。"),
    "Efecto Espora": ("孢子", "接觸時可能會使對手中毒、麻痺或睡眠。"),
    "Sincronía": ("同步", "將自己的中毒、麻痺或灼傷傳給對手。"),
    "Cuerpo Puro": ("恆淨之軀", "不會被對手降低能力。"),
    "Cura Natural": ("自然回復", "回到同伴身邊時治癒異常狀態。"),
    "Pararrayos": ("避雷針", "將電屬性招式引到自己身上，不會受傷且特攻提升。"),
    "Dicha": ("天恩", "託幸運之神的福，招式的追加效果容易出現。"),
    "Nado Rápido": ("悠游自如", "下雨時速度會提升。"),
    "Clorofila": ("葉綠素", "晴天時速度會提升。"),
    "Iluminación": ("發光", "透過發光使野生寶可夢容易出現。"),
    "Rastro": ("複製", "出場時複製對手的特性成為自己的特性。"),
    "Potencia": ("大力士", "使出的物理招式威力加倍。"),
    "Punto Tóxico": ("毒刺", "接觸到的對手可能會陷入中毒狀態。"),
    "Foco Interno": ("精神力", "因為擁有鍛煉過的精神，不會因對手的攻擊而畏縮。"),
    "Escudo Magma": ("岩漿鎧甲", "身披熱岩漿，不會陷入冰凍狀態。"),
    "Velo Agua": ("水幕", "被水幕包裹著，不會陷入灼傷狀態。"),
    "Imán": ("磁力", "以磁力吸住鋼屬性的寶可夢使其無法逃走。"),
    "Insonorizar": ("隔音", "不受聲音類招式的影響。"),
    "Cura Lluvia": ("雨盤", "下雨時會逐漸回復HP。"),
    "Chorro Arena": ("揚沙", "出場時引發沙暴。"),
    "Presión": ("壓迫感", "給予對手壓迫感使其大量消耗PP。"),
    "Sebo": ("厚脂肪", "因為被厚厚的脂肪保護著，火屬性和冰屬性招式的傷害會減半。"),
    "Madrugar": ("早起", "即使陷入睡眠狀態也能以兩倍速度醒來。"),
    "Cuerpo Llama": ("火焰之軀", "接觸到的對手可能會陷入灼傷狀態。"),
    "Fuga": ("逃跑", "一定能從野生寶可夢戰鬥中逃走。"),
    "Vista Lince": ("銳利目光", "因為擁有銳利的目光，命中率不會被降低。"),
    "Corte Fuerte": ("怪力鉗", "因為擁有自豪的怪力鉗，攻擊不會被降低。"),
    "Recogida": ("撿拾", "有時會撿來道具。"),
    "Ausente": ("懶惰", "使出招式後會休息一回合。"),
    "Entusiasmo": ("幹勁", "攻擊提升但命中率下降。"),
    "Gran Encanto": ("迷人之軀", "接觸到的對手可能會陷入著迷狀態。"),
    "Más": ("正電", "搭檔為負電或正電特性的寶可夢時特攻提升。"),
    "Menos": ("負電", "搭檔為正電或負電特性的寶可夢時特攻提升。"),
    "Predicción": ("陰晴不定", "根據天氣變化改變自身屬性。"),
    "Viscosidad": ("黏著", "因為被黏著物質包裹，道具不會被奪走。"),
    "Mudar": ("蛻皮", "透過蛻皮來治癒異常狀態。"),
    "Agallas": ("毅力", "陷入異常狀態時攻擊會提升。"),
    "Escama Especial": ("神奇鱗片", "陷入異常狀態時防禦會提升。"),
    "Lodo Líquido": ("污泥漿", "吸取HP的對手反而會受到傷害。"),
    "Espesura": ("茂盛", "HP減少時草屬性招式的威力會提升。"),
    "Mar Llamas": ("猛火", "HP減少時火屬性招式的威力會提升。"),
    "Torrente": ("激流", "HP減少時水屬性招式的威力會提升。"),
    "Enjambre": ("蟲之預感", "HP減少時蟲屬性招式的威力會提升。"),
    "Cabeza Roca": ("堅硬腦袋", "受到反作用力傷害的招式不會損失HP。"),
    "Sequía": ("日照", "出場時將天氣變為晴天。"),
    "Trampa Arena": ("沙穴", "使對手無法逃走。"),
    "Espíritu Vital": ("幹勁", "擁有幹勁的體質，不會陷入睡眠狀態。"),
    "Humo Blanco": ("白色煙霧", "不會被對手降低能力。"),
    "Energía Pura": ("瑜伽之力", "透過瑜伽之力使物理攻擊的威力加倍。"),
    "Caparazón": ("硬殼盔甲", "堅硬的甲殼使對手無法擊中要害。"),
    "Bucle Aire": ("氣閘", "使所有天氣的影響都消失。"),
    "Tumbos": ("蹣跚", "混亂時迴避率提升。"),
    "Electromotor": ("電氣引擎", "受到電屬性招式攻擊時不會受傷，速度反而會提升。"),
    "Rivalidad": ("鬥爭心", "面對相同性別的對手時攻擊提升，但面對不同性別時則下降。"),
    "Impasible": ("不屈之心", "每次畏縮時速度都會提升。"),
    "Manto Níveo": ("雪隱", "冰雹時迴避率提升。"),
    "Gula": ("貪吃鬼", "原本在HP減少一半時才會使用的樹果會提前食用。"),
    "Irascible": ("憤怒穴位", "被擊中要害時攻擊會大幅提升。"),
    "Liviano": ("輕裝", "失去持有的道具時速度會提升。"),
    "Ignífugo": ("耐熱", "受到的火屬性招式威力減半。"),
    "Simple": ("單純", "能力變化的效果加倍。"),
    "Piel Seca": ("乾燥皮膚", "下雨時和受到水屬性招式時會回復HP，晴天時和受到火屬性招式時HP會減少。"),
    "Descarga": ("下載", "根據對手防禦和特防的高低來提升自己的攻擊或特攻。"),
    "Puño Férreo": ("鐵拳", "使拳頭類招式的威力提升。"),
    "Antídoto": ("毒療", "中毒時不會受傷反而會回復HP。"),
    "Adaptable": ("適應力", "與自身同屬性招式的威力提升。"),
    "Encadenado": ("連續攻擊", "連續攻擊的招式一定能使出最多次數。"),
    "Hidratación": ("濕潤之軀", "下雨時異常狀態會治癒。"),
    "Poder Solar": ("太陽之力", "晴天時特攻提升但每回合HP減少。"),
    "Pies Rápidos": ("飛毛腿", "陷入異常狀態時速度提升。"),
    "Normalidad": ("一般皮膚", "所有屬性的招式都會變為一般屬性。"),
    "Francotirador": ("狙擊手", "擊中要害時傷害更大。"),
    "Muro Mágico": ("魔法防守", "不會受到攻擊招式以外的傷害。"),
    "Indefenso": ("無防守", "使雙方的招式都必定會命中。"),
    "Rezagado": ("慢出", "出招一定會比對手慢。"),
    "Experto": ("技術高手", "威力較低的招式威力會提升。"),
    "Defensa Hoja": ("葉子防守", "晴天時不會陷入異常狀態。"),
    "Zoquete": ("笨拙", "無法使用持有的道具。"),
    "Rompemoldes": ("破格", "可以無視對手特性的影響進行攻擊。"),
    "Afortunado": ("超幸運", "因為特別幸運，容易擊中要害。"),
    "Resquicio": ("餘燼", "自己瀕死時給予接觸到的對手傷害。"),
    "Anticipación": ("危險預知", "能夠察知對手持有的危險招式。"),
    "Alerta": ("預知夢", "出場時可以察知對手的一個招式。"),
    "Ignorante": ("純樸", "無視對手能力的變化來進行攻擊。"),
    "Cromolente": ("有色眼鏡", "效果不好的招式威力會提升。"),
    "Filtro": ("過濾", "受到效果絕佳的攻擊時傷害會減少。"),
    "Inicio Lento": ("慢啟動", "出場後的5回合內攻擊和速度減半。"),
    "Intrépido": ("膽量", "一般屬性和格鬥屬性的招式可以打中幽靈屬性的寶可夢。"),
    "Colector": ("引水", "將水屬性招式引到自己身上，不會受傷且特攻提升。"),
    "Gélido": ("冰凍之軀", "冰雹時會逐漸回復HP。"),
    "Roca Solida": ("堅硬岩石", "受到效果絕佳的攻擊時傷害會減少。"),
    "Nevada": ("降雪", "出場時引發冰雹。"),
    "Recogemiel": ("採蜜", "戰鬥結束後有時會採集到蜂蜜。"),
    "Cacheo": ("察覺", "出場時可以察知對手持有的道具。"),
    "Audaz": ("捨身", "帶有反作用力的招式威力會提升。"),
    "Multitipo": ("多屬性", "根據持有的石板改變屬性。"),
    "Don Floral": ("花之禮", "晴天時自己和同伴的攻擊與特防提升。"),
    "Mal Sueño": ("噩夢", "對睡眠狀態的對手造成少量傷害。"),
    "Hurto": ("順手牽羊", "被接觸時竊取對手的道具。"),
    "Potencia Bruta": ("強行", "招式的追加效果不會出現但威力會提升。"),
    "Acero Templado": ("鋼之工匠", "鋼屬性招式的威力提升。"),
    "Nerviosismo": ("緊張感", "使對手緊張得無法食用樹果。"),
    "Competitivo": ("不服輸", "能力被降低時攻擊會大幅提升。"),
    "Flaqueza": ("軟弱", "HP降到一半以下時攻擊和特攻會減半。"),
    "Cuerpo Maldito": ("詛咒之軀", "受到攻擊時有時會把對手的招式封住。"),
    "Alma Cura": ("治癒之心", "有時會治癒同伴的異常狀態。"),
    "Compiescolta": ("友情防守", "能減輕同伴受到的傷害。"),
    "Armadura Frágil": ("碎裂鎧甲", "受到物理攻擊時防禦降低但速度提升。"),
    "Metal Pesado": ("重金屬", "自身的體重加倍。"),
    "Metal Liviano": ("輕金屬", "自身的體重減半。"),
    "Compensación": ("多重鱗片", "HP全滿時受到的傷害減少。"),
    "Ímpetu Tóxico": ("中毒激升", "中毒狀態時物理攻擊的威力提升。"),
    "Ímpetu Ardiente": ("燃盡激升", "灼傷狀態時特殊攻擊的威力提升。"),
    "Cosecha": ("收穫", "有時能再次取得已使用過的樹果。"),
    "Telepatía": ("心靈感應", "讀取同伴的攻擊而迴避傷害。"),
    "Veleta": ("心情不定", "每回合會隨機大幅提升一項能力並降低另一項能力。"),
    "Funda": ("防塵", "不會受到沙暴和冰雹的傷害，也不會受到粉末類招式影響。"),
    "Toque Tóxico": ("毒手", "只是接觸就有可能使對手中毒。"),
    "Regeneración": ("再生力", "回到同伴身邊時會回復少量HP。"),
    "Sacapecho": ("挺胸", "防禦不會被降低。"),
    "Ímpetu Arena": ("撥沙", "沙暴時速度會提升。"),
    "Piel Milagro": ("奇蹟皮膚", "不容易受到變化招式的影響。"),
    "Cálculo Final": ("分析", "最後出招時招式威力會提升。"),
    "Ilusión": ("幻覺", "偽裝成隊伍中最後一隻寶可夢出場。"),
    "Impostor": ("變身者", "出場時會變身為對面的寶可夢。"),
    "Allanamiento": ("穿透", "可以無視對手的替身和反射壁等進行攻擊。"),
    "Momia": ("木乃伊", "被接觸時將對手的特性變為木乃伊。"),
    "Autoestima": ("自信過度", "打倒對手時攻擊會提升。"),
    "Justiciero": ("正義之心", "受到惡屬性招式攻擊時攻擊會提升。"),
    "Cobardía": ("膽怯", "受到惡、幽靈或蟲屬性的攻擊時速度會提升。"),
    "Espejomágico": ("魔法鏡", "能將變化招式反彈回去。"),
    "Herbívoro": ("食草", "受到草屬性招式攻擊時不會受傷，攻擊反而會提升。"),
    "Bromista": ("惡作劇之心", "能讓變化招式先制使出。"),
    "Poder Arena": ("沙之力", "沙暴時岩石、地面、鋼屬性招式的威力提升。"),
    "Punta Acero": ("鐵刺", "接觸到的對手會受到傷害。"),
    "Modo Daruma": ("達摩模式", "HP降到一半以下時外形會改變。"),
    "Tinovictoria": ("勝利之星", "自己和同伴的招式命中率提升。"),
    "Turbollama": ("渦輪火焰", "無視對手特性的影響進行攻擊。"),
    "Terravoltaje": ("兆級電壓", "無視對手特性的影響進行攻擊。"),
    "Quitanieves": ("撥雪", "冰雹時速度會提升。"),
    "Piel Feérica": ("妖精皮膚", "一般屬性的招式會變為妖精屬性且威力提升。"),
    "Coleóptero": ("甲蟲皮膚", "一般屬性的招式會變為蟲屬性且威力提升。"),
    "Piel Helada": ("冰凍皮膚", "一般屬性的招式會變為冰屬性且威力提升。"),
    "Garra Dura": ("硬爪", "接觸類招式的威力提升。"),
    "Poder Sabio": ("賢者之力", "特殊招式的威力提升。"),
    "Amor Filial": ("親子愛", "親子共同攻擊，可以攻擊2次。"),
    "Piel Tétrica": ("幽靈皮膚", "一般屬性的招式會變為幽靈屬性且威力提升。"),
    "Piel Eléctrica": ("電氣皮膚", "一般屬性的招式會變為電屬性且威力提升。"),
    "Espanto": ("驚嚇", "驚嚇對手使其特攻降低。"),
    "Iceberg": ("冰山", "不會受到反作用力傷害。"),
    "Pompa": ("水泡", "降低受到的火屬性招式傷害，提升水屬性招式威力，且不會灼傷。"),
    "Firmeza": ("持久力", "受到攻擊時防禦會提升。"),
    "Inflamable": ("易燃", "火屬性招式的威力提升。"),
    "Mandíbula Fuerte": ("強壯之顎", "咬擊類招式的威力提升。"),
    "Pelaje Recio": ("毛皮大衣", "受到的物理攻擊傷害減半。"),
    "Piel Celeste": ("飛行皮膚", "一般屬性的招式會變為飛行屬性且威力提升。"),
    "Tenacidad": ("好勝", "能力被降低時特攻會大幅提升。"),
    "Megadisparador": ("超級發射器", "波動和波導類招式的威力提升。"),
    "Albino": ("白化", "冰屬性招式的威力提升。"),
    "Respondón": ("唱反調", "能力變化的效果反轉。"),
    "Voz Fluida": ("濕潤之聲", "聲音類招式會變為水屬性。"),
    "Mutatipo": ("變幻自如", "變為將要使用的招式的屬性。"),
    "Disfraz": ("畫皮", "披著破布擋住1次攻擊。"),
    "Cambio Táctico": ("戰鬥切換", "根據使用的招式在盾牌形態和刀劍形態之間切換。"),
    "Peluche": ("毛茸茸", "受到的接觸類招式傷害減半，但受到的火屬性招式傷害加倍。"),
    "Veránima": ("夏之魂", "吸收特殊招式來提升特攻。"),
}

with open(INPUT, "r", encoding="utf-8-sig") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    line = line.rstrip("\n").rstrip("\r")
    if line.startswith("#") or line.strip() == "":
        new_lines.append(line)
        continue

    # Parse: id,INTERNAL,Name,"Description"
    reader = csv.reader(io.StringIO(line))
    try:
        parts = list(next(reader))
    except StopIteration:
        new_lines.append(line)
        continue

    if len(parts) >= 4:
        es_name = parts[2]
        if es_name in abilities_zh:
            zh_name, zh_desc = abilities_zh[es_name]
            parts[2] = zh_name
            parts[3] = zh_desc

    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(parts)
    new_lines.append(out.getvalue().rstrip("\r\n"))

with open(INPUT, "w", encoding="utf-8-sig", newline="") as f:
    f.write("\n".join(new_lines))

translated = sum(1 for l in new_lines if l.strip() and not l.startswith("#") and any(ord(c) > 0x2E80 for c in l))
total = sum(1 for l in new_lines if l.strip() and not l.startswith("#"))
print(f"Abilities: {translated}/{total} translated")
