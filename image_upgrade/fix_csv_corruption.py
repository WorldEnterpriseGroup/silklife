#!/usr/bin/env python3
"""
Fix CSV corruption in image_catalog.csv

Problem: Some rows have embedded ',true,' within description field, breaking CSV parsing
Solution: Remove ',true,' from descriptions and set upgraded column to 'true'
"""

import csv
import re

def fix_csv_corruption(input_file, output_file):
    """
    Fix corrupted CSV rows by removing embedded ',true,' from descriptions
    and updating the upgraded column
    """
    rows_fixed = 0
    total_rows = 0
    fixed_rows_info = []

    with open(input_file, 'r', encoding='utf-8') as infile:
        # Read entire file content
        content = infile.read()

    lines = content.strip().split('\n')
    header = lines[0]
    data_lines = lines[1:]

    fixed_lines = [header]

    for line_num, line in enumerate(data_lines, start=2):  # Start at 2 (row 1 is header)
        total_rows += 1

        # Check if line contains the corruption pattern
        if ',true,' in line and line.endswith(',false'):
            # This is a corrupted row
            # Pattern: description contains ",true," and row ends with ",false"

            # Remove the embedded ',true,' from the description
            fixed_line = line.replace(',true,', ',')

            # Change the final ',false' to ',true'
            if fixed_line.endswith(',false'):
                fixed_line = fixed_line[:-6] + ',true'

            fixed_lines.append(fixed_line)
            rows_fixed += 1

            # Extract filename for reporting
            match = re.search(r'^([^,]+)', line)
            filename = match.group(1) if match else f"Row {line_num}"
            fixed_rows_info.append((line_num, filename))

            print(f"✓ Fixed row {line_num}: {filename}")
        else:
            # Not corrupted, keep as-is
            fixed_lines.append(line)

    # Write fixed CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        outfile.write('\n'.join(fixed_lines) + '\n')

    return rows_fixed, total_rows, fixed_rows_info


if __name__ == '__main__':
    input_csv = '/mnt/d/silk/silklife/image_upgrade/image_catalog.csv'
    output_csv = '/mnt/d/silk/silklife/image_upgrade/image_catalog_fixed.csv'

    print("=" * 70)
    print("CSV Corruption Fix Script")
    print("=" * 70)
    print(f"Input:  {input_csv}")
    print(f"Output: {output_csv}")
    print()

    rows_fixed, total_rows, fixed_info = fix_csv_corruption(input_csv, output_csv)

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total rows processed: {total_rows}")
    print(f"Rows fixed: {rows_fixed}")
    print()

    if rows_fixed > 0:
        print("Fixed rows:")
        for row_num, filename in fixed_info:
            print(f"  - Row {row_num}: {filename}")
        print()
        print(f"✓ Successfully fixed {rows_fixed} corrupted rows")
        print(f"✓ Output saved to: {output_csv}")
    else:
        print("No corrupted rows found")
