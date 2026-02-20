#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pokemon Opalo PBS Translation Script
Translates items.txt, moves.txt, pokemon.txt, trainers.txt
from Spanish/English to Traditional Chinese (Taiwan)
"""
import re
import os
import sys
import json
import csv
import io

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'translations', 'pbs')

def load_glossary():
    """Load glossary from JSON file"""
    glossary_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'glossary.json')
    with open(glossary_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    result = {}
    def extract(obj):
        if isinstance(obj, dict):
            if 'terms' in obj and isinstance(obj['terms'], list):
                for t in obj['terms']:
                    if 'es' in t and 'zh_TW' in t:
                        result[t['es']] = t['zh_TW']
                    if 'internal' in t and 'zh_TW' in t:
                        result[t['internal']] = t['zh_TW']
            for k, v in obj.items():
                if k not in ('metadata', '_description'):
                    extract(v)
    extract(data.get('categories', {}))
    return result

# Will be populated by data loading functions
ITEM_TR = {}
MOVE_TR = {}
PKMN_TR = {}
TRAINER_CLASS_TR = {}

def init_data():
    """Initialize all translation data"""
    global ITEM_TR, MOVE_TR, PKMN_TR, TRAINER_CLASS_TR
    
    # Load from external data files if they exist
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'translation_data')
    
    for fname, target_name in [('items_zh.json', 'ITEM_TR'), ('moves_zh.json', 'MOVE_TR'), 
                                ('pokemon_zh.json', 'PKMN_TR'), ('trainers_zh.json', 'TRAINER_CLASS_TR')]:
        fpath = os.path.join(data_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, 'r', encoding='utf-8') as f:
                globals()[target_name] = json.load(f)

def translate_items():
    """Translate items.txt"""
    src = os.path.join(BASE, 'items.txt')
    with open(src, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    
    out_lines = []
    translated = 0
    total = 0
    
    for line in lines:
        line = line.rstrip('\n').rstrip('\r')
        if not line.strip() or line.strip().startswith('#'):
            out_lines.append(line)
            continue
        
        # Parse CSV-like format
        # Format: ID,INTERNAL,Name,PluralName,pocket,price,"Description",cat,f1,f2,extra
        total += 1
        
        # Extract internal code (field 2)
        parts = line.split(',', 3)
        if len(parts) < 3:
            out_lines.append(line)
            continue
        
        internal = parts[1]
        
        if internal in ITEM_TR:
            tr = ITEM_TR[internal]
            zh_name = tr.get('name', '')
            zh_plural = tr.get('plural', zh_name)
            zh_desc = tr.get('desc', '')
            
            if zh_name:
                # Reconstruct line with translated name, plural, and description
                # Need to carefully replace fields 3, 4, and the quoted description
                new_line = rebuild_item_line(line, zh_name, zh_plural, zh_desc)
                out_lines.append(new_line)
                translated += 1
            else:
                out_lines.append(line)
        else:
            out_lines.append(line)
    
    with open(src, 'w', encoding='utf-8-sig') as f:
        f.write('\n'.join(out_lines) + '\n' if out_lines else '')
    
    print(f'items.txt: {translated}/{total} entries translated')

def rebuild_item_line(line, zh_name, zh_plural, zh_desc):
    """Rebuild an item CSV line with translated fields"""
    # Parse the line carefully, handling quoted fields
    # Format: ID,INTERNAL,Name,PluralName,pocket,price,"Description",cat,f1,f2,extra
    
    # Use a regex to parse: handle quoted description field
    # Match: number,INTERNAL,name,plural,pocket,price,"desc",rest...
    m = re.match(r'^(\d+),([^,]+),([^,]+),([^,]+),(\d+),(\d+),("(?:[^"]*(?:""[^"]*)*)"?|[^,]*),(.*)', line)
    if not m:
        # Try simpler parsing
        parts = line.split(',')
        if len(parts) >= 7:
            parts[2] = zh_name
            parts[3] = zh_plural
            # Find and replace description
            if zh_desc:
                # Find the quoted description
                line_str = ','.join(parts)
                desc_match = re.search(r'"[^"]*"', line_str)
                if desc_match:
                    line_str = line_str[:desc_match.start()] + '"' + zh_desc + '"' + line_str[desc_match.end():]
                return line_str
            return ','.join(parts)
        return line
    
    id_num = m.group(1)
    internal = m.group(2)
    old_name = m.group(3)
    old_plural = m.group(4)
    pocket = m.group(5)
    price = m.group(6)
    old_desc = m.group(7)
    rest = m.group(8)
    
    if zh_desc:
        new_desc = '"' + zh_desc + '"'
    else:
        new_desc = old_desc
    
    return f'{id_num},{internal},{zh_name},{zh_plural},{pocket},{price},{new_desc},{rest}'

def translate_moves():
    """Translate moves.txt"""
    src = os.path.join(BASE, 'moves.txt')
    with open(src, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    
    out_lines = []
    translated = 0
    total = 0
    
    for line in lines:
        line = line.rstrip('\n').rstrip('\r')
        if not line.strip() or line.strip().startswith('#'):
            out_lines.append(line)
            continue
        
        total += 1
        # Format: ID,INTERNAL,Name,flags,power,TYPE,Category,accuracy,pp,effect,flags2,priority,flags3,"Description"
        parts = line.split(',', 3)
        if len(parts) < 3:
            out_lines.append(line)
            continue
        
        internal = parts[1]
        
        if internal in MOVE_TR:
            tr = MOVE_TR[internal]
            zh_name = tr.get('name', '')
            zh_desc = tr.get('desc', '')
            
            if zh_name:
                new_line = rebuild_move_line(line, zh_name, zh_desc)
                out_lines.append(new_line)
                translated += 1
            else:
                out_lines.append(line)
        else:
            out_lines.append(line)
    
    with open(src, 'w', encoding='utf-8-sig') as f:
        f.write('\n'.join(out_lines) + '\n' if out_lines else '')
    
    print(f'moves.txt: {translated}/{total} entries translated')

def rebuild_move_line(line, zh_name, zh_desc):
    """Rebuild a move CSV line with translated fields"""
    # Format: ID,INTERNAL,Name,flags,power,TYPE,Category,accuracy,pp,effect,flags2,priority,flags3,"Description"
    # Replace field 3 (Name) and last quoted field (Description)
    
    # Split into parts
    parts = line.split(',')
    if len(parts) < 3:
        return line
    
    parts[2] = zh_name
    
    if zh_desc:
        # Find and replace the quoted description (last quoted field)
        joined = ','.join(parts)
        # Replace last quoted string
        last_quote_start = joined.rfind('"')
        if last_quote_start > 0:
            first_quote = joined.rfind('"', 0, last_quote_start)
            if first_quote >= 0:
                joined = joined[:first_quote] + '"' + zh_desc + '"' + joined[last_quote_start+1:]
                return joined
    
    return ','.join(parts)

def translate_pokemon():
    """Translate pokemon.txt"""
    src = os.path.join(BASE, 'pokemon.txt')
    with open(src, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    
    translated_names = 0
    translated_dex = 0
    total = 0
    
    lines = content.split('\n')
    out_lines = []
    current_internal = None
    
    for line in lines:
        stripped = line.rstrip('\r')
        
        if stripped.startswith('InternalName='):
            current_internal = stripped[len('InternalName='):]
            total += 1
            out_lines.append(stripped)
        elif stripped.startswith('Name=') and current_internal:
            if current_internal in PKMN_TR:
                zh_name = PKMN_TR[current_internal].get('name', '')
                if zh_name:
                    out_lines.append(f'Name={zh_name}')
                    translated_names += 1
                else:
                    out_lines.append(stripped)
            else:
                out_lines.append(stripped)
        elif stripped.startswith('Pokedex=') and current_internal:
            if current_internal in PKMN_TR:
                zh_dex = PKMN_TR[current_internal].get('dex', '')
                if zh_dex:
                    out_lines.append(f'Pokedex={zh_dex}')
                    translated_dex += 1
                else:
                    out_lines.append(stripped)
            else:
                out_lines.append(stripped)
        else:
            out_lines.append(stripped)
    
    with open(src, 'w', encoding='utf-8-sig') as f:
        f.write('\n'.join(out_lines))
    
    print(f'pokemon.txt: {translated_names}/{total} names, {translated_dex}/{total} pokedex translated')

def translate_trainers():
    """Translate trainers.txt trainer class names"""
    src = os.path.join(BASE, 'trainers.txt')
    with open(src, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    
    out_lines = []
    translated = 0
    total_classes = 0
    in_separator = False
    expect_class = False
    
    for i, line in enumerate(lines):
        stripped = line.rstrip('\n').rstrip('\r')
        
        if stripped.startswith('#---'):
            in_separator = True
            expect_class = True
            out_lines.append(stripped)
            continue
        
        if expect_class and stripped and not stripped.startswith('#'):
            expect_class = False
            total_classes += 1
            if stripped in TRAINER_CLASS_TR:
                out_lines.append(TRAINER_CLASS_TR[stripped])
                translated += 1
            else:
                out_lines.append(stripped)
            continue
        
        expect_class = False
        out_lines.append(stripped)
    
    with open(src, 'w', encoding='utf-8-sig') as f:
        f.write('\n'.join(out_lines) + '\n' if out_lines else '')
    
    print(f'trainers.txt: {translated}/{total_classes} trainer classes translated')

if __name__ == '__main__':
    print('Loading translation data...')
    init_data()
    
    if not ITEM_TR and not MOVE_TR and not PKMN_TR:
        print('No translation data found. Please generate data files first.')
        print('Run: python generate_translation_data.py')
        sys.exit(1)
    
    print(f'Loaded: {len(ITEM_TR)} items, {len(MOVE_TR)} moves, {len(PKMN_TR)} pokemon, {len(TRAINER_CLASS_TR)} trainer classes')
    
    print('\nTranslating items.txt...')
    translate_items()
    
    print('\nTranslating moves.txt...')
    translate_moves()
    
    print('\nTranslating pokemon.txt...')
    translate_pokemon()
    
    print('\nTranslating trainers.txt...')
    translate_trainers()
    
    print('\nDone!')
