#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pokémon Opalo Text Extraction Tool
Extracts translatable text from Ruby Marshal format game data files.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Union

try:
    from rubymarshal.reader import load as ruby_load
except ImportError:
    print("Error: rubymarshal library not found. Install with: pip install rubymarshal")
    sys.exit(1)


def parse_ruby_data(data: Any, parent_key: str = "", depth: int = 0) -> List[Dict[str, Any]]:
    """
    Recursively parse Ruby Marshal data and extract text strings.
    
    Args:
        data: Parsed Ruby Marshal data structure
        parent_key: Parent key for context tracking
        
    Returns:
        List of extracted text entries with metadata
    """
    entries = []
    
    # Prevent infinite recursion
    if depth > 30:
        return entries
    
    # Handle Ruby UserDef objects (OrderedHash)
    if hasattr(data, 'attributes') and '@keys' in data.attributes:
        # This is an OrderedHash with keys
        keys = data.attributes['@keys']
        for idx, key in enumerate(keys):
            # Keys are byte strings, decode them
            if isinstance(key, bytes):
                try:
                    text = key.decode('utf-8')
                except UnicodeDecodeError:
                    text = key.decode('latin-1')
            else:
                text = str(key)
            
            if text.strip():
                entry_id = f"{parent_key}.{idx}" if parent_key else f"msg_{idx}"
                entries.append({
                    "id": entry_id,
                    "original": text,
                    "translation": "",
                    "context": {
                        "parent": parent_key or "root",
                        "index": idx,
                        "type": "ordered_hash_key"
                    }
                })
    
    # Handle regular dicts
    elif isinstance(data, dict):
        for key, value in data.items():
            # Convert Ruby symbols or objects to strings for keys
            key_str = str(key) if key is not None else "unknown"
            new_parent = f"{parent_key}.{key_str}" if parent_key else key_str
            
            if isinstance(value, str) and value.strip():
                # Found a string - create an entry
                entries.append({
                    "id": new_parent,
                    "original": value,
                    "translation": "",
                    "context": {
                        "parent": parent_key or "root",
                        "key": key_str,
                        "type": "dict_value"
                    }
                })
            else:
                # Recursively process nested structures
                entries.extend(parse_ruby_data(value, new_parent, depth + 1))
                
    # Handle lists and tuples
    elif isinstance(data, (list, tuple)):
        for idx, item in enumerate(data):
            new_parent = f"section_{idx}" if not parent_key else f"{parent_key}[{idx}]"
            
            if isinstance(item, str) and item.strip():
                entries.append({
                    "id": new_parent,
                    "original": item,
                    "translation": "",
                    "context": {
                        "parent": parent_key or "root",
                        "index": idx,
                        "type": "array_item"
                    }
                })
            else:
                entries.extend(parse_ruby_data(item, new_parent, depth + 1))
                
    # Handle direct strings
    elif isinstance(data, str) and data.strip():
        # Direct string value
        entries.append({
            "id": parent_key or "root",
            "original": data,
            "translation": "",
            "context": {
                "parent": "root",
                "type": "direct_value"
            }
        })
    
    # Handle byte strings
    elif isinstance(data, bytes):
        try:
            text = data.decode('utf-8')
        except UnicodeDecodeError:
            text = data.decode('latin-1')
        
        if text.strip():
            entries.append({
                "id": parent_key or "root",
                "original": text,
                "translation": "",
                "context": {
                    "parent": "root",
                    "type": "bytes_value"
                }
            })
    
    return entries


def extract_messages(input_file: Path, output_file: Path) -> None:
    """
    Extract messages from Ruby Marshal format file and save as JSON.
    
    Args:
        input_file: Path to input .dat file
        output_file: Path to output .json file
    """
    print(f"Reading: {input_file}")
    
    try:
        with open(input_file, 'rb') as f:
            data = ruby_load(f)
        print(f"✓ Successfully loaded Ruby Marshal data")
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        sys.exit(1)
    
    print(f"Extracting text strings...")
    entries = parse_ruby_data(data)
    
    print(f"✓ Extracted {len(entries)} text entries")
    
    # Prepare output structure
    output_data = {
        "metadata": {
            "source_file": str(input_file),
            "total_entries": len(entries),
            "source_language": "es",
            "target_language": "zh-TW",
            "extraction_version": "1.0"
        },
        "entries": entries
    }
    
    # Create output directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Writing to: {output_file}")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"✓ Successfully saved {len(entries)} entries to JSON")
    except Exception as e:
        print(f"✗ Error writing file: {e}")
        sys.exit(1)
    
    # Show sample entries
    if entries:
        print("\n--- Sample Entries (first 3) ---")
        for entry in entries[:3]:
            print(f"ID: {entry['id']}")
            print(f"Original: {entry['original'][:80]}{'...' if len(entry['original']) > 80 else ''}")
            print(f"Context: {entry['context']}")
            print()


def main():
    """Main entry point for the extraction tool."""
    parser = argparse.ArgumentParser(
        description='Extract translatable text from Pokémon Opalo game files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python extract.py Data/messages.dat -o translations/messages.json
  python extract.py ../Data/messages.dat --output=output.json
        """
    )
    
    parser.add_argument(
        'input_file',
        type=Path,
        help='Input Ruby Marshal format file (.dat)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=None,
        help='Output JSON file path (default: translations/<input_name>.json)'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not args.input_file.exists():
        print(f"Error: Input file not found: {args.input_file}")
        sys.exit(1)
    
    # Determine output file
    if args.output is None:
        output_file = Path('translations') / f"{args.input_file.stem}.json"
    else:
        output_file = args.output
    
    print("="*60)
    print("Pokémon Opalo Text Extraction Tool")
    print("="*60)
    
    extract_messages(args.input_file, output_file)
    
    print("\n" + "="*60)
    print("Extraction complete!")
    print("="*60)


if __name__ == '__main__':
    main()
