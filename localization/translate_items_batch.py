import json
import re
import os
from openai import AzureOpenAI

# Azure OpenAI 設定
client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-10-21",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
)

# 載入術語表
with open("D:/Opalo V2.11/localization/glossary.json", "r", encoding="utf-8") as f:
    glossary = json.load(f)

# 建立 ES -> ZH_TW 對照表
glossary_map = {}
for category_key, category in glossary["categories"].items():
    if "terms" in category:
        for term in category["terms"]:
            if isinstance(term, dict) and "es" in term and "zh_TW" in term:
                glossary_map[term["es"]] = term["zh_TW"]
    if "subcategories" in category:
        for subcat_key, subcat in category["subcategories"].items():
            if "terms" in subcat:
                for term in subcat["terms"]:
                    if isinstance(term, dict) and "es" in term and "zh_TW" in term:
                        glossary_map[term["es"]] = term["zh_TW"]

print(f"已載入 {len(glossary_map)} 個術語對照")

# 批次翻譯函數
def translate_batch(items_batch, batch_num, total_batches):
    prompt = f"""將以下寶可夢道具翻譯為繁體中文。請遵守：

1. **使用官方譯名**（優先級最高）：
{chr(10).join([f"   - {es} → {zh}" for es, zh in list(glossary_map.items())[:50]])}

2. **格式要求**：
   - 輸出純 JSON 陣列：[{{"name": "...", "plural": "...", "desc": "..."}}, ...]
   - 保留 HTML 標籤 (<b>, </b>)
   - 保留換行符 (\\n)
   - 道具名稱簡潔（2-6字）
   - 複數形式通常加「們」或不變

3. **翻譯原則**：
   - 石頭類：火之石、水之石、雷之石...
   - 藥品類：傷藥、解毒藥、萬能藥...
   - 球類：精靈球、超級球、大師球...
   - 化石類：貝殼化石、甲殼化石...
   - 保持遊戲風格，避免過於文言

待翻譯（批次 {batch_num}/{total_batches}）：
{json.dumps(items_batch, ensure_ascii=False, indent=2)}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是專業的寶可夢遊戲本地化翻譯。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        
        result_text = response.choices[0].message.content.strip()
        # 提取 JSON（可能包含在 ```json ... ``` 中）
        json_match = re.search(r'```json\s*(\[.*?\])\s*```', result_text, re.DOTALL)
        if json_match:
            result_text = json_match.group(1)
        
        return json.loads(result_text)
    except Exception as e:
        print(f"  ❌ 批次 {batch_num} 翻譯失敗: {e}")
        return None

# 讀取原檔案（保留 BOM）
input_path = "D:/Opalo V2.11/localization/translations/pbs/items.txt"
with open(input_path, "r", encoding="utf-8-sig") as f:
    lines = f.readlines()

print(f"讀取 {len(lines)} 行資料")

# 解析每行
items_data = []
for line_num, line in enumerate(lines, 1):
    parts = line.strip().split(',')
    if len(parts) >= 10:
        items_data.append({
            "line_num": line_num,
            "id": parts[0],
            "internal": parts[1],
            "name": parts[2],
            "plural": parts[3],
            "pocket": parts[4],
            "price": parts[5],
            "desc": parts[6],
            "rest": ','.join(parts[7:])  # 保留剩餘欄位
        })

print(f"解析 {len(items_data)} 個道具")

# 分批翻譯（每批 30 個）
batch_size = 30
translated_items = []

for i in range(0, len(items_data), batch_size):
    batch = items_data[i:i+batch_size]
    batch_num = i // batch_size + 1
    total_batches = (len(items_data) + batch_size - 1) // batch_size
    
    print(f"\n翻譯批次 {batch_num}/{total_batches} ({len(batch)} 個道具)...")
    
    # 準備翻譯資料
    to_translate = [{"name": item["name"], "plural": item["plural"], "desc": item["desc"]} for item in batch]
    
    # 呼叫 API
    translations = translate_batch(to_translate, batch_num, total_batches)
    
    if translations and len(translations) == len(batch):
        for j, item in enumerate(batch):
            item["name_zh"] = translations[j]["name"]
            item["plural_zh"] = translations[j]["plural"]
            item["desc_zh"] = translations[j]["desc"]
            translated_items.append(item)
        print(f"  ✅ 批次 {batch_num} 完成")
    else:
        print(f"  ⚠️ 批次 {batch_num} 失敗，保留原文")
        for item in batch:
            item["name_zh"] = item["name"]
            item["plural_zh"] = item["plural"]
            item["desc_zh"] = item["desc"]
            translated_items.append(item)

# 輸出翻譯後的檔案（保留 BOM）
output_lines = []
for item in translated_items:
    output_lines.append(f'{item["id"]},{item["internal"]},{item["name_zh"]},{item["plural_zh"]},{item["pocket"]},{item["price"]},{item["desc_zh"]},{item["rest"]}\n')

with open(input_path, "w", encoding="utf-8-sig") as f:
    f.writelines(output_lines)

print(f"\n✅ 翻譯完成！已更新 {input_path}")
print(f"   總計翻譯 {len(translated_items)} 個道具")
