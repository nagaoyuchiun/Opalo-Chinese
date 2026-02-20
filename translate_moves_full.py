# -*- coding: utf-8 -*-
import json
import re

# 讀取術語表
with open("D:\\Opalo V2.11\\localization\\glossary.json", "r", encoding="utf-8") as f:
    glossary = json.load(f)

# 建立西班牙語->繁體中文映射字典
term_map = {}
for category in glossary["categories"].values():
    if "terms" in category:
        for term in category["terms"]:
            if "es" in term and "zh_TW" in term:
                term_map[term["es"]] = term["zh_TW"]
    elif "subcategories" in category:
        for subcat in category["subcategories"].values():
            if "terms" in subcat:
                for term in subcat["terms"]:
                    if "es" in term and "zh_TW" in term:
                        term_map[term["es"]] = term["zh_TW"]

# 官方招式翻譯對照表 (第三世代～第七世代常見招式)
move_translations = {
    # Bug
    "MEGAHORN": "超級角擊", "ATTACKORDER": "攻擊指令", "BUGBUZZ": "蟲鳴",
    "XSCISSOR": "十字剪", "SIGNALBEAM": "信號光束", "UTURN": "急速折返",
    "STEAMROLLER": "壓路", "BUGBITE": "蟲咬", "SILVERWIND": "銀色旋風",
    "STRUGGLEBUG": "蟲之抵抗", "TWINEEDLE": "雙針", "FURYCUTTER": "連斬",
    "LEECHLIFE": "吸血", "PINMISSILE": "飛彈針", "DEFENDORDER": "防禦指令",
    "HEALORDER": "回復指令", "QUIVERDANCE": "蝶舞", "RAGEPOWDER": "憤怒粉",
    "SPIDERWEB": "蛛網", "STRINGSHOT": "吐絲", "TAILGLOW": "螢火",
    
    # Dark
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
    
    # Dragon
    "DRACOMETEOR": "流星群", "OUTRAGE": "逆鱗", "DRAGONPULSE": "龍之波動",
    "DRAGONCLAW": "龍爪", "SPACIALREND": "亞空裂斬", "ROAROFTIME": "時光咆哮",
    "DRAGONTAIL": "龍尾", "DRAGONBREATH": "龍息", "DRAGONRAGE": "龍之怒",
    "TWISTER": "龍捲風", "DUALCHOP": "二連劈", "DRAGONDANCE": "龍之舞",
    
    # Electric
    "THUNDER": "打雷", "THUNDERBOLT": "十萬伏特", "VOLTSWITCH": "伏特替換",
    "WILDCHARGE": "瘋狂伏特", "THUNDERPUNCH": "雷電拳", "DISCHARGE": "放電",
    "VOLTTACKLE": "伏特攻擊", "THUNDERSHOCK": "電擊", "SPARK": "電光",
    "THUNDERFANG": "雷電牙", "SHOCKWAVE": "電擊波", "ZAPCANNON": "電磁炮",
    "ELECTROWEB": "電網", "CHARGEBEAM": "充電光束", "PARABOLICCHARGE": "拋物充電",
    "CHARGE": "充電", "MAGNETRISE": "電磁飄浮", "THUNDERWAVE": "電磁波",
    
    # Fairy
    "MOONBLAST": "月亮之力", "PLAYROUGH": "嬉鬧", "DAZZLINGGLEAM": "魔法閃耀",
    "DRAININGKISS": "吸取之吻", "CHARM": "撒嬌", "DISARMINGVOICE": "魅惑之聲",
    "FAIRYWIND": "妖精之風", "BABYDOLLEYES": "圓瞳", "SWEETKISS": "天使之吻",
    "MOONLIGHT": "月光", "MISTYTERRAIN": "薄霧場地", "AROMATICMIST": "芳香薄霧",
    
    # Fighting
    "CLOSECOMBAT": "近身戰", "SUPERPOWER": "蠻力", "HIGHJUMPKICK": "飛膝踢",
    "AURASPHERE": "波導彈", "FOCUSBLAST": "真氣彈", "DRAINPUNCH": "吸取拳",
    "HAMMERARM": "臂錘", "DYNAMICPUNCH": "爆裂拳", "CROSSCHOP": "十字劈",
    "SKYUPPERCUT": "衝天拳", "BRICKBREAK": "劈瓦", "LOWKICK": "踢倒",
    "MACHPUNCH": "音速拳", "VITALTHROW": "借力摔", "SUBMISSION": "舍身撞擊",
    "KARATECHOP": "空手劈", "LOWSWEEP": "下盤踢", "CIRCLETHROW": "巴投",
    "STORMTHROW": "山嵐摔", "SACREDSWORD": "聖劍", "SECRETSWORD": "祕劍",
    "DOUBLEKICK": "二連踢", "TRIPPLEKICK": "連續踢", "ROLLINGKICK": "旋踢",
    "JUMPKICK": "飛踢", "REVERSAL": "起死回生", "REVENGE": "報復",
    "COUNTER": "雙倍奉還", "SEISMICTOSS": "地球上投", "FORCEPUNCH": "猛推",
    "BULKUP": "健美", "DETECT": "看穿", "QUICKGUARD": "快速防守",
    
    # Fire
    "FIREBLAST": "大字爆炎", "OVERHEAT": "過熱", "FLAREBLITZ": "閃焰衝鋒",
    "BLUEFLARE": "青焰", "SACREDFIRE": "神聖之火", "LAVAPLUME": "熔岩風暴",
    "ERUPTION": "噴火", "HEATWAVE": "熱風", "FLAMETHROWER": "噴射火焰",
    "FIREPUNCH": "火焰拳", "FIRESPIN": "火焰旋渦", "INFERNO": "煉獄",
    "FIREFANG": "火焰牙", "FLAMEBURST": "火焰彈", "FLAMECHARGE": "蓄能焰襲",
    "EMBER": "火花", "INCINERATE": "燒盡", "BLAZEKICK": "火焰踢",
    "FUSIONFLARE": "交錯火焰", "VCREATE": "V熱焰", "MAGMASTORM": "熔岩風暴",
    "WILLOWISP": "鬼火", "SUNNYDAY": "大晴天",
    
    # Flying
    "HURRICANE": "暴風", "BRAVEBIRD": "勇鳥猛攻", "SKY ATTACK": "神鳥猛擊",
    "AERIALACE": "燕返", "AIRCUTTER": "空氣利刃", "AIRSLASH": "空氣斬",
    "ACROBATICS": "雜技", "PLUCK": "啄食", "DRILLPECK": "啄鑽",
    "PECK": "啄", "WINGATTACK": "翅膀攻擊", "BOUNCE": "彈跳",
    "FLY": "飛翔", "SKYDROP": "自由落體", "GUST": "起風",
    "DEFOG": "清除濃霧", "ROOST": "羽棲", "TAILWIND": "順風",
    "FEATHERDANCE": "羽毛舞",
    
    # Ghost  
    "SHADOWFORCE": "暗影潛襲", "SHADOWBALL": "暗影球", "SHADOWCLAW": "暗影爪",
    "SHADOWPUNCH": "暗影拳", "SHADOWSNEAK": "影子偷襲", "OMINOUSWIND": "奇異之風",
    "HEX": "禍不單行", "NIGHTSHADE": "黑夜魔影", "CONFUSERAY": "奇異之光",
    "ASTONISH": "驚嚇", "LICK": "舌舔", "SPITE": "怨恨",
    "CURSE": "詛咒", "DESTINYBOND": "同命", "GRUDGE": "怨念",
    "TRICKORTREAT": "萬聖夜", "PHANTOMFORCE": "潛靈奇襲",
    
    # Grass
    "SOLARBEAM": "日光束", "WOODHAMMER": "木槌", "LEAFSTORM": "飛葉風暴",
    "POWERWHIP": "強力鞭打", "PETALDANCE": "花瓣舞", "SEEDFLARE": "種子閃光",
    "LEAFBLADE": "葉刃", "ENERGYBALL": "能量球", "GIGADRAIN": "終極吸取",
    "SEEDBOMB": "種子炸彈", "GRASSKNOT": "打草結", "MAGICALLEAF": "魔法葉",
    "RAZORLEAF": "飛葉快刀", "BULLETSEED": "種子機關槍", "NEEDLEARM": "尖刺臂",
    "VINEWHIP": "藤鞭", "ABSORB": "吸取", "MEGADRAIN": "超級吸取",
    "HORNLEECH": "木角", "LEAFAGE": "樹葉", "TROP KICK": "熱帶踢",
    "LEECHSEED": "寄生種子", "COTTONSPORE": "棉孢子", "STUNSPORE": "麻痺粉",
    "SLEEPPOWDER": "催眠粉", "POISONPOWDER": "毒粉", "SPORE": "蘑菇孢子",
    "WORRYSEED": "煩惱種子", "SYNTHESIS": "光合作用", "COTTONGUARD": "棉花防守",
    "INGRAIN": "扎根", "AROMATHERAPY": "芳香治療",
    
    # Ground
    "EARTHQUAKE": "地震", "EARTHPOWER": "大地之力", "DRILLRUN": "直衝鑽",
    "DIG": "挖洞", "BULLDOZE": "重踏", "MAGNITUDE": "震級",
    "BONEMERANG": "骨頭迴力鏢", "BONECLUB": "骨棒", "MUDBOMB": "泥巴炸彈",
    "MUDSPORT": "玩泥巴", "SANDATTACK": "潑沙", "MUDSHOT": "泥巴射擊",
    "MUDSLAP": "擲泥", "SANDTOMB": "流沙地獄", "SPIKES": "撒菱",
    "SANDSTORM": "沙暴",
    
    # Ice
    "BLIZZARD": "暴風雪", "ICEBEAM": "冰凍光束", "ICICLECRASH": "冰柱墜擊",
    "ICICLESPEAR": "冰錐", "FROSTBREATH": "冰息", "FREEZEDRY": "冷凍乾燥",
    "ICEPUNCH": "冰凍拳", "ICEFANG": "冰凍牙", "ICESHARD": "冰礫",
    "AVALANCHE": "雪崩", "AURORABEAM": "極光束", "GLACIATE": "冰凍世界",
    "POWDER SNOW": "細雪", "ICYWIND": "冰凍之風", "SHEERCOLD": "絕對零度",
    "MIST": "白霧", "HAZE": "黑霧", "HAIL": "冰雹",
    
    # Normal
    "HYPERBEAM": "破壞光線", "GIGAIMPACT": "超極衝擊", "EXPLOSION": "大爆炸",
    "SELFDESTRUCT": "自爆", "BODYSLAM": "泰山壓頂", "DOUBLEEDGE": "捨身衝撞",
    "RETURN": "報恩", "FRUSTRATION": "遷怒", "FACADE": "硬撐",
    "SLASH": "劈開", "STRENGTH": "怪力", "CRUSHCLAW": "撕裂爪",
    "SECRETPOWER": "秘密之力", "HEADBUTT": "頭錘", "TAKEDOWN": "猛撞",
    "THRASH": "大鬧一番", "DOUBLEHIT": "二連擊", "RAPIDSPIN": "高速旋轉",
    "HEADCHARGE": "雙倍攻擊", "CRUSHGRIP": "捏碎", "WRINGOUT": "絞緊",
    "ROCKCLIMB": "攀岩", "RETALIATE": "報仇", "GIGA IMPACT": "超極衝擊",
    "QUICKATTACK": "電光一閃", "EXTREMESPEED": "神速", "FEINT": "佯攻",
    "TACKLE": "撞擊", "POUND": "拍打", "SCRATCH": "抓", "VICEGRIP": "夾住",
    "FURYATTACK": "亂擊", "FURYSWIPES": "亂抓", "COMET PUNCH": "彗星拳",
    "CUT": "居合斬", "BIND": "綁緊", "WRAP": "緊束", "CONSTRICT": "縮緊",
    "BARRAGE": "投球", "EGGBOMB": "炸蛋", "HORNATTACK": "角撞",
    "HORNDRILL": "角鑽", "MEGAKICK": "百萬噸重踢", "MEGAPUNCH": "百萬噸重拳",
    "PAYDAY": "聚寶功", "TRIATTACK": "三重攻擊", "RAZORWIND": "旋風刀",
    "STOMP": "踩踏", "SPIKECANNON": "尖刺加農炮", "SLAM": "摔打",
    "SKULLBASH": "火箭頭錘", "DIZZY PUNCH": "迷昏拳", "CHIPAWAY": "識破",
    "ECHOEDVOICE": "回聲", "ENTRAINMENT": "找夥伴", "FALSESWIPE": "點到為止",
    "HEADSMASH": "雙刃頭錘", "LASTRESORT": "珍藏", "NATURALGIFT": "自然之力",
    "SKILLSWAP": "特性互換", "SUBSTITUTE": "替身", "SWORDSDANCE": "劍舞",
    "AGILITY": "高速移動", "DOUBLETEAM": "影分身", "RECOVER": "自我再生",
    "SOFTBOILED": "生蛋", "MINIMIZE": "變小", "SMOKESCREEN": "煙幕",
    "WITHDRAW": "縮入殼中", "DEFENSECURL": "變圓", "HARDEN": "變硬",
    "GROWL": "叫聲", "ROAR": "吼叫", "SING": "唱歌", "SUPERSONIC": "超音波",
    "SCREECH": "刺耳聲", "SHARPEN": "棱角化", "CONVERSION": "紋理",
    "CONVERSION2": "紋理2", "MIMIC": "模仿", "METRONOME": "揮指",
    "ENCORE": "再來一次", "SPLASH": "躍起", "TRANSFORM": "變身",
    "AMNESIA": "失憶", "MINDREADER": "心之眼", "LOCKON": "鎖定",
    "PROTECT": "守住", "BELLYDRUM": "腹鼓", "MILKDRINK": "喝牛奶",
    "PERISHSONG": "滅亡之歌", "ENDURE": "挺住", "SWAGGER": "虛張聲勢",
    "ATTRACT": "迷人", "SLEEPTALK": "夢話", "HEALBELL": "治癒鈴聲",
    "MORNINGSUN": "晨光", "BATONPASS": "接棒", "SAFEGUARD": "神秘守護",
    "SWEETSCENT": "甜甜香氣", "PAINSPLIT": "分擔痛楚", "SACREDFIRE": "神聖之火",
    "FOCUSENERGY": "聚氣", "FLASH": "閃光", "PSYCH UP": "自我暗示",
    "REFRESH": "煥然一新", "YAWN": "哈欠", "WISH": "祈願", "BLOCK": "擋路",
    "FOLLOWME": "看我嘛", "HELPINGHAND": "幫助", "MUDDY WATER": "濁流",
    "TICKLE": "撓癢", "SMELLINGSALTS": "清醒", "ODORSLEUTH": "氣味偵查",
    "SLACKOFF": "偷懶", "HOWL": "長嚎", "COVET": "渴望", "FEATHERDANCE": "羽毛舞",
    "TEETERDANCE": "搖晃舞", "WEATHERBALL": "氣象球", "SPIT UP": "噴出",
    "SWALLOW": "吞下", "STOCKPILE": "蓄力", "CAMOUFLAGE": "保護色",
    "TAILWHIP": "搖尾巴", "LEER": "瞪眼", "TRUMPCARD": "王牌",
    "WAKEUPSLAP": "喚醒巴掌", "ACUPRESSURE": "點穴", "POWERSHIFT": "力量互換",
    "GUARDSWAP": "防守互換", "POWERSWAP": "攻擊互換", "SPEEDSWAP": "速度互換",
    "MEFIRST": "搶先一步", "COPYCAT": "仿效", "PUNISHMENT": "懲罰",
    "LASTRESORT": "珍藏", "WRINGOUT": "絞緊", "CRUSHGRIP": "捏碎",
    "WORKUP": "自我激勵", "ROUND": "輪唱", "RETALIATE": "報仇",
    "AFTERYOU": "您先請", "SIMPLEBEAM": "單純光束", "ECHOEDVOICE": "回聲",
    "COIL": "盤蜷", "SHELLSMASH": "破殼", "SHIFTGEAR": "換檔",
    "STOREDPOWER": "輔助力量", "ELECTRIFY": "電氣化", "ROTOTILLER": "耕地",
    "HAPPYHOUR": "歡樂時光", "CELEBRATE": "慶祝", "HOLDHANDS": "牽手",
    "CONFIDE": "密語", "DIAMONDSTORM": "鑽石風暴", "HYPERSPACEFURY": "異次元猛攻",
    
    # Poison
    "GUNKSHOT": "垃圾射擊", "SLUDGEBOMB": "污泥炸彈", "SLUDGEWAVE": "污泥波",
    "POISONJAB": "毒擊", "CROSSPOISON": "十字毒刃", "SLUDGE": "污泥攻擊",
    "POISONSTING": "毒針", "VENOSHOCK": "毒液衝擊", "ACID": "溶解液",
    "ACIDSPRAY": "酸液炸彈", "SMOG": "煙霧", "CLEARSMOG": "清除之煙",
    "BELCH": "打嗝", "POISONTAIL": "毒尾", "POISONFANG": "劇毒牙",
    "COIL": "盤蜷", "TOXIC": "劇毒", "POISONGAS": "毒瓦斯",
    "TOXICSPIKES": "毒菱", "VENOMDRENCH": "毒液陷阱", "GASTROACID": "胃液",
    
    # Psychic
    "PSYCHIC": "精神強念", "PSYSHOCK": "精神衝擊", "PSYSTRIKE": "精神突進",
    "FUTURESIGHT": "預知未來", "HYPERSPACE HOLE": "異次元洞", "SYNCHRONOISE": "同步干擾",
    "ZENHEADBUTT": "意念頭錘", "PSYCHOCUT": "精神利刃", "EXTRASENSORY": "神通力",
    "PSYBEAM": "幻象光線", "CONFUSION": "念力", "PSYCHOSHIFT": "精神轉移",
    "STOREDPOWER": "輔助力量", "PSYCHUP": "自我暗示", "HEARTSTAMP": "愛心印章",
    "KINESIS": "折彎湯匙", "AGILITY": "高速移動", "TELEPORT": "瞬間移動",
    "REFLECT": "反射壁", "LIGHTSCREEN": "光牆", "AMNESIA": "失憶",
    "REST": "睡覺", "BARRIER": "屏障", "CALMMIND": "冥想",
    "COSMICPOWER": "宇宙力量", "MIRACLEEYE": "奇蹟之眼", "IMPRISON": "封印",
    "TRICKROOM": "戲法空間", "WONDERROOM": "奇妙空間", "MAGICROOM": "魔法空間",
    "HEALBLOCK": "回復封印", "HEALINGWISH": "治癒之願", "LUNARDANCE": "新月舞",
    "GRAVITY": "重力", "SKILLSWAP": "特性互換", "POWERTRICK": "力量戲法",
    "GUARDSPLIT": "防守平分", "POWERSPLIT": "力量平分", "SPEEDSPLIT": "速度平分",
    "PSYWAVE": "精神波", "LUCKYCHANT": "幸運咒語", "TRICK": "戲法",
    "ROLEPLAY": "扮演", "MAGICCOAT": "魔法反射", "MEDITATE": "瑜伽姿勢",
    "ALLYSWITCH": "交換場地", "TELEKINESIS": "意念移物",
    
    # Rock
    "STONEEDGE": "尖石攻擊", "ROCKWRECKER": "岩石炮", "HEADSMASH": "雙刃頭錘",
    "ROCKSLIDE": "岩崩", "POWERGEM": "力量寶石", "ANCIENTPOWER": "原始之力",
    "ROCKBLAST": "岩石爆擊", "ROCKTHROW": "落石", "ROCKTOMB": "岩石封鎖",
    "SMACKDOWN": "擊落", "ROLLOUT": "滾動", "STEALTHROCK": "隱形岩",
    "ROCKPOLISH": "岩石打磨", "SANDSTORM": "沙暴", "WIDEGUARD": "廣域防守",
    
    # Steel
    "IRONHEAD": "鐵頭", "FLASHCANNON": "加農光炮", "METEORMASH": "彗星拳",
    "BULLETPUNCH": "子彈拳", "IRONHEAD": "鐵頭", "METALBURST": "金屬爆炸",
    "MIRRORSHOT": "鏡光射擊", "STEELWING": "鋼翼", "MAGNETBOMB": "磁鐵炸彈",
    "GYRBALL": "陀螺球", "METALSOUND": "金屬音", "METALCLAW": "金屬爪",
    "HEAVYSLAM": "重磅衝撞", "STEELBEAM": "鋼鐵光束", "ANCHORSHOT": "錨打",
    "SMARTSTRIKE": "修長之角", "GEARBLADE": "齒輪飛盤", "AUTOMONIZE": "輕量化",
    "IRONDEFENSE": "鐵壁", "MAGNETRISE": "電磁飄浮", "SHIFTGEAR": "換檔",
    
    # Water
    "HYDROPUMP": "水砲", "SURF": "衝浪", "SCALD": "熱水", "MUDDYWATER": "濁流",
    "HYDROCANNON": "加農水炮", "WATERSPOUT": "噴水", "AQUATAIL": "水流尾",
    "DIVE": "潛水", "WATERFALL": "攀瀑", "AQUAJET": "水流噴射",
    "RAZORSHELL": "貝殼刃", "CRABHAMMER": "蟹鉗錘", "BRINE": "鹽水",
    "WATERPULSE": "水之波動", "OCTAZOOKA": "章魚桶炮", "BUBBLEBEAM": "泡沫光線",
    "BUBBLE": "泡沫", "WHIRLPOOL": "潮旋", "CLAMP": "貝殼夾擊",
    "WITHDRAW": "縮入殼中", "AQUARING": "水流環", "RAINDANCE": "求雨",
    "WATERSPORT": "玩水", "SOAK": "浸水",
}

# 招式描述翻譯模板（基於官方描述風格）
def translate_description(desc_es):
    """將西班牙語描述翻譯為繁體中文"""
    
    # 常見描述片段的翻譯
    patterns = {
        # 攻擊相關
        r"Ataca.*?con": "使用",
        r"Golpea.*?con": "用",
        r"Lanza": "發射",
        r"Dispara": "發射",
        r"Emite": "發出",
        r"Crea": "製造",
        r"Invoca": "召喚",
        r"Genera": "產生",
        
        # 效果相關
        r"Puede bajar": "有時會降低",
        r"Puede subir": "有時會提升",
        r"Puede causar": "有時會造成",
        r"Puede provocar": "有時會使",
        r"Baja": "降低",
        r"Sube": "提升",
        r"Aumenta": "提升",
        r"Reduce": "降低",
        
        # 對象
        r"del objetivo": "對手的",
        r"del rival": "對手的",
        r"del enemigo": "對手的",
        r"del usuario": "使用者的",
        r"del atacante": "攻擊方的",
        r"al objetivo": "對手",
        r"al rival": "對手",
        r"al usuario": "使用者",
        
        # 能力值
        r"Ataque": "攻擊",
        r"Defensa": "防禦",
        r"Ataque Especial": "特攻",
        r"Defensa Especial": "特防",
        r"Velocidad": "速度",
        r"Precisión": "命中率",
        r"Evasión": "迴避率",
        
        # 狀態
        r"envenenamiento": "中毒",
        r"parálisis": "麻痺",
        r"quemadura": "灼傷",
        r"congelación": "冰凍",
        r"sueño": "睡眠",
        r"confusión": "混亂",
        r"retroceso": "畏縮",
        
        # 動作
        r"Golpe crítico": "擊中要害",
        r"crítico": "要害",
        r"Daño": "傷害",
        r"Poder": "威力",
        r"turno": "回合",
        r"veces": "次",
    }
    
    result = desc_es
    for pattern, replacement in patterns.items():
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    
    # 應用術語表
    for es_term, zh_term in term_map.items():
        result = result.replace(es_term, zh_term)
    
    return result

# 讀取原始檔案
with open("D:\\Opalo V2.11\\localization\\translations\\pbs\\moves.txt", "r", encoding="utf-8-sig") as f:
    lines = f.readlines()

# 翻譯每一行
translated_lines = []
count = 0
for line in lines:
    if line.strip() == "" or line.startswith("#"):
        translated_lines.append(line)
        continue
    
    parts = line.strip().split(",")
    if len(parts) < 13:
        translated_lines.append(line)
        continue
    
    # 提取各個欄位
    move_id = parts[0]
    internal_name = parts[1]
    current_name = parts[2]
    
    # 使用官方翻譯（如果有）
    if internal_name in move_translations:
        zh_name = move_translations[internal_name]
    else:
        # 保留當前名稱（可能已經翻譯過）
        zh_name = current_name
    
    # 保留數值和屬性欄位
    function_code = parts[3]
    base_power = parts[4]
    move_type = parts[5]
    category = parts[6]
    accuracy = parts[7]
    total_pp = parts[8]
    add_effect = parts[9]
    target = parts[10]
    priority = parts[11]
    flags = parts[12]
    
    # 翻譯描述（最後一欄）
    if len(parts) >= 14:
        description = ",".join(parts[13:]).strip('"')
        
        # 如果描述明顯是西班牙語，進行翻譯
        if any(word in description for word in ["Ataca", "Golpea", "Lanza", "Puede", "con", "del", "que"]):
            zh_description = translate_description(description)
        else:
            # 已經是中文的描述保持原樣
            zh_description = description
    else:
        zh_description = ""
    
    # 重組行
    new_line = f'{move_id},{internal_name},{zh_name},{function_code},{base_power},{move_type},{category},{accuracy},{total_pp},{add_effect},{target},{priority},{flags},"{zh_description}"\n'
    translated_lines.append(new_line)
    count += 1
    
    if count % 50 == 0:
        print(f"已翻譯 {count} 行招式...")

# 寫回檔案（保留 UTF-8 BOM）
with open("D:\\Opalo V2.11\\localization\\translations\\pbs\\moves.txt", "w", encoding="utf-8-sig") as f:
    f.writelines(translated_lines)

print(f"✅ 完成！共翻譯 {count} 個招式")
