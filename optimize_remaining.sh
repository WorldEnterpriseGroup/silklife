#!/bin/bash
echo "=== Optimizing remaining homepage images ==="
echo ""

# Function to optimize an image
optimize_image() {
    local input=$1
    local width=$2
    local height=$3
    
    if [ ! -f "$input" ]; then
        echo "  ⚠ File not found: $input"
        return
    fi
    
    # Get original size
    BEFORE=$(stat -c%s "$input" 2>/dev/null || stat -f%z "$input" 2>/dev/null)
    BEFORE_KB=$((BEFORE / 1024))
    
    # Backup original
    cp "$input" "image_backups/backup_20251222_102506/"
    
    # Resize with ImageMagick
    echo "  Processing: $input"
    echo "    Original: $(identify -format "%wx%h" "$input") - ${BEFORE_KB}KB"
    
    convert "$input" -resize ${width}x${height} -quality 85 "$input"
    
    # Get new size
    AFTER=$(stat -c%s "$input" 2>/dev/null || stat -f%z "$input" 2>/dev/null)
    AFTER_KB=$((AFTER / 1024))
    SAVED=$((BEFORE - AFTER))
    SAVED_KB=$((SAVED / 1024))
    PERCENT=$((100 - (AFTER * 100 / BEFORE)))
    
    echo "    Optimized: ${width}x${height} - ${AFTER_KB}KB (saved ${SAVED_KB}KB, ${PERCENT}% reduction)"
    echo ""
}

# Optimize mega menu images (displayed at smaller sizes)
echo "1. Optimizing mega menu images (displayed at ~200x150)"
optimize_image "images/articles/yoga-mindful-movement.webp" 200 200
optimize_image "images/articles/yoga-breathing.webp" 200 200
optimize_image "images/articles/yoga-stillness.webp" 200 200

# Optimize Featured YACHT ecosystem images (displayed at 330x330)
echo "2. Optimizing featured ecosystem image"
optimize_image "images/articles/tech-coworking-innovation.webp" 330 330

echo "=== Optimization Complete ==="
