#!/bin/bash
echo "=== Images used on homepage that are still 1024x1024 ==="
echo ""
grep -o "src='images/articles/[^']*" index.html | cut -d"'" -f2 | while read img; do
    if [ -f "$img" ]; then
        size=$(identify -format "%wx%h" "$img" 2>/dev/null)
        if [ "$size" = "1024x1024" ]; then
            filesize=$(ls -lh "$img" | awk '{print $5}')
            echo "$img: $size ($filesize)"
        fi
    fi
done
