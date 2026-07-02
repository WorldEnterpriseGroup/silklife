#!/usr/bin/env python3
"""
Merge descriptions from original_descriptions.csv into image_upgrade/image_catalog.csv
"""

import csv
import os

def merge_descriptions():
    # File paths
    base_dir = '/mnt/d/silk/silklife'
    original_csv = os.path.join(base_dir, 'original_descriptions.csv')
    catalog_csv = os.path.join(base_dir, 'image_upgrade', 'image_catalog.csv')
    output_csv = os.path.join(base_dir, 'image_upgrade', 'image_catalog.csv')

    # Read original descriptions into a dictionary
    descriptions = {}
    with open(original_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            path = row['path']
            description = row['description']
            descriptions[path] = description

    print(f"Loaded {len(descriptions)} descriptions from original_descriptions.csv")

    # Read catalog and update descriptions
    catalog_rows = []
    restored_count = 0
    empty_count = 0

    with open(catalog_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        for row in reader:
            path = row['path']
            current_description = row['description']

            # If description is empty and we have one in original_descriptions
            if not current_description and path in descriptions:
                row['description'] = descriptions[path]
                restored_count += 1
                print(f"✓ Restored: {path}")
            elif not current_description:
                empty_count += 1

            catalog_rows.append(row)

    # Write updated catalog
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(catalog_rows)

    # Report
    print("\n" + "="*60)
    print("MERGE COMPLETE")
    print("="*60)
    print(f"Total images in catalog: {len(catalog_rows)}")
    print(f"Descriptions restored: {restored_count}")
    print(f"Still empty: {empty_count}")
    print(f"Updated catalog saved to: {output_csv}")

    return restored_count, empty_count

if __name__ == '__main__':
    merge_descriptions()
