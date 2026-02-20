#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, re, os

# Read source items file
with open(r'D:\Opalo V2.11\localization\translations\pbs\items.txt', 'r', encoding='utf-8-sig') as f:
    lines = [l.rstrip() for l in f.readlines()]

items = {}
for line in lines:
    if not line.strip() or line.startswith('#'):
        continue
    parts = line.split(',', 3)
    if len(parts) >= 3:
        internal = parts[1]
        items[internal] = line

print(f'Found {len(items)} items')

# Build comprehensive translation dictionary
TR = {}
