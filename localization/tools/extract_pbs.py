#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract translatable text from PBS text files (items.txt, moves.txt)."""

import json
import csv
import io
import sys
from pathlib import Path


def extract_items(pbs_path: Path, output_path: Path):
    """Extract items from PBS items.txt."""
    entries = []
    with open(pbs_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            reader = csv.reader(io.StringIO(line))
            try:
                fields = next(reader)
            except StopIteration:
                continue
            if len(fields) < 7:
                continue
            item_id = fields[0].strip()
            internal = fields[1]
            name = fields[2]
            plural = fields[3]
            desc = fields[6]

            if name.strip():
                entries.append({
                    'id': f'item_{item_id}.name',
                    'original': name,
                    'translation': '',
                    'context': {'parent': internal, 'key': 'name', 'type': 'pbs_field', 'item_id': int(item_id)}
                })
            if plural.strip():
                entries.append({
                    'id': f'item_{item_id}.plural',
                    'original': plural,
                    'translation': '',
                    'context': {'parent': internal, 'key': 'plural_name', 'type': 'pbs_field', 'item_id': int(item_id)}
                })
            if desc.strip():
                entries.append({
                    'id': f'item_{item_id}.description',
                    'original': desc,
                    'translation': '',
                    'context': {'parent': internal, 'key': 'description', 'type': 'pbs_field', 'item_id': int(item_id)}
                })

    output = {
        'metadata': {
            'source_file': 'PBS/items.txt (items.dat is custom binary)',
            'total_entries': len(entries),
            'source_language': 'es',
            'target_language': 'zh-TW',
            'extraction_version': '1.0',
            'note': 'Extracted from PBS text since items.dat uses custom binary format'
        },
        'entries': entries
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"items.json: {len(entries)} entries extracted")
    if entries:
        for e in entries[:3]:
            print(f"  {e['id']}: {e['original'][:60]}")


def extract_moves(pbs_path: Path, output_path: Path):
    """Extract moves from PBS moves.txt."""
    entries = []
    with open(pbs_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            reader = csv.reader(io.StringIO(line))
            try:
                fields = next(reader)
            except StopIteration:
                continue
            if len(fields) < 3:
                continue
            move_id = fields[0].strip()
            internal = fields[1]
            name = fields[2]
            # Description is the last quoted field
            last_field = fields[-1].strip()

            if name.strip():
                entries.append({
                    'id': f'move_{move_id}.name',
                    'original': name,
                    'translation': '',
                    'context': {'parent': internal, 'key': 'name', 'type': 'pbs_field', 'move_id': int(move_id)}
                })
            # Description: last field, typically longer text
            if last_field.strip() and len(last_field) > 10:
                entries.append({
                    'id': f'move_{move_id}.description',
                    'original': last_field,
                    'translation': '',
                    'context': {'parent': internal, 'key': 'description', 'type': 'pbs_field', 'move_id': int(move_id)}
                })

    output = {
        'metadata': {
            'source_file': 'PBS/moves.txt (moves.dat is custom binary)',
            'total_entries': len(entries),
            'source_language': 'es',
            'target_language': 'zh-TW',
            'extraction_version': '1.0',
            'note': 'Extracted from PBS text since moves.dat uses custom binary format'
        },
        'entries': entries
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"moves.json: {len(entries)} entries extracted")
    if entries:
        for e in entries[:3]:
            print(f"  {e['id']}: {e['original'][:60]}")


if __name__ == '__main__':
    base = Path(__file__).resolve().parent.parent.parent
    
    print("=" * 60)
    print("Extracting items from PBS/items.txt...")
    extract_items(base / 'PBS' / 'items.txt', base / 'localization' / 'translations' / 'items.json')
    
    print()
    print("Extracting moves from PBS/moves.txt...")
    extract_moves(base / 'PBS' / 'moves.txt', base / 'localization' / 'translations' / 'moves.json')
    print("=" * 60)
