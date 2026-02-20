#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PBS Translatable Field Extractor
Extracts only translatable fields from PBS files (pokemon.txt, moves.txt, items.txt),
filtering out all numeric/structural data to minimize token usage for LLM translation.
"""

import argparse
import csv
import io
import json
import re
import sys
from pathlib import Path

# Fields that need translation per PBS file type
POKEMON_TRANSLATABLE = {'Name', 'Kind', 'Pokedex'}
ITEMS_TRANSLATABLE_INDICES = {2: 'name', 3: 'plural_name', 6: 'description'}
MOVES_TRANSLATABLE_INDICES = {2: 'display_name', -1: 'description'}


def detect_file_type(pbs_path: Path) -> str:
    """Auto-detect PBS file type from filename and content."""
    name = pbs_path.stem.lower()
    if name == 'pokemon':
        return 'pokemon'
    elif name == 'moves':
        return 'moves'
    elif name == 'items':
        return 'items'
    # Fallback: peek at content
    with open(pbs_path, 'r', encoding='utf-8-sig') as f:
        first_lines = [f.readline() for _ in range(5)]
    for line in first_lines:
        if re.match(r'^\[\d+\]', line.strip()):
            return 'pokemon'
    return 'unknown'


def extract_pokemon(pbs_path: Path) -> dict:
    """Extract translatable fields from pokemon.txt (INI-style sections)."""
    entries = []
    current_section = None
    current_fields = {}

    def flush():
        if current_section and current_fields:
            entries.append({
                'section_id': current_section,
                'fields': dict(current_fields)
            })

    with open(pbs_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.rstrip('\n').rstrip('\r')
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            # Section header: [N]
            m = re.match(r'^\[(\d+)\]$', stripped)
            if m:
                flush()
                current_section = m.group(1)
                current_fields = {}
                continue
            # Key=Value
            if '=' in stripped:
                key, _, value = stripped.partition('=')
                key = key.strip()
                value = value.strip()
                if key in POKEMON_TRANSLATABLE and value:
                    current_fields[key] = value

    flush()

    return {
        'metadata': {
            'source_file': str(pbs_path).replace('\\', '/'),
            'file_type': 'pokemon',
            'total_entries': len(entries),
            'translatable_fields': sorted(POKEMON_TRANSLATABLE),
            'source_language': 'es',
            'target_language': 'zh-TW',
            'extraction_version': '2.0'
        },
        'entries': entries
    }


def extract_moves(pbs_path: Path) -> dict:
    """Extract translatable fields from moves.txt (CSV format)."""
    entries = []
    with open(pbs_path, 'r', encoding='utf-8-sig') as f:
        for line_num, line in enumerate(f, 1):
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
            internal = fields[1].strip()
            display_name = fields[2].strip()
            # Description is the last field (often quoted)
            description = fields[-1].strip() if len(fields) >= 14 else ''

            entry_fields = {}
            if display_name:
                entry_fields['display_name'] = display_name
            if description and len(description) > 3:
                entry_fields['description'] = description

            if entry_fields:
                entries.append({
                    'line_number': line_num,
                    'internal_name': internal,
                    'fields': entry_fields
                })

    return {
        'metadata': {
            'source_file': str(pbs_path).replace('\\', '/'),
            'file_type': 'moves',
            'total_entries': len(entries),
            'source_language': 'es',
            'target_language': 'zh-TW',
            'extraction_version': '2.0'
        },
        'entries': entries
    }


def extract_items(pbs_path: Path) -> dict:
    """Extract translatable fields from items.txt (CSV format)."""
    entries = []
    with open(pbs_path, 'r', encoding='utf-8-sig') as f:
        for line_num, line in enumerate(f, 1):
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
            internal = fields[1].strip()
            name = fields[2].strip()
            plural = fields[3].strip()
            desc = fields[6].strip()

            entry_fields = {}
            if name:
                entry_fields['name'] = name
            if plural:
                entry_fields['plural_name'] = plural
            if desc:
                entry_fields['description'] = desc

            if entry_fields:
                entries.append({
                    'line_number': line_num,
                    'internal_name': internal,
                    'fields': entry_fields
                })

    return {
        'metadata': {
            'source_file': str(pbs_path).replace('\\', '/'),
            'file_type': 'items',
            'total_entries': len(entries),
            'source_language': 'es',
            'target_language': 'zh-TW',
            'extraction_version': '2.0'
        },
        'entries': entries
    }


def main():
    parser = argparse.ArgumentParser(
        description='Extract translatable fields from PBS files (pokemon.txt, moves.txt, items.txt)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python extract_pbs.py PBS/pokemon.txt -o localization/translations/pbs/pokemon_translatable.json
  python extract_pbs.py PBS/moves.txt -o localization/translations/pbs/moves_translatable.json
  python extract_pbs.py PBS/items.txt -o localization/translations/pbs/items_translatable.json
        """
    )
    parser.add_argument('input_file', type=Path, help='Input PBS file path')
    parser.add_argument('-o', '--output', type=Path, default=None,
                        help='Output JSON file path')
    parser.add_argument('-t', '--type', choices=['pokemon', 'moves', 'items'],
                        default=None, help='Force file type (auto-detected if omitted)')

    args = parser.parse_args()

    if not args.input_file.exists():
        print(f"Error: Input file not found: {args.input_file}")
        sys.exit(1)

    file_type = args.type or detect_file_type(args.input_file)

    if file_type == 'pokemon':
        data = extract_pokemon(args.input_file)
    elif file_type == 'moves':
        data = extract_moves(args.input_file)
    elif file_type == 'items':
        data = extract_items(args.input_file)
    else:
        print(f"Error: Cannot detect file type for {args.input_file}")
        sys.exit(1)

    output_path = args.output
    if output_path is None:
        output_path = Path('localization/translations/pbs') / f"{args.input_file.stem}_translatable.json"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[{file_type}] {data['metadata']['total_entries']} entries → {output_path}")
    if data['entries']:
        for e in data['entries'][:3]:
            fields = e['fields']
            preview = ', '.join(f"{k}: {v[:40]}" for k, v in fields.items())
            print(f"  {preview}")


if __name__ == '__main__':
    main()
