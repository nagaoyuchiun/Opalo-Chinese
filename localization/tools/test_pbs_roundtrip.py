#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""End-to-end test for extract_pbs.py and repack_pbs.py."""

import json
import os
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE / 'localization' / 'tools'))

from extract_pbs import extract_pokemon, extract_moves


def test_pokemon_roundtrip():
    """Test: extract pokemon → fill translations → repack → verify."""
    print("=" * 60)
    print("TEST: pokemon.txt roundtrip")
    print("=" * 60)

    pbs_path = BASE / 'PBS' / 'pokemon.txt'
    data = extract_pokemon(pbs_path)

    # Only first 3 entries
    data['entries'] = data['entries'][:3]
    data['metadata']['total_entries'] = 3

    # Verify only Name/Kind/Pokedex extracted
    for e in data['entries']:
        keys = set(e['fields'].keys())
        assert keys <= {'Name', 'Kind', 'Pokedex'}, f"Unexpected fields: {keys}"
    print("✓ Only Name/Kind/Pokedex extracted (no numeric fields)")

    # Fill mock translations
    translations = {
        '1': {'Name': '妙蛙種子', 'Kind': '種子', 'Pokedex': '妙蛙種子能在陽光下打盹。'},
        '2': {'Name': '妙蛙草', 'Kind': '種子', 'Pokedex': '為了支撐花苞，妙蛙草的腿長得很壯。'},
        '3': {'Name': '妙蛙花', 'Kind': '種子', 'Pokedex': '妙蛙花的花朵據說營養充足就會色彩鮮艷。'},
    }
    for entry in data['entries']:
        sid = entry['section_id']
        if sid in translations:
            entry['fields'] = translations[sid]

    # Write translated JSON
    with tempfile.TemporaryDirectory() as tmpdir:
        json_path = Path(tmpdir) / 'pokemon_translated.json'
        output_path = Path(tmpdir) / 'pokemon_out.txt'

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Repack
        from repack_pbs import repack_pokemon
        repack_pokemon(data, pbs_path, output_path)

        # Verify output
        with open(output_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()

        lines = content.split('\n')

        # Check translations applied
        assert 'Name=妙蛙種子' in content, "Translation for Bulbasaur not found"
        assert 'Kind=種子' in content, "Translation for Kind not found"
        assert 'Name=妙蛙草' in content, "Translation for Ivysaur not found"
        assert 'Name=妙蛙花' in content, "Translation for Venusaur not found"
        print("✓ Translations applied correctly")

        # Check numeric fields preserved
        assert 'BaseStats=45,49,49,45,65,65' in content, "BaseStats modified!"
        assert 'Rareness=45' in content, "Rareness modified!"
        assert 'Height=0.7' in content, "Height modified!"
        assert 'InternalName=BULBASAUR' in content, "InternalName modified!"
        assert 'Type1=GRASS' in content, "Type1 modified!"
        assert 'Evolutions=IVYSAUR,Level,16' in content, "Evolutions modified!"
        print("✓ All numeric/structural fields preserved")

        # Check section 4 (Charmander) is untranslated (not in our 3 entries)
        assert 'Name=Charmander' in content, "Section 4 should be untouched"
        print("✓ Untranslated sections left intact")

    print("PASS ✓\n")


def test_moves_roundtrip():
    """Test: extract moves → fill translations → repack → verify."""
    print("=" * 60)
    print("TEST: moves.txt roundtrip")
    print("=" * 60)

    pbs_path = BASE / 'PBS' / 'moves.txt'
    data = extract_moves(pbs_path)

    # Only first 5 entries
    data['entries'] = data['entries'][:5]
    data['metadata']['total_entries'] = 5

    # Verify only display_name/description
    for e in data['entries']:
        keys = set(e['fields'].keys())
        assert keys <= {'display_name', 'description'}, f"Unexpected fields: {keys}"
    print("✓ Only display_name/description extracted")

    # Fill mock translations
    mock = {
        'MEGAHORN': {'display_name': '超級角擊', 'description': '用巨大的角猛烈撞擊。'},
        'ATTACKORDER': {'display_name': '攻擊指令', 'description': '召喚同伴發動攻擊。容易擊中要害。'},
        'BUGBUZZ': {'display_name': '蟲鳴', 'description': '振動翅膀產生音波攻擊。可能降低特防。'},
    }
    for entry in data['entries']:
        iname = entry['internal_name']
        if iname in mock:
            entry['fields'] = mock[iname]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / 'moves_out.txt'

        from repack_pbs import repack_moves
        repack_moves(data, pbs_path, output_path)

        with open(output_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()

        lines = content.strip().split('\n')

        # Check line 1: MEGAHORN translated
        assert '超級角擊' in lines[0], f"MEGAHORN display_name not translated: {lines[0]}"
        assert '用巨大的角猛烈撞擊' in lines[0], f"MEGAHORN description not translated: {lines[0]}"
        print("✓ MEGAHORN translated correctly")

        # Check numeric fields preserved in line 1
        assert ',120,' in lines[0], f"Power value changed in MEGAHORN: {lines[0]}"
        assert ',BUG,' in lines[0], f"Type changed in MEGAHORN: {lines[0]}"
        assert ',Physical,' in lines[0], f"Category changed in MEGAHORN: {lines[0]}"
        print("✓ Numeric fields preserved in moves")

        # Check untranslated lines (4, 5) still have original text
        # Line 4 is XSCISSOR (index 3), line 5 is SIGNALBEAM (index 4)
        assert 'Tijera X' in lines[3], f"Untranslated move changed: {lines[3]}"
        print("✓ Untranslated moves left intact")

    print("PASS ✓\n")


if __name__ == '__main__':
    test_pokemon_roundtrip()
    test_moves_roundtrip()
    print("=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)
