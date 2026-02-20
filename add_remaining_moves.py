import json

# 剩餘未翻譯招式的補充翻譯
ADDITIONAL_MOVES = {
    "Llama Fusión": "交錯火焰",
    "Fuegosagrado": "神聖之火",
    "Bomba Ígnea": "火焰彈",
    "Patada Ígnea": "火焰踢",
    "Danza Llama": "火之舞",
    "Colm. Ígneo": "火焰牙",
    "Voto Fuego": "火之誓約",
    "Calcinación": "燒盡",
    "Golpe Calor": "熱沖擊",
    "Día Soleado": "大晴天",
    "Fuego Fatuo": "鬼火",
    "Aerochorro": "噴射",
    "Bote": "彈跳",
    "Cháchara": "嘮叨",
    "Aire Afilado": "空氣利刃",
    "Danza Pluma": "羽舞",
    "Mov. Espejo": "鏡面屬性",
    "Viento Afín": "順風",
    "Golpe Umbrío": "暗影擊",
    "Garra Umbría": "暗影爪",
    "Vien. Aciago": "不祥之風",
    "Sombra Vil": "暗影偷襲",
    "Impresionar": "驚嚇",
    "Rayo Confuso": "奇異之光",
    "Mismodestino": "同命",
    "Pesadilla": "惡夢",
    "Planta Feroz": "瘋狂植物",
    "Lluevehojas": "飛葉風暴",
    "Danza Pétalo": "花瓣舞",
    "Fogonazo": "日光束",
    "Tormenta Hojas": "葉暴",
    "Látigo Ced": "藤鞭",
    "Hoja Aguda": "葉刃",
    "Energibola": "能量球",
    "Esfera Foliar": "能量球",
    "Perforador": "種子機關槍",
    "Hoja Oscura": "暗葉風暴",
    "Semilla": "種子炸彈",
    "Serradora": "葉刃",
    "Aladrón": "寄生種子",
    "Lluvia de Hoja": "落葉風暴",
    "Beso Hierba": "草之誓約",
    "Poder Tierra": "大地神力",
    "Gravedad Terrestre": "地球上投",
    "Trampa Arena": "流沙地獄",
    "Rayo Confuso": "奇異之光",
    "Beso Hielo": "冰凍之吻",
    "Rayo Helado": "冰凍光束",
    "Bruma": "白霧",
    "Deflagración": "過熱",
    "Sísmica": "大地神力",
    "Derrumbe": "岩崩",
    "Pedrada": "落石",
    "Roca Dentada": "尖石攻擊",
    "Guardia Baja": "看穿",
    "Baile Dragón": "龍之舞",
    "Vaho": "龍息",
    "Dragofuria": "龍之怒",
    "Lazo": "捆綁",
    "Constricción": "緊束",
    "Lazo": "束縛",
    "Amarre": "綁緊",
    "Transformación": "變身",
    "Doble Equipo": "影子分身",
    "Reducción": "縮小",
    "Pantalla Humo": "煙幕",
    "Destello": "奇異之光",
    "Rayo": "十萬伏特",
    "Rayo Aurora": "極光束",
    "Doblebofetón": "連環巴掌",
    "Golpescorpónicos": "連續拳",
    "Rayo Solar": "日光束",
    "Ataque Rápido": "電光一閃",
    "Rayo Carga": "充電光束",
    "Destructor": "破壞光線",
    "Enfado": "逆鱗",
    "Placaje": "衝擊",
    "Látigo": "搖尾巴",
    "Picoteo": "啄",
    "Vuelo": "飛翔",
    "Vendaval": "暴風",
    "Surf": "衝浪",
    "Rayo Hielo": "冰凍光束",
    "Ventisca": "暴風雪",
    "Psíquico": "精神強念",
    "Amnesia": "失憶",
    "Psicorrayo": "幻象術",
    "Hipnosis": "催眠術",
    "Meditación": "瑜伽姿勢",
    "Agilidad": "高速移動",
    "Teletransporte": "瞬間移動",
    "Reflejo": "反射壁",
    "Descanso": "睡覺",
    "Confusión": "念力",
    "Pantalla de Luz": "光牆",
    "Onda Mental": "精神擊破",
    "Barrera": "屏障",
    "Intercambio": "特性互換",
    "Terremoto": "地震",
    "Fisura": "地裂",
    "Excavar": "挖洞",
    "Tóxico": "劇毒",
    "Picotazo Veneno": "毒針",
    "Doble Filo": "雙刃頭槌",
    "Megacuerno": "超級角擊",
    "Hiperrayo": "破壞光線",
    "Malicioso": "瞪眼",
    "Gruñido": "叫聲",
    "Rugido": "吼叫",
    "Canto": "唱歌",
    "Supersónico": "超音波",
    "Sónico": "音爆",
    "Desactivar": "定身法",
    "Ácido": "溶解液",
    "Ascuas": "火花",
    "Lanzallamas": "噴射火焰",
    "Niebla": "白霧",
    "Pistola de Agua": "水槍",
    "Hidrobomba": "水炮",
    "Surf": "衝浪",
    "Rayo Hielo": "冰凍光束",
    "Ventisca": "暴風雪",
    "Psíquico": "精神強念",
    "Hipnosis": "催眠術",
    "Meditación": "瑜伽姿勢",
    "Teletransporte": "瞬間移動",
    "Confusión": "念力",
    "Puño Fuego": "火焰拳",
    "Puño Hielo": "冰凍拳",
    "Puño Trueno": "雷電拳",
    "Garra Metal": "金屬爪",
    "Garra Dragón": "龍爪",
    "Ala de Acero": "鋼翼",
    "Gigadrenado": "終極吸取",
    "Bomba Lodo": "污泥炸彈",
    "Rayo": "十萬伏特",
    "Trueno": "打雷",
    "Terremoto": "地震",
    "Excavar": "挖洞",
    "Ventisca": "暴風雪",
    "Rayo Hielo": "冰凍光束",
    "Psíquico": "精神強念",
    "Amnesia": "失憶",
    "Descanso": "睡覺",
    "Sustituto": "替身",
    "Hidro Bomba": "水炮",
    "Surf": "衝浪",
    "Vel Extrema": "神速",
    "Rayo": "十萬伏特",
    "Cuchillada": "劈開",
    "Cornada": "角撞",
    "Látigo": "搖尾巴",
    "Mordisco": "咬住",
    "Rugido": "吼叫",
    "Canto": "唱歌",
    "Supersónico": "超音波",
    "Gruñido": "叫聲",
    "Ataque Rápido": "電光一閃",
    "Doble Equipo": "影子分身",
    "Recuperación": "自我再生",
    "Endurecimiento": "變硬",
    "Minimizar": "縮小",
    "Pantalla de Humo": "煙幕",
    "Onda Confusa": "奇異之光",
    "Refugio": "縮入殼中",
    "Rizo Defensa": "變圓",
    "Barrera": "屏障",
    "Pantalla de Luz": "光牆",
    "Neblina": "白霧",
    "Reflejo": "反射壁",
    "Foco Energía": "聚氣",
    "Amnesia": "失憶",
    "Agilidad": "高速移動",
    "Descanso": "睡覺",
    "Sustituto": "替身",
    "Espada Atronadora": "雷劍",
    "Tijera": "剪刀十字拳",
    "Carga Semilla": "種子炸彈",
    "Ultratumba": "暗影擊",
    "Cambio Poder": "力量戲法",
    "Raíz": "扎根",
    "Anclaje": "扎根",
    "Cambio Almas": "心靈互換",
    "Ventisca de Pétalos": "落英繽紛",
    "Canto Mortal": "絕命",
    "Rayo Carga": "充電光束",
    "Cometa Fuego": "彗星拳",
    "Eructo": "打嗝",
    "Puño Inc": "增強拳",
    "Acua Aro": "水流環",
    "Imán Aéreo": "電磁飄浮",
    "Poder Pasado": "輔助力量",
    "Púas Tóxicas": "毒菱",
    "Meteorobola": "陀螺球",
    "Onda Certera": "波導彈",
    "Puño Certero": "真氣拳",
    "Sorpresa": "驚嚇",
    "A Bocajarro": "近身戰",
    "Envite Llamas": "閃焰衝鋒",
    "Viento Hielo": "冰凍之風",
    "Tormenta de Arena": "沙暴",
    "Latigazo": "強力鞭打",
    "Cambio de Fuerza": "力量互換",
    "Tinieblas": "暗影球",
    "Cortina de Humo": "煙幕",
    "Danza Dragón": "龍之舞",
    "Rayo Gélido": "冰凍光束",
    "Pulso Dragón": "龍之波動",
    "Deflagración": "過熱",
    "Cambio Banda": "交換場地",
    "Puño Incremento": "增強拳",
    "Diamante Tormenta": "鑽石風暴",
    "Llama Azul": "青焰"
}

# 更新主翻譯檔案
with open('PBS/moves.txt', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

# 載入當前完整字典
import sys
sys.path.append('.')

from complete_moves_translator import MOVES_FULL

# 合併翻譯
ALL_MOVES = {**MOVES_FULL, **ADDITIONAL_MOVES}

output_lines = []
translated = 0
still_missing = []

for line in lines:
    if not line.strip():
        output_lines.append(line)
        continue
    
    parts = line.strip().split(',')
    if len(parts) < 13:
        output_lines.append(line)
        continue
    
    move_id, internal, spanish_name = parts[0], parts[1], parts[2]
    
    desc_match = __import__('re').search(r',"(.+)"$', line.strip())
    spanish_desc = desc_match.group(1) if desc_match else ""
    
    if spanish_name in ALL_MOVES:
        chinese_name = ALL_MOVES[spanish_name]
        translated += 1
    else:
        chinese_name = spanish_name
        still_missing.append((move_id, spanish_name))
    
    chinese_desc = spanish_desc
    
    new_parts = parts[:2] + [chinese_name] + parts[3:-1]
    new_line = ','.join(new_parts) + f',"{chinese_desc}"\n'
    
    output_lines.append(new_line)

# 輸出
from pathlib import Path
output_path = Path('localization/translations/pbs/moves.txt')
with open(output_path, 'w', encoding='utf-8-sig') as f:
    f.writelines(output_lines)

print(f"✓ 完成！")
print(f"  已翻譯：{translated} / 631 個招式 ({translated/631*100:.1f}%)")
print(f"  仍未翻譯：{len(still_missing)} 個")

if len(still_missing) <= 30:
    print("\n剩餘未翻譯：")
    for mid, name in still_missing:
        print(f"  #{mid}: {name}")
