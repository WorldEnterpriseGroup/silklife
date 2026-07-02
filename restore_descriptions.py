#!/usr/bin/env python3
"""
Restore descriptions in image_catalog.csv from new_image_catalog.csv

This script:
1. Reads new_image_catalog.csv to extract original paths and enhanced prompts
2. Extracts original descriptions by removing the professional photography prefix/suffix
3. Updates image_catalog.csv with the extracted descriptions
"""

import csv
import os

# Paths
NEW_CATALOG = '/mnt/d/silk/silklife/image_upgrade/new_image_catalog.csv'
IMAGE_CATALOG = '/mnt/d/silk/silklife/image_upgrade/image_catalog.csv'

# Prefix and suffix to remove from enhanced prompts
PREFIX = "Professional documentary photography, f/11 aperture, deep depth of field with everything in sharp focus. "
SUFFIX = " Studio-quality lighting, cinematic composition, photojournalistic authenticity. No text overlays."

def extract_original_description(enhanced_prompt):
    """Extract original description from enhanced prompt by removing prefix and suffix"""
    desc = enhanced_prompt

    # Remove prefix if present
    if desc.startswith(PREFIX):
        desc = desc[len(PREFIX):]

    # Remove suffix if present
    if desc.endswith(SUFFIX):
        desc = desc[:-len(SUFFIX)]

    # Also handle variant suffixes
    variant_suffixes = [
        " Studio-quality lighting, cinematic composition, photojournalistic authenticity. No text overlays, no captions.",
        " Studio-quality lighting, cinematic composition, photojornalistic authenticity. No text overlays, no captions.",
        " Studio-quality lighting, cinematic composition, photojournalistic authenticity. No text overlays, no captions, no branding.",
        " Studio-quality lighting, cinematic composition, photojournalistic authenticity. No text overlays, no captions, no SILK Yoga branding, no Find Your Practice text.",
    ]

    for variant_suffix in variant_suffixes:
        if desc.endswith(variant_suffix):
            desc = desc[:-len(variant_suffix)]
            break

    return desc.strip()

def main():
    print("Starting description restoration...")
    print(f"Reading from: {NEW_CATALOG}")
    print(f"Updating: {IMAGE_CATALOG}")
    print()

    # Step 1: Read new_image_catalog.csv and build mapping
    original_to_description = {}

    with open(NEW_CATALOG, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            original_path = row.get('original_path', '').strip()
            enhanced_prompt = row.get('description', '').strip()

            if original_path and enhanced_prompt:
                # Extract original description
                original_desc = extract_original_description(enhanced_prompt)
                original_to_description[original_path] = original_desc

    print(f"Found {len(original_to_description)} enhanced descriptions")
    print()

    # Step 2: Read image_catalog.csv
    rows = []
    with open(IMAGE_CATALOG, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        for row in reader:
            rows.append(row)

    print(f"Read {len(rows)} rows from image_catalog.csv")
    print()

    # Step 3: Update descriptions
    updated_count = 0
    skipped_count = 0

    for row in rows:
        path = row['path']

        if path in original_to_description:
            old_desc = row.get('description', '')
            new_desc = original_to_description[path]
            row['description'] = new_desc
            updated_count += 1

            if old_desc != new_desc:
                print(f"Updated: {path}")
                print(f"  Old: '{old_desc}'")
                print(f"  New: '{new_desc}'")
                print()
        else:
            skipped_count += 1

    # Step 4: Write updated CSV
    with open(IMAGE_CATALOG, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("=" * 80)
    print("RESTORATION COMPLETE")
    print("=" * 80)
    print(f"Total rows: {len(rows)}")
    print(f"Descriptions restored: {updated_count}")
    print(f"Skipped (not in new_catalog): {skipped_count}")
    print()
    print("Sample original descriptions:")
    for i, (path, desc) in enumerate(list(original_to_description.items())[:5]):
        print(f"  {i+1}. {os.path.basename(path)}")
        print(f"     {desc[:80]}...")
        print()

if __name__ == '__main__':
    main()
