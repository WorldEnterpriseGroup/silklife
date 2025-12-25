#!/usr/bin/env python3
"""
Regenerate image_catalog.csv by scanning images directories and cross-referencing
with new_image_catalog.csv to mark upgraded images.
"""

import os
import csv
import subprocess
from pathlib import Path
from datetime import datetime

# Base directory
BASE_DIR = Path("/mnt/d/silk/silklife")
CATALOG_DIR = BASE_DIR / "image_upgrade"
NEW_CATALOG_PATH = CATALOG_DIR / "new_image_catalog.csv"
OUTPUT_PATH = CATALOG_DIR / "image_catalog.csv"

# Directories to scan
IMAGE_DIRS = [
    BASE_DIR / "images/articles",
    BASE_DIR / "images/homepage",
    BASE_DIR / "images/ads"
]

def load_new_catalog():
    """Load new_image_catalog.csv and create lookup dict"""
    upgraded_images = {}

    if not NEW_CATALOG_PATH.exists():
        print(f"Warning: {NEW_CATALOG_PATH} not found")
        return upgraded_images

    with open(NEW_CATALOG_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Normalize path
            path = row['path'].replace('\\', '/')

            # Skip paths that don't start with images/ (e.g., temp files)
            if not path.startswith('images/'):
                continue

            # Extract original description from enhanced prompt
            # Enhanced prompts start with "Professional documentary photography, f/11 aperture..."
            description = row.get('description', '').strip()

            # Remove the f/11 wrapper if present
            if description.startswith("Professional documentary photography, f/11 aperture"):
                # Split on ". " and find the actual content description
                # Pattern: "Professional documentary photography, f/11 aperture, deep depth of field with everything in sharp focus. [ACTUAL DESCRIPTION]. Studio-quality lighting..."
                parts = description.split('. ')

                # Find the content between the intro and the "Studio-quality" ending
                content_parts = []
                skip_first = True
                for part in parts:
                    if skip_first and 'sharp focus' in part:
                        skip_first = False
                        continue
                    if 'Studio-quality lighting' in part or 'No text overlays' in part:
                        break
                    if not skip_first:
                        content_parts.append(part)

                if content_parts:
                    description = '. '.join(content_parts).strip()
                    # Remove trailing period if present
                    if description.endswith('.'):
                        description = description[:-1]

            upgraded_images[path] = {
                'description': description,
                'model': row.get('model', 'gemini-3-pro-image-preview'),
                'date_modified': row.get('date_modified', '')
            }

    print(f"Loaded {len(upgraded_images)} upgraded images from new_image_catalog.csv")
    return upgraded_images

def get_image_info(image_path):
    """Get image dimensions and modification date"""
    try:
        # Get dimensions using identify command
        result = subprocess.run(
            ['identify', '-format', '%wx%h', str(image_path)],
            capture_output=True,
            text=True,
            check=True
        )
        dimensions = result.stdout.strip()

        # Get modification date
        mtime = os.path.getmtime(image_path)
        date_modified = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')

        return dimensions, date_modified
    except Exception as e:
        print(f"Error reading {image_path}: {e}")
        return "unknown", "unknown"

def scan_images():
    """Scan all image directories and build catalog"""
    images = []

    for image_dir in IMAGE_DIRS:
        if not image_dir.exists():
            print(f"Warning: Directory {image_dir} not found")
            continue

        # Find all image files recursively
        for ext in ['*.webp', '*.png', '*.jpg', '*.jpeg']:
            for image_path in image_dir.rglob(ext):
                # Get relative path from BASE_DIR
                rel_path = str(image_path.relative_to(BASE_DIR)).replace('\\', '/')

                # Get image info
                dimensions, date_modified = get_image_info(image_path)

                # Get file extension
                file_ext = image_path.suffix

                images.append({
                    'path': rel_path,
                    'type': file_ext,
                    'dimensions': dimensions,
                    'date_modified': date_modified
                })

    print(f"Found {len(images)} total images")
    return images

def merge_catalogs(images, upgraded_images):
    """Merge scanned images with upgraded image info"""
    catalog = []

    for img in images:
        path = img['path']

        # Check if this image was upgraded
        if path in upgraded_images:
            upgraded = upgraded_images[path]
            catalog.append({
                'path': path,
                'type': img['type'],
                'dimensions': img['dimensions'],
                'date_modified': img['date_modified'],
                'model': upgraded['model'],
                'description': upgraded['description'],
                'upgraded': 'true'
            })
        else:
            # Not upgraded yet
            catalog.append({
                'path': path,
                'type': img['type'],
                'dimensions': img['dimensions'],
                'date_modified': img['date_modified'],
                'model': 'gemini-2.5-flash',
                'description': '',
                'upgraded': 'false'
            })

    return catalog

def write_catalog(catalog):
    """Write catalog to CSV"""
    fieldnames = ['path', 'type', 'dimensions', 'date_modified', 'model', 'description', 'upgraded']

    with open(OUTPUT_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(catalog)

    print(f"Wrote catalog to {OUTPUT_PATH}")

def print_report(catalog):
    """Print summary report"""
    total = len(catalog)
    upgraded = sum(1 for img in catalog if img['upgraded'] == 'true')
    remaining = total - upgraded

    remaining_with_desc = sum(1 for img in catalog
                              if img['upgraded'] == 'false' and img['description'])
    remaining_empty = sum(1 for img in catalog
                         if img['upgraded'] == 'false' and not img['description'])

    print("\n" + "="*60)
    print("IMAGE CATALOG REGENERATION REPORT")
    print("="*60)
    print(f"Total images found:           {total}")
    print(f"Already upgraded:             {upgraded}")
    print(f"Remaining to upgrade:         {remaining}")
    print(f"  - With descriptions:        {remaining_with_desc}")
    print(f"  - Empty descriptions:       {remaining_empty}")
    print("="*60)

    # Show breakdown by directory
    print("\nBreakdown by directory:")
    dirs = {}
    for img in catalog:
        dir_name = img['path'].split('/')[1]  # e.g., 'articles', 'homepage', 'ads'
        if dir_name not in dirs:
            dirs[dir_name] = {'total': 0, 'upgraded': 0}
        dirs[dir_name]['total'] += 1
        if img['upgraded'] == 'true':
            dirs[dir_name]['upgraded'] += 1

    for dir_name, counts in sorted(dirs.items()):
        remaining = counts['total'] - counts['upgraded']
        print(f"  images/{dir_name}:  {counts['total']} total, {counts['upgraded']} upgraded, {remaining} remaining")

def main():
    print("Starting image catalog regeneration...")

    # Load upgraded images from new_image_catalog.csv
    upgraded_images = load_new_catalog()

    # Scan all images
    images = scan_images()

    # Merge catalogs
    catalog = merge_catalogs(images, upgraded_images)

    # Sort by path
    catalog.sort(key=lambda x: x['path'])

    # Write to file
    write_catalog(catalog)

    # Print report
    print_report(catalog)

if __name__ == '__main__':
    main()
