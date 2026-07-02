#!/bin/bash

# SILK Life HOMES Articles - Batch Sidebar Update Script
# This script updates all HOMES category articles with the new sage-themed sidebar

# Note: This is a reference script. The actual updates should be done via Claude Code Edit tool
# to ensure proper handling of HTML structure and indentation.

FILES=(
    "post-home-radiator-patience.html"
    "post-homes-community-stories.html"
    "post-homes-energy.html"
    "post-homes-gardens.html"
    "post-homes-garden-seasons.html"
    "post-homes-intentional-living.html"
    "post-homes-neighbors.html"
    "post-homes-real-stories.html"
    "post-homes-sacred-spaces.html"
    "post-homes-sustainable-design.html"
    "post-homes-sustainable-tips.html"
    "post-homes-tiny-house.html"
    "post-homes-downsizing-grace.html"
    "post-homes-tour.html"
    "post-intentional-home.html"
    "post-intentional-living.html"
    "post-intentional-qa.html"
    "post-ravenswood.html"
    "post-ravenswood-template.html"
    "post-restoration.html"
    "post-thrift-finds.html"
    "post-homes-radiator-whisperer.html"
)

echo "SILK Life HOMES Articles - Sidebar Update"
echo "========================================="
echo ""
echo "Total files to process: ${#FILES[@]}"
echo ""

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        if grep -q 'linear-gradient(135deg, #f4f7f2' "$file"; then
            echo "✓ $file - Already updated"
        else
            echo "✗ $file - Needs update"
        fi
    else
        echo "? $file - File not found"
    fi
done

echo ""
echo "Script complete. Use Claude Code Edit tool for actual updates."
