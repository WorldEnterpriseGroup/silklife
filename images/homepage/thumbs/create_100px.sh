#!/bin/bash
cd /mnt/d/silk/silklife/images/homepage/thumbs

# Create 100px versions from 330px images
convert ../hp-homes-sacred-spaces-330.avif -resize 100x100^ -gravity center -extent 100x100 -quality 50 hp-homes-sacred-spaces-100.avif
echo "Created hp-homes-sacred-spaces-100.avif"

convert ../hp-homes-community-stories-330.avif -resize 100x100^ -gravity center -extent 100x100 -quality 50 hp-homes-community-stories-100.avif
echo "Created hp-homes-community-stories-100.avif"

convert ../hp-arts-first-friday-330.avif -resize 100x100^ -gravity center -extent 100x100 -quality 50 hp-arts-first-friday-100.avif
echo "Created hp-arts-first-friday-100.avif"

convert ../hp-tech-modern-wellness-330.avif -resize 100x100^ -gravity center -extent 100x100 -quality 50 hp-tech-modern-wellness-100.avif
echo "Created hp-tech-modern-wellness-100.avif"

convert ../hp-tech-intentionality-330.avif -resize 100x100^ -gravity center -extent 100x100 -quality 50 hp-tech-intentionality-100.avif
echo "Created hp-tech-intentionality-100.avif"

echo "Done!"
