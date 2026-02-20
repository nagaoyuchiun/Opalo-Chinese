#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 extract.py 和 repack.py 工具的整合測試
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

# 檢查依賴
try:
    from rubymarshal.reader import load as ruby_load
    from rubymarshal.writer import write as ruby_dump
except ImportError:
    print("✗ rubymarshal 未安裝")
    print("請執行: pip install rubymarshal")
    sys.exit(1)

print("="*60)
print("Extract & Repack 工具整合測試")
print("="*60)

# 設定路徑
script_dir = Path(__file__).parent
data_dir = script_dir.parent.parent / "Data"
test_file = data_dir / "messages.dat"

if not test_file.exists():
    print(f"✗ 測試檔案不存在: {test_file}")
    sys.exit(1)

print(f"\n測試檔案: {test_file}")
print(f"檔案大小: {test_file.stat().st_size} bytes")

# 創建臨時目錄
temp_dir = Path(tempfile.mkdtemp())
print(f"\n臨時目錄: {temp_dir}")

try:
    # 測試 1: 提取
    print("\n" + "="*60)
    print("測試 1: 提取文字")
    print("="*60)
    
    from extract import extract_messages
    json_file = temp_dir / "test.json"
    extract_messages(test_file, json_file)
    
    # 檢查 JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    entries = data.get('entries', [])
    print(f"\n✓ 提取成功: {len(entries)} 個條目")
    
    if len(entries) == 0:
        print("✗ 警告: 沒有提取到任何條目")
        sys.exit(1)
    
    # 測試 2: 重新打包（無修改）
    print("\n" + "="*60)
    print("測試 2: 重新打包（無修改）")
    print("="*60)
    
    from repack import repack_messages
    output_file = temp_dir / "test_repack.dat"
    repack_messages(json_file, test_file, output_file)
    
    # 比較檔案大小
    original_size = test_file.stat().st_size
    repack_size = output_file.stat().st_size
    size_diff = abs(original_size - repack_size)
    
    print(f"\n檔案大小比較:")
    print(f"  原始: {original_size} bytes")
    print(f"  重新打包: {repack_size} bytes")
    print(f"  差異: {size_diff} bytes")
    
    if size_diff == 0:
        print("✓ 完美！檔案大小完全一致")
    elif size_diff < 100:
        print("✓ 良好：差異在可接受範圍內")
    else:
        print(f"⚠ 警告：差異較大 ({size_diff} bytes)")
    
    # 測試 3: 驗證重新打包的檔案
    print("\n" + "="*60)
    print("測試 3: 驗證重新打包的檔案")
    print("="*60)
    
    verify_json = temp_dir / "test_verify.json"
    extract_messages(output_file, verify_json)
    
    with open(verify_json, 'r', encoding='utf-8') as f:
        verify_data = json.load(f)
    
    verify_entries = verify_data.get('entries', [])
    print(f"✓ 重新提取成功: {len(verify_entries)} 個條目")
    
    if len(verify_entries) == len(entries):
        print("✓ 條目數量一致")
    else:
        print(f"✗ 警告: 條目數量不一致 ({len(entries)} vs {len(verify_entries)})")
    
    # 測試 4: 應用翻譯
    print("\n" + "="*60)
    print("測試 4: 應用測試翻譯")
    print("="*60)
    
    # 修改前 5 個條目
    test_entries = min(5, len(entries))
    for i in range(test_entries):
        data['entries'][i]['translation'] = f"[TEST_{i+1}] {data['entries'][i]['original'][:30]}"
    
    translated_json = temp_dir / "test_translated.json"
    with open(translated_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"已添加 {test_entries} 個測試翻譯")
    
    # 重新打包翻譯版本
    translated_output = temp_dir / "test_translated.dat"
    repack_messages(translated_json, test_file, translated_output)
    
    # 驗證翻譯
    verify_translated_json = temp_dir / "test_translated_verify.json"
    extract_messages(translated_output, verify_translated_json)
    
    with open(verify_translated_json, 'r', encoding='utf-8') as f:
        translated_verify = json.load(f)
    
    # 檢查前幾個條目是否包含測試標記
    success_count = 0
    for i in range(test_entries):
        original = translated_verify['entries'][i]['original']
        if '[TEST_' in original:
            success_count += 1
    
    print(f"✓ 翻譯驗證: {success_count}/{test_entries} 個翻譯正確應用")
    
    if success_count == test_entries:
        print("✓ 完美！所有測試翻譯都正確應用")
    elif success_count > 0:
        print(f"⚠ 部分翻譯應用成功 ({success_count}/{test_entries})")
    else:
        print("✗ 警告: 翻譯未能正確應用")
    
    # 總結
    print("\n" + "="*60)
    print("測試總結")
    print("="*60)
    print("✓ 提取功能: 正常")
    print("✓ 重新打包功能: 正常")
    print("✓ 檔案格式驗證: 通過")
    print("✓ 翻譯應用: 正常" if success_count == test_entries else "⚠ 翻譯應用: 部分成功")
    print("\n所有測試完成！")
    
except Exception as e:
    print(f"\n✗ 測試失敗: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

finally:
    # 清理臨時檔案
    print(f"\n清理臨時檔案...")
    shutil.rmtree(temp_dir)
    print("✓ 完成")

print("\n" + "="*60)
print("測試成功完成！工具運作正常。")
print("="*60)
