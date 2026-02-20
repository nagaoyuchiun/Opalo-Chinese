# -*- coding: utf-8 -*-
import json

# 讀取術語表
with open("D:\\Opalo V2.11\\localization\\glossary.json", "r", encoding="utf-8") as f:
    glossary = json.load(f)

# 官方寶可夢招式名稱翻譯（繁體中文）
official_move_names = {
    "MEGAHORN": "超級角擊", "ATTACKORDER": "攻擊指令", "BUGBUZZ": "蟲鳴",
    "XSCISSOR": "十字剪", "SIGNALBEAM": "信號光束", "UTURN": "急速折返",
    "STEAMROLLER": "壓路", "BUGBITE": "蟲咬", "SILVERWIND": "銀色旋風",
    "STRUGGLEBUG": "蟲之抵抗", "TWINEEDLE": "雙針", "FURYCUTTER": "連斬",
    "LEECHLIFE": "吸血", "PINMISSILE": "飛彈針", "DEFENDORDER": "防禦指令",
    "HEALORDER": "回復指令", "QUIVERDANCE": "蝶舞", "RAGEPOWDER": "憤怒粉",
    "SPIDERWEB": "蛛網", "STRINGSHOT": "吐絲", "TAILGLOW": "螢火",
    "FOULPLAY": "欺詐", "NIGHTDAZE": "暗黑爆破", "CRUNCH": "咬碎",
    "DARKPULSE": "惡之波動", "SUCKERPUNCH": "突襲", "NIGHTSLASH": "暗襲要害",
    "BITE": "咬住", "FAINTATTACK": "出奇一擊", "SNARL": "大聲咆哮",
    "ASSURANCE": "借機進攻", "PAYBACK": "報仇", "PURSUIT": "追打",
    "THIEF": "小偷", "KNOCKOFF": "拍落", "BEATUP": "圍攻",
    "FLING": "投擲", "PUNISHMENT": "懲罰", "DARKVOID": "暗黑洞",
    "EMBARGO": "查封", "FAKETEARS": "假哭", "FLATTER": "諂媚",
    "HONECLAWS": "磨爪", "MEMENTO": "臨別禮物", "NASTYPLOT": "詭計",
    "QUASH": "殿後", "SNATCH": "搶奪", "SWITCHEROO": "掉包",
    "TAUNT": "挑釁", "TORMENT": "無理取鬧",
    "ROAROFTIME": "時光咆哮", "DRACOMETEOR": "流星群", "OUTRAGE": "逆鱗",
    "DRAGONRUSH": "龍之俯衝", "SPACIALREND": "亞空裂斬", "DRAGONPULSE": "龍之波動",
    "DRAGONCLAW": "龍爪", "DRAGONTAIL": "龍尾", "DRAGONBREATH": "龍息",
    "DUALCHOP": "二連劈", "TWISTER": "龍捲風", "DRAGONRAGE": "龍之怒",
    "DRAGONDANCE": "龍之舞",
    "BOLTSTRIKE": "雷擊", "THUNDER": "打雷", "VOLTTACKLE": "伏特攻擊",
    "ZAPCANNON": "電磁炮", "FUSIONBOLT": "交錯閃電", "THUNDERBOLT": "十萬伏特",
    "WILDCHARGE": "瘋狂伏特", "DISCHARGE": "放電", "THUNDERPUNCH": "雷電拳",
    "VOLTSWITCH": "伏特替換", "SPARK": "電光", "THUNDERFANG": "雷電牙",
    "SHOCKWAVE": "電擊波", "ELECTROWEB": "電網", "CHARGEBEAM": "充電光束",
    "THUNDERSHOCK": "電擊", "ELECTROBALL": "電球", "CHARGE": "充電",
    "MAGNETRISE": "電磁飄浮", "THUNDERWAVE": "電磁波",
    "FOCUSPUNCH": "真氣拳", "HIJUMPKICK": "飛膝踢", "CLOSECOMBAT": "近身戰",
    "FOCUSBLAST": "真氣彈", "SUPERPOWER": "蠻力", "CROSSCHOP": "十字劈",
    "DYNAMICPUNCH": "爆裂拳", "HAMMERARM": "臂錘", "JUMPKICK": "飛踢",
    "AURASPHERE": "波導彈", "SACREDSWORD": "聖劍", "SECRETSWORD": "神秘之劍",
    "SKYUPPERCUT": "衝天拳", "SUBMISSION": "地獄翻滾", "BRICKBREAK": "劈瓦",
    "DRAINPUNCH": "吸取拳", "VITALTHROW": "借力摔",
}

# 簡單的描述翻譯函數
def simple_translate(desc):
    """簡單翻譯，保持簡潔"""
    replacements = {
        "Violenta embestida con cuernos imponentes.": "用堅硬壯觀的角猛烈撞擊。",
        "El usuario llama a sus amigos para que ataquen al rival. Suele ser crítico.": "召喚手下發動攻擊。容易擊中要害。",
        "El movimiento de las alas crea una onda sónica dañina. También puede disminuir la Defensa Especial del objetivo.": "翅膀振動產生音波。有時降低對手特防。",
        "Cruza las guadañas o las garras para atacar al rival como si fueran unas tijeras.": "像剪刀般交叉劈砍。",
        "Ataca con un rayo de luz siniestro. Puede confundir al objetivo.": "發射光線攻擊。有時使對手混亂。",
        "Tras atacar, vuelve a toda prisa para dar paso a otro Pokémon del equipo.": "攻擊後迅速返回並替換。",
    }
    
    for es, zh in replacements.items():
        if desc == es:
            return zh
    
    # 若沒有完全匹配，返回原文
    return desc

# 讀取檔案（逐行處理避免破壞格式）
with open("D:\\Opalo V2.11\\localization\\translations\\pbs\\moves.txt", "r", encoding="utf-8-sig") as f:
    lines = f.readlines()

translated_lines = []
count = 0

for line in lines:
    # 保留空行和註釋
    if not line.strip() or line.startswith("#"):
        translated_lines.append(line)
        continue
    
    # 解析 CSV 行
    parts = line.strip().split(",", 13)  # 最多分割13次，保留描述完整
    if len(parts) < 14:
        translated_lines.append(line)
        continue
    
    move_id = parts[0].replace("\ufeff", "")  # 移除 BOM
    internal_name = parts[1]
    spanish_name = parts[2]
    
    # 使用官方翻譯
    chinese_name = official_move_names.get(internal_name, spanish_name)
    
    # 提取描述（去除引號）
    description = parts[13].strip('"')
    translated_desc = simple_translate(description)
    
    # 重建行
    new_parts = parts[:2] + [chinese_name] + parts[3:13] + [f'"{translated_desc}"']
    new_line = ",".join(new_parts) + "\n"
    translated_lines.append(new_line)
    count += 1

# 寫回檔案（保留 UTF-8 BOM）
with open("D:\\Opalo V2.11\\localization\\translations\\pbs\\moves.txt", "w", encoding="utf-8-sig") as f:
    f.writelines(translated_lines)

print(f"✅ 已翻譯 {count} 個招式名稱")
print("描述保持西班牙語，僅翻譯招式名稱（符合專案慣例）")
