#!/usr/bin/env python3
"""
SILK Life Article Catalog Generator
Parses all post-*.html files and generates a comprehensive CSV catalog.
"""

import csv
import re
import os
from pathlib import Path
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
SILKLIFE_DIR = Path("/mnt/d/silk/silklife")
OUTPUT_CSV = SILKLIFE_DIR / "article_catalog.csv"
CHARACTERS_FILE = SILKLIFE_DIR / "CHARACTERS.md"

# Character names from CHARACTERS.md (extracted)
CHARACTER_NAMES = [
    "Bill Henderson", "Maya Chen", "Elena Martinez", "Tom Richardson",
    "Sarah Mitchell", "Emma Clarke", "Jacob Torres", "Rachel Kim",
    "Jesse Martinez", "Jordan Hayes", "Annie Walsh", "Sam Rivera",
    "Marcus Webb", "Rosa Delgado", "Charlie Brooks", "Deb Morrison",
    "Kevin Lee", "Patricia O'Brien", "Pat O'Brien", "Miguel Santos",
    "Grace Thompson", "David Chen", "Lucia Fernandez", "Robert Harrison",
    "Bob Harrison", "Helen Harrison", "James Walsh", "Jimmy Walsh",
    "Terri Washington", "Nathan Cross", "Iris Yamamoto", "Carl Jensen",
    "Maria Santos", "Alex Turner", "Dorothy Brennan", "Dot Brennan",
    "Frank Brennan", "Yuki Tanaka", "Omar Hassan", "Cynthia Moore",
    "Cindy Moore", "Peter Novak", "Susan Novak", "Jamal Williams",
    "Linda Chen", "Diego Fernandez", "Nancy Pierce", "Walter Pierce",
    "Walt Pierce", "Ruth Goldstein", "Howard Goldstein", "Megan O'Sullivan",
    "Tony Ricci", "Karen Mitchell", "Ben Okafor", "Evelyn Stone", "Evie Stone"
]

# First names for matching (some articles use first names only)
FIRST_NAMES = list(set([name.split()[0] for name in CHARACTER_NAMES]))


class HTMLTextExtractor(HTMLParser):
    """Extract text content from HTML."""
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip_tags = {'script', 'style', 'head'}
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag

    def handle_endtag(self, tag):
        self.current_tag = None

    def handle_data(self, data):
        if self.current_tag not in self.skip_tags:
            self.text.append(data.strip())

    def get_text(self):
        return ' '.join(t for t in self.text if t)


def read_file(filepath):
    """Read file content with encoding fallback."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='latin-1') as f:
            return f.read()


def extract_title(html_content, filename):
    """Extract article title."""
    # Try h1 with class post_title first
    match = re.search(r'<h1[^>]*class="post_title"[^>]*>(.*?)</h1>', html_content, re.DOTALL | re.IGNORECASE)
    if match:
        return re.sub(r'<[^>]+>', '', match.group(1)).strip()

    # Try any h1
    match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.DOTALL | re.IGNORECASE)
    if match:
        return re.sub(r'<[^>]+>', '', match.group(1)).strip()

    # Try title tag
    match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
    if match:
        title = match.group(1).strip()
        # Remove common suffixes
        for suffix in [' - SILK Life Magazine', ' - SILK Life', ' | SILK Life']:
            title = title.replace(suffix, '')
        return title

    return filename.replace('.html', '').replace('post-', '').replace('-', ' ').title()


def extract_author(html_content):
    """Extract article author."""
    # Try author detail pattern
    match = re.search(r'<li[^>]*class="detail author"[^>]*>.*?<a[^>]*>(.*?)</a>', html_content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Try By pattern
    match = re.search(r'By\s+<a[^>]*>(.*?)</a>', html_content, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Try By SILK Life Staff pattern
    match = re.search(r'<strong>By\s+(.*?)</strong>', html_content, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Try simple By pattern
    match = re.search(r'By\s+([A-Z][a-z]+\s+[A-Z][a-z]+)', html_content)
    if match:
        return match.group(1).strip()

    return "SILK Life Staff"


def extract_category(html_content, filename):
    """Extract article category."""
    # Try category link
    match = re.search(r'<li[^>]*class="detail category"[^>]*>.*?<a[^>]*href="category-([^"]+)\.html"', html_content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).upper()

    # Try category badge span
    match = re.search(r'<span[^>]*>([A-Z]+)</span>', html_content)
    if match and match.group(1) in ['YOGA', 'ARTS', 'CAFE', 'HOMES', 'TECH']:
        return match.group(1)

    # Infer from filename
    fname = filename.lower()
    if 'yoga' in fname or 'meditation' in fname or 'breath' in fname or 'kundalini' in fname or 'prenatal' in fname:
        return 'YOGA'
    elif 'arts' in fname or 'pottery' in fname or 'sculpt' in fname or 'art-walk' in fname:
        return 'ARTS'
    elif 'cafe' in fname or 'coffee' in fname or 'farm-table' in fname or 'recipe' in fname or 'kitchen' in fname or 'potluck' in fname:
        return 'CAFE'
    elif 'home' in fname or 'ravenswood' in fname or 'intentional' in fname or 'restoration' in fname:
        return 'HOMES'
    elif 'tech' in fname or 'digital' in fname or 'sustainable-tech' in fname:
        return 'TECH'

    return 'GENERAL'


def extract_images(html_content):
    """Extract all image sources from main content."""
    images = []

    # Find all img tags
    for match in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\']', html_content, re.IGNORECASE):
        src = match.group(1)
        # Skip placeholder/sample images for thumbnail detection
        if src and 'samples/' not in src.lower():
            images.append(src)

    return images


def extract_thumbnail(html_content, all_images):
    """Extract the primary thumbnail image."""
    # Try post_image class first
    match = re.search(r'<a[^>]*class="post_image[^"]*"[^>]*>.*?<img[^>]+src=["\']([^"\']+)["\']', html_content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)

    # Try first non-sample image
    for img in all_images:
        if 'samples/' not in img.lower() and 'ads/' not in img.lower():
            return img

    # Return first image from all if available
    if all_images:
        return all_images[0]

    return ""


def calculate_word_count(html_content):
    """Calculate word count of article content."""
    # Try to extract main content area
    content_match = re.search(r'<div[^>]*class="post_content[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>', html_content, re.DOTALL | re.IGNORECASE)
    if content_match:
        content = content_match.group(1)
    else:
        # For minimal template, try body content
        content_match = re.search(r'<div[^>]*style="font-size:16px[^"]*"[^>]*>(.*?)</div>', html_content, re.DOTALL)
        if content_match:
            content = content_match.group(1)
        else:
            content = html_content

    # Strip HTML tags
    text = re.sub(r'<[^>]+>', ' ', content)
    # Clean whitespace
    text = ' '.join(text.split())
    # Count words
    return len(text.split())


def check_header_complete(html_content):
    """Check if full header structure is present."""
    has_top_bar = 'header_top_bar_container' in html_content
    has_menu = 'menu_container' in html_content or 'sf-menu' in html_content
    has_header = 'header_container' in html_content
    return has_top_bar and has_menu and has_header


def check_footer_complete(html_content):
    """Check if full footer structure is present."""
    has_footer_container = 'footer_container' in html_content
    has_footer = 'class="footer"' in html_content or 'class="footer ' in html_content
    return has_footer_container and has_footer


def check_sidebar_complete(html_content):
    """Check if sidebar is present with content."""
    has_sidebar_column = 'column column_1_3' in html_content or 'column_1_3' in html_content
    has_sidebar_content = 'box_header' in html_content or 'sidebar-ad' in html_content

    # Check for actual sidebar sections
    has_tabs = 'tabs_navigation' in html_content
    has_related = 'More in' in html_content or 'Popular Articles' in html_content

    return has_sidebar_column and (has_sidebar_content or has_tabs or has_related)


def check_ad_in_sidebar(html_content):
    """Check if ads are present in sidebar."""
    # Look for sidebar ad div
    if 'class="sidebar-ad"' in html_content:
        return True
    if 'silk-ad-banner' in html_content:
        # Check if it's in sidebar area (column_1_3)
        sidebar_match = re.search(r'<div[^>]*class="column column_1_3"[^>]*>(.*?)</div>\s*</div>\s*</div>', html_content, re.DOTALL)
        if sidebar_match and 'silk-ad-banner' in sidebar_match.group(1):
            return True
    return False


def check_ad_in_body(html_content):
    """Check if ads are present in article body."""
    # Look for ad in main content area (column_2_3)
    main_match = re.search(r'<div[^>]*class="column column_2_3"[^>]*>(.*?)<div[^>]*class="column column_1_3"', html_content, re.DOTALL)
    if main_match:
        main_content = main_match.group(1)
        if 'sidebar-ad' in main_content or 'silk-ad-banner' in main_content:
            return True
    return False


def find_character_mentions(html_content):
    """Find all character names mentioned in the article."""
    mentioned = set()

    # Clean HTML for text matching
    text = re.sub(r'<[^>]+>', ' ', html_content)
    text = ' '.join(text.split())

    # Check for full names
    for name in CHARACTER_NAMES:
        if name in text:
            mentioned.add(name)

    return sorted(mentioned)


def detect_template_type(html_content):
    """Detect if article uses full or minimal template."""
    if 'header_top_bar_container' in html_content and 'menu_container' in html_content:
        return 'full'
    return 'minimal'


def extract_comment_count(html_content):
    """Extract number of comments."""
    match = re.search(r'(\d+)\s*Comments?', html_content, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 0


def extract_view_count(html_content):
    """Extract view count if displayed."""
    match = re.search(r'([\d,]+)\s*Views?', html_content, re.IGNORECASE)
    if match:
        return match.group(1).replace(',', '')
    return ""


def extract_tags(html_content):
    """Extract taxonomy tags."""
    tags = []
    # Find tags section
    tags_match = re.search(r'<ul[^>]*class="taxonomies tags[^"]*"[^>]*>(.*?)</ul>', html_content, re.DOTALL)
    if tags_match:
        for tag_match in re.finditer(r'<a[^>]*>(.*?)</a>', tags_match.group(1)):
            tag = tag_match.group(1).strip()
            if tag:
                tags.append(tag)
    return tags


def extract_meta_description(html_content):
    """Extract meta description."""
    match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html_content, re.IGNORECASE)
    if match:
        return match.group(1)
    return ""


def extract_publish_date(html_content):
    """Extract publish date."""
    # Try detail date
    match = re.search(r'<li[^>]*class="detail date"[^>]*>([^<]+)</li>', html_content)
    if match:
        return match.group(1).strip()

    # Try date pattern
    match = re.search(r'(\w+\s+\d{1,2},?\s+\d{4}|\d{1,2}\s+\w+\s+\d{4})', html_content)
    if match:
        return match.group(1)

    return ""


def calculate_completeness_score(data):
    """
    Calculate a completeness score (0-100) based on all metrics.

    Scoring breakdown:
    - Structure (40 points max):
      - header_complete: 15 points
      - footer_complete: 15 points
      - sidebar_complete: 10 points

    - Content Quality (30 points max):
      - word_count >= 800: 10 points (scaled: 5 for 400-799)
      - has thumbnail: 10 points
      - has meta_description: 5 points
      - has tags: 5 points

    - Monetization (15 points max):
      - ad_in_sidebar: 10 points
      - ad_in_article_body: 5 points

    - Engagement (10 points max):
      - comment_count > 0: 5 points (bonus +2 if > 10)
      - view_count > 0: 3 points

    - Authorship (5 points max):
      - Named author (not staff): 5 points
    """
    score = 0

    # Structure (40 points)
    if data['header_complete']:
        score += 15
    if data['footer_complete']:
        score += 15
    if data['sidebar_complete']:
        score += 10

    # Content Quality (30 points)
    word_count = data['word_count']
    if word_count >= 800:
        score += 10
    elif word_count >= 400:
        score += 5

    if data['thumbnail_link']:
        score += 10
    if data['meta_description']:
        score += 5
    if data['tags']:
        score += 5

    # Monetization (15 points)
    if data['ad_in_sidebar']:
        score += 10
    if data['ad_in_article_body']:
        score += 5

    # Engagement (10 points)
    if data['comment_count'] > 0:
        score += 5
        if data['comment_count'] > 10:
            score += 2
    if data['view_count']:
        score += 3

    # Authorship (5 points)
    author = data['author'].lower()
    if author and 'staff' not in author and author != 'silk life':
        score += 5

    return score


def parse_article(filepath):
    """Parse a single article and return all extracted data."""
    filename = os.path.basename(filepath)

    try:
        html_content = read_file(filepath)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None

    # Extract all images first
    all_images = extract_images(html_content)

    # Extract all data
    data = {
        'filename': filename,
        'title': extract_title(html_content, filename),
        'word_count': calculate_word_count(html_content),
        'photo_links': '|'.join(all_images),
        'thumbnail_link': extract_thumbnail(html_content, all_images),
        'author': extract_author(html_content),
        'community_members': '|'.join(find_character_mentions(html_content)),
        'category': extract_category(html_content, filename),
        'header_complete': check_header_complete(html_content),
        'footer_complete': check_footer_complete(html_content),
        'sidebar_complete': check_sidebar_complete(html_content),
        'ad_in_sidebar': check_ad_in_sidebar(html_content),
        'ad_in_article_body': check_ad_in_body(html_content),
        'template_type': detect_template_type(html_content),
        'comment_count': extract_comment_count(html_content),
        'view_count': extract_view_count(html_content),
        'tags': '|'.join(extract_tags(html_content)),
        'meta_description': extract_meta_description(html_content),
        'publish_date': extract_publish_date(html_content),
    }

    # Calculate completeness score
    data['completeness_score'] = calculate_completeness_score(data)

    return data


def main():
    """Main function to generate the CSV catalog."""
    print("SILK Life Article Catalog Generator")
    print("=" * 50)

    # Find all article files
    article_files = list(SILKLIFE_DIR.glob('post-*.html'))
    print(f"Found {len(article_files)} articles to process")

    # Process articles in parallel
    results = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_file = {executor.submit(parse_article, f): f for f in article_files}

        for i, future in enumerate(as_completed(future_to_file), 1):
            filepath = future_to_file[future]
            try:
                data = future.result()
                if data:
                    results.append(data)
                    if i % 20 == 0:
                        print(f"  Processed {i}/{len(article_files)} articles...")
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

    print(f"Successfully parsed {len(results)} articles")

    # Sort by category and title
    results.sort(key=lambda x: (x['category'], x['title']))

    # Define CSV columns
    columns = [
        'filename', 'title', 'word_count', 'photo_links', 'thumbnail_link',
        'author', 'community_members', 'category', 'header_complete',
        'footer_complete', 'sidebar_complete', 'ad_in_sidebar', 'ad_in_article_body',
        'template_type', 'comment_count', 'view_count', 'tags', 'meta_description',
        'publish_date', 'completeness_score'
    ]

    # Write CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nCSV written to: {OUTPUT_CSV}")

    # Print summary statistics
    print("\n" + "=" * 50)
    print("SUMMARY STATISTICS")
    print("=" * 50)

    # Category breakdown
    categories = {}
    for r in results:
        cat = r['category']
        categories[cat] = categories.get(cat, 0) + 1
    print("\nArticles by Category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")

    # Template types
    templates = {}
    for r in results:
        t = r['template_type']
        templates[t] = templates.get(t, 0) + 1
    print("\nTemplate Types:")
    for t, count in sorted(templates.items()):
        print(f"  {t}: {count}")

    # Completeness stats
    header_complete = sum(1 for r in results if r['header_complete'])
    footer_complete = sum(1 for r in results if r['footer_complete'])
    sidebar_complete = sum(1 for r in results if r['sidebar_complete'])
    has_sidebar_ads = sum(1 for r in results if r['ad_in_sidebar'])
    has_body_ads = sum(1 for r in results if r['ad_in_article_body'])

    print("\nCompleteness Metrics:")
    print(f"  Header complete: {header_complete}/{len(results)} ({100*header_complete/len(results):.1f}%)")
    print(f"  Footer complete: {footer_complete}/{len(results)} ({100*footer_complete/len(results):.1f}%)")
    print(f"  Sidebar complete: {sidebar_complete}/{len(results)} ({100*sidebar_complete/len(results):.1f}%)")
    print(f"  Ads in sidebar: {has_sidebar_ads}/{len(results)} ({100*has_sidebar_ads/len(results):.1f}%)")
    print(f"  Ads in body: {has_body_ads}/{len(results)} ({100*has_body_ads/len(results):.1f}%)")

    # Word count stats
    word_counts = [r['word_count'] for r in results]
    print("\nWord Count Statistics:")
    print(f"  Total words: {sum(word_counts):,}")
    print(f"  Average: {sum(word_counts)/len(word_counts):.0f}")
    print(f"  Min: {min(word_counts)}")
    print(f"  Max: {max(word_counts)}")

    # Completeness score stats
    scores = [r['completeness_score'] for r in results]
    print("\nCompleteness Score Statistics (0-100):")
    print(f"  Average: {sum(scores)/len(scores):.1f}")
    print(f"  Min: {min(scores)}")
    print(f"  Max: {max(scores)}")

    # Score distribution
    perfect = sum(1 for s in scores if s >= 90)
    good = sum(1 for s in scores if 70 <= s < 90)
    fair = sum(1 for s in scores if 50 <= s < 70)
    poor = sum(1 for s in scores if s < 50)
    print(f"\n  Score Distribution:")
    print(f"    90-100 (Excellent): {perfect} articles")
    print(f"    70-89 (Good): {good} articles")
    print(f"    50-69 (Fair): {fair} articles")
    print(f"    0-49 (Needs Work): {poor} articles")

    # Bottom 10 articles by completeness
    sorted_by_score = sorted(results, key=lambda x: x['completeness_score'])
    print("\n  Bottom 10 Articles (Priority for Improvement):")
    for r in sorted_by_score[:10]:
        print(f"    {r['completeness_score']:3d} - {r['filename']}")


if __name__ == '__main__':
    main()
