#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PBS Translatable Field Repacker
Reads translated JSON and the original PBS file, then stitches translated fields
back into the original while preserving all numeric/structural data untouched.
"""

import argparse
import csv
import io
import json
import re
import sys
from pathlib import Path


def repack_pokemon(json_data: dict, original_path: Path, output_path: Path):
    """Repack translated fields into pokemon.txt (INI-style sections)."""
    # Build lookup: section_id -> {field: translated_value}
    translations = {}
    for entry in json_data.get('entries', []):
        sid = str(entry.get('section_id', ''))
        fields = entry.get('fields', {})
        if sid and fields:
            translations[sid] = fields

    translatable_keys = set(json_data.get('metadata', {}).get(
        'translatable_fields', ['Name', 'Kind', 'Pokedex']))

    current_section = None
    output_lines = []
    applied = 0

    with open(original_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            raw = line.rstrip('\n').rstrip('\r')
            stripped = raw.strip()

            # Section header
            m = re.match(r'^\[(\d+)\]$', stripped)
            if m:
                current_section = m.group(1)
                output_lines.append(raw)
                continue

            # Key=Value in a section
            if current_section and '=' in stripped and not stripped.startswith('#'):
                key, _, value = stripped.partition('=')
                key_stripped = key.strip()
                if (key_stripped in translatable_keys and
                        current_section in translations and
                        key_stripped in translations[current_section]):
                    translated = translations[current_section][key_stripped]
                    if translated:
                        output_lines.append(f"{key_stripped}={translated}")
                        applied += 1
                        continue

            output_lines.append(raw)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    # Write with BOM to match original format
    with open(output_path, 'w', encoding='utf-8-sig', newline='\r\n') as f:
        f.write('\n'.join(output_lines))
        if output_lines and not output_lines[-1] == '':
            f.write('\n')

    print(f"[pokemon] {applied} fields replaced → {output_path}")


def repack_moves(json_data: dict, original_path: Path, output_path: Path):
    """Repack translated fields into moves.txt (CSV format)."""
    # Build lookup: line_number -> {field: translated_value}
    by_line = {}
    by_internal = {}
    for entry in json_data.get('entries', []):
        ln = entry.get('line_number')
        internal = entry.get('internal_name', '')
        fields = entry.get('fields', {})
        if ln:
            by_line[ln] = fields
        if internal:
            by_internal[internal] = fields

    output_lines = []
    applied = 0
    line_num = 0

    with open(original_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line_num += 1
            raw = line.rstrip('\n').rstrip('\r')
            stripped = raw.strip()

            if not stripped or stripped.startswith('#'):
                output_lines.append(raw)
                continue

            reader = csv.reader(io.StringIO(stripped))
            try:
                fields = next(reader)
            except StopIteration:
                output_lines.append(raw)
                continue

            if len(fields) < 3:
                output_lines.append(raw)
                continue

            # Find translation by line number or internal name
            trans = by_line.get(line_num) or by_internal.get(fields[1].strip())

            if trans:
                if 'display_name' in trans and trans['display_name']:
                    fields[2] = trans['display_name']
                    applied += 1
                if 'description' in trans and trans['description']:
                    # Description is the last field, wrapped in quotes
                    fields[-1] = trans['description']
                    applied += 1

            # Rebuild CSV line
            out = io.StringIO()
            writer = csv.writer(out, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(fields)
            output_lines.append(out.getvalue().rstrip('\r\n'))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8-sig', newline='\r\n') as f:
        f.write('\n'.join(output_lines))
        if output_lines and output_lines[-1] != '':
            f.write('\n')

    print(f"[moves] {applied} fields replaced → {output_path}")


def repack_items(json_data: dict, original_path: Path, output_path: Path):
    """Repack translated fields into items.txt (CSV format)."""
    by_line = {}
    by_internal = {}
    for entry in json_data.get('entries', []):
        ln = entry.get('line_number')
        internal = entry.get('internal_name', '')
        fields = entry.get('fields', {})
        if ln:
            by_line[ln] = fields
        if internal:
            by_internal[internal] = fields

    output_lines = []
    applied = 0
    line_num = 0

    with open(original_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line_num += 1
            raw = line.rstrip('\n').rstrip('\r')
            stripped = raw.strip()

            if not stripped or stripped.startswith('#'):
                output_lines.append(raw)
                continue

            reader = csv.reader(io.StringIO(stripped))
            try:
                fields = next(reader)
            except StopIteration:
                output_lines.append(raw)
                continue

            if len(fields) < 7:
                output_lines.append(raw)
                continue

            trans = by_line.get(line_num) or by_internal.get(fields[1].strip())

            if trans:
                if 'name' in trans and trans['name']:
                    fields[2] = trans['name']
                    applied += 1
                if 'plural_name' in trans and trans['plural_name']:
                    fields[3] = trans['plural_name']
                    applied += 1
                if 'description' in trans and trans['description']:
                    fields[6] = trans['description']
                    applied += 1

            out = io.StringIO()
            writer = csv.writer(out, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(fields)
            output_lines.append(out.getvalue().rstrip('\r\n'))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8-sig', newline='\r\n') as f:
        f.write('\n'.join(output_lines))
        if output_lines and output_lines[-1] != '':
            f.write('\n')

    print(f"[items] {applied} fields replaced → {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Repack translated JSON fields back into PBS files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python repack_pbs.py localization/translations/pbs/pokemon_translatable.json -r PBS/pokemon.txt -o patches/PBS/pokemon.txt
  python repack_pbs.py localization/translations/pbs/moves_translatable.json -r PBS/moves.txt -o patches/PBS/moves.txt
        """
    )
    parser.add_argument('json_file', type=Path, help='Translated JSON file')
    parser.add_argument('-r', '--reference', type=Path, required=True,
                        help='Original PBS file for structure reference')
    parser.add_argument('-o', '--output', type=Path, default=None,
                        help='Output PBS file path (default: patches/PBS/<name>.txt)')

    args = parser.parse_args()

    if not args.json_file.exists():
        print(f"Error: JSON file not found: {args.json_file}")
        sys.exit(1)
    if not args.reference.exists():
        print(f"Error: Reference PBS file not found: {args.reference}")
        sys.exit(1)

    with open(args.json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    file_type = json_data.get('metadata', {}).get('file_type', '')
    if not file_type:
        # Fallback: detect from reference filename
        stem = args.reference.stem.lower()
        if stem == 'pokemon':
            file_type = 'pokemon'
        elif stem == 'moves':
            file_type = 'moves'
        elif stem == 'items':
            file_type = 'items'

    output_path = args.output
    if output_path is None:
        output_path = Path('patches/PBS') / args.reference.name

    if file_type == 'pokemon':
        repack_pokemon(json_data, args.reference, output_path)
    elif file_type == 'moves':
        repack_moves(json_data, args.reference, output_path)
    elif file_type == 'items':
        repack_items(json_data, args.reference, output_path)
    else:
        print(f"Error: Unknown file type '{file_type}'")
        sys.exit(1)


if __name__ == '__main__':
    main()
