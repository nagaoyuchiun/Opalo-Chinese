#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quick script to inspect Ruby Marshal data structure"""

from rubymarshal.reader import load
import sys

def inspect_structure(data, depth=0, max_depth=3, max_items=5):
    """Recursively inspect and print data structure"""
    indent = "  " * depth
    
    if depth > max_depth:
        print(f"{indent}... (max depth reached)")
        return
    
    data_type = type(data).__name__
    
    if isinstance(data, dict):
        print(f"{indent}Dict with {len(data)} items:")
        for i, (key, value) in enumerate(list(data.items())[:max_items]):
            print(f"{indent}  Key: {repr(key)} ({type(key).__name__})")
            print(f"{indent}  Value:", end=" ")
            if isinstance(value, str):
                print(f"'{value[:50]}...' (len={len(value)})" if len(value) > 50 else f"'{value}'")
            else:
                print()
                inspect_structure(value, depth + 2, max_depth, max_items)
        if len(data) > max_items:
            print(f"{indent}  ... and {len(data) - max_items} more items")
    
    elif isinstance(data, (list, tuple)):
        print(f"{indent}{data_type} with {len(data)} items:")
        for i, item in enumerate(data[:max_items]):
            print(f"{indent}  [{i}]:", end=" ")
            if isinstance(item, str):
                print(f"'{item[:50]}...' (len={len(item)})" if len(item) > 50 else f"'{item}'")
            else:
                print()
                inspect_structure(item, depth + 2, max_depth, max_items)
        if len(data) > max_items:
            print(f"{indent}  ... and {len(data) - max_items} more items")
    
    elif isinstance(data, str):
        print(f"{indent}String: '{data[:100]}...' (len={len(data)})" if len(data) > 100 else f"{indent}String: '{data}'")
    
    else:
        print(f"{indent}{data_type}: {repr(data)[:100]}")

if __name__ == '__main__':
    file_path = sys.argv[1] if len(sys.argv) > 1 else 'Data/messages.dat'
    
    print(f"Inspecting: {file_path}\n")
    
    with open(file_path, 'rb') as f:
        data = load(f)
    
    print(f"Root type: {type(data).__name__}")
    print("="*60)
    inspect_structure(data)
