#!/usr/bin/env python3
"""
Add photo_count column to article_catalog.csv
Counts actual article photos (excludes ads from /ads/ directory)
Flags articles with < 3 photos
"""

import csv
from pathlib import Path

def count_non_ad_photos(photo_links_str):
    """Count photos that are NOT ads (exclude paths containing /ads/)"""
    if not photo_links_str or photo_links_str.strip() == '':
        return 0

    photos = photo_links_str.split('|')
    non_ad_photos = [p for p in photos if '/ads/' not in p.strip()]
    return len(non_ad_photos)

def main():
    csv_path = Path('/mnt/d/silk/silklife/article_catalog.csv')

    # Read the CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    # Insert photo_count after tag_count
    if 'photo_count' not in fieldnames:
        tag_count_index = fieldnames.index('tag_count')
        fieldnames = list(fieldnames)
        fieldnames.insert(tag_count_index + 1, 'photo_count')

    # Process each row
    for row in rows:
        # Count non-ad photos
        photo_count = count_non_ad_photos(row.get('photo_links', ''))
        row['photo_count'] = str(photo_count)

        # Add needs_more_photos to issues if < 3 photos
        if photo_count < 3:
            issues = row.get('issues', '')
            if issues and 'needs_more_photos' not in issues:
                row['issues'] = issues + '|needs_more_photos'
            elif not issues:
                row['issues'] = 'needs_more_photos'

    # Write updated CSV
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Print summary
    total = len(rows)
    needs_photos = sum(1 for r in rows if int(r['photo_count']) < 3)
    avg_photos = sum(int(r['photo_count']) for r in rows) / total if total > 0 else 0

    print(f"✓ Updated {csv_path}")
    print(f"  Total articles: {total}")
    print(f"  Average photos per article: {avg_photos:.1f}")
    print(f"  Articles needing more photos (< 3): {needs_photos} ({needs_photos/total*100:.1f}%)")

if __name__ == '__main__':
    main()
