#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pokémon Opalo 批次翻譯工具
讀取 messages.json 並套用術語表進行基礎翻譯處理。

用法:
  python translate.py <input.json> --glossary <glossary.json> -o <output.json>
  python translate.py <input.json> --stats
  python translate.py <input.json> --glossary <glossary.json> -o <output.json> --batch-size 100 --start 500
"""

import argparse
import json
import re
import sys
import os

# 需要保留的特殊標記模式
VARIABLE_PATTERN = re.compile(
    r'(\\PN|\\Pokemon|\\pn|\\pokemon|\\sh|\\[a-zA-Z]+|'
    r'\{[^}]*\}|'
    r'<[^>]+>|'
    r'\\n)'
)

# 純符號/數字/空白判斷
SKIP_PATTERNS = [
    re.compile(r'^\s*$'),           # 空白
    re.compile(r'^[\d\s.,%]+$'),    # 純數字
    re.compile(r'^[^\w\s]+$'),      # 純符號（無字母數字）
    re.compile(r'^\.\.\.$'),        # 省略號
    re.compile(r'^-+$'),            # 純破折號
    re.compile(r'^[=\-_*#]+$'),     # 分隔線
]


def load_glossary(glossary_path):
    """從 glossary.json 載入術語表，建立 es -> zh_TW 對照表"""
    with open(glossary_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    glossary = {}

    def extract_terms(obj):
        """遞迴提取所有 terms"""
        if isinstance(obj, dict):
            if 'terms' in obj and isinstance(obj['terms'], list):
                for term in obj['terms']:
                    if 'es' in term and 'zh_TW' in term:
                        glossary[term['es']] = term['zh_TW']
            for key, val in obj.items():
                if key not in ('metadata', '_description'):
                    extract_terms(val)
        elif isinstance(obj, list):
            for item in obj:
                extract_terms(item)

    if 'categories' in data:
        extract_terms(data['categories'])
    else:
        extract_terms(data)

    return glossary


def should_skip(text):
    """判斷是否應跳過此條目（空字串、純數字、純符號等）"""
    if not text or not text.strip():
        return True
    for pattern in SKIP_PATTERNS:
        if pattern.match(text.strip()):
            return True
    return False


def apply_glossary(text, glossary):
    """
    嘗試用術語表翻譯文字。
    - 完全匹配：整個 original 就是術語表中的詞條
    - 回傳 (translated_text, is_full_match)
    """
    stripped = text.strip()

    # 完全匹配
    if stripped in glossary:
        return glossary[stripped], True

    return None, False


def apply_glossary_partial(text, glossary):
    """
    對文字進行部分術語替換。
    按術語長度降序排列，避免短詞誤替換長詞的一部分。
    回傳替換後的文字和替換次數。
    """
    result = text
    replacements = 0

    # 提取需要保護的標記
    protected = []
    def protect(match):
        protected.append(match.group(0))
        return f'\x00PROT{len(protected)-1}\x00'

    result = VARIABLE_PATTERN.sub(protect, result)

    # 按長度降序排列術語
    sorted_terms = sorted(glossary.items(), key=lambda x: len(x[0]), reverse=True)

    for es_term, zh_term in sorted_terms:
        if len(es_term) < 3:  # 跳過過短的術語避免誤替換
            continue
        # 使用單字邊界匹配（西文）
        pattern = re.compile(r'\b' + re.escape(es_term) + r'\b', re.IGNORECASE)
        new_result = pattern.sub(zh_term, result)
        if new_result != result:
            replacements += 1
            result = new_result

    # 恢復受保護的標記
    for i, p in enumerate(protected):
        result = result.replace(f'\x00PROT{i}\x00', p)

    return result, replacements


def process_entries(entries, glossary, start=0, batch_size=None, mark_human=True):
    """
    處理翻譯條目。

    Args:
        entries: 條目列表
        glossary: 術語對照表
        start: 起始索引
        batch_size: 每批數量（None = 全部）
        mark_human: 是否標記需人工翻譯的條目

    Returns:
        stats dict
    """
    end = min(start + batch_size, len(entries)) if batch_size else len(entries)
    stats = {
        'total': end - start,
        'already_translated': 0,
        'glossary_exact': 0,
        'glossary_partial': 0,
        'skipped': 0,
        'needs_human': 0,
        'processed_range': f'{start}-{end-1}'
    }

    for i in range(start, end):
        entry = entries[i]
        original = entry.get('original', '')
        current_translation = entry.get('translation', '')

        # 已有翻譯則跳過
        if current_translation and not current_translation.startswith('[TODO'):
            stats['already_translated'] += 1
            continue

        # 應跳過的條目
        if should_skip(original):
            entry['translation'] = original  # 保持原樣
            stats['skipped'] += 1
            continue

        # 嘗試完全匹配
        translated, is_full = apply_glossary(original, glossary)
        if is_full:
            entry['translation'] = translated
            stats['glossary_exact'] += 1
            continue

        # 嘗試部分替換
        partial_result, num_replacements = apply_glossary_partial(original, glossary)
        if num_replacements > 0:
            if mark_human:
                entry['translation'] = f'[TODO:部分] {partial_result}'
            else:
                entry['translation'] = partial_result
            stats['glossary_partial'] += 1
            continue

        # 無法翻譯，標記需人工翻譯
        if mark_human:
            entry['translation'] = f'[TODO:人工] {original}'
        stats['needs_human'] += 1

    return stats


def print_stats(entries, detailed=False):
    """顯示翻譯進度統計"""
    total = len(entries)
    translated = 0
    todo_partial = 0
    todo_human = 0
    empty = 0
    skipped = 0

    for entry in entries:
        t = entry.get('translation', '')
        original = entry.get('original', '')
        if not t:
            empty += 1
        elif t.startswith('[TODO:部分]'):
            todo_partial += 1
        elif t.startswith('[TODO:人工]'):
            todo_human += 1
        elif should_skip(original) and t == original:
            skipped += 1
        else:
            translated += 1

    print(f'\n{"="*50}')
    print(f'  翻譯進度統計')
    print(f'{"="*50}')
    print(f'  總條目數:       {total:>8,}')
    print(f'  已翻譯:         {translated:>8,}  ({translated/total*100:.1f}%)')
    print(f'  部分翻譯(TODO): {todo_partial:>8,}  ({todo_partial/total*100:.1f}%)')
    print(f'  待人工翻譯:     {todo_human:>8,}  ({todo_human/total*100:.1f}%)')
    print(f'  已跳過:         {skipped:>8,}  ({skipped/total*100:.1f}%)')
    print(f'  未處理:         {empty:>8,}  ({empty/total*100:.1f}%)')
    print(f'{"="*50}')

    if detailed:
        # 顯示前幾個未翻譯的條目
        print(f'\n  前 10 個未處理條目:')
        count = 0
        for i, entry in enumerate(entries):
            if not entry.get('translation', ''):
                print(f'    [{i}] {entry["id"]}: {entry["original"][:60]}...')
                count += 1
                if count >= 10:
                    break


def main():
    parser = argparse.ArgumentParser(
        description='Pokémon Opalo 批次翻譯工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  # 套用術語表翻譯
  python translate.py messages.json --glossary glossary.json -o messages_out.json

  # 從第 500 條開始，每批 100 條
  python translate.py messages.json --glossary glossary.json -o messages_out.json --start 500 --batch-size 100

  # 只看統計
  python translate.py messages.json --stats
        '''
    )
    parser.add_argument('input', help='輸入的翻譯 JSON 檔案')
    parser.add_argument('--glossary', '-g', help='術語表 JSON 檔案路徑')
    parser.add_argument('-o', '--output', help='輸出 JSON 檔案路徑（預設覆蓋輸入檔）')
    parser.add_argument('--batch-size', '-b', type=int, default=None,
                        help='每批處理的條目數量')
    parser.add_argument('--start', '-s', type=int, default=0,
                        help='從第 N 條開始處理（支援斷點續譯）')
    parser.add_argument('--stats', action='store_true',
                        help='顯示翻譯進度統計')
    parser.add_argument('--no-mark', action='store_true',
                        help='不標記 [TODO] 前綴')
    parser.add_argument('--detailed', '-d', action='store_true',
                        help='顯示詳細統計（含未翻譯條目範例）')

    args = parser.parse_args()

    # 載入翻譯檔案
    print(f'載入翻譯檔案: {args.input}')
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)

    entries = data.get('entries', [])
    print(f'共 {len(entries):,} 條條目')

    # 純統計模式
    if args.stats:
        print_stats(entries, detailed=args.detailed)
        return

    # 需要術語表才能翻譯
    if not args.glossary:
        print('錯誤: 翻譯模式需要指定 --glossary 參數', file=sys.stderr)
        sys.exit(1)

    # 載入術語表
    print(f'載入術語表: {args.glossary}')
    glossary = load_glossary(args.glossary)
    print(f'共 {len(glossary)} 個術語')

    # 處理翻譯
    print(f'\n開始處理 (起始: {args.start}, 批次大小: {args.batch_size or "全部"})...')
    stats = process_entries(
        entries,
        glossary,
        start=args.start,
        batch_size=args.batch_size,
        mark_human=not args.no_mark
    )

    # 顯示處理結果
    print(f'\n處理結果 (範圍: {stats["processed_range"]}):')
    print(f'  已有翻譯:     {stats["already_translated"]:>6}')
    print(f'  術語完全匹配: {stats["glossary_exact"]:>6}')
    print(f'  術語部分替換: {stats["glossary_partial"]:>6}')
    print(f'  已跳過:       {stats["skipped"]:>6}')
    print(f'  需人工翻譯:   {stats["needs_human"]:>6}')

    # 儲存結果
    output_path = args.output or args.input
    print(f'\n儲存至: {output_path}')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print('完成！')

    # 顯示整體統計
    print_stats(entries)


if __name__ == '__main__':
    main()
