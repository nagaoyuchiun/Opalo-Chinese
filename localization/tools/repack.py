#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pokémon Opalo Text Repack Tool
Repacks translated JSON back to Ruby Marshal format game data files.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Union

try:
    from rubymarshal.reader import load as ruby_load
    from rubymarshal.writer import write as ruby_dump
except ImportError:
    print("Error: rubymarshal library not found. Install with: pip install rubymarshal")
    sys.exit(1)


def apply_translations(data: Any, translations: Dict[str, str], parent_key: str = "") -> Any:
    """
    Recursively apply translations to Ruby Marshal data structure.
    
    Args:
        data: Parsed Ruby Marshal data structure
        translations: Dictionary mapping IDs to translated text
        parent_key: Parent key for context tracking
        
    Returns:
        Modified data structure with translations applied
    """
    # Handle Ruby UserDef objects (OrderedHash) with @keys attribute
    if hasattr(data, 'attributes') and '@keys' in data.attributes:
        # This is an OrderedHash - modify the keys in place
        keys = data.attributes['@keys']
        for idx, key in enumerate(keys):
            # Decode the key to string
            if isinstance(key, bytes):
                try:
                    text = key.decode('utf-8')
                except UnicodeDecodeError:
                    text = key.decode('latin-1')
            else:
                text = str(key)
            
            # Check if we have a translation
            entry_id = f"{parent_key}.{idx}" if parent_key else f"msg_{idx}"
            if entry_id in translations and translations[entry_id]:
                # Apply translation by encoding back to bytes
                translated = translations[entry_id]
                try:
                    data.attributes['@keys'][idx] = translated.encode('utf-8')
                except AttributeError:
                    data.attributes['@keys'][idx] = translated
        
        return data
    
    # Handle regular dicts
    elif isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            key_str = str(key) if key is not None else "unknown"
            new_parent = f"{parent_key}.{key_str}" if parent_key else key_str
            
            if isinstance(value, str) and value.strip():
                # Check if we have a translation for this path
                if new_parent in translations:
                    translated = translations[new_parent]
                    # Only apply non-empty translations
                    new_dict[key] = translated if translated else value
                else:
                    new_dict[key] = value
            else:
                # Recursively process nested structures
                new_dict[key] = apply_translations(value, translations, new_parent)
        return new_dict
        
    elif isinstance(data, list):
        new_list = []
        for idx, item in enumerate(data):
            # Match extract.py's parent_key format for lists
            new_parent = f"section_{idx}" if not parent_key else f"{parent_key}[{idx}]"
            
            if isinstance(item, str) and item.strip():
                # Check if we have a translation for this path
                if new_parent in translations:
                    translated = translations[new_parent]
                    new_list.append(translated if translated else item)
                else:
                    new_list.append(item)
            else:
                new_list.append(apply_translations(item, translations, new_parent))
        return new_list
        
    elif isinstance(data, tuple):
        # Convert to list, process, then back to tuple
        new_list = []
        for idx, item in enumerate(data):
            new_parent = f"{parent_key}[{idx}]"
            
            if isinstance(item, str) and item.strip():
                if new_parent in translations:
                    translated = translations[new_parent]
                    new_list.append(translated if translated else item)
                else:
                    new_list.append(item)
            else:
                new_list.append(apply_translations(item, translations, new_parent))
        return tuple(new_list)
        
    elif isinstance(data, str) and data.strip():
        # Direct string value
        key = parent_key or "root"
        if key in translations:
            translated = translations[key]
            return translated if translated else data
        return data
    
    # For all other types, return as-is
    return data


def load_translation_json(json_file: Path) -> tuple[Any, Dict[str, str], Dict[str, Any]]:
    """
    Load translation JSON and extract the translation mapping.
    
    Args:
        json_file: Path to translation JSON file
        
    Returns:
        Tuple of (metadata, translations_dict, full_data)
    """
    print(f"Reading translations from: {json_file}")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ Successfully loaded translation file")
    except Exception as e:
        print(f"✗ Error reading JSON file: {e}")
        sys.exit(1)
    
    # Extract metadata
    metadata = data.get('metadata', {})
    entries = data.get('entries', [])
    
    # Build translation mapping: ID -> translation
    translations = {}
    translated_count = 0
    
    for entry in entries:
        entry_id = entry.get('id', '')
        translation = entry.get('translation', '')
        
        if entry_id:
            translations[entry_id] = translation
            if translation:
                translated_count += 1
    
    print(f"✓ Loaded {len(entries)} entries ({translated_count} translated)")
    
    return metadata, translations, data


def repack_messages(json_file: Path, original_file: Path, output_file: Path) -> None:
    """
    Repack translated JSON back to Ruby Marshal format.
    
    Args:
        json_file: Path to translation JSON file
        original_file: Path to original .dat file (for structure reference)
        output_file: Path to output .dat file
    """
    print(f"\nReading original file: {original_file}")
    
    try:
        with open(original_file, 'rb') as f:
            original_data = ruby_load(f)
        print(f"✓ Successfully loaded original Ruby Marshal data")
    except Exception as e:
        print(f"✗ Error reading original file: {e}")
        sys.exit(1)
    
    # Load translations
    metadata, translations, json_data = load_translation_json(json_file)
    
    # Verify source file matches
    source_file = metadata.get('source_file', '')
    if source_file and original_file.name not in source_file:
        print(f"⚠ Warning: Source file mismatch")
        print(f"  JSON metadata: {source_file}")
        print(f"  Original file: {original_file.name}")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            sys.exit(1)
    
    print(f"\nApplying translations...")
    translated_data = apply_translations(original_data, translations)
    
    # Create output directory if needed
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Writing to: {output_file}")
    
    try:
        with open(output_file, 'wb') as f:
            ruby_dump(f, translated_data)
        print(f"✓ Successfully saved repacked data")
    except Exception as e:
        print(f"✗ Error writing file: {e}")
        sys.exit(1)
    
    # Verify the repacked file can be read back
    print(f"\nVerifying repacked file...")
    try:
        with open(output_file, 'rb') as f:
            verify_data = ruby_load(f)
        print(f"✓ Verification successful: File can be read back")
    except Exception as e:
        print(f"✗ Verification failed: {e}")
        print(f"⚠ Warning: The output file may be corrupted!")
        sys.exit(1)
    
    # Show statistics
    print(f"\n--- Statistics ---")
    print(f"Total entries: {metadata.get('total_entries', 0)}")
    print(f"Translations applied: {sum(1 for t in translations.values() if t)}")
    print(f"Output file size: {output_file.stat().st_size} bytes")


def main():
    """Main entry point for the repack tool."""
    parser = argparse.ArgumentParser(
        description='Repack translated JSON back to Pokémon Opalo game files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Repack with original file for structure reference
  python repack.py translations/messages.json -r Data/messages.dat -o patches/messages.dat
  
  # Auto-detect original file location
  python repack.py translations/messages.json --output patches/messages.dat
        """
    )
    
    parser.add_argument(
        'json_file',
        type=Path,
        help='Input translation JSON file'
    )
    
    parser.add_argument(
        '-r', '--reference',
        type=Path,
        default=None,
        help='Original .dat file for structure reference (auto-detect if not specified)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=None,
        help='Output .dat file path (default: patches/<source_name>.dat)'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Skip verification prompts'
    )
    
    args = parser.parse_args()
    
    # Validate input JSON file
    if not args.json_file.exists():
        print(f"Error: Translation JSON file not found: {args.json_file}")
        sys.exit(1)
    
    # Try to auto-detect original file if not specified
    if args.reference is None:
        # Load JSON to get source file info
        try:
            with open(args.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            source_file = data.get('metadata', {}).get('source_file', '')
            
            if source_file:
                # Try to find the file in Data/ directory
                possible_paths = [
                    Path('Data') / source_file,
                    Path('../Data') / source_file,
                    Path('../../Data') / source_file,
                ]
                
                for path in possible_paths:
                    if path.exists():
                        args.reference = path
                        print(f"Auto-detected original file: {path}")
                        break
        except Exception as e:
            print(f"Warning: Could not auto-detect original file: {e}")
    
    if args.reference is None:
        print("Error: Could not find original .dat file")
        print("Please specify with -r/--reference option")
        sys.exit(1)
    
    if not args.reference.exists():
        print(f"Error: Original file not found: {args.reference}")
        sys.exit(1)
    
    # Determine output file
    if args.output is None:
        output_file = Path('patches') / args.reference.name
    else:
        output_file = args.output
    
    print("="*60)
    print("Pokémon Opalo Text Repack Tool")
    print("="*60)
    
    repack_messages(args.json_file, args.reference, output_file)
    
    print("\n" + "="*60)
    print("Repack complete!")
    print("="*60)


if __name__ == '__main__':
    main()
