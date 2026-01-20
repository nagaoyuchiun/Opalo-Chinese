#!/usr/bin/env python3
"""測試提取 rxdata/dat 檔案中的文字"""
import os
import sys

# 嘗試使用 rubymarshal
try:
    import rubymarshal.reader as reader
    print("✓ rubymarshal 已安裝")
except ImportError:
    print("✗ rubymarshal 未安裝，請執行: pip install rubymarshal")
    sys.exit(1)

def extract_strings_from_object(obj, path="", depth=0):
    """遞迴提取物件中的所有字串"""
    strings = []
    
    if depth > 20:  # 防止無限遞迴
        return strings
    
    if isinstance(obj, (str, bytes)):
        if isinstance(obj, bytes):
            try:
                text = obj.decode('utf-8')
            except:
                try:
                    text = obj.decode('latin-1')
                except:
                    return strings
        else:
            text = obj
        
        # 只收集有意義的文字（長度 > 1 且包含字母）
        if len(text) > 1 and any(c.isalpha() for c in text):
            strings.append({"path": path, "text": text})
    
    elif isinstance(obj, dict):
        for key, value in obj.items():
            new_path = f"{path}.{key}" if path else str(key)
            strings.extend(extract_strings_from_object(value, new_path, depth+1))
    
    elif isinstance(obj, (list, tuple)):
        for i, item in enumerate(obj):
            new_path = f"{path}[{i}]"
            strings.extend(extract_strings_from_object(item, new_path, depth+1))
    
    elif hasattr(obj, '__dict__'):
        for key, value in obj.__dict__.items():
            new_path = f"{path}.{key}" if path else str(key)
            strings.extend(extract_strings_from_object(value, new_path, depth+1))
    
    elif hasattr(obj, 'attributes'):
        try:
            attrs = obj.attributes
            if isinstance(attrs, dict):
                for key, value in attrs.items():
                    new_path = f"{path}.{key}" if path else str(key)
                    strings.extend(extract_strings_from_object(value, new_path, depth+1))
        except:
            pass
    
    return strings


def test_file(filepath):
    """測試讀取單一檔案"""
    print(f"\n{'='*60}")
    print(f"測試檔案: {os.path.basename(filepath)}")
    print(f"{'='*60}")
    
    try:
        with open(filepath, 'rb') as f:
            data = reader.load(f)
        
        print(f"✓ 成功讀取！")
        print(f"  資料類型: {type(data).__name__}")
        
        # 提取字串
        strings = extract_strings_from_object(data)
        print(f"  找到 {len(strings)} 個文字字串")
        
        # 顯示範例
        if strings:
            print(f"\n  前 10 個範例:")
            for i, s in enumerate(strings[:10]):
                text = s['text'][:60] + "..." if len(s['text']) > 60 else s['text']
                print(f"    {i+1}. {text}")
        
        return len(strings)
        
    except Exception as e:
        print(f"✗ 讀取失敗: {e}")
        return 0


def main():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, "Data")
    
    # 測試幾個關鍵檔案
    test_files = [
        os.path.join(data_path, "messages.dat"),
        os.path.join(data_path, "items.dat"),
        os.path.join(data_path, "trainers.dat"),
        os.path.join(data_path, "Map001.rxdata"),
    ]
    
    total = 0
    success = 0
    
    for filepath in test_files:
        if os.path.exists(filepath):
            count = test_file(filepath)
            total += 1
            if count > 0:
                success += 1
        else:
            print(f"\n⚠ 檔案不存在: {filepath}")
    
    print(f"\n{'='*60}")
    print(f"總結: 測試 {total} 個檔案，{success} 個成功提取")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
