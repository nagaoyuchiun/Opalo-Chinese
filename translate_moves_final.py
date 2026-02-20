import json
import re
import os
from pathlib import Path

# 完整的寶可夢招式名稱對照表（中西對照）
COMPLETE_MOVE_TRANSLATIONS = {
    # 蟲系
    "Megacuerno": "超級角擊",
    "Al Ataque": "攻擊指令",
    "Zumbido": "蟲鳴",
    "Tijera X": "十字剪",
    "Doble Rayo": "信號光束",
    "Ida y Vuelta": "急速折返",
    "Rodillo Púas": "重壓",
    "Picadura": "蟲咬",
    "Viento Plata": "銀色旋風",
    "Estoicismo": "蟲之抵抗",
    "Dobleataque": "雙針",
    "Cortefuria": "連斬",
    "Chupavidas": "吸血",
    "Pin Misil": "飛彈針",
    "A Defender": "防禦指令",
    "Auxilio": "回復指令",
    "Danza Aleteo": "蝶舞",
    "Polvo Ira": "憤怒粉",
    "Telaraña": "蜘蛛網",
    "Disp. Demora": "吐絲",
    "Ráfaga": "尾巴發光",
    
    # 惡系
    "Juego Sucio": "欺詐",
    "Pulso Noche": "暗黑爆破",
    "Triturar": "咬碎",
    "Pulso Umbrío": "惡之波動",
    "Golpe Bajo": "突襲",
    "Tajo Umbrio": "暗襲要害",
    "Mordisco": "咬住",
    "Finta": "出奇一擊",
    "Alarido": "大聲咆哮",
    "Buena Baza": "以牙還牙",
    "Vendetta": "報仇",
    "Persecución": "追打",
    "Ladrón": "小偷",
    "Desarme": "拍落",
    "Paliza": "圍攻",
    "Lanzamiento": "投擲",
    "Castigo": "懲罰",
    "Brecha Negra": "暗黑洞",
    "Embargo": "查封",
    "Llanto Falso": "假哭",
    "Camelo": "吹捧",
    "Afilagarras": "磨爪",
    "Legado": "臨別禮物",
    "Maquinación": "詭計",
    "Último Lugar": "殿後",
    "Robo": "搶奪",
    "Trapicheo": "掉包",
    "Mofa": "挑釁",
    "Tormento": "無理取鬧",
    
    # 龍系
    "Distorción": "時光咆哮",
    "Cometa Draco": "流星群",
    "Enfado": "逆鱗",
    "Carga Dragón": "龍之俯衝",
    "Corte Vacío": "亞空裂斬",
    "Pulso Dragón": "龍之波動",
    "Garra Dragón": "龍爪",
    "Cola Dragón": "龍尾",
    "Dragoaliento": "龍息",
    "Golpe Bis": "二連劈",
    "Ciclón": "龍捲風",
    "Furia Dragón": "龍之怒",
    "Danza Dragón": "龍之舞",
    "Ascenso Draco": "畫龍點睛",
    
    # 電系
    "At. Fulgor": "閃電交擊",
    "Trueno": "打雷",
    "Placaje Eléc.": "伏特攻擊",
    "Electrocañón": "電磁炮",
    "Rayo Fusión": "交錯閃電",
    "Rayo": "十萬伏特",
    "Voltio Cruel": "瘋狂伏特",
    "Chispazo": "放電",
    "Puño Trueno": "雷電拳",
    "Voltiocambio": "伏特替換",
    "Chispa": "電光",
    "Colm. Rayo": "雷電牙",
    "Onda Voltio": "電擊波",
    "Electrotela": "電網",
    "Rayo Carga": "充電光束",
    "Impactrueno": "電擊",
    "Bola Voltio": "電球",
    "Carga": "充電",
    "Levitón": "電磁飄浮",
    "Onda Trueno": "電磁波",
    "Electrobaba": "電蛛網",
    
    # 格鬥系
    "Puño Certero": "真氣拳",
    "Pat. S. Alta": "飛膝踢",
    "A Bocajarro": "近身戰",
    "Onda Certera": "真氣彈",
    "Fuerza Bruta": "蠻力",
    "Tajo Cruzado": "十字劈",
    "Puñodinámico": "爆裂拳",
    "Machada": "臂錘",
    "Patada Salto": "飛踢",
    "Esfera Aural": "波導彈",
    "Espadasanta": "聖劍",
    "Sablemístico": "神秘之劍",
    "Gancho Alto": "衝天拳",
    "Sumisión": "地球上投",
    "Demolición": "劈瓦",
    "Puño Drenaje": "吸取拳",
    "Tiro Vital": "借力摔",
    "Rev. Roca": "岩石封鎖",
    "Kárate": "空手劈",
    "Vuelo": "飛翔",
    "Fuerza": "怪力",
    "Plancha Voladora": "飛身重壓",
    "Puño Incremento": "增強拳",
    
    # 火系
    "Envite Ígneo": "閃焰衝鋒",
    "Anillo Ígneo": "火焰漩渦",
    "Pirotecnia": "大字爆炸",
    "V de Fuego": "大字爆",
    "Nitrocarga": "蓄能焰襲",
    "Lanzallamas": "噴射火焰",
    "Llamarada": "過熱",
    "Garra Ígnea": "火焰拳",
    "Rueda Fuego": "火焰輪",
    "Colm. Igneo": "火焰牙",
    "Vendaval Ígneo": "熱風",
    "Ascuas": "火花",
    "Llamarada": "噴出",
    "Infierno": "煉獄",
    "Puño Fuego": "火焰拳",
    "Furia": "憤怒",
    "Sofoco": "火焰彈",
    "Manto Ígneo": "蓄能焰襲",
    "Luz de Ruina": "破滅之光",
    "Rompehielos": "藍色火焰",
    "Fuego Lunar": "魔法火焰",
    "Místicalfire": "魔法火焰",
    "Choque Vapor": "蒸汽噴射",
    "Látigo Ígneo": "火焰鞭",
    
    # 飛行系
    "Pájaro Osado": "勇鳥猛攻",
    "Golpe Aéreo": "空氣斬",
    "Picotazo": "啄",
    "Cielo": "自由落體",
    "Pico Taladro": "啄鑽",
    "Vuelo": "飛翔",
    "Vendaval": "暴風",
    "Tajo Aéreo": "空氣利刃",
    "Respiro": "羽棲",
    "Acróbata": "雜技",
    "Ataque Aéreo": "神鳥猛擊",
    "Ataque Ala": "翅膀攻擊",
    "Tornado": "起風",
    "Pico": "啄食",
    "Viento Feérico": "妖精之風",
    "Ala de Acero": "鋼翼",
    "Pluma Letal": "羽擊",
    "Tormenta": "暴風",
    "Despejar": "順風",
    "Viento Cortante": "空氣斬",
    "Defensa": "擋格",
    "Ala Mortal": "死亡之翼",
    "Desbandada": "鳥嘴加農炮",
    "Ala Funesta": "不祥之翼",
    "Alabis": "雙翼",
    
    # 幽靈系
    "Golpe Fantasma": "暗影擊",
    "Bola Sombra": "暗影球",
    "Garraumbría": "暗影爪",
    "Puño Sombra": "暗影拳",
    "Lengüetazo": "舔",
    "Infortunio": "惡夢",
    "Maldición": "詛咒",
    "Rencor": "怨恨",
    "Rabia": "憤怒",
    "Condena": "黑色目光",
    "Mismo Destino": "同命",
    "Imp. Nocturno": "黑夜魔影",
    "Asombro": "驚嚇",
    "Resentimiento": "怨恨",
    "Maldignición": "怨念",
    "Limpia Sueños": "夢境騷擾",
    "Ojos Terribles": "恐怖臉",
    "Drenánima": "靈魂吸取",
    "Fuerza Fantasma": "潛靈奇襲",
    "Absorbesencia": "精神強念",
    
    # 草系
    "Látigo Cepa": "藤鞭",
    "Hoja Afilada": "飛葉快刀",
    "Tormenta Floral": "落英繽紛",
    "Rayo Solar": "日光束",
    "Latigazo": "強力鞭打",
    "Hoja Aguda": "葉刃",
    "Abismo de Hojas": "能量球",
    "Hoja Mágica": "魔法葉",
    "Semilladora": "種子機關槍",
    "Gigadrenado": "終極吸取",
    "Astadrenaje": "木角",
    "Ciclón Hojas": "葉刃",
    "Hoja Mágica": "魔法葉",
    "Brazo Pincho": "尖刺臂",
    "Hoja Afilada": "飛葉快刀",
    "Voto Planta": "草之誓約",
    "Megaagotar": "超級吸取",
    "Látigo Cepa": "藤鞭",
    "Semilladora": "種子機關槍",
    "Absorber": "吸取",
    "Hierba Lazo": "打草結",
    "Aromaterapia": "芳香治療",
    "Rizo Algodón": "棉花防守",
    "Esporagodón": "棉孢子",
    "Silbato": "草笛",
    "Arraigo": "扎根",
    "Drenadoras": "寄生種子",
    "Somnífero": "催眠粉",
    "Espora": "蘑菇孢子",
    "Paralizador": "麻痺粉",
    "Síntesis": "光合作用",
    "Abatidoras": "煩惱種子",
    "Zarzas": "荊棘蔓生",
    "Brazo Musgo": "苔蘚拳",
    
    # 地面系
    "Terremoto": "地震",
    "Tierra Viva": "大地神力",
    "Excavar": "挖洞",
    "Taladradora": "直衝鑽",
    "Hueso Palo": "骨棒",
    "Bomba Fango": "泥巴炸彈",
    "Terratemblor": "重踏",
    "Disp. Lodo": "泥巴射擊",
    "Huesomerang": "骨頭迴力鏢",
    "Bucle Arena": "流沙地獄",
    "Ataque Óseo": "骨棒亂打",
    "Bofetón Lodo": "擲泥",
    "Fisura": "地裂",
    "Magnitud": "震級",
    "Chapoteolodo": "玩泥巴",
    "Ataque Arena": "潑沙",
    "Púas": "撒菱",
    "Mil Temblores": "千波激盪",
    "Geoimpacto": "地核錘",
    "Furia Totémica": "圖騰之怒",
    "Arenas Ardientes": "灼熱沙地",
    "Fuerza Equina": "千里踢",
    
    # 冰系
    "Rayo Gélido": "冰凍伏特",
    "Llama Gélida": "極寒冷焰",
    "Ventisca": "暴風雪",
    "Rayo Hielo": "冰凍光束",
    "Chuzos": "冰柱墜擊",
    "Puño Hielo": "冰凍拳",
    "Rayo Aurora": "極光束",
    "Mundo Gélido": "冰凍世界",
    "Colm. Hielo": "冰凍牙",
    "Alud": "雪崩",
    "Viento Hielo": "冰凍之風",
    "Vaho Gélido": "冰息",
    "Canto Helado": "冰礫",
    "Nieve Polvo": "粉雪",
    "Bola Hielo": "冰球",
    "Carámbano": "冰錐針",
    "Frío Polar": "絕對零度",
    "Granizo": "冰雹",
    "Niebla": "黑霧",
    "Neblina": "白霧",
    "Liofilización": "冷凍乾燥",
    "Patada Gélida": "三旋擊",
    "Triple Áxel": "三旋擊",
    
    # 一般系
    "Explosión": "大爆炸",
    "Autodestru.": "自爆",
    "Giga Impacto": "終極衝擊",
    "Hiperrayo": "破壞光線",
    "Última Baza": "珍藏",
    "Doble Filo": "雙刃頭槌",
    "Ariete": "爆炸頭突襲",
    "Megapatada": "百萬噸重踢",
    "Golpe": "暴走",
    "Bomba Huevo": "蛋蛋炸彈",
    "Sentencia": "制裁光礫",
    "Cabezazo": "火箭頭槌",
    "Vozarrón": "巨聲",
    "Treparrocas": "攀岩",
    "Derribo": "猛撞",
    "Alboroto": "吵鬧",
    "Golpe Cuerpo": "泰山壓頂",
    "Tecno Shock": "高科技光炮",
    "Vel. Extrema": "神速",
    "Hip.Colmillo": "必殺門牙",
    "Megapuño": "百萬噸重拳",
    "V. Cortante": "旋風刀",
    "Atizar": "摔打",
    "Fuerza": "怪力",
    "Triataque": "三重攻擊",
    "Garra Brutal": "擊碎",
    "Cantoarcaico": "古老之歌",
    "Guardia Baja": "看穿",
    "Puño Mareo": "迷昏拳",
    "Imagen": "意念頭槌",
    "Golpe Cabeza": "頭槌",
    "Represalia": "報仇",
    "Daño Secreto": "祕密之力",
    "Cuchillada": "劈開",
    "Cornada": "角撞",
    "Pisotón": "踩踏",
    "Antojo": "渴望",
    "Canon": "輪唱",
    "Estímulo": "氣味偵測",
    "Rapidez": "高速星星",
    "Agarre": "夾住",
    "Bostezo": "哈欠",
    "Caricatura": "滑稽表演",
    "Estruendo": "爆音波",
    "Láser Esencia": "本源超載",
    
    # 毒系
    "Lanza Mugre": "垃圾射擊",
    "Onda Tóxica": "污泥波",
    "Bomba Lodo": "污泥炸彈",
    "Puya Nociva": "毒擊",
    "Veneno X": "十字毒刃",
    "Residuos": "污泥攻擊",
    "Cargatóxica": "毒液衝擊",
    "Nieblaclara": "清除之煙",
    "Colmillo Ven": "劇毒牙",
    "Cola Veneno": "毒尾",
    "Ácido": "溶解液",
    "Bomba Ácida": "酸液炸彈",
    "Polución": "濁霧",
    "Picotazo Ven": "毒針",
    "Armad. Ácida": "溶化",
    "Enrosque": "盤蜷",
    "Bilis": "胃液",
    "Gas Venenoso": "毒瓦斯",
    "Polvo Veneno": "毒粉",
    "Tóxico": "劇毒",
    "Púas Tóxicas": "毒菱",
    "Danza Vudú": "巫毒舞",
    "Belch": "打嗝",
    "Fell Stinger": "致命針刺",
    
    # 超能力系
    "Psicoataque": "精神突進",
    "Come Sueños": "食夢",
    "Premonición": "預知未來",
    "Onda Mental": "精神擊破",
    "Psíquico": "精神強念",
    "Paranormal": "神通力",
    "Psicocarga": "精神衝擊",
    "Cabezazo Zen": "意念頭槌",
    "Resplandor": "光澤電炮",
    "Bola Neblina": "薄霧球",
    "Psico-corte": "精神利刃",
    "Sincrorruido": "同步干擾",
    "Psicorrayo": "幻象術",
    "Arrumaco": "愛的印記",
    "Confusión": "念力",
    "Manto Espejo": "鏡面反射",
    "Psicoonda": "精神波",
    "Poderreserva": "輔助力量",
    "Agilidad": "高速移動",
    "Cambio Banda": "交換場地",
    "Amnesia": "失憶",
    "Barrera": "屏障",
    "Paz Mental": "冥想",
    "Masa Cósmica": "宇宙力量",
    "Gravedad": "重力",
    "Isoguardia": "防守平分",
    "Cambia Def.": "防守互換",
    "Anticura": "封印回復",
    "Pulso Cura": "治癒波動",
    "Deseo Cura": "治癒之願",
    "Cambia Almas": "心靈互換",
    "Hipnosis": "催眠術",
    "Sellar": "封印",
    "Kinético": "念力",
    "Pantalla Luz": "光牆",
    "Danza Lunar": "新月舞",
    "Capa Mágica": "魔法反射",
    "Zona Mágica": "魔法空間",
    "Meditación": "瑜伽姿勢",
    "Gran Ojo": "奇蹟之眼",
    "Isofuerza": "力量平分",
    "Cambia Fue.": "力量互換",
    "Truco Fuerza": "力量戲法",
    "Psico-cambio": "精神轉移",
    "Reflejo": "反射壁",
    "Descanso": "睡覺",
    "Imitación": "扮演",
    "Intercambio": "特性互換",
    "Telequinesis": "意念移物",
    "Teletransp.": "瞬間移動",
    "Truco": "戲法",
    "Espacio Raro": "戲法空間",
    "Zona Extraña": "奇妙空間",
    "Psicocolmillo": "精神之牙",
    "Pipa de la Paz": "和平之煙",
    "Fuerzaesencia": "靈魂之力",
    
    # 岩石系
    "Roca Afilada": "尖石攻擊",
    "Avalancha": "岩崩",
    "Pedrada": "岩石爆擊",
    "Rev. Roca": "岩石封鎖",
    "Tumba Rocas": "岩石爆擊",
    "Lanzarrocas": "落石",
    "Pulimento": "磨亮",
    "Trampa Rocas": "隱形岩",
    "Antiaéreo": "廣域防守",
    "Roca Veloz": "岩石快打",
    "Tormenta de Diamantes": "鑽石風暴",
    "Lingotazo": "金塊猛擊",
    "Corte Pétreo": "岩石利刃",
    
    # 鋼系
    "Cabezahierro": "鐵頭",
    "Garra Metal": "金屬爪",
    "Ala de Acero": "鋼翼",
    "Represalia": "金屬爆炸",
    "Rueda Bola": "陀螺球",
    "Defensa Férrea": "鐵壁",
    "Pulimento": "自我激勵",
    "Trinchar": "連斬",
    "Ferroimpacto": "金屬爆炸",
    "Cuerno Certero": "精準攻擊",
    
    # 水系
    "Hidrobomba": "水炮",
    "Hidroariete": "水流裂破",
    "Hidrocañón": "水炮",
    "Salpicar": "濺水",
    "Surf": "衝浪",
    "Cascada": "攀瀑",
    "Acua Cola": "水流尾",
    "Salmuera": "鹽水",
    "Hidropulso": "水之波動",
    "Buceo": "潛水",
    "Pistola Agua": "水槍",
    "Tenaza": "緊束",
    "Torbellino": "潮漩",
    "Burbuja": "泡沫",
    "Acua Aro": "水流環",
    "Danza Lluvia": "祈雨",
    "Anegar": "浸水",
    "Hidrochorro": "玩水",
    "Refugio": "縮入殼中",
    "Shuriken de Agua": "飛水手裏劍",
    "Chorro Vapor": "蒸汽噴發",
    "Pulso Origen": "根源波動",
    "Viraje": "水流噴射",
    
    # 妖精系
    "Brillo Mágico": "魔法閃耀",
    "Voz Cautivadora": "魅惑之聲",
    "Beso Drenaje": "吸取之吻",
    "Viento Feérico": "妖精之風",
    "Fuerza Lunar": "月亮之力",
    "Carantoña": "嬉鬧",
    "Geocontrol": "大地神力",
    "Luz de Ruina": "破滅之光",
    "Flecha Astral": "星光箭雨",
    
    # Opalo 原創招式
    "Tiroteo": "連射",
    "Fuego Lunar": "月火",
    "Maldignición": "怨火",
    "Limpia Sueños": "淨夢",
    "Ala Funesta": "凶兆之翼",
    "Furia Totémica": "圖騰之怒",
    "Sombratela": "暗影絲",
    "Abrazo Feroz": "兇猛擁抱",
    "Geoimpacto": "大地衝擊",
    "Borrasca": "暴雨雷",
    "Ojos Terribles": "恐怖凝視",
    "Drenánima": "魂吸",
    "Danza Vudú": "巫毒舞",
    "Choque Vapor": "蒸氣爆擊",
    "Patada Gélida": "冰凍踢",
    "Colm. Salvaje": "野性獠牙",
    "Brazo Musgo": "苔蘚臂",
    "Caricatura": "漫畫化",
    "Viraje": "水之折返",
    "Escaramuza": "突擊",
    "Cuerno Certero": "銳角",
    "Arenas Ardientes": "灼沙",
    "Fuerza Equina": "馬力",
    "Bola de Polen": "花粉球",
    "Psicocolmillo": "念力牙",
    "Triple Áxel": "三旋踢",
    "Lariat Oscuro": "惡之衣",
    "Roca Veloz": "岩石突襲",
    "Plancha": "飛撲",
    "Flecha Astral": "星光箭",
    "Látigo Ígneo": "火鞭",
    "Ala Bis": "雙翅",
    "Lingotazo": "金塊投",
    "Absorbesencia": "精華吸取",
    "Ferroimpacto": "鋼鐵衝擊",
    "Corte Pétreo": "岩刃",
    "Fiebre del Oro": "淘金熱",
    "Desbandada": "飛鳥撤退",
    "Rompehielos": "破冰",
    "Trinchar": "三連斬",
    "Zarzas": "荊棘",
    "Pipa de la Paz": "和平煙斗",
    "Fuerzaesencia": "精華之力",
    
    # 更多常見招式
    "Protección": "守住",
    "Detección": "看穿",
    "Aguante": "挺住",
    "Desarme": "拍落",
    "Poder Pasado": "輔助力量",
    "Llave Giro": "瘋狂滾壓",
    "Pataleta": "蠻幹",
    "Giro Fuego": "火焰輪",
    "Chispa": "電光",
    "Azote": "拍打",
    "Golpes Furia": "連續拳",
    "Doble Bofetón": "連環巴掌",
    "Canto": "唱歌",
    "Transformación": "變身",
    "Mimético": "模仿",
}

# 載入詞彙表
with open('localization/glossary.json', 'r', encoding='utf-8') as f:
    glossary = json.load(f)

# 建立西班牙文到中文的對照字典
term_map = {}
for category in glossary['categories'].values():
    if 'terms' in category:
        for term in category['terms']:
            term_map[term['es']] = term['zh_TW']
    if 'subcategories' in category:
        for subcat in category['subcategories'].values():
            if 'terms' in subcat:
                for term in subcat['terms']:
                    term_map[term['es']] = term['zh_TW']

def apply_glossary(text):
    """使用詞彙表替換文本中的術語"""
    # 按長度排序，優先替換長詞
    sorted_terms = sorted(term_map.items(), key=lambda x: len(x[0]), reverse=True)
    for es_term, zh_term in sorted_terms:
        # 使用單詞邊界匹配，避免部分匹配
        pattern = r'\b' + re.escape(es_term) + r'\b'
        text = re.sub(pattern, zh_term, text, flags=re.IGNORECASE)
    return text

# 讀取原始檔案
with open('PBS/moves.txt', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

print(f'總共 {len(lines)} 行')
print('開始完整翻譯...\n')

# 批量處理翻譯
translated_lines = []
missing_translations = []

for i, line in enumerate(lines, 1):
    if not line.strip():
        translated_lines.append(line)
        continue
    
    # 解析格式
    parts = line.strip().split(',')
    if len(parts) < 13:
        translated_lines.append(line)
        continue
    
    move_id = parts[0]
    internal_name = parts[1]
    spanish_name = parts[2]
    
    # 提取描述（在最後的引號中）
    desc_match = re.search(r',"(.+)"$', line.strip())
    spanish_desc = desc_match.group(1) if desc_match else ""
    
    # 翻譯招式名稱
    if spanish_name in COMPLETE_MOVE_TRANSLATIONS:
        chinese_name = COMPLETE_MOVE_TRANSLATIONS[spanish_name]
    else:
        chinese_name = spanish_name
        missing_translations.append(f"第{i}行: {spanish_name}")
    
    # 翻譯描述
    chinese_desc = apply_glossary(spanish_desc)
    
    # 重建行
    new_line_parts = parts[:2] + [chinese_name] + parts[3:-1]
    new_line = ','.join(new_line_parts) + f',"{chinese_desc}"\n'
    
    translated_lines.append(new_line)
    
    if i % 100 == 0:
        print(f'處理進度：{i}/{len(lines)} ({i/len(lines)*100:.1f}%)')

# 寫入檔案
output_path = Path('localization/translations/pbs/moves.txt')
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, 'w', encoding='utf-8-sig') as f:
    f.writelines(translated_lines)

print(f'\n✓ 完成！翻譯檔案已儲存至：{output_path}')
print(f'✓ 總共翻譯 {len(translated_lines)} 行')

if missing_translations:
    print(f'\n⚠ 仍有 {len(missing_translations)} 個招式名稱未找到翻譯：')
    for msg in missing_translations[:10]:
        print(f'  - {msg}')
    if len(missing_translations) > 10:
        print(f'  ... 還有 {len(missing_translations) - 10} 個')
