# SILK Life Magazine - Project Instructions

This file provides guidance to Claude Code when working with the SILK Life magazine website.

---

## Project Overview

**SILK Life** is the lifestyle magazine for the SILK community, featuring intimate personal stories from ~50 community members living in retrofitted Victorian cottages in the Ohio River Valley.

- **Domain:** silklife.org
- **Type:** Static HTML magazine website
- **Content:** 90+ articles across 5 categories
- **Tier:** 2 (reports to SILK Corp)

**SILK Core Values:** **S**trength, **I**ntegrity, **L**ove, **K**nowledge

---

## SILK Ecosystem

SILK Life aggregates stories from across the SILK ecosystem:

```
                    ┌─────────────────────┐
                    │     SILK CORP       │
                    │   silkcorp.org      │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │ SILK YACHT  │     │ SILK LIFE   │     │ SILK WOMEN  │
    │  (5 Sites)  │     │ (THIS SITE) │     │ silkwomen   │
    └──────┬──────┘     └─────────────┘     └─────────────┘
           │
    ┌──────┴──────┬──────────┬──────────┬──────────┐
    │             │          │          │          │
    ▼             ▼          ▼          ▼          ▼
  YOGA         ARTS        CAFE       HOMES       TECH
```

### YACHT Properties (Content Sources)

| Site | Domain | Focus | SILK Life Category |
|------|--------|-------|-------------------|
| **SILK Yoga** | silkyoga.org | Wellness, mindfulness, retreats | `category-yoga.html` |
| **SILK Arts** | silkarts.org | Creative expression, galleries | `category-arts.html` |
| **SILK Cafe** | silkcafe.org | Community gathering, farm-to-table | `category-cafe.html` |
| **SILK Homes** | silkhomes.org | Intentional living, co-housing | `category-homes.html` |
| **SILK Tech** | silktech.org | Digital wellness, innovation | `category-tech.html` |

### Other SILK Properties

| Site | Domain | Purpose | Relationship to SILK Life |
|------|--------|---------|--------------------------|
| **SILK Corp** | silkcorp.org | Parent company hub | Corporate oversight |
| **SILK Women** | silkwomen.org | Global women's empowerment | Cross-promote women's stories |
| **SILK Hive** | silkhive.org | Member portal, collaboration | Future: member-only content |
| **SILK Guide** | (internal) | Brand guidelines | Design standards reference |

---

## Character Guide

**CRITICAL:** Before writing ANY SILK Life content, consult the character guide.

- **Location:** `/mnt/d/silk/silklife/CHARACTERS.md`
- **Contents:** 50 established characters with full profiles
- **Required reading:** Names, ages, professions, locations, house descriptions, personalities

### Core Characters (Quick Reference)

| Name | Age | Role | Location | Notable |
|------|-----|------|----------|---------|
| Bill Henderson | 73 | Community elder | Ravenswood, Front St | Wraparound porch gathering spot |
| Maya Chen | 32 | Garden coordinator | Ravenswood, Front St | Saturday coffee host |
| Tom Richardson | 45 | Silent helper | Ravenswood, Front St | 6am runs; fixes things |
| Sarah Mitchell | 34 | Innkeeper | Marietta, Second St | Three chickens; SILK Homes property |
| Emma Clarke | 38 | Social connector | Ravenswood, Front St | SCOBY grower; knows everyone |
| Elena Martinez | 41 | Night nurse/potter | Ravenswood, Front St | ER nights; pottery weekends |

### Community Locations

| Town | State | Population | Character |
|------|-------|------------|-----------|
| Ravenswood | WV | ~25 SILK members | Primary hub; tight-knit |
| Parkersburg | WV | ~15 SILK members | Working-class; diverse |
| Marietta | OH | ~10 SILK members | College town; arts scene |

---

## Physical Property Details

All stories take place in **authentic 1880s-1890s Victorian cottages**. These are NOT modern renovations.

### Architectural Characteristics
- **Era:** 1880s-1890s Victorian
- **Ceiling Height:** 9-12 feet
- **Room Size:** Small, intimate rooms
- **Floors:** Original wide-plank hardwood (worn, authentic patina)
- **Windows:** Tall double-hung with wavy antique glass
- **Features:** Original radiators, plaster medallions, parlors, wraparound porches

### Interior Elements
- **Walls:** Period-appropriate paint (sage green, dusty blue, warm yellow) or Victorian wallpaper
- **Trim:** White-painted crown molding, baseboards
- **Furniture:** Dark wood Victorian pieces, worn but cared for
- **Modern additions:** Visible but not hidden (window AC, basic appliances)

### What It Is NOT
- No modern farmhouse shiplap
- No open concept layouts
- No stainless steel appliances
- No granite/marble counters
- No staged/glamorous interiors

---

## Writing Style

### Voice & Tone
- **Intimate, first-person narratives** - Personal stories, not journalism
- **Self-practice focus** - NO workshops, classes, or paid instructors
- **Honest imperfection** - Failed sourdough, awkward yoga, learning curves
- **Specific moments** - "Tuesday at 6:47 AM" not "mornings"
- **Community through presence** - Neighbors showing up, not formal events

### What to Include
- Specific times and dates
- Sensory details (radiator clanking, coffee smell, river sounds)
- Character names from CHARACTERS.md
- Real street names (Front Street, Market Street, River Road)
- Victorian house details (parlor, porch, bay window)
- Imperfect outcomes (burnt bread, sore muscles, awkward silences)

### What to Avoid
- Generic wellness speak
- Perfect Instagram moments
- Professional instruction/workshops
- Formal community "events"
- Unnamed characters
- Vague locations

### Example Good Opening
> "It was 6:47 on a Tuesday when I finally admitted my sourdough starter was dead. Maya found me staring at the jar on my kitchen counter—the one by the bay window where the morning light hits just right—and didn't say anything. Just set down a fresh jar of her own starter and started making coffee."

### Example Bad Opening
> "Starting my wellness journey has been transformative. Through our community workshops, I've learned so much about mindful living and sustainable practices."

---

## Image Guidelines

### Size Conventions

| Use Case | Dimensions | Location |
|----------|------------|----------|
| Homepage thumbnails | 330x242 | `images/articles/` or `images/homepage/` |
| Homepage squares | 330x330 | `images/homepage/hp-*-330.webp` |
| Article hero | 1024x1024 | `images/articles/` |
| Carousel banners | 510x187 | `images/homepage/hp-*-510.webp` |

### Photo Style
- **Realistic, documentary-style** photography
- **Cozy, humble, authentic** - not staged or glamorous
- **People in casual attire** - sweaters, jeans, flannel (no suits)
- **Small intimate spaces** with natural daylight
- **Format:** WebP preferred

### Naming Conventions
```
images/articles/[category]-[topic].webp
images/homepage/hp-[topic]-[number]-[size].webp

Examples:
images/articles/cafe-farm-table.webp
images/articles/yoga-morning-practice.webp
images/homepage/hp-yoga-11-330.webp
images/homepage/hp-arts-02-510.webp
```

---

## Site Structure

```
silklife/
├── index.html                    # Homepage
├── CHARACTERS.md                 # Character database (READ THIS)
├── CNAME                         # silklife.org
│
├── category-yoga.html            # YACHT category pages
├── category-arts.html
├── category-cafe.html
├── category-homes.html
├── category-tech.html
│
├── post-*.html                   # Individual articles (~90)
│
├── style/
│   ├── style.css                 # Main styles
│   ├── silk-life.css             # Custom SILK Life styles
│   └── responsive.css            # Mobile styles
│
├── images/
│   ├── articles/                 # Article images (330x242, 1024x1024)
│   ├── homepage/                 # Homepage-specific images
│   └── samples/                  # Template placeholder images
│
└── js/
    └── main.js                   # Site JavaScript
```

### Article File Naming
```
post-[category]-[topic].html

Examples:
post-yoga-morning-practice.html
post-cafe-farm-table.html
post-home-sustainable-living.html
post-arts-pottery-studio.html
post-tech-digital-wellness.html
```

---

## Content Categories

### YOGA (category-yoga.html)
- Personal meditation practices
- Home yoga routines
- Breathing exercises
- Mindfulness moments
- **NOT:** Studio classes, paid instructors, retreats

### ARTS (category-arts.html)
- Personal creative projects
- Home art spaces (basement studios, sun porch offices)
- Community art walks
- Elena's pottery, Rachel's photography, Ben's portraits
- **NOT:** Professional galleries, art schools

### CAFE (category-cafe.html)
- Home cooking stories
- Garden-to-table experiences
- Community meals (Bill's porch, Maya's kitchen)
- Coffee rituals, bread baking
- **NOT:** Restaurant reviews, professional chefs

### HOMES (category-homes.html)
- Victorian cottage living
- Radiator struggles, drafty windows
- Sustainable home practices
- Co-housing experiences
- **NOT:** Real estate listings, renovation shows

### TECH (category-tech.html)
- Digital wellness, phone boundaries
- Rural connectivity challenges
- Remote work from Victorian cottages
- Omar's repair café, tech help traditions
- **NOT:** Product reviews, gadget worship

---

## Development

### Local Server
```bash
# Python
python -m http.server 8000

# Node
npx serve

# VS Code Live Server
# Right-click index.html → Open with Live Server
```

### Adding New Articles
1. Copy existing `post-*.html` as template
2. Update title, meta description, content
3. Add character names from CHARACTERS.md
4. Create/resize images to correct dimensions
5. Add to relevant category page
6. Update homepage if featured

### GitHub
- **Repo:** WorldEnterpriseGroup/silklife
- **Hosting:** GitHub Pages
- **Branch:** gh-pages (live), master (development)

---

## Color Palette

| Element | Color | Hex |
|---------|-------|-----|
| Primary | Warm Coral | #E07A5F |
| Secondary | Cream | #F4F1DE |
| Accent | Forest Green | #3D405B |
| Text | Dark Gray | #333333 |
| Highlight | Sage Green | #81B29A |

### Typography
- **Headings:** Playfair Display
- **Body:** Inter
- **Quotes:** Lora (italic)

---

## Cross-Site Links

Always link to sibling SILK sites where relevant:

```html
<!-- In footer or related content -->
<a href="https://silkcorp.org">SILK Corp</a>
<a href="https://silkyoga.org">SILK Yoga</a>
<a href="https://silkarts.org">SILK Arts</a>
<a href="https://silkcafe.org">SILK Cafe</a>
<a href="https://silkhomes.org">SILK Homes</a>
<a href="https://silkwomen.org">SILK Women</a>
```

---

## Quick Reference

| Task | Action |
|------|--------|
| New article | Copy `post-*.html`, update content, add to category |
| New character | Add to CHARACTERS.md first, then reference |
| Homepage image | Must be 330x242 for thumbnails, 330x330 for squares |
| Article image | 1024x1024 for hero, resize for thumbnails |
| Writing check | Is it first-person? Specific time? Named character? Imperfect? |

---

*This document is the canonical reference for SILK Life development. Consult CHARACTERS.md before writing any community content.*
