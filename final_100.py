# -*- coding: utf-8 -*-
import re
from pathlib import Path

FINAL_ALL_MOVES = {
    "Danza Amiga": "找伙伴", "Campana Cura": "治愈鈴聲", "Aullido": "長嚎",
    "Beso Amoroso": "迷人之吻", "Yo Primero": "搶先一步", "Batido": "喝牛奶",
    "Luz Lunar": "月光", "Sol Matinal": "晨光", "Clonatipo": "反射屬性",
    "Alivio": "煥然一新", "Cara Susto": "鬼面", "Chirrido": "刺耳聲",
    "Rompecoraza": "破殼", "Onda Simple": "單純光束", "Esquema": "寫生",
    "Amortiguador": "生蛋", "Salpicadura": "躍起", "Reserva": "蓄力",
    "Tragar": "吞下", "Beso Dulce": "天使之吻", "Dulce Aroma": "甜甜香氣",
    "Danza Espada": "劍舞", "Látigo": "搖尾巴", "Danza Caos": "搖晃舞",
    "Cosquillas": "搔癢", "Remolino": "吹飛", "Transformación": "變身",
    "Deseo": "祈願", "Avivar": "自我激勵", "Bostezo": "哈欠",
    "Acua Aro": "水流環", "Danza Llama": "火之舞", "Fogonazo": "日光束",
    "Lluevehojas": "飛葉風暴", "Planta Feroz": "瘋狂植物",
    "Llama Fusión": "交錯火焰", "Bomba Ígnea": "火焰彈", "Patada Ígnea": "火焰踢",
    "Voto Fuego": "火之誓約", "Calcinación": "燒盡", "Golpe Calor": "高溫重壓",
    "Día Soleado": "大晴天", "Fuego Fatuo": "鬼火", "Aerochorro": "空氣斬",
    "Bote": "彈跳", "Cháchara": "嘮叨", "Aire Afilado": "空氣利刃",
    "Danza Pluma": "羽毛舞", "Mov. Espejo": "鏡面屬性", "Viento Afín": "順風",
    "Golpe Umbrío": "暗影擊", "Garra Umbría": "暗影爪", "Vien. Aciago": "不祥之風",
    "Sombra Vil": "暗影偷襲", "Impresionar": "驚嚇", "Rayo Confuso": "奇異之光",
    "Mismodestino": "同命", "Pesadilla": "惡夢", "Danza Pétalo": "花瓣舞",
    "Fuegosagrado": "神聖之火"
}

with open('PBS/moves.txt', 'r', encoding='utf-8-sig') as f:
    es_lines = f.readlines()

with open('localization/translations/pbs/moves.txt', 'r', encoding='utf-8-sig') as f:
    cn_lines = f.readlines()

es_to_cn = {}
for es_l, cn_l in zip(es_lines, cn_lines):
    if not es_l.strip():
        continue
    es_p = es_l.strip().split(',')
    cn_p = cn_l.strip().split(',')
    if len(es_p) >= 3 and len(cn_p) >= 3:
        es_to_cn[es_p[2]] = cn_p[2]

es_to_cn.update(FINAL_ALL_MOVES)

output = []
done = 0
left = []

for es_l in es_lines:
    if not es_l.strip():
        output.append(es_l)
        continue
    
    p = es_l.strip().split(',')
    if len(p) < 13:
        output.append(es_l)
        continue
    
    mid, internal, es_name = p[0], p[1], p[2]
    desc = re.search(r',"(.+)"$', es_l.strip())
    desc = desc.group(1) if desc else ''
    
    cn_name = es_to_cn.get(es_name, es_name)
    if cn_name != es_name:
        done += 1
    else:
        left.append(f'#{mid} {internal}: {es_name}')
    
    new = ','.join(p[:2] + [cn_name] + p[3:-1]) + f',"{desc}"\n'
    output.append(new)

from pathlib import Path
out = Path('localization/translations/pbs/moves.txt')
with open(out, 'w', encoding='utf-8-sig') as f:
    f.writelines(output)

pct = done/631*100
print(f'✅ 翻譯完成！')
print(f'   已翻譯：{done} / 631 ({pct:.2f}%)')
print(f'   保留：{len(left)}')
if left:
    print(f'\n剩餘清單：')
    for x in left[:20]:
        print(f'   {x}')
else:
    print(f'\n🎉 100% 完成！')
print(f'\n📁 {out}')
