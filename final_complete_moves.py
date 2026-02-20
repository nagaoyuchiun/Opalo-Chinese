# -*- coding: utf-8 -*-
import re
from pathlib import Path

# 最終補完：剩餘58個招式
FINAL_58_MOVES = {
    "Bomba Germen": "種子炸彈",
    "At. Rápido": "電光一閃",
    "Giro Rápido": "高速旋轉",
    "Clavo Cañón": "飛彈針",
    "Puño Cometa": "彗星拳",
    "Repetición": "纏繞",
    "Venganza": "忍耐",
    "Agarrón": "緊握",
    "Frustración": "遷怒",
    "Presente": "禮物",
    "Retribución": "報恩",
    "Bomba Sónica": "音爆",
    "Superdiente": "憤怒門牙",
    "Estrujón": "絞緊",
    "Acupresión": "穴位",
    "Cede Paso": "您先請",
    "Atracción": "迷人",
    "Ofrenda": "傳遞禮物",
    "Camuflaje": "保護色",
    "Seducción": "誘惑",
    "Conversión2": "紋理2",
    "Copión": "仿效",
    "Anulación": "定身法",
    "Señuelo": "看我嘛",
    "Profecía": "識破",
    "Deslumbrar": "蛇瞪眼",
    "Desarrollo": "生長",
    "Fijar Blanco": "鎖定",
    "Conjuro": "幸運咒語",
    "Mal de Ojo": "黑色目光",
    "Metrónomo": "揮指",
    "Telépata": "心之眼",
    "Divide Dolor": "分擔痛楚",
    "Más Psique": "自我暗示",
    "Reciclaje": "回收利用",
    "Afilar": "磨礪",
    "Relajo": "偷懶",
    "Sonámbulo": "夢話",
    "Pantallahumo": "煙幕",
    "Contoneo": "虛張聲勢",
    "Deseo": "祈願",
    "Joya de Luz": "力量寶石",
    "Desenrollar": "滾動",
    "Torm. Arena": "沙暴",
    "Deseo Oculto": "破滅之願",
    "Cola Férrea": "鐵尾",
    "Puño Meteoro": "彗星拳",
    "Bomba Imán": "磁鐵炸彈",
    "Puño Bala": "子彈拳",
    "Giro Bola": "陀螺球",
    "Def. Férrea": "鐵壁",
    "Eco Metálico": "金屬音",
    "Martillazo": "蟹鉗錘",
    "Concha Filo": "貝殼刃",
    "Pulpocañón": "章魚桶炮",
    "Aguijón Letal": "致命針刺",
    "Moflete Estático": "蹭蹭臉頰",
    "Carga Parábola": "拋物面充電"
}

# 載入先前的所有翻譯
from complete_moves_translator import MOVES_FULL
from add_remaining_moves import ADDITIONAL_MOVES

# 合併所有翻譯
ALL_MOVES_COMPLETE = {**MOVES_FULL, **ADDITIONAL_MOVES, **FINAL_58_MOVES}

print(f"總翻譯字典：{len(ALL_MOVES_COMPLETE)} 個招式")

# 處理檔案
with open('PBS/moves.txt', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

output_lines = []
translated_count = 0
untranslated_list = []

for line in lines:
    if not line.strip():
        output_lines.append(line)
        continue
    
    parts = line.strip().split(',')
    if len(parts) < 13:
        output_lines.append(line)
        continue
    
    move_id, internal, spanish_name = parts[0], parts[1], parts[2]
    
    desc_match = re.search(r',"(.+)"$', line.strip())
    spanish_desc = desc_match.group(1) if desc_match else ""
    
    # 翻譯招式名稱
    if spanish_name in ALL_MOVES_COMPLETE:
        chinese_name = ALL_MOVES_COMPLETE[spanish_name]
        translated_count += 1
    else:
        chinese_name = spanish_name
        untranslated_list.append(f"#{move_id} {internal}: {spanish_name}")
    
    # 保留描述（已進行術語替換）
    chinese_desc = spanish_desc
    
    # 重建行
    new_parts = parts[:2] + [chinese_name] + parts[3:-1]
    new_line = ','.join(new_parts) + f',"{chinese_desc}"\n'
    
    output_lines.append(new_line)

# 輸出
output_path = Path('localization/translations/pbs/moves.txt')
with open(output_path, 'w', encoding='utf-8-sig') as f:
    f.writelines(output_lines)

print(f"\n✅ 翻譯完成！")
print(f"   已翻譯：{translated_count} / 631 ({translated_count/631*100:.1f}%)")
print(f"   未翻譯：{len(untranslated_list)}")

if len(untranslated_list) > 0:
    print(f"\n⚠️  剩餘未翻譯招式：")
    for item in untranslated_list[:20]:
        print(f"   {item}")
    if len(untranslated_list) > 20:
        print(f"   ... 還有 {len(untranslated_list) - 20} 個")
else:
    print("\n�� 所有招式名稱已完整翻譯！")

print(f"\n📁 輸出檔案：{output_path}")
