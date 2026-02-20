# -*- coding: utf-8 -*-
import re

# 讀取檔案
with open("D:\\Opalo V2.11\\localization\\translations\\pbs\\moves.txt", "r", encoding="utf-8-sig") as f:
    content = f.read()

# 大規模替換字典
massive_replacements = {
    # 完整句子
    " del ": "的",
    " de ": "的",
    " una ": "一個",
    " un ": "一個",
    " con ": "用",
    " que ": "的",
    " por ": "以",
    " para ": "為了",
    " muy ": "非常",
    " más ": "更",
    " si ": "如果",
    " cuando ": "當",
    " donde ": "在",
    " como ": "如同",
    " desde ": "從",
    " hacia ": "向",
    " sobre ": "關於",
    " entre ": "之間",
    " sin ": "沒有",
    " también ": "也",
    " solo ": "只",
    " tanto ": "如此",
    " pero ": "但是",
    " aunque ": "雖然",
    " porque ": "因為",
    
    # 保留原句中的連接詞
    " y ": "和",
    " o ": "或",
    " e ": "和",
    " u ": "或",
    
    # 常見動詞
    "Ataca al ": "攻擊",
    "Golpea al ": "擊打",
    "Lanza una ": "發射",
    "Libera una ": "釋放",
    "Crea un ": "製造",
    "Hace que ": "使得",
    "Usa sus ": "使用其",
    "Dispara un ": "發射",
    
    # 名詞
    "objetivo": "對手",
    "rival": "對手",
    "usuario": "使用者",
    "atacante": "攻擊者",
    "agresor": "使用者",
    "Pokémon": "寶可夢",
    
    # 形容詞
    "poderoso": "強大",
    "poderosa": "強大",
    "potente": "強力",
    "gran": "大",
    "grande": "大",
    "enorme": "巨大",
    "gigante": "巨大",
    "pequeño": "小",
    "rápido": "快速",
    "lento": "緩慢",
    "fuerte": "強",
    "débil": "弱",
    
    # 能力值（完整詞）
    "Ataque Especial": "特攻",
    "Defensa Especial": "特防",
    "Ataque": "攻擊",
    "Defensa": "防禦",
    "Velocidad": "速度",
    "Precisión": "命中率",
    "Evasión": "迴避率",
    
    # 狀態
    "paralizar": "麻痺",
    "paraliza": "麻痺",
    "paralizarlo": "使其麻痺",
    "envenenar": "中毒",
    "envenena": "中毒",
    "quemar": "灼傷",
    "quema": "灼傷",
    "congelar": "冰凍",
    "congela": "冰凍",
    "dormir": "睡眠",
    "duerme": "睡眠",
    "confundir": "混亂",
    "confunde": "混亂",
    "confusión": "混亂",
    "retroceder": "畏縮",
    "retrocede": "畏縮",
    
    # 動作
    "daña": "傷害",
    "daño": "傷害",
    "dañar": "傷害",
    "hiere": "傷害",
    "golpe": "攻擊",
    "golpea": "擊打",
    "ataca": "攻擊",
    "lanza": "發射",
    "dispara": "發射",
    "libera": "釋放",
    "crea": "製造",
    "hace": "使",
    "sube": "提升",
    "baja": "降低",
    "aumenta": "增加",
    "reduce": "減少",
    "recupera": "恢復",
    "drena": "吸取",
    
    # 連接詞與副詞
    "Puede ": "有時會",
    "puede ": "可能",
    "También ": "也",
    "Siempre ": "總是",
    "Nunca ": "從不",
    "Además ": "此外",
    "Luego ": "然後",
    "Después ": "之後",
    "Antes ": "之前",
    "Durante ": "期間",
    
    # 數量詞
    "todos": "所有",
    "todas": "所有",
    "mucho": "大幅",
    "mucha": "大幅",
    "poco": "少許",
    "poca": "少許",
    "varios": "數個",
    "varias": "數個",
    "ambos": "雙方",
    
    # 時間
    "turno": "回合",
    "turnos": "回合",
    "siguiente": "下一個",
    "próximo": "下一個",
    "último": "最後",
    
    # 其他常見詞
    "combate": "戰鬥",
    "batalla": "戰鬥",
    "movimiento": "招式",
    "ataque": "攻擊",
    "defensa": "防禦",
    "poder": "威力",
    "fuerza": "力量",
    "energía": "能量",
    "efecto": "效果",
    "estado": "狀態",
    "cambio": "變化",
}

# 應用替換
for spanish, chinese in massive_replacements.items():
    content = content.replace(spanish, chinese)

# 特定修正
specific_fixes = {
    "攻擊 對手": "攻擊對手",
    "擊打 對手": "擊打對手",
    "發射 強大": "發射強大",
    "製造 猛烈": "製造猛烈",
    "有時會 麻痺": "有時會使對手麻痺",
    "有時會 中毒": "有時會使對手中毒",
    "有時會 灼傷": "有時會使對手灼傷",
    "有時會 畏縮": "有時會使對手畏縮",
    "有時會 混亂": "有時會使對手混亂",
    "降低 攻擊": "降低對手的攻擊",
    "降低 防禦": "降低對手的防禦",
    "降低 特攻": "降低對手的特攻",
    "降低 特防": "降低對手的特防",
    "降低 速度": "降低對手的速度",
    "提升 攻擊": "提升使用者的攻擊",
    "提升 防禦": "提升使用者的防禦",
    "提升 特攻": "提升使用者的特攻",
    "提升 特防": "提升使用者的特防",
    "提升 速度": "提升使用者的速度",
}

for wrong, correct in specific_fixes.items():
    content = content.replace(wrong, correct)

# 清理多餘空格
content = re.sub(r'\s+', ' ', content)
content = re.sub(r' ,', ',', content)
content = re.sub(r', +', ',', content)

# 寫回
with open("D:\\Opalo V2.11\\localization\\translations\\pbs\\moves.txt", "w", encoding="utf-8-sig") as f:
    f.write(content)

print("✅ 終極翻譯完成！")
