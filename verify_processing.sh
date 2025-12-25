#!/bin/bash

# SILK Life HOMES Articles Processing Verification Script

echo "======================================"
echo "SILK Life HOMES Articles Status Check"
echo "======================================"
echo ""

FILES=(
    "post-home-community-garden.html"
    "post-home-community-gathering.html"
    "post-home-sustainable-living.html"
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

completed=0
pending=0

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        if grep -q 'linear-gradient(135deg, #f4f7f2' "$file"; then
            echo "✓ $file"
            ((completed++))
        else
            echo "✗ $file"
            ((pending++))
        fi
    else
        echo "? $file (NOT FOUND)"
    fi
done

echo ""
echo "======================================"
echo "Summary:"
echo "  Completed: $completed / 25"
echo "  Pending:   $pending / 25"
echo "  Progress:  $((completed * 100 / 25))%"
echo "======================================"
