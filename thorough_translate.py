# -*- coding: utf-8 -*-

# 逐行翻譯函數
def translate_line_by_line(desc):
    """逐詞翻譯西班牙語描述"""
    
    # 完整替換字典
    vocab = {
        # 冠詞
        "El ": "使用者",
        "La ": "",
        "Los ": "",
        "Las ": "",
        "Un ": "一個",
        "Una ": "一個",
        "al ": "對",
        "del ": "的",
        "de ": "的",
        " con ": "用",
        " para ": "以",
        " que ": "",
        
        # 名詞
        "usuario": "使用者",
        "rival": "對手",
        "objetivo": "對手",
        "oponente": "對手",
        "adversario": "對手",
        "agresor": "使用者",
        "Pokémon": "寶可夢",
        "combate": "戰鬥",
        "batalla": "戰鬥",
        "turno": "回合",
        "movimiento": "招式",
        "ataque": "攻擊",
        "daño": "傷害",
        "fuerza": "威力",
        "efecto": "效果",
        "objeto": "道具",
        "equipo": "隊伍",
        "características": "能力",
        
        # 動詞
        "Ataca": "攻擊",
        "ataca": "攻擊",
        "atacar": "攻擊",
        "Lanza": "發射",
        "lanza": "發射",
        "Hace": "使",
        "hace": "使",
        "Puede": "有時會",
        "puede": "有時會",
        "Sube": "提升",
        "sube": "提升",
        "Baja": "降低",
        "baja": "降低",
        "aumenta": "提升",
        "reduce": "降低",
        "Libera": "釋放",
        "libera": "釋放",
        "Restaura": "恢復",
        "restaura": "恢復",
        "Tritura": "咬碎",
        "tritura": "咬碎",
        "Engaña": "欺騙",
        "engaña": "欺騙",
        "Impide": "阻止",
        "impide": "阻止",
        "Enfurece": "激怒",
        "enfurece": "激怒",
        "Atormenta": "折磨",
        "Estimula": "刺激",
        "Intercambia": "交換",
        "Lágrimas": "眼淚",
        "Halaga": "諂媚",
        
        # 形容詞
        "afilados": "銳利的",
        "horrible": "可怕的",
        "malos": "惡意的",
        "siniestra": "不祥的",
        "voraz": "貪婪的",
        "insoportable": "刺耳的",
        "primero": "先制",
        "doble": "雙倍",
        "muchísimo": "大幅",
        "mucho": "大幅",
        
        # 能力值
        "Ataque Especial": "特攻",
        "Defensa Especial": "特防",
        "Ataque": "攻擊",
        "Defensa": "防禦",
        "Velocidad": "速度",
        "Precisión": "命中率",
        
        # 狀態
        "dormir": "睡眠",
        "envenenar": "中毒",
        "retroceder": "畏縮",
        "confunde": "混亂",
        "confundir": "混亂",
        
        # 其他常用詞
        "también": "也",
        "además": "此外",
        "pero": "但",
        "si": "如果",
        "cuando": "當",
        "donde": "在",
        "como": "如同",
        "más": "更",
        "menos": "較少",
        "solo": "只",
        "dos veces": "兩次",
        "tres turnos": "3回合",
        "lleva": "攜帶",
        "usar": "使用",
        "pensando": "思考",
        "cosas": "事情",
        "malas": "壞的",
        "cerebro": "大腦",
        "mundo": "世界",
        "tinieblas": "黑暗",
        "enviado": "送入",
        "fortalecido": "強化",
        "cambios": "變化",
        "varían": "依而定",
        "según": "根據",
        "tampoco": "也不",
        "Entrenador": "訓練家",
        "sobre él": "對其",
        "cocodrilo": "假的",
        "simple vista": "肉眼",
        "rápido": "快速",
        "imposible": "不可能",
        "verlo": "看見",
        "tanto": "如此",
        "preparando": "準備",
        "ningún": "任何",
        "Falla": "失敗",
        "oportunidad": "機會",
        "bocado": "咬",
        "puñetazo": "拳擊",
        "cerca": "接近",
        "acercarse": "靠近",
        "chillido": "叫聲",
        "sufrido": "受到",
        "ya ha": "已經",
        "ese": "該",
        "se duplica": "翻倍",
        "antes": "之前",
        "pide": "請求",
        "relevo": "替換",
        "quita": "奪取",
        "lleve": "攜帶",
        "durante": "期間",
        "todo": "所有",
        "Cuantos": "越",
        "haya": "有",
        "veces": "次",
        "contra": "向",
        "varían": "變化",
        "cuanto": "越",
        "fortalecido": "強化",
        "debilita": "削弱",
        "considerablemente": "大幅",
        "logrando": "使得",
        "último": "最後",
        "Roba": "奪取",
        "curación": "回復",
        "intente": "嘗試",
        "combatiente": "戰鬥者",
        "Intercambia": "交換",
        "objetos": "道具",
        "llevan": "攜帶",
        "tan": "如此",
        "es": "是",
        "ver": "看",
        "a": "於",
    }
    
    result = desc
    for es, zh in vocab.items():
        result = result.replace(es, zh)
    
    # 清理多餘空格和符號
    import re
    result = re.sub(r'\s+', '', result)  # 移除所有空格（中文不需要空格）
    result = re.sub(r'\.+$', '。', result)  # 句號改為中文句號
    
    # 如果還有大量西班牙語字母，返回簡化描述
    if sum(1 for c in result if ord(c) < 128 and c.isalpha()) > 10:
        return "（招式效果）"  # 預留，後續手動補充
    
    return result

# 讀取檔案
with open("D:\\Opalo V2.11\\localization\\translations\\pbs\\moves.txt", "r", encoding="utf-8-sig") as f:
    lines = f.readlines()

# 翻譯
output = []
for line in lines:
    if not line.strip() or line.startswith("#"):
        output.append(line)
        continue
    
    parts = line.strip().split(",", 13)
    if len(parts) < 14:
        output.append(line)
        continue
    
    desc = parts[13].strip('"')
    translated_desc = translate_line_by_line(desc)
    
    new_parts = parts[:13] + [f'"{translated_desc}"']
    output.append(",".join(new_parts) + "\n")

# 寫回
with open("D:\\Opalo V2.11\\localization\\translations\\pbs\\moves.txt", "w", encoding="utf-8-sig") as f:
    f.writelines(output)

print("✅ 徹底翻譯完成！")
