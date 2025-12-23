#!/bin/bash
# Image optimization script for SILK Life homepage
# Resizes oversized images to their actual display dimensions

echo "=== SILK Life Image Optimization ==="
echo "Starting optimization process..."
echo ""

# Create backup directory
mkdir -p image_backups
BACKUP_DIR="image_backups/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Track total savings
TOTAL_BEFORE=0
TOTAL_AFTER=0

# Function to optimize an image
optimize_image() {
    local input=$1
    local width=$2
    local height=$3
    local output=$4
    
    if [ -z "$output" ]; then
        output=$input
    fi
    
    if [ ! -f "$input" ]; then
        echo "  ⚠ File not found: $input"
        return
    fi
    
    # Get original size
    BEFORE=$(stat -c%s "$input" 2>/dev/null || stat -f%z "$input" 2>/dev/null)
    BEFORE_KB=$((BEFORE / 1024))
    
    # Backup original
    cp "$input" "$BACKUP_DIR/"
    
    # Resize with ImageMagick
    echo "  Processing: $input"
    echo "    Original: $(identify -format "%wx%h" "$input") - ${BEFORE_KB}KB"
    
    convert "$input" -resize ${width}x${height} -quality 85 "$output"
    
    # Get new size
    AFTER=$(stat -c%s "$output" 2>/dev/null || stat -f%z "$output" 2>/dev/null)
    AFTER_KB=$((AFTER / 1024))
    SAVED=$((BEFORE - AFTER))
    SAVED_KB=$((SAVED / 1024))
    PERCENT=$((100 - (AFTER * 100 / BEFORE)))
    
    echo "    Optimized: ${width}x${height} - ${AFTER_KB}KB (saved ${SAVED_KB}KB, ${PERCENT}% reduction)"
    echo ""
    
    TOTAL_BEFORE=$((TOTAL_BEFORE + BEFORE))
    TOTAL_AFTER=$((TOTAL_AFTER + AFTER))
}

echo "1. Fixing hp-cafe-04-330.webp (should be 330x242, currently 1024x1024)"
optimize_image "images/homepage/hp-cafe-04-330.webp" 330 242

echo "2. Optimizing main carousel article images (displayed at ~330x330 in 'Latest Stories')"
optimize_image "images/articles/arts-painting-nook.webp" 330 330
optimize_image "images/articles/cafe-farm-table.webp" 330 330
optimize_image "images/articles/home-community-gathering.webp" 330 330
optimize_image "images/articles/morning-practice-parlor.webp" 330 330
optimize_image "images/articles/tech-digital-wellness-porch.webp" 330 330

# Also optimize the .png version
if [ -f "images/articles/morning-practice-parlor.png" ]; then
    echo "3. Converting and optimizing .png to .webp"
    BEFORE=$(stat -c%s "images/articles/morning-practice-parlor.png" 2>/dev/null || stat -f%z "images/articles/morning-practice-parlor.png" 2>/dev/null)
    BEFORE_KB=$((BEFORE / 1024))
    echo "  Processing: images/articles/morning-practice-parlor.png"
    echo "    Original: $(identify -format "%wx%h" "images/articles/morning-practice-parlor.png") - ${BEFORE_KB}KB"
    
    cp "images/articles/morning-practice-parlor.png" "$BACKUP_DIR/"
    convert "images/articles/morning-practice-parlor.png" -resize 330x330 -quality 85 "images/articles/morning-practice-parlor-optimized.webp"
    
    AFTER=$(stat -c%s "images/articles/morning-practice-parlor-optimized.webp" 2>/dev/null || stat -f%z "images/articles/morning-practice-parlor-optimized.webp" 2>/dev/null)
    AFTER_KB=$((AFTER / 1024))
    SAVED=$((BEFORE - AFTER))
    SAVED_KB=$((SAVED / 1024))
    PERCENT=$((100 - (AFTER * 100 / BEFORE)))
    
    echo "    Optimized: 330x330 - ${AFTER_KB}KB (saved ${SAVED_KB}KB, ${PERCENT}% reduction)"
    echo "    Note: Created new file morning-practice-parlor-optimized.webp"
    echo ""
fi

# Calculate total savings
TOTAL_BEFORE_KB=$((TOTAL_BEFORE / 1024))
TOTAL_AFTER_KB=$((TOTAL_AFTER / 1024))
TOTAL_SAVED=$((TOTAL_BEFORE - TOTAL_AFTER))
TOTAL_SAVED_KB=$((TOTAL_SAVED / 1024))
TOTAL_PERCENT=$((100 - (TOTAL_AFTER * 100 / TOTAL_BEFORE)))

echo "=== Optimization Complete ==="
echo "Total size before: ${TOTAL_BEFORE_KB}KB"
echo "Total size after:  ${TOTAL_AFTER_KB}KB"
echo "Total saved:       ${TOTAL_SAVED_KB}KB (${TOTAL_PERCENT}% reduction)"
echo ""
echo "Backups saved to: $BACKUP_DIR"
echo ""
echo "To restore original files, run:"
echo "  cp $BACKUP_DIR/* images/articles/"
echo "  cp $BACKUP_DIR/* images/homepage/"
