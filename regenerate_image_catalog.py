#!/usr/bin/env python3
"""
Regenerate complete image_catalog.csv by scanning all images in the silklife directory.
Cross-references with new_image_catalog.csv to mark upgraded images.
"""

import os
import csv
from pathlib import Path
from datetime import datetime
import subprocess

# Base directory
BASE_DIR = Path('/mnt/d/silk/silklife')
IMAGES_DIR = BASE_DIR / 'images'
OUTPUT_FILE = BASE_DIR / 'image_upgrade' / 'image_catalog.csv'
UPGRADED_FILE = BASE_DIR / 'image_upgrade' / 'new_image_catalog.csv'

def get_image_dimensions(filepath):
    """Get image dimensions using identify command."""
    try:
        result = subprocess.run(
            ['identify', '-format', '%wx%h', str(filepath)],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return "unknown"
    except Exception as e:
        print(f"Error getting dimensions for {filepath}: {e}")
        return "unknown"

def get_file_modified_time(filepath):
    """Get file modification time."""
    try:
        mtime = os.path.getmtime(filepath)
        return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"Error getting mtime for {filepath}: {e}")
        return ""

def load_upgraded_paths():
    """Load set of upgraded image paths from new_image_catalog.csv."""
    upgraded = set()
    try:
        with open(UPGRADED_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Store both the path and original_path (if exists)
                if row.get('path'):
                    upgraded.add(row['path'])
                if row.get('original_path'):
                    upgraded.add(row['original_path'])
    except Exception as e:
        print(f"Error loading upgraded paths: {e}")
    return upgraded

def find_all_images():
    """Find all .png and .webp images in the images directory."""
    images = []
    for ext in ['*.png', '*.webp']:
        images.extend(IMAGES_DIR.rglob(ext))
    return sorted(images)

def generate_catalog():
    """Generate complete image catalog."""
    # Load upgraded paths
    upgraded_paths = load_upgraded_paths()
    print(f"Loaded {len(upgraded_paths)} upgraded image paths")

    # Find all images
    all_images = find_all_images()
    print(f"Found {len(all_images)} total images")

    # Prepare CSV data
    catalog_rows = []

    for img_path in all_images:
        # Get relative path from BASE_DIR
        rel_path = img_path.relative_to(BASE_DIR)
        rel_path_str = str(rel_path).replace('\\', '/')  # Normalize to forward slashes

        # Get file extension
        file_type = img_path.suffix

        # Get dimensions
        dimensions = get_image_dimensions(img_path)

        # Get modified time
        date_modified = get_file_modified_time(img_path)

        # Default model
        model = "gemini-2.5-flash"

        # Empty description (to be backfilled later)
        description = ""

        # Check if upgraded
        upgraded = "true" if rel_path_str in upgraded_paths else "false"

        catalog_rows.append({
            'path': rel_path_str,
            'type': file_type,
            'dimensions': dimensions,
            'date_modified': date_modified,
            'model': model,
            'description': description,
            'upgraded': upgraded
        })

    # Write CSV
    print(f"\nWriting {len(catalog_rows)} rows to {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['path', 'type', 'dimensions', 'date_modified', 'model', 'description', 'upgraded']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(catalog_rows)

    # Print summary
    upgraded_count = sum(1 for row in catalog_rows if row['upgraded'] == 'true')
    print(f"\nCatalog regenerated successfully!")
    print(f"Total images: {len(catalog_rows)}")
    print(f"Upgraded: {upgraded_count}")
    print(f"Not upgraded: {len(catalog_rows) - upgraded_count}")

if __name__ == '__main__':
    generate_catalog()
